
# Reinforcement Learning

Reinforcement learning (RL) is a branch of machine learning in which an agent learns to make decisions by interacting with an environment to maximize cumulative rewards. Unlike supervised learning, which uses labeled input–output pairs, RL relies on trial-and-error feedback (rewards or penalties) received from the environment.

## Key Questions

### What is the difference between reinforcement learning and supervised learning?

In supervised learning the model learns from a fixed dataset of input–output pairs. In reinforcement learning the agent learns by interacting with an environment and receiving rewards or penalties based on its actions; there are no explicit labeled correct actions.

### What is Q-learning in reinforcement learning?

Q-learning is a model-free, off-policy reinforcement learning algorithm that estimates the value (expected cumulative reward) of taking an action in a given state. It stores values in a Q-table and updates them using the Bellman equation as the agent gains experience.

### What is a Q-table?

A Q-table is a two-dimensional table that maps state–action pairs to Q-values: Q(s, a). Each row corresponds to a state and each column to an action. The agent chooses actions by looking up Q-values and typically selecting the action with the highest value for the current state.

### Example of a Q-table

Below is a simple example showing three states (S1–S3) and four actions per state. Each entry is the estimated Q-value for that state–action pair.

| State | Action 1 | Action 2 | Action 3 | Action 4 |
|-------:|:--------:|:--------:|:--------:|:--------:|
| S1    |   0.5    |   0.2    |   0.1    |   0.0    |
| S2    |   0.3    |   0.6    |   0.4    |   0.2    |
| S3    |   0.0    |   0.1    |   0.7    |   0.5    |

### How to interpret a Q-table

Each row represents a state and each column represents an action. A larger Q-value for (s,a) means the agent expects higher cumulative reward from taking action `a` in state `s` and following the policy thereafter. The agent typically selects the action with the highest Q-value (greedy selection), though exploration strategies (e.g., ε-greedy) are commonly used during learning to find better policies.

## Quick references / next steps

- See `1 - Q-Learning.ipynb` in this folder for a worked example (FrozenLake) and a complete implementation.

