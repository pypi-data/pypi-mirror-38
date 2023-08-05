u"""
The ``evaluate`` subcommand can be used to
evaluate a trained model against a dataset
and report any metrics calculated by the model.

.. code-block:: bash

    $ allennlp evaluate --help
    usage: allennlp evaluate [-h] [--output-file OUTPUT_FILE]
                             [--weights-file WEIGHTS_FILE]
                             [--cuda-device CUDA_DEVICE] [-o OVERRIDES]
                             [--include-package INCLUDE_PACKAGE]
                             archive_file input_file

    Evaluate the specified model + dataset

    positional arguments:
    archive_file          path to an archived trained model
    input_file            path to the file containing the evaluation data

    optional arguments:
    -h, --help            show this help message and exit
    --output-file OUTPUT_FILE
                            path to output file to save metrics
    --weights-file WEIGHTS_FILE
                            a path that overrides which weights file to use
    --cuda-device CUDA_DEVICE
                            id of GPU to use (if any)
    -o OVERRIDES, --overrides OVERRIDES
                            a JSON structure used to override the experiment
                            configuration
    --include-package INCLUDE_PACKAGE
                            additional packages to include
"""


from __future__ import with_statement
from __future__ import absolute_import
#typing
import argparse
import logging
import json

import torch

from allennlp.commands.subcommand import Subcommand
from allennlp.common.checks import check_for_gpu
from allennlp.common.util import prepare_environment
from allennlp.common.tqdm import Tqdm
from allennlp.data import Instance
from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.iterators import DataIterator
from allennlp.models.archival import load_archive
from allennlp.models.model import Model
from io import open

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Evaluate(Subcommand):
    def add_subparser(self, name     , parser                            )                           :
        # pylint: disable=protected-access
        description = u'''Evaluate the specified model + dataset'''
        subparser = parser.add_parser(
                name, description=description, help=u'Evaluate the specified model + dataset')

        subparser.add_argument(u'archive_file', type=unicode, help=u'path to an archived trained model')

        subparser.add_argument(u'input_file', type=unicode, help=u'path to the file containing the evaluation data')

        subparser.add_argument(u'--output-file', type=unicode, help=u'path to output file')

        subparser.add_argument(u'--weights-file',
                               type=unicode,
                               help=u'a path that overrides which weights file to use')

        cuda_device = subparser.add_mutually_exclusive_group(required=False)
        cuda_device.add_argument(u'--cuda-device',
                                 type=int,
                                 default=-1,
                                 help=u'id of GPU to use (if any)')

        subparser.add_argument(u'-o', u'--overrides',
                               type=unicode,
                               default=u"",
                               help=u'a JSON structure used to override the experiment configuration')

        subparser.set_defaults(func=evaluate_from_args)

        return subparser


def evaluate(model       ,
             instances                    ,
             data_iterator              ,
             cuda_device     )                  :
    _warned_tqdm_ignores_underscores = False
    check_for_gpu(cuda_device)
    with torch.no_grad():
        model.eval()

        iterator = data_iterator(instances,
                                 num_epochs=1,
                                 shuffle=False,
                                 cuda_device=cuda_device)
        logger.info(u"Iterating over dataset")
        generator_tqdm = Tqdm.tqdm(iterator, total=data_iterator.get_num_batches(instances))
        for batch in generator_tqdm:
            model(**batch)
            metrics = model.get_metrics()
            if (not _warned_tqdm_ignores_underscores and
                        any(metric_name.startswith(u"_") for metric_name in metrics)):
                logger.warning(u"Metrics with names beginning with \"_\" will "
                               u"not be logged to the tqdm progress bar.")
                _warned_tqdm_ignores_underscores = True
            description = u', '.join([u"%s: %.2f" % (name, value) for name, value
                                     in list(metrics.items()) if not name.startswith(u"_")]) + u" ||"
            generator_tqdm.set_description(description, refresh=False)

        return model.get_metrics(reset=True)


def evaluate_from_args(args                    )                  :
    # Disable some of the more verbose logging statements
    logging.getLogger(u'allennlp.common.params').disabled = True
    logging.getLogger(u'allennlp.nn.initializers').disabled = True
    logging.getLogger(u'allennlp.modules.token_embedders.embedding').setLevel(logging.INFO)

    # Load from archive
    archive = load_archive(args.archive_file, args.cuda_device, args.overrides, args.weights_file)
    config = archive.config
    prepare_environment(config)
    model = archive.model
    model.eval()

    # Load the evaluation data

    # Try to use the validation dataset reader if there is one - otherwise fall back
    # to the default dataset_reader used for both training and validation.
    validation_dataset_reader_params = config.pop(u'validation_dataset_reader', None)
    if validation_dataset_reader_params is not None:
        dataset_reader = DatasetReader.from_params(validation_dataset_reader_params)
    else:
        dataset_reader = DatasetReader.from_params(config.pop(u'dataset_reader'))
    evaluation_data_path = args.input_file
    logger.info(u"Reading evaluation data from %s", evaluation_data_path)
    instances = dataset_reader.read(evaluation_data_path)

    iterator_params = config.pop(u"validation_iterator", None)
    if iterator_params is None:
        iterator_params = config.pop(u"iterator")
    iterator = DataIterator.from_params(iterator_params)
    iterator.index_with(model.vocab)

    metrics = evaluate(model, instances, iterator, args.cuda_device)

    logger.info(u"Finished evaluating.")
    logger.info(u"Metrics:")
    for key, metric in list(metrics.items()):
        logger.info(u"%s: %s", key, metric)

    output_file = args.output_file
    if output_file:
        with open(output_file, u"w") as file:
            json.dump(metrics, file, indent=4)
    return metrics
