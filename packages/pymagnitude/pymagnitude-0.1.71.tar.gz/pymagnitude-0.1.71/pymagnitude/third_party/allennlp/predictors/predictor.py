
from __future__ import absolute_import
#typing
import json

from allennlp.common import Registrable
from allennlp.common.checks import ConfigurationError
from allennlp.common.util import JsonDict, sanitize
from allennlp.data import DatasetReader, Instance
from allennlp.models import Model
from allennlp.models.archival import load_archive

# a mapping from model `type` to the default Predictor for that type
DEFAULT_PREDICTORS = {
        u'srl': u'semantic-role-labeling',
        u'decomposable_attention': u'textual-entailment',
        u'bidaf': u'machine-comprehension',
        u'bidaf-ensemble': u'machine-comprehension',
        u'simple_tagger': u'sentence-tagger',
        u'crf_tagger': u'sentence-tagger',
        u'coref': u'coreference-resolution',
        u'constituency_parser': u'constituency-parser',
}

class Predictor(Registrable):
    u"""
    a ``Predictor`` is a thin wrapper around an AllenNLP model that handles JSON -> JSON predictions
    that can be used for serving models through the web API or making predictions in bulk.
    """
    def __init__(self, model       , dataset_reader               )        :
        self._model = model
        self._dataset_reader = dataset_reader

    def load_line(self, line     )            :  # pylint: disable=no-self-use
        u"""
        If your inputs are not in JSON-lines format (e.g. you have a CSV)
        you can override this function to parse them correctly.
        """
        return json.loads(line)

    def dump_line(self, outputs          )       :  # pylint: disable=no-self-use
        u"""
        If you don't want your outputs in JSON-lines format
        you can override this function to output them differently.
        """
        return json.dumps(outputs) + u"\n"

    def predict_json(self, inputs          )            :
        instance = self._json_to_instance(inputs)
        return self.predict_instance(instance)

    def predict_instance(self, instance          )            :
        outputs = self._model.forward_on_instance(instance)
        return sanitize(outputs)

    def _json_to_instance(self, json_dict          )            :
        u"""
        Converts a JSON object into an :class:`~allennlp.data.instance.Instance`
        and a ``JsonDict`` of information which the ``Predictor`` should pass through,
        such as tokenised inputs.
        """
        raise NotImplementedError

    def predict_batch_json(self, inputs                )                  :
        instances = self._batch_json_to_instances(inputs)
        return self.predict_batch_instance(instances)

    def predict_batch_instance(self, instances                )                  :
        outputs = self._model.forward_on_instances(instances)
        return sanitize(outputs)

    def _batch_json_to_instances(self, json_dicts                )                  :
        u"""
        Converts a list of JSON objects into a list of :class:`~allennlp.data.instance.Instance`s.
        By default, this expects that a "batch" consists of a list of JSON blobs which would
        individually be predicted by :func:`predict_json`. In order to use this method for
        batch prediction, :func:`_json_to_instance` should be implemented by the subclass, or
        if the instances have some dependency on each other, this method should be overridden
        directly.
        """
        instances = []
        for json_dict in json_dicts:
            instances.append(self._json_to_instance(json_dict))
        return instances

    @classmethod
    def from_path(cls, archive_path     , predictor_name      = None)               :
        u"""
        Instantiate a :class:`Predictor` from an archive path.

        If you need more detailed configuration options, such as running the predictor on the GPU,
        please use `from_archive`.

        Parameters
        ----------
        archive_path The path to the archive.

        Returns
        -------
        A Predictor instance.
        """
        return Predictor.from_archive(load_archive(archive_path), predictor_name)

    @classmethod
    def from_archive(cls, archive         , predictor_name      = None)               :
        u"""
        Instantiate a :class:`Predictor` from an :class:`~allennlp.models.archival.Archive`;
        that is, from the result of training a model. Optionally specify which `Predictor`
        subclass; otherwise, the default one for the model will be used.
        """
        # Duplicate the config so that the config inside the archive doesn't get consumed
        config = archive.config.duplicate()

        if not predictor_name:
            model_type = config.get(u"model").get(u"type")
            if not model_type in DEFAULT_PREDICTORS:
                raise ConfigurationError("No default predictor for model type {model_type}.\n"\
                                         "Please specify a predictor explicitly.")
            predictor_name = DEFAULT_PREDICTORS[model_type]

        dataset_reader_params = config[u"dataset_reader"]
        dataset_reader = DatasetReader.from_params(dataset_reader_params)

        model = archive.model
        model.eval()

        return Predictor.by_name(predictor_name)(model, dataset_reader)
