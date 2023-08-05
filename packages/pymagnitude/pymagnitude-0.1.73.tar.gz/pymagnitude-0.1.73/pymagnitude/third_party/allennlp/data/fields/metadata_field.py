# pylint: disable=no-self-use

from __future__ import absolute_import
#typing

#overrides

from allennlp.data.fields.field import Field


class MetadataField(Field):
    u"""
    A ``MetadataField`` is a ``Field`` that does not get converted into tensors.  It just carries
    side information that might be needed later on, for computing some third-party metric, or
    outputting debugging information, or whatever else you need.  We use this in the BiDAF model,
    for instance, to keep track of question IDs and passage token offsets, so we can more easily
    use the official evaluation script to compute metrics.

    We don't try to do any kind of smart combination of this field for batched input - when you use
    this ``Field`` in a model, you'll get a list of metadata objects, one for each instance in the
    batch.

    Parameters
    ----------
    metadata : ``Any``
        Some object containing the metadata that you want to store.  It's likely that you'll want
        this to be a dictionary, but it could be anything you want.
    """
    def __init__(self, metadata     )        :
        self.metadata = metadata

    #overrides
    def get_padding_lengths(self)                  :
        return {}

    #overrides
    def as_tensor(self,
                  padding_lengths                ,
                  cuda_device      = -1)             :
        # pylint: disable=unused-argument
        return self.metadata  # type: ignore

    #overrides
    def empty_field(self)                   :
        return MetadataField(None)

    @classmethod
    #overrides
    def batch_tensors(cls, tensor_list                 )             :  # type: ignore
        return tensor_list  # type: ignore


    def __str__(self)       :
        return "MetadataField (print field.metadata to see specific information)."
