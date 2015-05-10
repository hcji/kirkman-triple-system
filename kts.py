#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Martin Veselovsky'

import logging

logger = logging.getLogger(__name__)


class KTS():
    def __init__(self, order):
        if order % 6 != 3:
            raise ValueError('Order number %s does not satisfy necessary '
                             'condition "order `mod` 6 = 3"'.format(order))

        # Construction 1.1 [45, Theorem 6]
        self.q = int(order / 2)
        if order % 2 == 1 and self.isprime(self.q):
            self.create_blocks = self.create_blocks_1
            self.create_parallel = self.create_parallel_1

        # Construction 1.2 [45, Theorem 5]
        else:
            self.q = int(order / 3)
            if order % 3 == 0 and self.isprime(self.q):
                self.create_blocks = self.create_blocks_2
                self.create_parallel = self.create_parallel_2
            else:
                raise ValueError('Not possible')

        self.order = order
        self.t = int((self.q - 1) / 6)

        self.points = range(1, order + 1)
        self.blocks = {}
        self.classes = {}

    def create_parallel_1(self):
        """
        Construction 1.1
        Obtain parallel classes by developing through Galois Field (self.q)
        """
        for i in range(self.q):
            self.create_blocks(number=i)
            self.classes[i] = self.blocks

    def create_blocks_1(self, alpha=3, number=0):
        """
        Construction 1.1
        Obtain blocks that create one parallel class.
        :param alpha: primitive element in Galois Field (self.q)
        :param number: iteration (offset) number according to Galois Field
        """
        m = 0

        right = self.add_mod(self.pow_mod(alpha, self.t), 1)
        while m < 10:
            alpha_m = self.pow_mod(alpha, m)
            left = self.add_mod(alpha_m, alpha_m)

            print('right: %s, left: %s, m: %s' % (right, left, m))

            if left == right:
                break
            m += 1
        print('alpha = %s, m = %s' % (alpha, m))

        get = lambda index: self.points[index]
        get1 = lambda index: get(self.add_mod(index, number))
        get2 = lambda index: get(self.add_mod(index, number) + self.q)

        # references A^0
        self.blocks = {'a_': (self.points[number],
                              self.points[number + self.q],
                              self.points[-1])}

        # references A_i, B_i
        for i in range(0, self.t):
            self.blocks['a' + str(i)] = \
                (get2(self.pow_mod(alpha, i + m + self.t)),
                 get2(self.pow_mod(alpha, i + m + 3 * self.t)),
                 get2(self.pow_mod(alpha, i + m + 5 * self.t)))

            self.blocks['b' + str(i)] = \
                (get1(self.pow_mod(alpha, i)),
                 get1(self.pow_mod(alpha, i + self.t)),
                 get2(self.pow_mod(alpha, i + m)))

        # references B_i
        for i in range(2 * self.t, 3 * self.t):
            self.blocks['b' + str(i)] = \
                (get1(self.pow_mod(alpha, i)),
                 get1(self.pow_mod(alpha, i + self.t)),
                 get2(self.pow_mod(alpha, i + m)))

        # references B_i
        for i in range(4 * self.t, 5 * self.t):
            self.blocks['b' + str(i)] = \
                (get1(self.pow_mod(alpha, i)),
                 get1(self.pow_mod(alpha, i + self.t)),
                 get2(self.pow_mod(alpha, i + m)))

    def create_parallel_2(self):
        """
        Construction 1.2
        Obtain parallel classes by developing through Galois Field (self.q).
        Another parallel classes are made from 'a_i' blocks. These are referenced as remainder
        triples which means, that these triples are arranged by 'block_key' with values
        constructed as (origin class_name, triple).
        """

        # first obtain all parallel classes developing through Galois Field
        # but set of parallel classes are super set of real parallel classes at the moment
        self.create_parallel_1()

        real_classes = {}           # i.e.   0  { 'a_': (1, 8, 15) ,  'b0,1': (2, 3, 5), ... }
        remainder_triples = {}      # i.e.   a2 {    0: (3, 12, 16),       1: (4, 13, 17), ... }

        # split super set to get real parallel classes and remainder triples
        for class_key, class_blocks in self.classes.items():
            real_classes[class_key] = {}

            for block_key, block_triple in class_blocks.items():
                i = block_key[1]

                # 'a_i' blocks logic
                if block_key[0] == 'a':
                    if i == '_' \
                            or self.t <= int(i) <= 2 * self.t - 1 \
                            or 3 * self.t <= int(i) <= 4 * self.t - 1 \
                            or 5 * self.t <= int(i) <= 6 * self.t - 1:
                        real_classes[class_key][block_key] = block_triple
                    else:
                        # swap block_key/class_key
                        remainder_triples.setdefault(block_key, {})[class_key] = block_triple

                # 'b_i' blocks logic
                elif block_key[0] == 'b':
                    if 0 <= int(i) <= self.t - 1:
                        real_classes[class_key][block_key] = block_triple
                    else:
                        # remainder_triples[class_key][block_key] = block_triple
                        remainder_triples.setdefault(block_key, {})[class_key] = block_triple

        for k, v in real_classes.items():
            print(k, v)

        for k, v in remainder_triples.items():
            print(k, v)

        # another = {}
        # for class_key, class_blocks in remainder_triples.items():
        #     for block_key, block_triple in class_blocks.items():
        #         another.setdefault(block_key, []).append(block_triple)
        #
        # for k, v in another.items():
        #     print(k, v)
        #
        # self.classes = {}
        # for class_key, class_blocks in real_classes.items():
        #     for block_triple in class_blocks.values():
        #         self.classes.setdefault(class_key, []).append(block_triple)
        # for class_key, class_blocks in another.items():
        #     for block_triple in class_blocks:
        #         self.classes.setdefault(class_key, []).append(block_triple)

        self.classes = {}
        for class_key, class_blocks in real_classes.items():
            for block_triple in class_blocks.values():
                self.classes.setdefault(class_key, []).append(block_triple)
        for class_key, class_blocks in remainder_triples.items():
            for block_triple in class_blocks.values():
                self.classes.setdefault(class_key, []).append(block_triple)

        self.print_classes()
        print()

    def am(self, number, addition):
        result = number + addition
        if number < self.q:
            if result > self.q:
                return result - self.q
            else:
                return result
        elif self.q <= number < self.q * 2:
            if result > self.q * 2:
                return result - self.q
            else:
                return result
        elif number >= self.q * 2:
            if result > self.q * 3:
                return result - self.q
            else:
                return result

    def create_blocks_2(self, alpha=3, number=0):
        """
        Construction 1.2
        Obtain blocks that create super set of one parallel class.
        :param alpha: primitive element in Galois Field (self.q)
        :param number: iteration (offset) number according to Galois Field
        """

        groups = {
            1: self.points[:self.q],
            2: self.points[self.q:self.q * 2],
            3: self.points[self.q * 2:]
        }

        get = lambda index, group: groups[group][self.add_mod(index, number)]

        # references A^0
        self.blocks = {'a_': (groups[1][number], groups[2][number], groups[3][number])}

        # references B_i,j
        for i in range(0, self.t):
            for j in (1, 2, 3):
                self.blocks['b' + str(i) + ',' + str(j)] = \
                    (get(self.pow_mod(alpha, i), j),
                     get(self.pow_mod(alpha, i + 2 * self.t), j),
                     get(self.pow_mod(alpha, i + 4 * self.t), j))

        # references A_i
        for i in range(0, 6 * self.t):
            self.blocks['a' + str(i)] = \
                (get(self.pow_mod(alpha, i), 1),
                 get(self.pow_mod(alpha, i + 2 * self.t), 2),
                 get(self.pow_mod(alpha, i + 4 * self.t), 3))

            # parallel = {}
            # for k, v in self.blocks.items():
            # if k[0] == 'a':
            #         if k[1] == '_':
            #             parallel[k] = v
            #         else:
            #             i = int(k[1])
            #             if self.t <= i <= 2 * self.t - 1 \
            #                     or 3 * self.t <= i <= 4 * self.t - 1 \
            #                     or 5 * self.t <= i <= 6 * self.t - 1:
            #                 parallel[k] = v
            #     elif k[0] == 'b':
            #         i = int(k[1])
            #         if 0 <= i <= self.t - 1:
            #             parallel[k] = v
            # self.blocks = parallel

    def pow_mod(self, number, power):
        return (number ** power) % self.q

    def add_mod(self, number, addition):
        result = number + addition
        return result if result < self.q else result % self.q

    def __str__(self):
        s = 'Points: %s \n' % str([p for p in self.points])
        s += 'Prime power q: %s \n' % self.q
        s += 'Blocks: \n'
        for k, v in self.blocks.items():
            s += k + ': ' + str(v) + '\n'
        return s

    def print_classes(self):
        for k, v in self.classes.items():
            print(k, v)

    def test_classes(self):
        triples = set()
        for c in self.classes.values():
            row = set()
            for b in c:     # ????? .values()
                triples.add(b)
                [row.add(x) for x in b]

            assert len(row) == self.order
        assert len(triples) == len(self.classes) * len(self.classes[0])

    # method taken from
    # https://www.daniweb.com/software-development/python/
    # code/216880/check-if-a-number-is-a-prime-number-python
    @staticmethod
    def isprime(n):
        """check if integer n is a prime"""
        # make sure n is a positive integer
        n = abs(int(n))
        # 0 and 1 are not primes
        if n < 2:
            return False
        # 2 is the only even prime number
        if n == 2:
            return True
        # all other even numbers are not primes
        if not n & 1:
            return False
        # range starts with 3 and only needs to go up the squareroot of n
        # for all odd numbers
        for x in range(3, int(n ** 0.5) + 1, 2):
            if n % x == 0:
                return False
        return True