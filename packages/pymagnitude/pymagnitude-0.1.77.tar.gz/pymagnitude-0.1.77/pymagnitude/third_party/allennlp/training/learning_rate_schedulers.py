u"""
AllenNLP just uses
`PyTorch learning rate schedulers <http://pytorch.org/docs/master/optim.html#how-to-adjust-learning-rate>`_,
with a thin wrapper to allow registering them and instantiating them ``from_params``.

The available learning rate schedulers are

* `"step" <http://pytorch.org/docs/master/optim.html#torch.optim.lr_scheduler.StepLR>`_
* `"multi_step" <http://pytorch.org/docs/master/optim.html#torch.optim.lr_scheduler.MultiStepLR>`_
* `"exponential" <http://pytorch.org/docs/master/optim.html#torch.optim.lr_scheduler.ExponentialLR>`_
* `"reduce_on_plateau" <http://pytorch.org/docs/master/optim.html#torch.optim.lr_scheduler.ReduceLROnPlateau>`_
* `"cosine" <http://pytorch.org/docs/master/optim.html#torch.optim.lr_scheduler.CosineAnnealingLR>`_
"""


from __future__ import absolute_import
#typing

import torch.optim.lr_scheduler
#overrides
from allennlp.common.checks import ConfigurationError
from allennlp.common.params import Params
from allennlp.common.registrable import Registrable
try:
    from itertools import izip
except:
    izip = zip



class LearningRateScheduler(Registrable):
    u"""
    This class just allows us to implement ``Registrable`` for Pytorch :class:`LRSchedulers`.
    """
    def __init__(self, lr_scheduler)        :
        self.lr_scheduler = lr_scheduler

    def step(self, metric       , epoch                = None):
        raise NotImplementedError

    def step_batch(self, batch_num_total               ):
        if batch_num_total is not None:
            if hasattr(self.lr_scheduler, u'step_batch'):
                self.lr_scheduler.step_batch(batch_num_total)
            return

    # Requires custom from_params
    @classmethod
    def from_params(cls, optimizer                       , params        ):  # type: ignore
        # pylint: disable=arguments-differ
        scheduler = params.pop_choice(u"type", LearningRateScheduler.list_available())

        schedulers = LearningRateScheduler.by_name(scheduler)(optimizer, **params.as_dict())  # type: ignore
        if isinstance(schedulers, torch.optim.lr_scheduler.ReduceLROnPlateau):
            return LearningRateWithMetricsWrapper(schedulers)
        else:
            return LearningRateWithoutMetricsWrapper(schedulers)


class LearningRateWithoutMetricsWrapper(LearningRateScheduler):
    u"""
    A wrapper around learning rate schedulers that do not require metrics
    """
    def __init__(self, lr_scheduler                                       )        :  # pylint: disable=protected-access
        super(LearningRateWithoutMetricsWrapper, self).__init__(lr_scheduler)
        self.lr_scheduler = lr_scheduler

    #overrides
    def step(self, metric       , epoch                = None):
        self.lr_scheduler.step(epoch)


class LearningRateWithMetricsWrapper(LearningRateScheduler):
    u"""
    A wrapper around learning rate schedulers that require metrics,
    At the moment there is only a single instance of this lrs. It is the ReduceLROnPlateau
    """
    def __init__(self, lr_scheduler                                            )        :
        super(LearningRateWithMetricsWrapper, self).__init__(lr_scheduler)
        self.lr_scheduler = lr_scheduler

    #overrides
    def step(self, metric       , epoch                = None):
        if metric is None:
            raise ConfigurationError(u"The reduce_on_plateau learning rate scheduler requires "
                                     u"a validation metric to compute the schedule and therefore "
                                     u"must be used with a validation dataset.")
        self.lr_scheduler.step(metric, epoch)


class NoamLR(torch.optim.lr_scheduler._LRScheduler): # pylint: disable=protected-access
    u"""
    Implements the Noam Learning rate schedule. This corresponds to increasing the learning rate
    linearly for the first ``warmup_steps`` training steps, and decreasing it thereafter proportionally
    to the inverse square root of the step number, scaled by the inverse square root of the
    dimensionality of the model. Time will tell if this is just madness or it's actually important.

    Parameters
    ----------
    model_size : ``int``, required.
        The hidden size parameter which dominates the number of parameters in your model.
    warmup_steps: ``int``, required.
        The number of steps to linearly increase the learning rate.
    factor : ``float``, optional (default = 1.0).
        The overall scale factor for the learning rate decay.
    """
    def __init__(self,
                 optimizer                       ,
                 model_size     ,
                 warmup_steps     ,
                 factor        = 1.0,
                 last_epoch      = -1)        :
        self.warmup_steps = warmup_steps
        self.factor = factor
        self.model_size = model_size
        super(NoamLR, self).__init__(optimizer, last_epoch=last_epoch)

    def step(self, epoch=None):
        pass

    def step_batch(self, epoch=None):
        if epoch is None:
            epoch = self.last_epoch + 1
        self.last_epoch = epoch
        for param_group, learning_rate in izip(self.optimizer.param_groups, self.get_lr()):
            param_group[u'lr'] = learning_rate


    def get_lr(self):
        step = max(self.last_epoch, 1)
        scale = self.factor *  (self.model_size ** (-0.5) *
                                min(step ** (-0.5), step * self.warmup_steps ** (-1.5)))

        return [scale for _ in range(len(self.base_lrs))]

# We just use the Pytorch LRSchedulers, so here we force them into
# Registry._registry so we can build them from params.
Registrable._registry[LearningRateScheduler] = {   # pylint: disable=protected-access
        u"step": torch.optim.lr_scheduler.StepLR,
        u"multi_step": torch.optim.lr_scheduler.MultiStepLR,
        u"exponential": torch.optim.lr_scheduler.ExponentialLR,
        u"reduce_on_plateau": torch.optim.lr_scheduler.ReduceLROnPlateau,
        u"cosine": torch.optim.lr_scheduler.CosineAnnealingLR,
        u"noam": NoamLR,
}
