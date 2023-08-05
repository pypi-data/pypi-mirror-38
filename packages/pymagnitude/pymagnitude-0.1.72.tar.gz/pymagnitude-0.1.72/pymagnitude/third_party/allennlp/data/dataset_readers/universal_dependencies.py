

from __future__ import with_statement
from __future__ import absolute_import
#typing
import logging

#overrides
from conllu.parser import parse_line, DEFAULT_FIELDS

from allennlp.common.file_utils import cached_path
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.fields import Field, TextField, SequenceLabelField, MetadataField
from allennlp.data.instance import Instance
from allennlp.data.token_indexers import SingleIdTokenIndexer, TokenIndexer
from allennlp.data.tokenizers import Token
from io import open
try:
    from itertools import izip
except:
    izip = zip


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def lazy_parse(text     , fields        = DEFAULT_FIELDS):
    for sentence in text.split(u"\n\n"):
        if sentence:
            yield [parse_line(line, fields)
                   for line in sentence.split(u"\n")
                   if line and not line.strip().startswith(u"#")]


class UniversalDependenciesDatasetReader(DatasetReader):
    u"""
    Reads a file in the conllu Universal Dependencies format. Additionally,
    in order to make it easy to structure a model as predicting arcs, we add a
    dummy 'ROOT_HEAD' token to the start of the sequence.

    Parameters
    ----------
    token_indexers : ``Dict[str, TokenIndexer]``, optional (default=``{"tokens": SingleIdTokenIndexer()}``)
        The token indexers to be applied to the words TextField.
    """
    def __init__(self,
                 token_indexers                          = None,
                 lazy       = False)        :
        super(UniversalDependenciesDatasetReader, self).__init__(lazy)
        self._token_indexers = token_indexers or {u'tokens': SingleIdTokenIndexer()}

    #overrides
    def _read(self, file_path     ):
        # if `file_path` is a URL, redirect to the cache
        file_path = cached_path(file_path)

        with open(file_path, u'r') as conllu_file:
            logger.info(u"Reading UD instances from conllu dataset at: %s", file_path)

            for annotation in  lazy_parse(conllu_file.read()):
                # CoNLLU annotations sometimes add back in words that have been elided
                # in the original sentence; we remove these, as we're just predicting
                # dependencies for the original sentence.
                # We filter by None here as elided words have a non-integer word id,
                # and are replaced with None by the conllu python library.
                annotation = [x for x in annotation if x[u"id"] is not None]

                heads = [x[u"head"] for x in annotation]
                tags = [x[u"deprel"] for x in annotation]
                words = [x[u"form"] for x in annotation]
                pos_tags = [x[u"upostag"] for x in annotation]
                yield self.text_to_instance(words, pos_tags, list(izip(tags, heads)))

    #overrides
    def text_to_instance(self,  # type: ignore
                         words           ,
                         upos_tags           ,
                         dependencies                        = None)            :
        # pylint: disable=arguments-differ
        u"""
        Parameters
        ----------
        words : ``List[str]``, required.
            The words in the sentence to be encoded.
        upos_tags : ``List[str]``, required.
            The universal dependencies POS tags for each word.
        dependencies ``List[Tuple[str, int]]``, optional (default = None)
            A list of  (head tag, head index) tuples. Indices are 1 indexed,
            meaning an index of 0 corresponds to that word being the root of
            the dependency tree.

        Returns
        -------
        An instance containing words, upos tags, dependency head tags and head
        indices as fields.
        """
        fields                   = {}

        tokens = TextField([Token(w) for w in words], self._token_indexers)
        fields[u"words"] = tokens
        fields[u"pos_tags"] = SequenceLabelField(upos_tags, tokens, label_namespace=u"pos")
        if dependencies is not None:
            # We don't want to expand the label namespace with an additional dummy token, so we'll
            # always give the 'ROOT_HEAD' token a label of 'root'.
            fields[u"head_tags"] = SequenceLabelField([x[0] for x in dependencies],
                                                     tokens,
                                                     label_namespace=u"head_tags")
            fields[u"head_indices"] = SequenceLabelField([int(x[1]) for x in dependencies],
                                                        tokens,
                                                        label_namespace=u"head_index_tags")

        fields[u"metadata"] = MetadataField({u"words": words, u"pos": upos_tags})
        return Instance(fields)

UniversalDependenciesDatasetReader = DatasetReader.register(u"universal_dependencies")(UniversalDependenciesDatasetReader)
