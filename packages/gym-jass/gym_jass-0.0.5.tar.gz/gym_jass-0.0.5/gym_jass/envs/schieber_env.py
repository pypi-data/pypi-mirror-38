import gym
from gym import spaces

from schieber.game import Game
from schieber.player.random_player import RandomPlayer
from schieber.player.greedy_player.greedy_player import GreedyPlayer
from schieber.team import Team


class SchieberEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-257, 257)  # our points minus opponent team's points. reward is always given at the end of one game

    # by looking into the code of ppo2 in openai/baselines the ob_space and ac_space are not even used!
    action_space = spaces.Discrete(36)  # cards on the hand of 36 cards available
    observation_space = spaces.Discrete(36)  # cards on the hand of 36 cards available

    # observation_space = spaces.Dict({
    #    "stiche": spaces.MultiDiscrete([[]]),  # use list of boxes
    #    "trumpf": spaces.Discrete(6),  # number of possible trumpfs (geschoben excluded)
    #    "cards_on_table": spaces.MultiDiscrete([[]])  # use list of boxes
    # })

    def __init__(self):
        player = GreedyPlayer(name='RL')
        players = [player, RandomPlayer(name='Donald'), RandomPlayer(name='Barrack'), RandomPlayer(name='Hillary')]

        team_1 = Team(players=[players[0], players[2]])
        team_2 = Team(players=[players[1], players[3]])
        teams = [team_1, team_2]

        # disable counting factor to make skill more important
        self.game = Game(teams, point_limit=1000, use_counting_factor=False)
        self.game.play()

    def step(self, action):
        """Run one timestep of the environment's dynamics. When end of
        episode is reached, you are responsible for calling `reset()`
        to reset this environment's state.

        Accepts an action and returns a tuple (observation, reward, done, info).

        Parameters
        ----------
        action (object): an action provided by the environment

        Returns
        -------
        observation, reward, episode_over, info : tuple
            observation (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        self._take_action(action)
        reward = self._get_reward()
        observation = self._get_observation()
        episode_over = self.game.is_over
        if episode_over:
            self.reset()
        return observation, reward, episode_over, {}

    def reset(self):
        """Resets the state of the environment and returns an initial observation.

                Returns: observation (object): the initial observation of the
                    space.
        """
        self.game.reset_points()
        self.game.play()
        return self._get_observation()

    def render(self, mode='human', close=False):
        """Renders the environment.

                The set of supported modes varies per environment. (And some
                environments do not support rendering at all.) By convention,
                if mode is:

                - human: render to the current display or terminal and
                  return nothing. Usually for human consumption.
                - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
                  representing RGB values for an x-by-y pixel image, suitable
                  for turning into a video.
                - ansi: Return a string (str) or StringIO.StringIO containing a
                  terminal-style text representation. The text can include newlines
                  and ANSI escape sequences (e.g. for colors).

                Note:
                    Make sure that your class's metadata 'render.modes' key includes
                      the list of supported modes. It's recommended to call super()
                      in implementations to use the functionality of this method.

                Args:
                    mode (str): the mode to render with
                    close (bool): close all open renderings

                Example:

                class MyEnv(Env):
                    metadata = {'render.modes': ['human', 'rgb_array']}

                    def render(self, mode='human'):
                        if mode == 'rgb_array':
                            return np.array(...) # return RGB frame suitable for video
                        elif mode is 'human':
                            ... # pop up a window and render
                        else:
                            super(MyEnv, self).render(mode=mode) # just raise an exception
                """
        print(self.game.get_status())

    def seed(self, seed=None):
        """Sets the seed for this env's random number generator(s).

        Note:
            Some environments use multiple pseudorandom number generators.
            We want to capture all such seeds used in order to ensure that
            there aren't accidental correlations between multiple generators.

        Returns:
            list<bigint>: Returns the list of seeds used in this env's random
              number generators. The first value in the list should be the
              "main" seed, or the value which a reproducer should pass to
              'seed'. Often, the main seed equals the provided 'seed', but
              this won't be true if seed=None, for example.
        """
        # Seeding makes everything more predictable and reproducible.
        # But this could also be a problem because the players might be more exploitable.

        if seed is not None:
            self.game.seed = seed + 0
            self.game.players[1].seed = seed + 1
            self.game.players[2].seed = seed + 2
            self.game.players[3].seed = seed + 3
        return

    def _take_action(self, action):
        player = self.game.players[0]
        assert type(player) == GreedyPlayer
        pass

    def _get_reward(self):
        if self.game.is_over:
            return self.game.teams[0].points - self.game.teams[1].points
        else:
            return 0

    def _get_observation(self):
        return 1  # just return dummy number (ob_space maybe is not even used)
        # return self.game.get_status()
