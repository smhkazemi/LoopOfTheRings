import collections
import random
import time
from bisect import bisect_left


class Task:
    def __init__(self, type, max_execution_time, basic_reward):
        self.type = type
        self.max_execution_time = max_execution_time
        self.basic_reward = basic_reward

    def clac_reward(self, actual_run_time):
        if actual_run_time >= self.max_execution_time:
            return actual_run_time / 4.
        return self.basic_reward + (
                    self.basic_reward * (self.max_execution_time - actual_run_time) / self.max_execution_time)


class SWSE:  # Simulated Workstation Environment
    servers = collections.OrderedDict()  # id to server
    distances = collections.OrderedDict()  # id to position
    position_threshold = 16
    ru = 0.2
    reputation_weight_w1 = 0.6
    latency_weight_w2 = 0.4


def get_random_id():
    random.seed(int(round(time.time() * 1000)))
    num = int(random.random() * 1000000000)
    while num in SWSE.servers.keys():
        num = int(random.random() * 1000000000)
    return num


class PoERDataStructure:
    def __init__(self, leader):
        self.blockID = get_random_id()
        self.credit = 0
        self.currentViewNum = 0
        self.currentSequenceNum = 0
        self.leaderID = leader.id
        self.sequenceNumOfBlock = 0
        self.numPreVotes = 0
        self.numReady = 0
        self.numOfView = 0


def binary_search(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] >= x:
        return i
    else:
        return -1


class EdgeServer:
    def __init__(self, position):
        self.reputation_parameter = 0
        self.min_reputation = 0
        self.max_reputation = 0
        self.position = position
        self.id = get_random_id()

    def update_reputation_parameter(self, extra_reward):
        self.reputation_parameter = (SWSE.ru * extra_reward) + (self.reputation_parameter * (1 - SWSE.ru))
        if self.min_reputation > self.reputation_parameter:
            self.min_reputation = self.reputation_parameter
        if self.max_reputation < self.reputation_parameter:
            self.max_reputation = self.reputation_parameter

    def calc_score(self, position):
        latency_diff = abs(self.position - position)
        return \
            (SWSE.reputation_weight_w1 * (self.reputation_parameter - self.min_reputation)
             / (self.max_reputation - self.min_reputation)) + (
                        SWSE.latency_weight_w2 * latency_diff / max(position, self.position))

    def publish_a_task(self, task):
        servers = list(SWSE.servers.values())
