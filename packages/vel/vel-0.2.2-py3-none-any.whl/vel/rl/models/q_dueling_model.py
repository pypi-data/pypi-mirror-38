import gym

from vel.api.base import LinearBackboneModel, Model, ModelFactory
from vel.rl.api import Rollout, Evaluator
from vel.rl.modules.dueling_q_head import DuelingQHead
from vel.rl.models.q_model import QModelEvaluator


class QDuelingModel(Model):
    """ Wraps a backbone model into API we need for Deep Q-Learning """

    def __init__(self, backbone: LinearBackboneModel, action_space: gym.Space):
        super().__init__()

        self.backbone = backbone
        self.q_head = DuelingQHead(input_dim=backbone.output_dim, action_space=action_space)

    def forward(self, observations):
        """ Model forward pass """
        advantage_features, value_features = self.backbone(observations)
        q_values = self.q_head(advantage_features, value_features)

        return q_values

    def reset_weights(self):
        """ Initialize weights to reasonable defaults """
        self.backbone.reset_weights()
        self.q_head.reset_weights()

    def step(self, observations):
        """ Sample action from an action space for given state """
        q_values = self(observations)

        return {
            'actions': self.q_head.sample(q_values),
            'values': q_values
        }

    def evaluate(self, rollout: Rollout) -> Evaluator:
        """ Evaluate model on a rollout """
        return QModelEvaluator(self, rollout)


class QDuelingModelFactory(ModelFactory):
    """ Factory  class for policy gradient models """
    def __init__(self, backbone: ModelFactory):
        self.backbone = backbone

    def instantiate(self, **extra_args):
        """ Instantiate the model """
        backbone = self.backbone.instantiate(**extra_args)
        return QDuelingModel(backbone, extra_args['action_space'])


def create(backbone: ModelFactory):
    """ DQN model factory """
    return QDuelingModelFactory(backbone=backbone)
