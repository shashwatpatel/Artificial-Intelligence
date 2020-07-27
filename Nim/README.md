## Task:

Write an AI that teaches itself to play Nim through reinforcement learning, using the ε-Greedy Q-Learning method.


## Background:

The game of Nim is played with two players, starting with a number of piles, with each pile containing a number of objects. On each player's turn they must remove any number of objects (minimum 1) from a single non-empty pile. The game is typically played as a _misère_ game, where the person to remove the last object from the game loses. However it can also be played as a _normal play_ game, where the person to remove the last object wins. In our implementation, the game will be in the _misère_ format.


### Solutions to Nim:

Nim has been mathematically solved. A general strategy to win a game of nim involves use of a metric known as the 'nim-sum' for the current game state. The nim-sum is the binary digital sum of the heap sizes, otherwise known as the 'exclusive or' operation. For example if the game board constists of 4 heaps, each heap having 0, 3, 4, and 5 objects in it respectively, the nim-sum for the game is:

```
        Objects   Binary
Heap A    0         000
Heap B    3         011
Heap C    4         100
Heap D    5         101
  ----------------------
          Nim-Sum:  010
```

The winning strategy during normal play is to finish every move with a nim-sum of zero (000). When played as a _misère_ game, this strategy is also optimum until the move would leave only heaps of size one. In this case the correct move is to leave an odd number of heaps of size one, such that the opposing player will always remove the last object, and so lose.

While a program could therefore be written to play Nim in the mathematically optimal way, this project instead uses reinforcement learning in order to train an AI to play Nim. Note that since we are playing _misère_ and the board we are using starts with a nim-sum of 0, if the second player plays optimally, they should always win.


### Reinforcement Learning: Q-Learning

Reinforcement Learning is a process whereby an AI agent is given rewards or punishments for actions taken in a certain state, and thereby learns the optimal actions to take in a given state in the future. For this project we are using the Q-learning algorithm, where the AI learns a function Q(s, a) which estimates the value of performing action 'a' in state 's'. Below is a general outline of the algorithm:

* The Q-learning algorithm starts with Q(s, a) = 0 for all states s and actions a, as it has no initial knowledge about which actions are more valuble to take in any state.
* From an initial state s, an available action will be taken, transitioning to a new state s', and a reward (or punishment) given for the action.
* The agent then updates its estimate for Q(s, a), using the most recently received reward, its old estimate, and the estimated future reward, following this formula:

![Q_{updated}(s, a) \leftarrow Q_{old}(s, a) + \alpha ((Reward_{current} + Reward_{future}) - Q_{old}(s, a))](https://render.githubusercontent.com/render/math?math=Q_%7Bupdated%7D(s%2C%20a)%20%5Cleftarrow%20Q_%7Bold%7D(s%2C%20a)%20%2B%20%5Calpha%20((Reward_%7Bcurrent%7D%20%2B%20Reward_%7Bfuture%7D)%20-%20Q_%7Bold%7D(s%2C%20a)))

where α is the 'learning rate' - how much new information is valued over known information.

* The agent then continues to make moves until the end of the game, and plays multiple repeated games, each time maintaining and updating the values for Q(s, a), gradually learning better and better estimates for the values of all possible actions from any state, if enough games are played.


### ε-Greedy Decision Making:

While a Greedy Decision Making algorithm would always pick the action for any state with the highest estimated value (Q(s, a)), if an AI agent only ever makes greedy moves, it may never learn a globally optimal solution. In such a case once the agent learns a series of states and actions with positive rewards, it will always take this series of actions, and never explore any actions with an unknown reward (i.e. 0).

To avoid the agent finding one rewarding but non-optimal route of play, the Greedy Decision Making algorithm can be modified to an ε-Greedy algorithm. In this case the AI will choose any possible action at random with probability ε, and with probability 1-ε will pick action with the highest estimated value, as in the Greedy algorithm. This allows the AI to explore actions with unknown results, even when actions with known rewards are available, allowing the AI to estimate Q(s, a) for all possible states and actions.


### Representaion of Nim:

In this implementation:

* An action that loses the game will have a reward of -1
* An action that results in the other player losing the game will have a reward of 1
* An action that results in the game continuing has an immediate reward of 0, but will also have some future reward

* A "state" of the Nim game is just the current size of all the piles, and can be repesented as a list, e.g. the state of a -pile game of Nim could be `[1, 1, 3, 5]`.
* An action in the Nim game is a pair of integers `(i, j)` representing the action of taking j objects from pile i.
  * e.g. applying action `(3, 5)` to state `[1, 1, 3, 5]` would result in the new state `[1, 1, 3, 0]`


## Specification:

Complete the implementation of get_q_value, update_q_value, best_future_reward, and choose_action in nim.py. For each of these functions, any time a function accepts a state as input, you may assume it is a list of integers. Any time a function accepts an action as input, you may assume it is an integer pair (i, j) of a pile i and a number of objects j.

The get_q_value function should accept as input a state and action and return the corresponding Q-value for that state/action pair.

* Recall that Q-values are stored in the dictionary self.q. The keys of self.q should be in the form of (state, action) pairs, where state is a tuple of all piles sizes in order, and action is a tuple (i, j) representing a pile and a number.
* If no Q-value for the state/action pair exists in self.q, then the function should return 0.

The update_q_value function takes a state state, an action action, an existing Q value old_q, a current reward reward, and an estimate of future rewards future_rewards, and updates the Q-value for the state/action pair according to the Q-learning formula.

* Recall that the Q-learning formula is: Q(s, a) <- old value estimate + alpha * (new value estimate - old value estimate)
* Recall that alpha is the learning rate associated with the NimAI object.
* The old value estimate is just the existing Q-value for the state/action pair. The new value estimate should be the sum of the current reward and the estimated future reward.

The best_future_reward function accepts a state as input and returns the best possible reward for any available action in that state, according to the data in self.q.

* For any action that doesn’t already exist in self.q for the given state, you should assume it has a Q-value of 0.
* If no actions are available in the state, you should return 0.

The choose_action function should accept a state as input (and optionally an epsilon flag for whether to use the epsilon-greedy algorithm), and return an available action in that state.

* If epsilon is False, your function should behave greedily and return the best possible action available in that state (i.e., the action that has the highest Q-value, using 0 if no Q-value is known).
* If epsilon is True, your function should behave according to the epsilon-greedy algorithm, choosing a random available action with probability self.epsilon and otherwise choosing the best action available.
* If multiple actions have the same Q-value, any of those options is an acceptable return value.
