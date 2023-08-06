import numpy as np
import random
import warnings
from math import log, ceil
from queue import Queue
from .index_priority_queue import QNode, IndexPriorityQueue
from typing import Tuple, List


class FastPriorReplayBuffer:
    def __init__(self, buffer_size=8000, batch_size=32, alpha=0.33,
                 min_prior=0.1, max_prior=10, initial_b=0.4,
                 total_episode = 2000):
        self.buffer_size = buffer_size
        self.buff = SegmentTree(buffer_size, use_max_space=True)
        self.batch_size = batch_size
        self.alpha = alpha
        self.min_prior = min_prior
        self.max_prior = max_prior
        self.initial_b = initial_b
        self._b = initial_b
        self.b_increment_per_episode = (1 - initial_b) / total_episode

    def add(self, *args):
        self.buff.put_unknown_p(args)

    def increase_b(self):
        self._b += self.b_increment_per_episode

    def sample(self):
        """

        :param batch_size:
        :return: states, next_states, actions, rewards
        """
        chosen_slice, batch, prob = self.buff.sample_batch_with_slice(self.batch_size)
        return chosen_slice, [np.array(x) for x in zip(*batch)]

    def sample_with_weights(self):
        """

        :param batch_size:
        :return: states, next_states, actions, rewards
        """
        chosen_slice, batch, prob = self.buff.sample_batch_with_slice(self.batch_size)
        n = len(self.buff)
        return chosen_slice, [np.array(x) for x in zip(*batch)], np.power(prob*n, -self._b)

    def set_prior(self, p_slice, priors):
        for index, p in zip(p_slice, priors):
            p = min(max(self.min_prior, p), self.max_prior)
            p = p ** self.alpha
            self.buff.set_p(index, p)

    def update_per_episode(self):
        self.increase_b()

    def __len__(self):
        return len(self.buff)


class Node:
    def __init__(self, data, p):
        if p < 0:
            raise ValueError('p cannot be assign to negative value')
        self.dat = data
        self.p = p

    def __lt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.p < other
        return self.p < other.p

    def __gt__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.p > other
        return self.p > other.p

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.p == other.p

    def __ne__(self, other):
        if not isinstance(other, Node):
            return False
        return not self == other

    def __repr__(self):
        return f'Node({self.dat}, {self.p})'

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.p + other
        return self.p + other.p

    def __radd__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.p + other
        return self.p + other.p

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.p / other
        return self.p / other.p

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.p - other
        return self.p - other.p

    def __rsub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return other - self.p
        return other.p - self.p


class SegmentTree:
    def __init__(self, max_len, use_max_space=False):
        self.low, self.high = 0, -1
        self.size = pow(2, int(ceil(log(max_len, 2))))
        if not use_max_space:
            self.max_len = max_len
        else:
            self.max_len = self.size
        self.sum = [0] * (2 * self.size - 1)
        self.queue = IndexPriorityQueue()
        self.unknown_buff = Queue()

    def build(self, arr):
        self.high = len(arr)
        for a in arr:
            self.put(a)

    def put(self, node, priority=None):
        if not isinstance(node, Node):
            if priority is None:
                raise ValueError('Please provide the p value')
            node = Node(node, priority)

        if self.high + 1 < self.max_len:
            self.high += 1
            idx = self.high
        else:
            q_node = self.queue.get_nowait()
            old_node, idx = q_node.dat, q_node.index
            if old_node > node:
                warnings.warn('Did not push the node because the node.p is smaller than the min p')
                self.queue.put(QNode(old_node, idx))
                return idx
        self.queue.put(QNode(node, idx))
        self.set(idx, node)
        return idx

    def put_unknown_p(self, data):
        """
        There are times when we do not know the priority,
        and we need to put them in the next batch.

        :param data:
        :return:
        """
        node = Node(data, 1)
        idx = None
        v = 10
        while idx is None:
            idx = self.put(node, v)
            v += 1
        self.unknown_buff.put((idx, node))

    def set_p(self, idx, p):
        self.queue.set_p(idx, p)
        self._set_p(idx, p)

    def _set_p(self, idx, p):
        pos = idx + self.size - 1
        self.sum[pos].p = p
        while True:
            pos = (pos - 1) // 2
            self.sum[pos] = self.sum[2 * pos + 1] + self.sum[2 * pos + 2]
            if pos == 0:
                break

    def set(self, idx, val):
        self.queue.set(idx, val)
        self._set(idx, val)

    def _set(self, idx, val):
        pos = idx + self.size - 1
        self.sum[pos] = val
        while True:
            pos = (pos - 1) // 2
            self.sum[pos] = self.sum[2 * pos + 1] + self.sum[2 * pos + 2]
            if pos == 0:
                break

    def _m_query(self, q_low, q_high):
        """
        This is for test only
        :param q_low:
        :param q_high:
        :return:
        """
        the_sum = self._query(q_low, q_high, 0, self.size - 1, 0)
        if isinstance(the_sum, Node):
            return the_sum.p
        return the_sum

    def _query(self, q_low, q_high, low, high, pos):
        if q_low <= low and q_high >= high:
            return self.sum[pos]
        if q_low > high or q_high < low:
            return 0
        mid = (low + high) // 2

        return self._query(q_low, q_high, low, mid, 2 * pos + 1) \
               + self._query(q_low, q_high, mid + 1, high, 2 * pos + 2)

    def get_prob(self, idx):
        return self.sum[idx + self.size - 1].p / self.sum[0]

    def sample_batch(self, batch_size) -> List:
        return [self.sample()[1].dat for _ in range(batch_size)]

    def sample_batch_with_slice(self, batch_size) -> Tuple[List, List, List]:
        slices = []
        data = []
        probs = []
        while not self.unknown_buff.empty():
            idx, node = self.unknown_buff.get_nowait()
            slices.append(idx)
            data.append(node.dat)
            probs.append(self.get_prob(idx))
            batch_size -= 1
            if batch_size == 0:
                break

        # Add lowest score data to the training batch
        # so as to update the corresponding loss (priority)
        if self.high + 1 >= self.max_len:
            q_node = self.queue.top()
            idx, node = q_node.index, q_node.dat
            probs.append(self.get_prob(idx))
            data.append(node.dat)
            slices.append(idx)
            batch_size -= 1

        for i in range(batch_size):
            idx, node = self.sample()
            probs.append(self.get_prob(idx))
            slices.append(idx)
            data.append(node.dat)

        probs = np.array(probs)
        return slices, data, probs

    def sample_node_batch(self, batch_size) -> List[Node]:
        return [self.sample()[1] for _ in range(batch_size)]

    def sample(self) -> Tuple[int, Node]:
        random_v = random.random() * self.sum[0]
        pos, node = self._find_leaf(random_v)
        return pos, node

    def _find_leaf(self, v):
        pos = 0
        left_pos = pos * 2 + 1
        right_pos = left_pos + 1
        while right_pos < 2*self.size - 1:
            if v > self.sum[left_pos]:
                v -= self.sum[left_pos]
                pos = right_pos
            else:
                pos = left_pos
            left_pos = pos * 2 + 1
            right_pos = left_pos + 1
        return pos - self.size + 1, self.sum[pos]

    def __len__(self):
        return self.high + 1

    def top(self):
        node = self.queue.top()
        return node.dat
