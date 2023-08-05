"""Module for the base class of all metrics."""

from abc import ABC, abstractmethod

from irl_benchmark.irl.collect import collect_trajs


class BaseMetric(ABC):
    """The base class of all metrics."""

    def __init__(self, metric_input: dict = None):
        """

        Parameters
        ----------
        metric_input: dict
            This dictionary contains relevant data to initialize metrics.
            The dictionary is filled in each :class:`irl_benchmark.experiment.run.Run`.
            Available fields are 'env', 'expert_trajs', and 'true_reward'.
        """
        assert 'env' in metric_input.keys()
        assert 'expert_trajs' in metric_input.keys()
        assert 'true_reward' in metric_input.keys()
        self.metric_input = metric_input
        self.env = metric_input['env']

    @abstractmethod
    def evaluate(self, evaluation_input: dict = None) -> float:
        """Evaluate the metric given some input and return result.

        Parameters
        ----------
        evaluation_input: dict

        Returns
        -------
        float
            The metric for the given input
        """
        raise NotImplementedError()

    def generate_traj_if_not_exists(self, evaluation_input: dict):
        """ Generate trajectories and store them in evaluation input.
        If evaluation input already contains trajectories, do nothing.

        Parameters
        ----------
        evaluation_input

        Returns
        -------
        dict
            evaluation_input
        """
        assert 'irl_agent' in evaluation_input.keys()
        if not 'irl_trajs' in evaluation_input:
            print('generating new trajs for metrics')
            evaluation_input['irl_trajs'] = collect_trajs(
                self.env, evaluation_input['irl_agent'], 100)
        else:
            print('reuse generated trajs for metric')
        return evaluation_input['irl_trajs']
