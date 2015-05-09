#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Martin Veselovsky'

import argparse
import logging
from kts import KTS

logging.basicConfig(level=logging.DEBUG)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('order', type=int)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    kts = KTS(args.order)
    # kts.create_blocks()
    # print(kts)
    kts.create_parallel()
    kts.print_classes()
    kts.test_classes()