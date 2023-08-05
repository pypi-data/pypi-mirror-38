
from __future__ import absolute_import
#typing

#overrides
import torch

from allennlp.data.fields.field import Field
from allennlp.data.fields.sequence_field import SequenceField
from allennlp.common.checks import ConfigurationError


class IndexField(Field):
    u"""
    An ``IndexField`` is an index into a
    :class:`~allennlp.data.fields.sequence_field.SequenceField`, as might be used for representing
    a correct answer option in a list, or a span begin and span end position in a passage, for
    example.  Because it's an index into a :class:`SequenceField`, we take one of those as input
    and use it to compute padding lengths.

    Parameters
    ----------
    index : ``int``
        The index of the answer in the :class:`SequenceField`.  This is typically the "correct
        answer" in some classification decision over the sequence, like where an answer span starts
        in SQuAD, or which answer option is correct in a multiple choice question.  A value of
        ``-1`` means there is no label, which can be used for padding or other purposes.
    sequence_field : ``SequenceField``
        A field containing the sequence that this ``IndexField`` is a pointer into.
    """
    def __init__(self, index     , sequence_field               )        :
        self.sequence_index = index
        self.sequence_field = sequence_field

        if not isinstance(index, int):
            raise ConfigurationError(u"IndexFields must be passed integer indices. "
                                     u"Found index: {} with type: {}.".format(index, type(index)))

    #overrides
    def get_padding_lengths(self)                  :
        # pylint: disable=no-self-use
        return {}

    #overrides
    def as_tensor(self,
                  padding_lengths                ,
                  cuda_device      = -1)                :
        # pylint: disable=unused-argument
        tensor = torch.LongTensor([self.sequence_index])
        return tensor if cuda_device == -1 else tensor.cuda(cuda_device)

    #overrides
    def empty_field(self):
        return IndexField(-1, self.sequence_field.empty_field())

    def __str__(self)       :
        return "IndexField with index: {self.sequence_index}."
