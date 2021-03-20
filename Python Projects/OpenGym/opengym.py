# opengym.py
"""Volume 2: Open Gym
<Name>
<Class>
<Date>
"""

import gym
import numpy as np
from IPython.display import clear_output
import random

def find_qvalues(env,alpha=.1,gamma=.6,epsilon=.1):
    """
    Use the Q-learning algorithm to find qvalues.

    Parameters:
        env (str): environment name
        alpha (float): learning rate
        gamma (float): discount factor
        epsilon (float): maximum value

    Returns:
        q_table (ndarray nxm)
    """
    # Make environment
    env = gym.make(env)
    # Make Q-table
    q_table = np.zeros((env.observation_space.n,env.action_space.n))

    # Train
    for i in range(1,100001):
        # Reset state
        state = env.reset()

        epochs, penalties, reward, = 0,0,0
        done = False

        while not done:
            # Accept based on alpha
            if random.uniform(0,1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            # Take action
            next_state, reward, done, info = env.step(action)

            # Calculate new qvalue
            old_value = q_table[state,action]
            next_max = np.max(q_table[next_state])

            new_value = (1-alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value

            # Check if penalty is made
            if reward == -10:
                penalties += 1

            # Get next observation
            state = next_state
            epochs += 1

        # Print episode number
        if i % 100 == 0:
            clear_output(wait=True)
            print(f"Episode: {i}")

    print("Training finished.")
    return q_table

# Problem 1
def random_blackjack(n):
    """
    Play a random game of Blackjack. Determine the
    percentage the player wins out of n times.

    Parameters:
        n (int): number of iterations

    Returns:
        percent (float): percentage that the player
                         wins
    """
    env = gym.make('Blackjack-v0')
    gamesWon = 0
    for i in range(n): # play n games of blackjack
        reward = 0
        done = False
        env.reset()
        while not done: # make random steps until the game ends
            observation = env.reset()
            observation, reward, done, info = env.step(env.action_space.sample())
            
        if reward == 1: # determine if the player won
            gamesWon += 1

    env.close()
    return gamesWon / n



# Problem 2
def blackjack(n=11):
    """
    Play blackjack with naive algorithm.

    Parameters:
        n (int): maximum accepted player hand

    Return:
        percent (float): percentage of 10000 iterations
                         that the player wins
    """
    env = gym.make('Blackjack-v0')
    win = 0
    total = 10000
    for i in range(10000): # Play plackjack 10000 times
        env.reset()
        done = False
        obs = (0, 0, 0)
        while not done: # Play until the player stands, or busts
            if obs[0] <= n: # If the player's cumulative card sum is less than or equal to n, draw another card
                obs, reward, done, info = env.step(1)
            else: # If the player's sum is greater than n, stand
                obs, reward, done, info = env.step(0)
                
        if reward == 1: # Check if the player won the game
            win += 1
    env.close()
    return win / total

# Problem 3
def cartpole():
    """
    Solve CartPole-v0 by checking the velocity
    of the tip of the pole

    Return:
        iterations (integer): number of steps or iterations
                              to solve the environment
    """
    env = gym.make("CartPole-v0")
    
    try:
        env.reset()
        done = False
        pole_vel = 0
        iter = 0
        while not done: # take steps until an end condition is met
            env.render()
            
            if pole_vel > 0: # If the pole is falling to the right, move cart left
                obs, reward, done, info = env.step(1)
                
            else: # If the pole is falling to the left, move cart right
                obs, reward, done, info = env.step(0)
            iter += 1
            if done:
                break
            pole_vel = obs[3] # Update pole velocity

    finally:
        env.close()
        return iter



# Problem 4
def car():
    """
    Solve MountainCar-v0 by checking the position
    of the car.

    Return:
        iterations (integer): number of steps or iterations
                              to solve the environment
    """
    env = gym.make("MountainCar-v0")

    try:
        env.reset()
        done = False
        car_vel = 0
        iter = 0
        while not done:
            env.render()
            if car_vel > 0: # Determine whether to accelerate or reverse
                obs, reward, done, info = env.step(2)
            else:
                obs, reward, done, info = env.step(0)
            iter += 1
            if done:
                break
            car_vel = obs[1] # Update information
    finally:
        env.close()
        return iter

# Problem 5
def taxi(q_table):
    """
    Compare naive and q-learning algorithms.

    Parameters:
        q_table (ndarray nxm): table of qvalues

    Returns:
        naive (flaot): mean reward of naive algorithm
                       of 10000 runs
        q_reward (float): mean reward of Q-learning algorithm
                          of 10000 runs
    """
    env = gym.make('Taxi-v3')
    
    random_reward = 0
    for i in range(10000):
        done = False
        env.reset()
        while not done:
            obs, reward, done, info = env.step(env.action_space.sample())
        random_reward += reward
        
    env.close()
    env = gym.make('Taxi-v3')
    
    q_reward = 0
    for i in range(10000):
        done = False
        env.reset()
        j = 0
        while not done:
            obs, reward, done, info = env.step(np.argmax(q_table[j,:]))
            j = obs
        q_reward += reward
    
    env.close()
    return random_reward / 10000, q_reward / 10000




    