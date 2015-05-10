#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Bc. Martin Veselovsky
# Email:  xvesel60@stud.fit.vutbr.cz

from numbthy import is_prime, is_primitive_root, power_mod, factor


class KTS():
    """
    Kirkman Triple System (KTS)

    Implementation based on publication:

        Stinson, D.: A survey of Kirkman triple systems and related designs.
        Discrete Mathematics, Volume 92, Issues 1–3, 17 November 1991, Pages 371–393,
        ISSN 0012-365X, doi:http://dx.doi.org/10.1016/0012-365X(91)90294-C.
        URL http://www.sciencedirect.com/science/article/pii/0012365X9190294C
    """

    def __init__(self, order):
        """
        Initialize with proper construction method.
        Raise ValueError if KTS order number does not satisfy necessary condition
        for creation of Kirkman Triple System.
        :param order: order of KTS, e.g. number of participants
        """
        if order % 6 != 3:
            raise ValueError('Order number %s does not satisfy necessary '
                             'condition "order `mod` 6 = 3"'.format(order))

        # Construction 1.1 [45, Theorem 6]
        self.q = int(order / 2)
        if order % 2 == 1 and self.is_prime_power(self.q) and self.q % 6 == 1:
            self.method_name = 'Construction 1.1'
            self.create_blocks = self.create_blocks_1
            self.create_parallel = self.create_parallel_1

        # Construction 1.2 [45, Theorem 5]
        else:
            self.q = int(order / 3)
            if order % 3 == 0 and self.is_prime_power(self.q) and self.q % 6 == 1:
                self.method_name = 'Construction 1.2'
                self.create_blocks = self.create_blocks_2
                self.create_parallel = self.create_parallel_2
            else:
                raise ValueError('Not possible')

        self.order = order
        self.t = int((self.q - 1) / 6)

        self.points = range(1, order + 1)
        self.blocks = {}
        self.classes = {}
        self.solution = {}

    @staticmethod
    def is_prime_power(n):
        if is_prime(n):
            return True
        if len(factor(n)) == 1:
            return True
        return False

    def solve(self):
        """
        Solve problem by construction 1.1 or 1.2 depending on KTS order.
        :return: dictionary of days containing array of triples for each day
        """
        self.create_parallel()
        day = 0
        for class_blocks in self.classes.values():
            day += 1
            for block_triple in class_blocks.values():
                self.solution.setdefault(day, []).append(block_triple)
        return self.solution

    def create_parallel_1(self):
        """
        Construction 1.1
        Obtain parallel classes by developing through Galois Field (self.q)
        """
        for i in range(self.q):
            self.create_blocks(i)
            self.classes[i] = self.blocks

    def create_blocks_1(self, number=0):
        """
        Construction 1.1
        Obtain blocks that create one parallel class.
        :param number: iteration (offset) number according to Galois Field
        """

        # first obtain alpha (primitive element in Galois Field) and m (by specified equation)
        alpha, m = 0, 0
        for a in range(self.q):
            if is_primitive_root(a, self.q):
                for _m in range(self.q):
                    # let me satisfy the equation --> 2 * alpha^m = alpha^t + 1
                    right = self.add_mod(power_mod(a, self.t, self.q), 1)
                    _a = power_mod(a, _m, self.q)
                    left = self.add_mod(_a, _a)
                    if left == right:
                        alpha, m = a, _m
                        break

        # split points to groups
        groups = {
            1: self.points[:self.q],
            2: self.points[self.q:],
        }

        get = lambda index, group: groups[group][self.add_mod(index, number)]

        # references A^0
        self.blocks = {'a_': (groups[1][number],
                              groups[2][number],
                              groups[2][-1])}

        # references A_i, B_i
        for i in range(0, self.t):
            self.blocks['a' + str(i)] = \
                (get(power_mod(alpha, i + m + self.t, self.q), 2),
                 get(power_mod(alpha, i + m + 3 * self.t, self.q), 2),
                 get(power_mod(alpha, i + m + 5 * self.t, self.q), 2))

            self.blocks['b' + str(i)] = \
                (get(power_mod(alpha, i, self.q), 1),
                 get(power_mod(alpha, i + self.t, self.q), 1),
                 get(power_mod(alpha, i + m, self.q), 2))

        # references B_i
        for i in range(2 * self.t, 3 * self.t):
            self.blocks['b' + str(i)] = \
                (get(power_mod(alpha, i, self.q), 1),
                 get(power_mod(alpha, i + self.t, self.q), 1),
                 get(power_mod(alpha, i + m, self.q), 2))

        # references B_i
        for i in range(4 * self.t, 5 * self.t):
            self.blocks['b' + str(i)] = \
                (get(power_mod(alpha, i, self.q), 1),
                 get(power_mod(alpha, i + self.t, self.q), 1),
                 get(power_mod(alpha, i + m, self.q), 2))

    def create_parallel_2(self):
        """
        Construction 1.2
        Obtain parallel classes by developing through Galois Field (self.q).
        Other parallel classes are made from 'a_i' blocks. These are referenced as remainder
        triples which means, that these triples are arranged by 'block_key' with values
        constructed as (origin class name, triple).
        """

        # first obtain all parallel classes developing through Galois Field
        # but set of parallel classes are super set of real parallel classes at the moment
        self.create_parallel_1()

        real_classes = {}       # i.e.   0  { 'a_': (1, 8, 15) ,  'b0,1': (2, 3, 5), ... }
        remainder_triples = {}  # i.e.   a2 {    0: (3, 12, 16),       1: (4, 13, 17), ... }

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
                        remainder_triples.setdefault(block_key, {})[class_key] = block_triple

                # 'b_i' blocks logic
                elif block_key[0] == 'b':
                    if 0 <= int(i) <= self.t - 1:
                        real_classes[class_key][block_key] = block_triple
                    else:
                        remainder_triples.setdefault(block_key, {})[class_key] = block_triple

        self.classes = {}
        self.classes.update(real_classes)
        self.classes.update(remainder_triples)

    def create_blocks_2(self, number=0):
        """
        Construction 1.2
        Obtain blocks that create super set of one parallel class.
        :param number: iteration (offset) number according to Galois Field
        """

        # first obtain alpha (primitive element in Galois Field)
        alpha = 0
        for a in range(self.q):
            if is_primitive_root(a, self.q):
                alpha = a
                break

        # split points to groups
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
                    (get(power_mod(alpha, i, self.q), j),
                     get(power_mod(alpha, i + 2 * self.t, self.q), j),
                     get(power_mod(alpha, i + 4 * self.t, self.q), j))

        # references A_i
        for i in range(0, 6 * self.t):
            self.blocks['a' + str(i)] = \
                (get(power_mod(alpha, i, self.q), 1),
                 get(power_mod(alpha, i + 2 * self.t, self.q), 2),
                 get(power_mod(alpha, i + 4 * self.t, self.q), 3))

    def test_classes(self):
        """
        Test all parallel classes blocks for uniqueness and completeness within the class.
        """
        triples = set()
        for c in self.classes.values():
            row = set()
            for b in c.values():
                triples.add(b)
                [row.add(x) for x in b]

            assert len(row) == self.order, \
                'There are missing %s / %s values in class' % (len(row), self.order)
        assert len(triples) == len(self.classes) * len(self.classes[0]), \
            'There are some triples more times than one'

    def add_mod(self, number, addition):
        result = number + addition
        return result if result < self.q else result % self.q

    def print_classes(self):
        for k, v in self.classes.items():
            print(k, v)

    def print_solution(self):
        for day, blocks in self.solution.items():
            print('Day %2s: ' % day, end='')
            for block_triple in blocks:
                print(str(block_triple).ljust(12), end='  ')
            print()

    def __str__(self):
        s = 'Kirkman triple system (KTS)\n' \
            '  Order: %s \n' \
            '  Points %s \n' \
            '  Prime power: %s \n' \
            '  Method used: %s \n' \
            '  Solution: %s days' % \
            (self.order, self.points, self.q, self.method_name, len(self.solution))
        return s