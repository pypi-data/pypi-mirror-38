
from __future__ import absolute_import
#typing

#overrides
import torch
from torch.nn import Dropout

from allennlp.modules.feedforward import FeedForward
from allennlp.modules.layer_norm import LayerNorm
from allennlp.modules.seq2seq_encoders.multi_head_self_attention import MultiHeadSelfAttention
from allennlp.modules.seq2seq_encoders.seq2seq_encoder import Seq2SeqEncoder
from allennlp.nn.activations import Activation
from allennlp.nn.util import add_positional_features
try:
    from itertools import izip
except:
    izip = zip



class StackedSelfAttentionEncoder(Seq2SeqEncoder):
    # pylint: disable=line-too-long
    u"""
    Implements a stacked self-attention encoder similar to the Transformer
    architecture in `Attention is all you Need
    <https://www.semanticscholar.org/paper/Attention-Is-All-You-Need-Vaswani-Shazeer/0737da0767d77606169cbf4187b83e1ab62f6077>`_ .

    This encoder combines 3 layers in a 'block':

    1. A 2 layer FeedForward network.
    2. Multi-headed self attention, which uses 2 learnt linear projections
       to perform a dot-product similarity between every pair of elements
       scaled by the square root of the sequence length.
    3. Layer Normalisation.

    These are then stacked into ``num_layers`` layers.

    Parameters
    ----------
    input_dim : ``int``, required.
        The input dimension of the encoder.
    hidden_dim : ``int``, required.
        The hidden dimension used for the _input_ to self attention layers
        and the _output_ from the feedforward layers.
    projection_dim : ``int``, required.
        The dimension of the linear projections for the self-attention layers.
    feedforward_hidden_dim : ``int``, required.
        The middle dimension of the FeedForward network. The input and output
        dimensions are fixed to ensure sizes match up for the self attention layers.
    num_layers : ``int``, required.
        The number of stacked self attention -> feedfoward -> layer normalisation blocks.
    num_attention_heads : ``int``, required.
        The number of attention heads to use per layer.
    use_positional_encoding: ``bool``, optional, (default = True)
        Whether to add sinusoidal frequencies to the input tensor. This is strongly recommended,
        as without this feature, the self attention layers have no idea of absolute or relative
        position (as they are just computing pairwise similarity between vectors of elements),
        which can be important features for many tasks.
    dropout_prob : ``float``, optional, (default = 0.1)
        The dropout probability for the feedforward network.
    residual_dropout_prob : ``float``, optional, (default = 0.2)
        The dropout probability for the residual connections.
    attention_dropout_prob : ``float``, optional, (default = 0.1)
        The dropout probability for the attention distributions in each attention layer.
    """
    def __init__(self,
                 input_dim     ,
                 hidden_dim     ,
                 projection_dim     ,
                 feedforward_hidden_dim     ,
                 num_layers     ,
                 num_attention_heads     ,
                 use_positional_encoding       = True,
                 dropout_prob        = 0.1,
                 residual_dropout_prob        = 0.2,
                 attention_dropout_prob        = 0.1)        :
        super(StackedSelfAttentionEncoder, self).__init__()

        self._use_positional_encoding = use_positional_encoding
        self._attention_layers = []
        self._feedfoward_layers = []
        self._layer_norm_layers = []
        self._feed_forward_layer_norm_layers = []

        feedfoward_input_dim = input_dim
        for i in range(num_layers):
            feedfoward = FeedForward(feedfoward_input_dim,
                                     activations=[Activation.by_name(u'relu')(),
                                                  Activation.by_name(u'linear')()],
                                     hidden_dims=[feedforward_hidden_dim, hidden_dim],
                                     num_layers=2,
                                     dropout=dropout_prob)

            self.add_module("feedforward_{i}", feedfoward)
            self._feedfoward_layers.append(feedfoward)

            feedforward_layer_norm = LayerNorm(feedfoward.get_output_dim())
            self.add_module("feedforward_layer_norm_{i}", feedforward_layer_norm)
            self._feed_forward_layer_norm_layers.append(feedforward_layer_norm)

            self_attention = MultiHeadSelfAttention(num_heads=num_attention_heads,
                                                    input_dim=hidden_dim,
                                                    attention_dim=projection_dim,
                                                    values_dim=projection_dim,
                                                    attention_dropout_prob=attention_dropout_prob)
            self.add_module("self_attention_{i}", self_attention)
            self._attention_layers.append(self_attention)

            layer_norm = LayerNorm(self_attention.get_output_dim())
            self.add_module("layer_norm_{i}", layer_norm)
            self._layer_norm_layers.append(layer_norm)

            feedfoward_input_dim = hidden_dim

        self.dropout = Dropout(residual_dropout_prob)
        self._input_dim = input_dim
        self._output_dim = self._attention_layers[-1].get_output_dim()

    #overrides
    def get_input_dim(self)       :
        return self._input_dim

    #overrides
    def get_output_dim(self)       :
        return self._output_dim

    #overrides
    def is_bidirectional(self):
        return False

    #overrides
    def forward(self, inputs              , mask              ): # pylint: disable=arguments-differ
        if self._use_positional_encoding:
            output = add_positional_features(inputs)
        else:
            output = inputs
        for (attention,
             feedforward,
             feedforward_layer_norm,
             layer_norm) in izip(self._attention_layers,
                                self._feedfoward_layers,
                                self._feed_forward_layer_norm_layers,
                                self._layer_norm_layers):
            cached_input = output
            # Project output of attention encoder through a feedforward
            # network and back to the input size for the next layer.
            # shape (batch_size, timesteps, input_size)
            feedforward_output = feedforward(output)
            feedforward_output = self.dropout(feedforward_output)
            if feedforward_output.size() == cached_input.size():
                # First layer might have the wrong size for highway
                # layers, so we exclude it here.
                feedforward_output = feedforward_layer_norm(feedforward_output + cached_input)
            # shape (batch_size, sequence_length, hidden_dim)
            attention_output = attention(feedforward_output, mask)
            output = layer_norm(self.dropout(attention_output) + feedforward_output)

        return output

StackedSelfAttentionEncoder = Seq2SeqEncoder.register(u"stacked_self_attention")(StackedSelfAttentionEncoder)
