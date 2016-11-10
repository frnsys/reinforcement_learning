import random
from time import sleep
from environment import Environment


class QLearner():
    def __init__(self, state, environment, rewards, discount=0.5, explore=0.5, learning_rate=1):
        """
        - state: the agent's starting state
        - rewards: a reward function, taking a state as input, or a mapping of states to a reward value
        - discount: how much the agent values future rewards over immediate rewards
        - explore: with what probability the agent "explores", i.e. chooses a random action
        - learning_rate: how quickly the agent learns. For deterministic environments (like ours), this should be left at 1
        """
        self.discount = discount
        self.explore = explore
        self.learning_rate = learning_rate
        self.R = rewards.get if isinstance(rewards, dict) else rewards

        # our state is just our position
        self.state = state
        self.reward = 0
        self.env = environment

        # initialize Q
        self.Q = {}

    def reset(self, state):
        self.state = state
        self.reward = 0

    def actions(self, state):
        return self.env.actions(state)

    def _take_action(self, state, action):
        r, c = state
        if action == 'up':
            r -= 1
        elif action == 'down':
            r += 1
        elif action == 'right':
            c += 1
        elif action == 'left':
            c -= 1

        # return new state
        return (r,c)

    def step(self, action=None):
        """take an action"""
        # check possible actions given state
        actions = self.actions(self.state)

        # if this is the first time in this state,
        # initialize possible actions
        if self.state not in self.Q:
            self.Q[self.state] = {a: 0 for a in actions}

        if action is None:
            if random.random() < self.explore:
                action = random.choice(actions)
            else:
                action = self._best_action(self.state)
        elif action not in actions:
            raise ValueError('unrecognized action!')

        # remember this state and action
        # so we can later remember
        # "from this state, taking this action is this valuable"
        prev_state = self.state

        # update state
        self.state = self._take_action(self.state, action)

        # update the previous state/action based on what we've learned
        self._learn(prev_state, action, self.state)
        return action

    def _best_action(self, state):
        """choose the best action given a state"""
        actions_rewards = list(self.Q[state].items())
        return max(actions_rewards, key=lambda x: x[1])[0]

    def _learn(self, prev_state, action, new_state):
        """update Q-value for the last taken action"""
        if new_state not in self.Q:
            self.Q[new_state] = {a: 0 for a in self.actions(new_state)}
        reward = self.R(new_state)
        self.reward += reward
        self.Q[prev_state][action] = self.Q[prev_state][action] + self.learning_rate * (reward + self.discount * max(self.Q[new_state].values()) - self.Q[prev_state][action])


def choose_action(agent):
    """interactively choose action for agent"""
    actions = agent.actions(agent.state)
    action = None
    while action is None:
        try:
            action = input('what should I do? {} >>> '.format(actions))
            if action == 'quit':
                return True
            agent.step(action)
        except ValueError:
            action = None
    return False


def play_and_visualize(agent, episodes):
    agent.explore = 0
    mean_reward = 0
    for i in range(episodes):
        steps = 0
        game_over = False
        # start at a random position
        pos = random.choice(env.starting_positions)
        agent.reset(pos)
        env.render(agent.state)
        print('starting')
        print('mean reward: {}'.format(mean_reward/i if i > 0 else 0))
        sleep(1)
        while not game_over:
            agent.step()
            env.render(agent.state)
            steps += 1
            print('steps: {}, reward: {}'.format(steps, agent.reward))
            print('mean reward: {}'.format(mean_reward/i if i > 0 else 0))
            sleep(0.4)
            game_over = env.is_terminal_state(agent.state)
        mean_reward += agent.reward
        sleep(1)


if __name__ == '__main__':
    INTERACTIVE = False
    TRAIN = True

    # define the gridworld environment
    env = Environment([
        [   0,  0,    0,  0,    0, None, None],
        [   0,  0,    5,  0,    0,    0, None],
        [   0,  0, None,  5, None,    0, None],
        [None,  0,    5,  5, None,   10,    0]
    ])

    # start at a random position
    pos = random.choice(env.starting_positions)

    # try discount=0.1 and discount=0.9
    DISCOUNT = 0.9
    LEARNING_RATE = 1
    agent = QLearner(pos, env, env.reward, discount=DISCOUNT, learning_rate=LEARNING_RATE)

    if INTERACTIVE:
        i = 0
        env.render(agent.state)
        while True:
            done = choose_action(agent)
            if done:
                break
            env.render(agent.state)
            print('step: {:03d}, explore: {:.2f}, discount: {}'.format(i, agent.explore, agent.discount))
            for pos, vals in agent.Q.items():
                print('{} -> {}'.format(pos, vals))
            i += 1

    else:
        if TRAIN:
            print('training...')
            episodes = 500
            agent.explore = 0.5
            for i in range(episodes):
                game_over = False
                pos = random.choice(env.starting_positions)
                agent.reset(pos)
                while not game_over:
                    agent.step()
                    game_over = env.is_terminal_state(agent.state)
            print('done training')

            # let's see how it does
            print('after training...')
            play_and_visualize(agent, 5)

        else:
            print('without training...')
            play_and_visualize(agent, 5)

        from policy import PolicyRenderer
        renderer = PolicyRenderer(agent, env, cell_size=100)
        renderer.render().save('/tmp/gridworld.png')
