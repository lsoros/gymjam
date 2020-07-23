# -*- coding: utf-8 -*-
"""LunarLandarColab.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bsj2hxdJAb92gok2t_JsCTOxxMwdnq4W
"""

import sys
import numpy as np
from random import randint
import gym
from time import time
from gym.wrappers import Monitor
from collections import deque
import pickle
import os
import time
import argparse
from checkpointing import Checkpoint
from gym.wrappers.monitoring.video_recorder import VideoRecorder
import zlib

# edit this to customize the output directory, remember to add trailing slash.
RESULTS_OUTPUT_DIR = "/Users/bharathsurianarayanan/Desktop/gymjam/lander_steps_stats/"
# use this to control whether checkpointing is activated or not
CHECKPOINT_ENABLED = False
CHECKPOINT_PREFIX = "untitled"
CHECKPOINT_RESUME = False
CHECKPOINTS_DIR = "checkpoints"
CHECKPOINT_FREQUENCY = 100

ME_ENDPOINT_BC = 'ME-endpointBC'
ME_POLYHASH_BC = 'ME-polyhashBC'
ME_FITNESS_BC = 'ME-fitnessBC'
ME_ENTROPY_BC = 'ME-entropyBC'
MODES = [ME_ENDPOINT_BC, ME_POLYHASH_BC, ME_FITNESS_BC, ME_ENTROPY_BC]
lander_steps_differences_list=np.zeros(100021)
lander_steps_differences_list.fill(-80)
max_lander_contacts_difference=-80
DEFAULT_SEED = 1009
current_run=0
current_run_id=-1

# A generic game evaluator.
# Make specific evaluators if feature info is
# required to be recorded and stored.


class GameEvaluator:
    def __init__(self, game_name, seed=1009, num_rep=1, mode=None):
        self.env = gym.make(game_name)
        self.seed = seed
        self.num_rep = num_rep
        self.num_actions = self.env.action_space.n
        self.mode = mode
        print(self.num_actions)

    def run(self, agent, render=False):
        agent.fitness = 0
        self.env.seed(self.seed)
        env = self.env
        # if render:
        #     env = Monitor(env, './videos/'+str(time())+'/')
        observation = env.reset()

        action_frequency = [0] * self.num_actions

        action_count = 0
        done = False
        positive_rewards=0
        steps_between_landers_contacting_the_ground=0
        lander_contacts_difference=-80
        both_legs_touching_ground=False
        global max_lander_contacts_difference
        global lander_steps_differences_list
        global current_run
        global current_run_id

        if render:
            # env.render()
            rec=VideoRecorder(env,path='/Users/bharathsurianarayanan/Desktop/gymjam/videoResults/'+ current_run_id+'.mp4')


        while not done:
            if render:
            #    env.render()
                rec.capture_frame()


            pos = min(action_count//self.num_rep, len(agent.commands)-1)
            action = agent.commands[pos]
            action_count += 1

            observation, reward, done, info = env.step(action)
            # if(reward>0):
            #     positive_rewards+=1
            # print(observation)

            
            if(observation[6]==1.0 and observation[7]==1.0 and both_legs_touching_ground==False ):
                both_legs_touching_ground=True

                lander_contacts_difference=steps_between_landers_contacting_the_ground
                # print('time taken to contact the ground',steps_between_landers_contacting_the_ground)
            if(observation[6]==1.0 or observation[7]==1.0):
                # print('initial contact with the ground made')
                steps_between_landers_contacting_the_ground+=1

            agent.fitness += reward

            action_frequency[action] += 1

        final_observation = list(observation)
        if(render):
            rec.close()
        # print('positive_rewards are',positive_rewards)
        if(lander_contacts_difference>max_lander_contacts_difference):
            max_lander_contacts_difference=lander_contacts_difference
            print('new max difference is',max_lander_contacts_difference)

        # if(lander_contacts_difference!=-80):
        #     print('time to touch the ground',lander_contacts_difference)
        
        lander_steps_differences_list[current_run]=lander_contacts_difference
        

        current_run+=1
    
        # save to the csv file after every 1000 individuals are evaluated
        if(current_run%1000==0):
            np.savetxt("lander_steps_differences_list"+current_run_id+".csv",lander_steps_differences_list,delimiter=",")
        if(agent.fitness>=200):
            print('agent fitness is ',agent.fitness)

        # For experiment 2D MAP-Elites polyhashBC

        if self.mode == ME_POLYHASH_BC:
            # calculate polynomial hash
            b1 = 3
            b2 = 7

            runningHash1 = 0
            runningHash2 = 0
            for cmd in agent.commands:
                runningHash1 = (runningHash1 * b1 + cmd) % len(agent.commands)
                runningHash2 = (runningHash2 * b2 + cmd) % len(agent.commands)
            agent.features = (runningHash1, runningHash2)
        # For experiment fitnessBC
        elif self.mode == ME_FITNESS_BC:
            agent.features = (agent.fitness, agent.fitness)
        # For experiment entropyBC
        elif self.mode == ME_ENTROPY_BC:
            # calculate RLE approximation
            numNewChars = 0
            prevChar = -2
            for cmd in agent.commands:
                if cmd != prevChar:
                    numNewChars = numNewChars + 1
                    prevChar = cmd
            agent.features = (numNewChars, numNewChars)
        # For experiment endpointBC and others
        else:
            # agent.features = tuple(final_observation[:1])
            # if(lander_contacts_difference==-80):
            #     lander_contacts_difference=101
            # print('length of commandes is',len(agent.commands))
            original_string='.'.join(str(e) for e in agent.commands)
            # print('original length is ',len(original_string))
            compressed_string=zlib.compress(original_string.encode("utf-8"))
            compressed_length=len(compressed_string)
            # print('length of compressed_string is ',len(compressed_string))
            # print('compressed_string is ',compressed_string)

            agent.features=(lander_contacts_difference,lander_contacts_difference)

        agent.action_count = action_count


class Agent:

    def __init__(self, game, sequence_len):
        self.fitness = 0
        self.game = game
        self.sequence_len = sequence_len
        self.commands = [
            randint(0, game.num_actions-1) for _ in range(sequence_len)
        ]

    def mutate(self):
        child = Agent(self.game, self.sequence_len)
        i = randint(0, self.sequence_len-1)
        offset = randint(1, self.game.num_actions)
        child.commands[i] = \
            (child.commands[i] + offset) % self.game.num_actions
        return child


class LinearSizer:
    def __init__(self, start_size, end_size):
        self.min_size = start_size
        self.range = end_size-start_size

    def get_size(self, portion_done):
        size = int((portion_done+1e-9)*self.range) + self.min_size
        return min(size, self.min_size+self.range)


class ExponentialSizer:
    def __init__(self, start_size, end_size):
        self.min_size = start_size
        self.max_size = end_size

    def get_size(self, portion_done):
        cur_size = self.max_size
        while portion_done < 0.5 and cur_size > self.min_size:
            cur_size //= 2
            portion_done *= 2

        return cur_size


class EmptyBuffer:

    def is_overpopulated(self):
        return False

    def add_individual(self, to_add):
        pass

    def remove_individual(self):
        return None


class SlidingBuffer:

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer_queue = deque(maxlen=buffer_size+1)

    def is_overpopulated(self):
        return len(self.buffer_queue) > self.buffer_size

    def add_individual(self, to_add):
        self.buffer_queue.append(to_add)

    def remove_individual(self):
        return self.buffer_queue.popleft()


def runRS(run_id, game, sequence_len, num_individuals, checkpoint=None):
    best_fitness = -10 ** 18
    best_sequence = None
    whenfound = 0

    for agent_id in range(num_individuals):
        agent = Agent(game, sequence_len)
        game.run(agent)

        if agent.fitness > best_fitness:
            best_fitness = agent.fitness
            best_sequence = agent.commands
            whenfound = agent_id

            # Save agent
            if checkpoint and checkpoint.checkpoint_enabled:
                checkpoint.save(agent)

            game.run(agent, render=False)

        if agent_id % 100 == 0:
            print(agent_id, best_fitness)

    with open('{}results_{}.txt'.format(RESULTS_OUTPUT_DIR, run_id), 'a') as f:
        f.write(str(whenfound) + " " + str(best_fitness) + "\n")

    return best_fitness, best_sequence


def runES(run_id, game, sequence_len, is_plus=False,
          num_parents=None, population_size=None,
          num_generations=None, checkpoint=None):

    best_fitness = -10 ** 18
    best_sequence = None
    whenfound = 0

    population = [Agent(game, sequence_len) for _ in range(population_size)]
    for p in population:
        game.run(p)
        if p.fitness > best_fitness:
            best_fitness = p.fitness
            best_sequence = p.commands

            if checkpoint and checkpoint.checkpoint_enabled:
                checkpoint.save(p)

    print(best_fitness)

    for curGen in range(num_generations):
        population.sort(reverse=True, key=lambda p: p.fitness)
        parents = population[:num_parents]

        population = []
        for i in range(population_size):
            p = parents[randint(0, len(parents)-1)]
            child = p.mutate()
            game.run(child)

            if child.fitness > best_fitness:
                best_fitness = child.fitness
                best_sequence = child.commands
                whenfound = curGen*population_size + i
                game.run(child, render=False)

                if checkpoint and checkpoint.checkpoint_enabled:
                    checkpoint.save(child)

            population.append(child)

        print(curGen, parents[0].fitness, best_fitness)

        if is_plus:
            population += parents

    with open('{}results_{}.txt'.format(RESULTS_OUTPUT_DIR, run_id), 'a') as f:
        f.write(str(whenfound) + " " + str(best_fitness) + "\n")

    return best_fitness, best_sequence

# This is the feature map


class FixedFeatureMap:

    def __init__(self, num_to_evaluate, buffer_size, boundaries, sizer):

        # Clock for resizing the map.
        self.num_individuals_to_evaluate = num_to_evaluate
        self.num_individuals_added = 0

        # Feature to individual mapping.
        self.num_features = len(boundaries)
        self.boundaries = boundaries
        self.elite_map = {}
        self.elite_indices = []

        # A group is the number of cells along
        # each dimension in the feature space.
        self.group_sizer = sizer
        self.num_groups = 3

        if buffer_size == None:
            self.buffer = EmptyBuffer()
        else:
            self.buffer = SlidingBuffer(buffer_size)

    def get_feature_index(self, feature_id, feature):
        low_bound, high_bound = self.boundaries[feature_id]
        if feature <= low_bound:
            return 0
        if high_bound <= feature+1e-9:
            return self.num_groups-1

        gap = high_bound - low_bound
        pos = feature - low_bound
        index = int(self.num_groups * pos / gap)
        return index

    def get_index(self, agent):
        index = tuple(self.get_feature_index(i, v)
                      for i, v in enumerate(agent.features))
        return index

    def add_to_map(self, to_add):
        index = self.get_index(to_add)
        # NOTE: when replaced replaced_elite is True...
        replaced_elite = False
        if index not in self.elite_map:
            self.elite_indices.append(index)
            self.elite_map[index] = to_add
            replaced_elite = True
        elif self.elite_map[index].fitness < to_add.fitness:
            self.elite_map[index] = to_add
            replaced_elite = True
        # if replaced_elite == True:
        # save mutation
        return replaced_elite

    def remove_from_map(self, to_remove):
        index = self.get_index(to_remove)
        if index in self.elite_map and self.elite_map[index] == to_remove:
            del self.elite_map[index]
            self.elite_indices.remove(index)
            return True

        return False

    def remap(self, next_num_groups):
        print('remap', '{}x{}'.format(next_num_groups, next_num_groups))
        self.num_groups = next_num_groups

        all_elites = self.elite_map.values()
        self.elite_indices = []
        self.elite_map = {}
        for elite in all_elites:
            self.add_to_map(elite)

    # Possible places to add "checkpoint hook"
    def add(self, to_add):
        self.num_individuals_added += 1
        portion_done = \
            self.num_individuals_added / self.num_individuals_to_evaluate
        next_num_groups = self.group_sizer.get_size(portion_done)
        if next_num_groups != self.num_groups:
            self.remap(next_num_groups)

        replaced_elite = self.add_to_map(to_add)
        self.buffer.add_individual(to_add)
        if self.buffer.is_overpopulated():
            self.remove_from_map(self.buffer.remove_individual())

        return replaced_elite

    def get_random_elite(self):
        pos = randint(0, len(self.elite_indices)-1)
        index = self.elite_indices[pos]
        return self.elite_map[index]

# For testing to make sure that the map works
# if __name__ == '__main__':
#    linear_sizer = LinearSizer(2, 10)
#    linear_sizer = ExponentialSizer(2, 500)
#    feature_map = FixedFeatureMap(100, None, [(0, 10), (0, 10)], linear_sizer)
#    print(feature_map.num_individuals_to_evaluate)

    #linear_sizer = ExponentialSizer(2, 500)
    #feature_map = FixedFeatureMap(500, 10, [(0, 10), (0, 10)], linear_sizer)
    #game = GameEvaluator('LunarLander-v2')

    # for x in range(0, 100):
    #    agent = Agent(game, 200)
    #    agent.features = (x%10, (x+5)%10)
    #    agent.fitness = -x
        #print(x, feature_map.add(agent))
    #    feature_map.add(agent)


def runME(run_id, game, sequence_len,
          init_pop_size=-1, num_individuals=-1, sizer_type='Linear',
          sizer_range=(10, 10), buffer_size=None, checkpoint=None, mode=None):

    best_fitness = -10 ** 18
    best_sequence = None
    whenfound = 0
    global lander_steps_differences_list
    global current_run_id
    current_run_id=run_id
    sizer = None
    if sizer_type == 'Linear':
        sizer = LinearSizer(*sizer_range)
    elif sizer_type == 'Exponential':
        sizer = ExponentialSizer(*sizer_range)
    print('mode is',mode)
    # Experiment branches...
    if mode == ME_POLYHASH_BC:
        feature_ranges = [(0.0, sequence_len), (0.0, sequence_len)]
    # For experiment fitnessBC
    elif mode == ME_FITNESS_BC:
        feature_ranges = [(-300.0, 300.0), (-300.0, 300.0)]
    # For experiment entropyBC
    elif mode == ME_ENTROPY_BC:
        feature_ranges = [(0.0, sequence_len), (0.0, sequence_len)]
    # For experiment endpointBC and others
    else:
        # feature_ranges = [(-1.0, 1.0), (0.0, 1.0)]
        # feature_ranges = [(0.0, 101.0), (0.0, 101.0)]
        feature_ranges = [(0.0, sequence_len), (0.0, sequence_len)]



    # Yes, this array slice is invariant across all branches above.
    feature_ranges = feature_ranges[:2]

    print(feature_ranges)
    # 0. This is where the map is initialized
    if checkpoint and checkpoint.checkpoint_resume and checkpoint.checkpoint_data:
        print("Using preloaded checkpoint data...")
        feature_map = checkpoint.checkpoint_data
    else:
        feature_map = FixedFeatureMap(num_individuals, buffer_size,
                                      feature_ranges, sizer)

    session_checkpoint_time = int(time.time())
    num_checkpoints = 0
    # num_individuals=1

    for individuals_evaluated in range(num_individuals):
        cur_agent = None
        if individuals_evaluated < init_pop_size:
            cur_agent = Agent(game, sequence_len)
        else:
            cur_agent = feature_map.get_random_elite().mutate()

        game.run(cur_agent)
        # Keep track of changes here...
        did_add = feature_map.add(cur_agent)

        # On each add (i.e. data change) update the checkpoint file.
        if did_add and checkpoint and checkpoint.checkpoint_enabled:
            checkpoint.save(feature_map)

        if cur_agent.fitness > best_fitness:
            print('improved:', cur_agent.fitness, cur_agent.action_count)
            best_fitness = cur_agent.fitness
            best_sequence = cur_agent.commands
            # print(type(best_sequence))
            print('best sequence is ',best_sequence)

            whenfound = individuals_evaluated
            env=game.env
            # env.reset()
            # env.render()
            env.reset()
            game.run(cur_agent, render=True)

        if individuals_evaluated % 1000 == 0:
            #elites = [feature_map.elite_map[index] for index in feature_map.elite_map]
            #indicies = [index for index in feature_map.elite_map]
            #features = list(zip(*[a.features for a in elites]))
            # for f in features:
            #    print(sorted(f))
            # print(indicies)
            print('evaluated ',individuals_evaluated)
            print(individuals_evaluated, best_fitness,
                  len(feature_map.elite_indices))
    # Storing the bestsequence to simulate the lander moves later
    with open('best_fitness_{}.txt'.format(run_id), 'w') as filehandle:
        for listitem in best_sequence:
            filehandle.write('%s\n' % listitem)

    with open('{}results_{}.txt'.format(RESULTS_OUTPUT_DIR, run_id), 'a') as f:
        f.write(str(whenfound) + " " + str(best_fitness) + "\n")

    # Add one final checkpoint no matter what
    if checkpoint and checkpoint.checkpoint_enabled:
        checkpoint.save(feature_map)

    return best_fitness, best_sequence

def main(args=None):
    num_actions = args.num_actions if args.num_actions else 100
    num_parents = args.num_parents if args.num_parents else 10
    num_individuals = args.num_individuals if args.num_individuals else 100000
    search_type = args.search_type if args.search_type else 'ME'
    population_size = args.population_size if args.population_size else 100
    init_population_size = args.init_population_size if args.init_population_size else 1000
    num_generations = args.num_generations if args.num_generations else 1000
    checkpoint_dir = args.checkpoint_dir if args.checkpoint_dir else CHECKPOINTS_DIR
    checkpoint_enabled = args.checkpoint_enabled if args.checkpoint_enabled else CHECKPOINT_ENABLED
    checkpoint_prefix = args.checkpoint_prefix if args.checkpoint_prefix else CHECKPOINT_PREFIX
    checkpoint_resume = args.checkpoint_resume if args.checkpoint_resume else CHECKPOINT_RESUME
    checkpoint_frequency = args.checkpoint_frequency if args.checkpoint_frequency else 1000
    seed = args.seed if args.seed else DEFAULT_SEED
    sizer_range = tuple(args.sizer_range) if args.sizer_range else (200, 200)
    # print('sizer range is ',sizer_range)
    is_plus = args.is_plus # NOTE: this defaults to false
    mode = args.mode
    #game = GameEvaluator('Qbert-v0', seed=1009, num_rep=2)
    game = GameEvaluator('LunarLander-v2', seed=seed, num_rep=3, mode=mode)
    run_id = args.run_id if args.run_id else 'untitled_run'
    checkpoint_data = None

    checkpoint = None
    if checkpoint_enabled:
        checkpoint = Checkpoint(
            checkpoint_resume=checkpoint_resume,
            checkpoint_prefix=checkpoint_prefix,
            checkpoint_frequency=checkpoint_frequency,
            checkpoint_dir=checkpoint_dir,
            checkpoint_enabled=checkpoint_enabled,
            search_type=search_type
        )

        if checkpoint_resume:
            # Look for checkpoint matching prefix
            checkpoint.checkpoint_data = checkpoint.find_latest_checkpoint()

    if search_type == 'ES':
        runES(run_id, game,
              num_actions,
              is_plus=is_plus,
              num_parents=num_parents,
              population_size=population_size,
              num_generations=num_generations,
              checkpoint=checkpoint)
    elif search_type == 'RS':
        runRS(run_id, game, num_actions, num_individuals, checkpoint=checkpoint)
    elif search_type == 'ME':
        runME(run_id, game,
              num_actions,
              init_pop_size=init_population_size,
              num_individuals=num_individuals,
              sizer_type='Linear',
              sizer_range=sizer_range,
              buffer_size=None,
              checkpoint=checkpoint,
              mode=ME_ENDPOINT_BC
              )

    elif search_type == 'test':
        from gymjam.search import Agent
        cur_agent = Agent(game, num_actions)
        while True:
            game.run(cur_agent, render=False)

    game.env.close()

# Define args
parser = argparse.ArgumentParser(description='LunarLander runner')

# Supported args
parser.add_argument('--search-type', metavar='S', type=str,
                    choices=['ES', 'RS', 'ME'])
parser.add_argument('--is-plus', action='store_true', default=False)
parser.add_argument('--num-actions', metavar='A', type=int)
parser.add_argument('--num-parents', metavar='P', type=int)
parser.add_argument('--num-generations', metavar='G', type=int)
parser.add_argument('--num-individuals', metavar='I', type=int)
parser.add_argument('--population-size', metavar='P', type=int)
parser.add_argument('--init-population-size', metavar='IP', type=int)
parser.add_argument('--checkpoint-dir', metavar='C', type=str, default='')
parser.add_argument('--checkpoint-prefix', metavar='CP', type=str, default='')
parser.add_argument('--checkpoint-frequency', metavar='F', type=int, default=CHECKPOINT_FREQUENCY)
parser.add_argument('--checkpoint-enabled', default=CHECKPOINT_ENABLED, action='store_true')
parser.add_argument('--checkpoint-resume', default=CHECKPOINT_RESUME, action='store_true')
parser.add_argument('--run-id', default='', type=str)
parser.add_argument('--seed', metavar='S', type=int, default=DEFAULT_SEED)
parser.add_argument('--mode', metavar='M', type=str)
parser.add_argument('--sizer-range', metavar='SR', type=int, nargs=2)


if __name__ == '__main__':
    args = parser.parse_args()
    sys.exit(main(args))
