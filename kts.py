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

        logger.debug('KTS of order %s', order)

        self.order = order
        self.q = int(order / 2)
        self.t = int((self.q - 1) / 6)

        self.points = range(1, order + 1)
        self.blocks = {}
        self.classes = {}

    def create_parallel(self):

        for i in range(self.q):
            self.create_blocks(number=i)
            self.classes[i] = self.blocks

    def create_blocks(self, alpha=3, number=0):

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
            for b in c.values():
                triples.add(b)
                [row.add(x) for x in b]

            assert len(row) == self.order
        assert len(triples) == len(self.classes) * len(self.blocks)
