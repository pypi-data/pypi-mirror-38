#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import argparse
from cve import core_value_decode, core_value_encode


def main():
    parse = argparse.ArgumentParser(description='encode / decode input')
    parse.add_argument('source', type=str if sys.version_info[0] == 3 else lambda s: unicode(s, 'utf-8'))
    group = parse.add_mutually_exclusive_group()
    group.add_argument('--decode', '-d',
                       action='store_const',
                       dest='operation',
                       const='decode',
                       help='decode the core socialist values encoding to utf-8')
    group.add_argument('--encode', '-e',
                       action='store_const',
                       dest='operation',
                       const='encode',
                       help='encode the utf-8 to core socialist values encoding')
    parse.set_defaults(operation='encode')

    if not sys.stdin.isatty():
        sys.argv.append(sys.stdin.read()[:-1])

    args = parse.parse_args()
    if args.operation == 'encode':
        output = core_value_encode(args.source)
    else:
        output = core_value_decode(args.source)

    if sys.version_info[0] == 2:
        output = output.encode('utf-8')

    print(output)


if __name__ == '__main__':
    main()

