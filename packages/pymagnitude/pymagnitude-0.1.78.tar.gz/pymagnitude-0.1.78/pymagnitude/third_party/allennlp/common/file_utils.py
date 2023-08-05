u"""
Utilities for working with the local dataset cache.
"""




from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import
from builtins import str
import os
import logging
import shutil
import tempfile
import json
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse
import tempfile
#typing
from hashlib import sha256
from functools import wraps

import boto3
from botocore.exceptions import ClientError
import requests

from allennlp.common.tqdm import Tqdm
from io import open

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

CACHE_ROOT = tempfile.gettempdir()
DATASET_CACHE = str(CACHE_ROOT +'/'+ u"datasets")


def url_to_filename(url     , etag      = None)       :
    u"""
    Convert `url` into a hashed filename in a repeatable way.
    If `etag` is specified, append its hash to the url's, delimited
    by a period.
    """
    url_bytes = url.encode(u'utf-8')
    url_hash = sha256(url_bytes)
    filename = url_hash.hexdigest()

    if etag:
        etag_bytes = etag.encode(u'utf-8')
        etag_hash = sha256(etag_bytes)
        filename += u'.' + etag_hash.hexdigest()

    return filename


def filename_to_url(filename     , cache_dir      = None)                   :
    u"""
    Return the url and etag (which may be ``None``) stored for `filename`.
    Raise ``FileNotFoundError`` if `filename` or its stored metadata do not exist.
    """
    if cache_dir is None:
        cache_dir = DATASET_CACHE

    cache_path = os.path.join(cache_dir, filename)
    if not os.path.exists(cache_path):
        raise FileNotFoundError(u"file {} not found".format(cache_path))

    meta_path = cache_path + u'.json'
    if not os.path.exists(meta_path):
        raise FileNotFoundError(u"file {} not found".format(meta_path))

    with open(meta_path) as meta_file:
        metadata = json.load(meta_file)
    url = metadata[u'url']
    etag = metadata[u'etag']

    return url, etag


def cached_path(url_or_filename                  , cache_dir      = None)       :
    u"""
    Given something that might be a URL (or might be a local path),
    determine which. If it's a URL, download the file and cache it, and
    return the path to the cached file. If it's already a local path,
    make sure the file exists and then return the path.
    """
    if cache_dir is None:
        cache_dir = DATASET_CACHE
    url_or_filename = str(url_or_filename)

    parsed = urlparse(url_or_filename)

    if parsed.scheme in (u'http', u'https', u's3'):
        # URL, so get it from the cache (downloading if necessary)
        return get_from_cache(url_or_filename, cache_dir)
    elif os.path.exists(url_or_filename):
        # File, and it exists.
        return url_or_filename
    elif parsed.scheme == u'':
        # File, but it doesn't exist.
        raise FileNotFoundError(u"file {} not found".format(url_or_filename))
    else:
        # Something unknown
        raise ValueError(u"unable to parse {} as a URL or as a local path".format(url_or_filename))


def split_s3_path(url     )                   :
    u"""Split a full s3 path into the bucket name and path."""
    parsed = urlparse(url)
    if not parsed.netloc or not parsed.path:
        raise ValueError(u"bad s3 path {}".format(url))
    bucket_name = parsed.netloc
    s3_path = parsed.path
    # Remove '/' at beginning of path.
    if s3_path.startswith(u"/"):
        s3_path = s3_path[1:]
    return bucket_name, s3_path


def s3_request(func          ):
    u"""
    Wrapper function for s3 requests in order to create more helpful error
    messages.
    """

    @wraps(func)
    def wrapper(url     , *args, **kwargs):
        try:
            return func(url, *args, **kwargs)
        except ClientError as exc:
            if int(exc.response[u"Error"][u"Code"]) == 404:
                raise FileNotFoundError(u"file {} not found".format(url))
            else:
                raise

    return wrapper


@s3_request
def s3_etag(url     )                 :
    u"""Check ETag on S3 object."""
    s3_resource = boto3.resource(u"s3")
    bucket_name, s3_path = split_s3_path(url)
    s3_object = s3_resource.Object(bucket_name, s3_path)
    return s3_object.e_tag


@s3_request
def s3_get(url     , temp_file    )        :
    u"""Pull a file directly from S3."""
    s3_resource = boto3.resource(u"s3")
    bucket_name, s3_path = split_s3_path(url)
    s3_resource.Bucket(bucket_name).download_fileobj(s3_path, temp_file)


def http_get(url     , temp_file    )        :
    req = requests.get(url, stream=True)
    content_length = req.headers.get(u'Content-Length')
    total = int(content_length) if content_length is not None else None
    progress = Tqdm.tqdm(unit=u"B", total=total)
    for chunk in req.iter_content(chunk_size=1024):
        if chunk: # filter out keep-alive new chunks
            progress.update(len(chunk))
            temp_file.write(chunk)
    progress.close()


# TODO(joelgrus): do we want to do checksums or anything like that?
def get_from_cache(url     , cache_dir      = None)       :
    u"""
    Given a URL, look for the corresponding dataset in the local cache.
    If it's not there, download it. Then return the path to the cached file.
    """
    if cache_dir is None:
        cache_dir = DATASET_CACHE

    os.makedirs(cache_dir)

    # Get eTag to add to filename, if it exists.
    if url.startswith(u"s3://"):
        etag = s3_etag(url)
    else:
        response = requests.head(url, allow_redirects=True)
        if response.status_code != 200:
            raise IOError(u"HEAD request failed for url {} with status code {}"
                          .format(url, response.status_code))
        etag = response.headers.get(u"ETag")

    filename = url_to_filename(url, etag)

    # get cache path to put the file
    cache_path = os.path.join(cache_dir, filename)

    if not os.path.exists(cache_path):
        # Download to temporary file, then copy to cache dir once finished.
        # Otherwise you get corrupt cache entries if the download gets interrupted.
        with tempfile.NamedTemporaryFile() as temp_file:
            logger.info(u"%s not found in cache, downloading to %s", url, temp_file.name)

            # GET file object
            if url.startswith(u"s3://"):
                s3_get(url, temp_file)
            else:
                http_get(url, temp_file)

            # we are copying the file before closing it, so flush to avoid truncation
            temp_file.flush()
            # shutil.copyfileobj() starts at the current position, so go to the start
            temp_file.seek(0)

            logger.info(u"copying %s to cache at %s", temp_file.name, cache_path)
            with open(cache_path, u'wb') as cache_file:
                shutil.copyfileobj(temp_file, cache_file)

            logger.info(u"creating metadata file for %s", cache_path)
            meta = {u'url': url, u'etag': etag}
            meta_path = cache_path + u'.json'
            with open(meta_path, u'w') as meta_file:
                json.dump(meta, meta_file)

            logger.info(u"removing temp file %s", temp_file.name)

    return cache_path


def get_file_extension(path     , dot=True, lower       = True):
    ext = os.path.splitext(path)[1]
    ext = ext if dot else ext[1:]
    return ext.lower() if lower else ext
