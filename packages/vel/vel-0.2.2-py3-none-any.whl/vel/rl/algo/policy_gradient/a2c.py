import torch
import torch.nn.functional as F

from vel.api.metrics.averaging_metric import AveragingNamedMetric
from vel.rl.api.base import OptimizerAlgoBase
from vel.math.functions import explained_variance


class A2CPolicyGradient(OptimizerAlgoBase):
    """ Simplest policy gradient - calculate loss as an advantage of an actor versus value function """
    def __init__(self, entropy_coefficient, value_coefficient, max_grad_norm):
        super().__init__(max_grad_norm)

        self.entropy_coefficient = entropy_coefficient
        self.value_coefficient = value_coefficient

    def calculate_gradient(self, batch_info, device, model, rollout):
        """ Calculate loss of the supplied rollout """
        evaluator = model.evaluate(rollout)

        # Use evaluator interface to get the what we are interested in from the model
        advantages = evaluator.get('rollout:estimated_advantages')
        returns = evaluator.get('rollout:estimated_returns')
        rollout_values = evaluator.get('rollout:estimated_values')

        logprobs = evaluator.get('model:action:logprobs')
        values = evaluator.get('model:estimated_values')
        entropy = evaluator.get('model:entropy')

        # Actual calculations. Pretty trivial
        policy_loss = -torch.mean(advantages * logprobs)
        value_loss = 0.5 * F.mse_loss(values, returns)
        policy_entropy = torch.mean(entropy)

        loss_value = (
            policy_loss - self.entropy_coefficient * policy_entropy + self.value_coefficient * value_loss
        )

        loss_value.backward()

        return {
            'policy_loss': policy_loss.item(),
            'value_loss': value_loss.item(),
            'policy_entropy': policy_entropy.item(),
            'advantage_norm': torch.norm(advantages).item(),
            'explained_variance': explained_variance(returns, rollout_values)
        }

    def metrics(self) -> list:
        """ List of metrics to track for this learning process """
        return [
            AveragingNamedMetric("value_loss"),
            AveragingNamedMetric("policy_entropy"),
            AveragingNamedMetric("policy_loss"),
            AveragingNamedMetric("grad_norm"),
            AveragingNamedMetric("advantage_norm"),
            AveragingNamedMetric("explained_variance")
        ]


def create(entropy_coefficient, value_coefficient, max_grad_norm):
    return A2CPolicyGradient(entropy_coefficient, value_coefficient, max_grad_norm)
