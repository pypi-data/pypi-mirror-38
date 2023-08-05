from __future__ import with_statement
from __future__ import absolute_import
#typing
import json
import tarfile

#overrides

from allennlp.common.checks import ConfigurationError
from allennlp.common.file_utils import cached_path
from allennlp.common.util import pad_sequence_to_length
from allennlp.data.vocabulary import Vocabulary
from allennlp.data.tokenizers.token import Token
from allennlp.data.token_indexers.token_indexer import TokenIndexer
try:
    from itertools import izip
except:
    izip = zip

class OpenaiTransformerBytePairIndexer(TokenIndexer):
    u"""
    Generates the indices for the byte-pair encoding used by
    the OpenAI transformer language model: https://blog.openai.com/language-unsupervised/

    This is unlike most of our TokenIndexers in that its
    indexing is not based on a `Vocabulary` but on a fixed
    set of mappings that are loaded by the constructor.
    """
    # pylint: disable=no-self-use
    def __init__(self,
                 encoder                 = None,
                 byte_pairs                        = None,
                 n_ctx      = 512,
                 model_path      = None)        :

        too_much_information = model_path and (encoder or byte_pairs)
        too_little_information = not model_path and not (encoder and byte_pairs)

        if too_much_information or too_little_information:
            raise ConfigurationError(u"must specify either model path or (encoder + byte_pairs) but not both")

        if model_path:
            model_path = cached_path(model_path)

            # Load encoder and byte_pairs from tar.gz
            with tarfile.open(model_path) as tmp:
                encoder_name = [m.name for m in tmp.getmembers() if u'encoder_bpe' in m.name.next()]
                encoder_info = tmp.extractfile(encoder_name)

                if encoder_info:
                    encoder = json.loads(encoder_info.read())
                else:
                    raise ConfigurationError("expected encoder_bpe file in archive {model_path}")

                bpe_name = [m.name for m in tmp.getmembers() if m.name.endswith(u'.bpe').next() ]
                bpe_info = tmp.extractfile(bpe_name)

                if bpe_info:
                    # First line is "version", last line is blank
                    lines = bpe_info.read().decode(u'utf-8').split(u'\n')[1:-1]
                    # Convert "b1 b2" -> (b1, b2)
                    byte_pairs = [tuple(line.split()) for line in lines]  # type: ignore
                else:
                    raise ConfigurationError("expected .bpe file in archive {model_path}")

        self.encoder = encoder
        self.decoder = dict((word_id, word) for word, word_id in self.encoder.items())

        # Compute ranks
        self.bpe_ranks = dict((pair, idx) for idx, pair in enumerate(byte_pairs))

        self.cache = {}
        self.n_ctx = n_ctx

    #overrides
    def count_vocab_items(self, token       , counter                           ):
        # If we only use pretrained models, we don't need to do anything here.
        pass

    def byte_pair_encode(self, token       , lowercase       = True)             :
        if lowercase:
            text = token.text.lower()
        else:
            text = token.text

        if text in self.cache:
            return self.cache[text]

        # Split into letters, but add a `</w>` to the last
        word = [c for c in text[:-1]]
        word.append(text[-1] + u'</w>')

        # Get unique pairs (prev_symbol, next_symbol)
        pairs = set((prev_symbol, next_symbol)
                 for prev_symbol, next_symbol in izip(word, word[1:]))

        if not pairs:
            return [text + u'</w>']

        while True:
            # Find the highest ranked pair
            bigram = min(pairs, key=lambda pair: self.bpe_ranks.get(pair, float(u'inf')))

            # If that pair is not actually ranked, stop.
            if bigram not in self.bpe_ranks:
                break

            # Split up the pair
            first, second = bigram

            # and make a helper for a new word
            new_word = []
            i = 0

            # Iterate over the letters of the word
            while i < len(word):
                try:
                    # Find first occurrence of `first` after i,
                    j = word.index(first, i)
                    # add all the characters preceding it,
                    new_word.extend(word[i:j])
                    # and update i to j
                    i = j
                except ValueError:
                    # `first` didn't occur, so just add the rest
                    new_word.extend(word[i:])
                    break  # out of while i < len(word)

                # At this point we know word[i] == first
                if i < len(word) - 1 and word[i + 1] == second:
                    new_word.append(first + second)
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1

            word = new_word
            if len(word) == 1:
                break  # out of while True
            else:
                pairs = set((prev_symbol, next_symbol)
                         for prev_symbol, next_symbol in izip(word, word[1:]))

        if u' '.join(word) == u'\n  </w>':
            word = [u'\n</w>']

        self.cache[text] = word
        return word


    #overrides
    def tokens_to_indices(self,
                          tokens             ,
                          _vocabulary            ,
                          index_name     )                        :
        text_tokens = []
        offsets = []
        offset = -1

        for token in tokens:
            bpe_tokens = [self.encoder.get(t, 0) for t in self.byte_pair_encode(token)]
            offset += len(bpe_tokens)
            offsets.append(offset)
            text_tokens.extend(bpe_tokens)

        num_tokens = len(text_tokens)

        # If there's too many tokens, that's going to cause problems.
        if num_tokens > self.n_ctx:
            raise RuntimeError("The transformer model has a maximum sequence length of {self.n_ctx} "
                               "but your byte pair encoded sequence has length {num_tokens}. "
                               "The offending text input is {tokens}.")

        # If there's too few tokens, just pad with zeros.
        text_tokens.extend(0 for _ in range(self.n_ctx - num_tokens))

        return {
                index_name: text_tokens,
                "{index_name}-offsets": offsets,
                # add mask here according to the original tokens,
                # because calling util.get_text_field_mask on the
                # "byte pair" tokens will produce the wrong shape
                u"mask": [1 for _ in offsets]
        }

    #overrides
    def get_padding_token(self)       :
        return 0

    #overrides
    def get_padding_lengths(self, token     )                  :  # pylint: disable=unused-argument
        return {}

    #overrides
    def pad_token_sequence(self,
                           tokens                      ,
                           desired_num_tokens                ,
                           padding_lengths                )                        :  # pylint: disable=unused-argument
        return dict((key, pad_sequence_to_length(val, desired_num_tokens[key]))
                for key, val in tokens.items())

OpenaiTransformerBytePairIndexer = TokenIndexer.register(u"openai_transformer_byte_pair")(OpenaiTransformerBytePairIndexer)
