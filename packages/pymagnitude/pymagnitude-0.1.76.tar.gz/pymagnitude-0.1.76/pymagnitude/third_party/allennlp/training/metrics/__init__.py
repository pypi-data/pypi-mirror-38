u"""
A :class:`~allennlp.training.metrics.metric.Metric` is some quantity or quantities
that can be accumulated during training or evaluation; for example,
accuracy or F1 score.
"""


from __future__ import absolute_import
# from allennlp.training.metrics.metric import Metric
# from allennlp.training.metrics.average import Average
# from allennlp.training.metrics.boolean_accuracy import BooleanAccuracy
# from allennlp.training.metrics.categorical_accuracy import CategoricalAccuracy
# from allennlp.training.metrics.conll_coref_scores import ConllCorefScores
# from allennlp.training.metrics.entropy import Entropy
# from allennlp.training.metrics.evalb_bracketing_scorer import EvalbBracketingScorer, DEFAULT_EVALB_DIR
# from allennlp.training.metrics.f1_measure import F1Measure
# from allennlp.training.metrics.mention_recall import MentionRecall
# from allennlp.training.metrics.span_based_f1_measure import SpanBasedF1Measure
# from allennlp.training.metrics.squad_em_and_f1 import SquadEmAndF1
# from allennlp.training.metrics.wikitables_accuracy import WikiTablesAccuracy
# from allennlp.training.metrics.attachment_scores import AttachmentScores

class Metric:
    pass

class Average:
    pass

class BooleanAccuracy:
    pass

class CategoricalAccuracy:
    pass

class ConllCorefScores:
    pass

class Entropy:
    pass

class EvalbBracketingScorer:
    pass

DEFAULT_EVALB_DIR = None

class F1Measure:
    pass

class MentionRecall:
    pass

class SpanBasedF1Measure:
    pass

class SquadEmAndF1:
    pass

class WikiTablesAccuracy:
    pass

class AttachmentScores:
    pass

