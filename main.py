#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

from kts import KTS


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('order', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    kts = KTS(args.order)
    kts.solve()
    kts.test_classes()
    kts.print_solution(print_heading=True)
