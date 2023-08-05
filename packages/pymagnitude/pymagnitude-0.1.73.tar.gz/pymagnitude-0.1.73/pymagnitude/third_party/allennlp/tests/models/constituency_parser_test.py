# pylint: disable=no-self-use,invalid-name,no-value-for-parameter


from __future__ import division
from __future__ import absolute_import
from nltk import Tree
import torch

from allennlp.common.testing.model_test_case import ModelTestCase
from allennlp.models.constituency_parser import SpanInformation
from allennlp.training.metrics import EvalbBracketingScorer

class SpanConstituencyParserTest(ModelTestCase):

    def setUp(self):
        EvalbBracketingScorer.compile_evalb()
        super(SpanConstituencyParserTest, self).setUp()
        self.set_up_model(self.FIXTURES_ROOT / u"constituency_parser" / u"constituency_parser.json",
                          self.FIXTURES_ROOT / u"data" / u"example_ptb.trees")

    def tearDown(self):
        EvalbBracketingScorer.clean_evalb()
        super(SpanConstituencyParserTest, self).tearDown()

    def test_span_parser_can_save_and_load(self):
        self.ensure_model_can_train_save_and_load(self.param_file)

    def test_batch_predictions_are_consistent(self):
        self.ensure_batch_predictions_are_consistent()

    def test_forward_can_handle_a_single_word_as_input(self):
        # A very annoying edge case: the PTB has several single word sentences.
        # when running with a batch size 1, we have to be very careful
        # about how we .squeeze/.unsqueeze things to make sure it still runs.
        text = {u"tokens": torch.LongTensor([[1]])}
        pos_tags = torch.LongTensor([[1]])
        spans = torch.LongTensor([[[0, 0]]])
        label = torch.LongTensor([[1]])
        self.model(text, spans, [{u"tokens": [u"hello"]}], pos_tags, label)

    def test_decode_runs(self):
        self.model.eval()
        training_tensors = self.dataset.as_tensor_dict()
        output_dict = self.model(**training_tensors)
        decode_output_dict = self.model.decode(output_dict)
        assert set(decode_output_dict.keys()) == set([u'spans', u'class_probabilities', u'trees',
                                                  u'tokens', u'pos_tags', u'num_spans', u'loss'])
        metrics = self.model.get_metrics(reset=True)
        metric_keys = set(metrics.keys())
        assert u"evalb_precision" in metric_keys
        assert u"evalb_recall" in metric_keys
        assert u"evalb_f1_measure" in metric_keys

    def test_resolve_overlap_conflicts_greedily(self):
        spans = [SpanInformation(start=1, end=5, no_label_prob=0.7,
                                 label_prob=0.2, label_index=2),
                 SpanInformation(start=2, end=7, no_label_prob=0.5,
                                 label_prob=0.3, label_index=4)]
        resolved_spans = self.model.resolve_overlap_conflicts_greedily(spans)
        assert resolved_spans == [SpanInformation(start=2, end=7, no_label_prob=0.5,
                                                  label_prob=0.3, label_index=4)]

    def test_construct_tree_from_spans(self):
        # (S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))
        tree_spans = [((0, 1), u'D'), ((1, 2), u'N'), ((0, 2), u'NP'),
                      ((2, 3), u'V'), ((3, 4), u'D'), ((4, 5), u'N'),
                      ((3, 5), u'NP'), ((2, 5), u'VP'), ((0, 5), u'S')]
        sentence = [u"the", u"dog", u"chased", u"the", u"cat"]
        tree = self.model.construct_tree_from_spans(dict((x, y) for x, y in tree_spans), sentence)
        correct_tree = Tree.fromstring(u"(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
        assert tree == correct_tree

    def test_construct_tree_from_spans_handles_nested_labels(self):
        # The tree construction should split the "S-NP" into (S (NP ...)).
        tree_spans = [((0, 1), u'D'), ((1, 2), u'N'), ((0, 2), u'S-NP')]
        sentence = [u"the", u"dog"]
        tree = self.model.construct_tree_from_spans(dict((x, y) for x, y in tree_spans), sentence)
        correct_tree = Tree.fromstring(u"(S (NP (D the) (N dog)))")
        assert tree == correct_tree

    def test_tree_construction_with_too_few_spans_creates_trees_with_depth_one_word_nodes(self):
        # We only have a partial tree here: (S (NP (D the) (N dog)). Decoding should
        # recover this from the spans, whilst attaching all other words to the root node with
        # XX POS tag labels, as the right hand side splits will not occur in tree_spans.
        tree_spans = [((0, 1), u'D'), ((1, 2), u'N'), ((0, 2), u'NP'), ((0, 5), u'S')]
        sentence = [u"the", u"dog", u"chased", u"the", u"cat"]
        tree = self.model.construct_tree_from_spans(dict((x, y) for x, y in tree_spans), sentence)
        correct_tree = Tree.fromstring(u"(S (NP (D the) (N dog)) (XX chased) (XX the) (XX cat))")
        assert tree == correct_tree
