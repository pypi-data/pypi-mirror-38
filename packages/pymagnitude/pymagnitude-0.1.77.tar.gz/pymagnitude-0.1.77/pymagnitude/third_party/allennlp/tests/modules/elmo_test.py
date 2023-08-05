# pylint: disable=no-self-use,invalid-name,protected-access



from __future__ import division
from __future__ import with_statement
from __future__ import absolute_import
import os
import json
import warnings
#typing
from io import open
try:
    from itertools import izip
except:
    izip = zip


with warnings.catch_warnings():
    warnings.filterwarnings(u"ignore", category=FutureWarning)
    import h5py
import numpy
import torch

from allennlp.common.testing import AllenNlpTestCase
from allennlp.data.token_indexers.elmo_indexer import ELMoTokenCharactersIndexer
from allennlp.data.token_indexers.single_id_token_indexer import SingleIdTokenIndexer
from allennlp.data import Token, Vocabulary, Instance
from allennlp.data.dataset import Batch
from allennlp.data.iterators import BasicIterator
from allennlp.modules.elmo import _ElmoBiLm, Elmo, _ElmoCharacterEncoder
from allennlp.modules.token_embedders import ElmoTokenEmbedder
from allennlp.data.fields import TextField
from allennlp.nn.util import remove_sentence_boundaries


class ElmoTestCase(AllenNlpTestCase):
    def setUp(self):
        super(ElmoTestCase, self).setUp()
        self.elmo_fixtures_path = self.FIXTURES_ROOT / u'elmo'
        self.options_file = unicode(self.elmo_fixtures_path / u'options.json')
        self.weight_file = unicode(self.elmo_fixtures_path / u'lm_weights.hdf5')
        self.sentences_json_file = unicode(self.elmo_fixtures_path / u'sentences.json')
        self.sentences_txt_file = unicode(self.elmo_fixtures_path / u'sentences.txt')

    def _load_sentences_embeddings(self):
        u"""
        Load the test sentences and the expected LM embeddings.

        These files loaded in this method were created with a batch-size of 3.
        Due to idiosyncrasies with TensorFlow, the 30 sentences in sentences.json are split into 3 files in which
        the k-th sentence in each is from batch k.

        This method returns a (sentences, embeddings) pair where each is a list of length batch_size.
        Each list contains a sublist with total_sentence_count / batch_size elements.  As with the original files,
        the k-th element in the sublist is in batch k.
        """
        with open(self.sentences_json_file) as fin:
            sentences = json.load(fin)

        # the expected embeddings
        expected_lm_embeddings = []
        for k in range(len(sentences)):
            embed_fname = os.path.join(
                    self.elmo_fixtures_path, u'lm_embeddings_{}.hdf5'.format(k)
            )
            expected_lm_embeddings.append([])
            with h5py.File(embed_fname, u'r') as fin:
                for i in range(10):
                    sent_embeds = fin[u'%s' % i][...]
                    sent_embeds_concat = numpy.concatenate(
                            (sent_embeds[0, :, :], sent_embeds[1, :, :]),
                            axis=-1
                    )
                    expected_lm_embeddings[-1].append(sent_embeds_concat)

        return sentences, expected_lm_embeddings

    @staticmethod
    def get_vocab_and_both_elmo_indexed_ids(batch                 ):
        instances = []
        indexer = ELMoTokenCharactersIndexer()
        indexer2 = SingleIdTokenIndexer()
        for sentence in batch:
            tokens = [Token(token) for token in sentence]
            field = TextField(tokens,
                              {u'character_ids': indexer,
                               u'tokens': indexer2})
            instance = Instance({u"elmo": field})
            instances.append(instance)

        dataset = Batch(instances)
        vocab = Vocabulary.from_instances(instances)
        dataset.index_instances(vocab)
        return vocab, dataset.as_tensor_dict()[u"elmo"]


class TestElmoBiLm(ElmoTestCase):
    def test_elmo_bilm(self):
        # get the raw data
        sentences, expected_lm_embeddings = self._load_sentences_embeddings()

        # load the test model
        elmo_bilm = _ElmoBiLm(self.options_file, self.weight_file)

        # Deal with the data.
        indexer = ELMoTokenCharactersIndexer()

        # For each sentence, first create a TextField, then create an instance
        instances = []
        for batch in izip(*sentences):
            for sentence in batch:
                tokens = [Token(token) for token in sentence.split()]
                field = TextField(tokens, {u'character_ids': indexer})
                instance = Instance({u"elmo": field})
                instances.append(instance)

        vocab = Vocabulary()

        # Now finally we can iterate through batches.
        iterator = BasicIterator(3)
        iterator.index_with(vocab)
        for i, batch in enumerate(iterator(instances, num_epochs=1, shuffle=False)):
            lm_embeddings = elmo_bilm(batch[u'elmo'][u'character_ids'])
            top_layer_embeddings, mask = remove_sentence_boundaries(
                    lm_embeddings[u'activations'][2],
                    lm_embeddings[u'mask']
            )

            # check the mask lengths
            lengths = mask.data.numpy().sum(axis=1)
            batch_sentences = [sentences[k][i] for k in range(3)]
            expected_lengths = [
                    len(sentence.split()) for sentence in batch_sentences
            ]
            self.assertEqual(lengths.tolist(), expected_lengths)

            # get the expected embeddings and compare!
            expected_top_layer = [expected_lm_embeddings[k][i] for k in range(3)]
            for k in range(3):
                self.assertTrue(
                        numpy.allclose(
                                top_layer_embeddings[k, :lengths[k], :].data.numpy(),
                                expected_top_layer[k],
                                atol=1.0e-6
                        )
                )

    def test_elmo_char_cnn_cache_does_not_raise_error_for_uncached_words(self):
        sentences = [[u"This", u"is", u"OOV"], [u"so", u"is", u"this"]]
        in_vocab_sentences = [[u"here", u"is"], [u"a", u"vocab"]]
        oov_tensor = self.get_vocab_and_both_elmo_indexed_ids(sentences)[1]
        vocab, in_vocab_tensor = self.get_vocab_and_both_elmo_indexed_ids(in_vocab_sentences)
        words_to_cache = list(vocab.get_token_to_index_vocabulary(u"tokens").keys())
        elmo_bilm = _ElmoBiLm(self.options_file, self.weight_file, vocab_to_cache=words_to_cache)

        elmo_bilm(in_vocab_tensor[u"character_ids"], in_vocab_tensor[u"tokens"])
        elmo_bilm(oov_tensor[u"character_ids"], oov_tensor[u"tokens"])

    def test_elmo_bilm_can_cache_char_cnn_embeddings(self):
        sentences = [[u"This", u"is", u"a", u"sentence"],
                     [u"Here", u"'s", u"one"],
                     [u"Another", u"one"]]
        vocab, tensor = self.get_vocab_and_both_elmo_indexed_ids(sentences)
        words_to_cache = list(vocab.get_token_to_index_vocabulary(u"tokens").keys())
        elmo_bilm = _ElmoBiLm(self.options_file, self.weight_file)
        elmo_bilm.eval()
        no_cache = elmo_bilm(tensor[u"character_ids"], tensor[u"character_ids"])

        # ELMo is stateful, so we need to actually re-initialise it for this comparison to work.
        elmo_bilm = _ElmoBiLm(self.options_file, self.weight_file, vocab_to_cache=words_to_cache)
        elmo_bilm.eval()
        cached = elmo_bilm(tensor[u"character_ids"], tensor[u"tokens"])

        numpy.testing.assert_array_almost_equal(no_cache[u"mask"].data.cpu().numpy(),
                                                cached[u"mask"].data.cpu().numpy())
        for activation_cached, activation in izip(cached[u"activations"], no_cache[u"activations"]):
            numpy.testing.assert_array_almost_equal(activation_cached.data.cpu().numpy(),
                                                    activation.data.cpu().numpy(), decimal=6)

class TestElmo(ElmoTestCase):
    def setUp(self):
        super(TestElmo, self).setUp()

        self.elmo = Elmo(self.options_file, self.weight_file, 2, dropout=0.0)

    def _sentences_to_ids(self, sentences):
        indexer = ELMoTokenCharactersIndexer()

        # For each sentence, first create a TextField, then create an instance
        instances = []
        for sentence in sentences:
            tokens = [Token(token) for token in sentence]
            field = TextField(tokens, {u'character_ids': indexer})
            instance = Instance({u'elmo': field})
            instances.append(instance)

        dataset = Batch(instances)
        vocab = Vocabulary()
        dataset.index_instances(vocab)
        return dataset.as_tensor_dict()[u'elmo'][u'character_ids']

    def test_elmo(self):
        # Correctness checks are in ElmoBiLm and ScalarMix, here we just add a shallow test
        # to ensure things execute.
        sentences = [[u'The', u'sentence', u'.'],
                     [u'ELMo', u'helps', u'disambiguate', u'ELMo', u'from', u'Elmo', u'.']]

        character_ids = self._sentences_to_ids(sentences)
        output = self.elmo(character_ids)
        elmo_representations = output[u'elmo_representations']
        mask = output[u'mask']

        assert len(elmo_representations) == 2
        assert list(elmo_representations[0].size()) == [2, 7, 32]
        assert list(elmo_representations[1].size()) == [2, 7, 32]
        assert list(mask.size()) == [2, 7]

    def test_elmo_4D_input(self):
        sentences = [[[u'The', u'sentence', u'.'],
                      [u'ELMo', u'helps', u'disambiguate', u'ELMo', u'from', u'Elmo', u'.']],
                     [[u'1', u'2'], [u'1', u'2', u'3', u'4', u'5', u'6', u'7']],
                     [[u'1', u'2', u'3', u'4', u'50', u'60', u'70'], [u'The']]]

        all_character_ids = []
        for batch_sentences in sentences:
            all_character_ids.append(self._sentences_to_ids(batch_sentences))

        # (2, 3, 7, 50)
        character_ids = torch.cat([ids.unsqueeze(1) for ids in all_character_ids], dim=1)
        embeddings_4d = self.elmo(character_ids)

        # Run the individual batches.
        embeddings_3d = []
        for char_ids in all_character_ids:
            self.elmo._elmo_lstm._elmo_lstm.reset_states()
            embeddings_3d.append(self.elmo(char_ids))

        for k in range(3):
            numpy.testing.assert_array_almost_equal(
                    embeddings_4d[u'elmo_representations'][0][:, k, :, :].data.numpy(),
                    embeddings_3d[k][u'elmo_representations'][0].data.numpy()
            )

    def test_elmo_with_module(self):
        # We will create the _ElmoBilm class and pass it in as a module.
        sentences = [[u'The', u'sentence', u'.'],
                     [u'ELMo', u'helps', u'disambiguate', u'ELMo', u'from', u'Elmo', u'.']]

        character_ids = self._sentences_to_ids(sentences)
        elmo_bilm = _ElmoBiLm(self.options_file, self.weight_file)
        elmo = Elmo(None, None, 2, dropout=0.0, module=elmo_bilm)
        output = elmo(character_ids)
        elmo_representations = output[u'elmo_representations']

        assert len(elmo_representations) == 2
        for k in range(2):
            assert list(elmo_representations[k].size()) == [2, 7, 32]

    def test_elmo_bilm_can_handle_higher_dimensional_input_with_cache(self):
        sentences = [[u"This", u"is", u"a", u"sentence"],
                     [u"Here", u"'s", u"one"],
                     [u"Another", u"one"]]
        vocab, tensor = self.get_vocab_and_both_elmo_indexed_ids(sentences)
        words_to_cache = list(vocab.get_token_to_index_vocabulary(u"tokens").keys())
        elmo_bilm = Elmo(self.options_file, self.weight_file, 1, vocab_to_cache=words_to_cache)
        elmo_bilm.eval()

        individual_dim = elmo_bilm(tensor[u"character_ids"], tensor[u"tokens"])
        elmo_bilm = Elmo(self.options_file, self.weight_file, 1, vocab_to_cache=words_to_cache)
        elmo_bilm.eval()

        expanded_word_ids = torch.stack([tensor[u"tokens"] for _ in range(4)], dim=1)
        expanded_char_ids = torch.stack([tensor[u"character_ids"] for _ in range(4)], dim=1)
        expanded_result = elmo_bilm(expanded_char_ids, expanded_word_ids)
        split_result = [x.squeeze(1) for x in torch.split(expanded_result[u"elmo_representations"][0], 1, dim=1)]
        for expanded in split_result:
            numpy.testing.assert_array_almost_equal(expanded.data.cpu().numpy(),
                                                    individual_dim[u"elmo_representations"][0].data.cpu().numpy())


class TestElmoRequiresGrad(ElmoTestCase):
    def _run_test(self, requires_grad):
        embedder = ElmoTokenEmbedder(self.options_file, self.weight_file, requires_grad=requires_grad)
        batch_size = 3
        seq_len = 4
        char_ids = torch.from_numpy(numpy.random.randint(0, 262, (batch_size, seq_len, 50)))
        embeddings = embedder(char_ids)
        loss = embeddings.sum()
        loss.backward()

        elmo_grads = [param.grad for name, param in embedder.named_parameters() if u'_elmo_lstm' in name]
        if requires_grad:
            # None of the elmo grads should be None.
            assert all([grad is not None for grad in elmo_grads])
        else:
            # All of the elmo grads should be None.
            assert all([grad is None for grad in elmo_grads])

    def test_elmo_requires_grad(self):
        self._run_test(True)

    def test_elmo_does_not_require_grad(self):
        self._run_test(False)


class TestElmoTokenRepresentation(ElmoTestCase):
    def test_elmo_token_representation(self):
        # Load the test words and convert to char ids
        with open(os.path.join(self.elmo_fixtures_path, u'vocab_test.txt'), u'r') as fin:
            words = fin.read().strip().split(u'\n')

        vocab = Vocabulary()
        indexer = ELMoTokenCharactersIndexer()
        tokens = [Token(word) for word in words]

        indices = indexer.tokens_to_indices(tokens, vocab, u"elmo")
        # There are 457 tokens. Reshape into 10 batches of 50 tokens.
        sentences = []
        for k in range(10):
            char_indices = indices[u"elmo"][(k * 50):((k + 1) * 50)]
            sentences.append(
                    indexer.pad_token_sequence(
                            {u'key': char_indices}, desired_num_tokens={u'key': 50}, padding_lengths={}
                    )[u'key']
            )
        batch = torch.from_numpy(numpy.array(sentences))

        elmo_token_embedder = _ElmoCharacterEncoder(self.options_file, self.weight_file)
        elmo_token_embedder_output = elmo_token_embedder(batch)

        # Reshape back to a list of words and compare with ground truth.  Need to also
        # remove <S>, </S>
        actual_embeddings = remove_sentence_boundaries(
                elmo_token_embedder_output[u'token_embedding'],
                elmo_token_embedder_output[u'mask']
        )[0].data.numpy()
        actual_embeddings = actual_embeddings.reshape(-1, actual_embeddings.shape[-1])

        embedding_file = os.path.join(self.elmo_fixtures_path, u'elmo_token_embeddings.hdf5')
        with h5py.File(embedding_file, u'r') as fin:
            expected_embeddings = fin[u'embedding'][...]

        assert numpy.allclose(actual_embeddings[:len(tokens)], expected_embeddings, atol=1e-6)

    def test_elmo_token_representation_bos_eos(self):
        # The additional <S> and </S> embeddings added by the embedder should be as expected.
        indexer = ELMoTokenCharactersIndexer()

        elmo_token_embedder = _ElmoCharacterEncoder(self.options_file, self.weight_file)

        for correct_index, token in [[0, u'<S>'], [2, u'</S>']]:
            indices = indexer.tokens_to_indices([Token(token)], Vocabulary(), u"correct")
            indices = torch.from_numpy(numpy.array(indices[u"correct"])).view(1, 1, -1)
            embeddings = elmo_token_embedder(indices)[u'token_embedding']
            assert numpy.allclose(embeddings[0, correct_index, :].data.numpy(), embeddings[0, 1, :].data.numpy())
