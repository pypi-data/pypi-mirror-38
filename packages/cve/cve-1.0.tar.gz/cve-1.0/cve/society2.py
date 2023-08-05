#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import random
import argparse
from io import StringIO
from functools import partial
import sys

core_value = (u'富强', u'民主', u'文明', u'和谐',
              u'自由', u'平等', u'公正', u'法治',
              u'爱国', u'敬业', u'诚信', u'友善')


is_py3 = sys.version_info[0] == 3


def str2hex(unicode_str):
    """
    转换字符串为16进制生成器
    :param unicode_str:
    :return:
    """
    for _ in unicode_str:
        for h in _.encode('utf-8').encode('hex'):
            yield h


def hex2twelve(hex_gen):
    """
    转换16进制为12进制
    其中，对于大于10的十六进制数字，
    采取随机两种方式：
    10 + hex_num - 10 表示，即 a -> 100, f -> 105
    11 + hex_num - 6 表示， 即 a -> 114, f -> 119
    :param hex_gen:
    :return: generator()
    """
    for h in hex_gen:
        h = int(h, 16)
        if h < 10:
            yield h
        elif random.randint(0, 1):
            yield 10
            yield h - 10
        else:
            yield 11
            yield h - 6


def twelve_2_core_value(twelve_iter):
    """
    根据12进制下标转换
    :param twelve_iter:
    :return:
    """
    for index in twelve_iter:
        yield core_value[index]


def core_value_2_twelve(core_value_str):
    """
    将社会主义核心价值观转换为12进制
    :param core_value_str:
    :return:
    """
    for word in iter(partial(StringIO(core_value_str).read, 2), ''):
        yield core_value.index(word)


def twelve2hex(twelve_iter):
    """
    将12进制转换为16进制
    :param twelve_iter:
    :return:
    """
    for twelve in twelve_iter:
        if twelve < 10:
            yield twelve
        elif twelve == 10:
            yield 10 + next(twelve_iter)
        else:
            yield 6 + next(twelve_iter)


def hex2bytes(hex_iter):
    """
    将十六进制转换为bytes对象
    :param hex_iter:
    :return:
    """
    for h in hex_iter:
        b = '{:x}{:x}'.format(h, next(hex_iter))
        yield b.decode('hex')


def core_value_encode(origin):
    """
    转换utf-8编码为社会主义核心价值观编码
    :param origin:
    :return:
    """
    hex_str = str2hex(origin)
    twelve = hex2twelve(hex_str)
    core_value_iter = twelve_2_core_value(twelve)
    return ''.join(core_value_iter)


def core_value_decode(origin):
    """
    将社会主义核心价值观编码转换为utf-8编码
    :param origin:
    :return:
    """
    twelve_iter = core_value_2_twelve(origin)
    hex_iter = twelve2hex(twelve_iter)
    bytes_iter = hex2bytes(hex_iter)
    return (b''.join(bytes_iter)).decode('utf-8')


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='encode / decode input')
    parse.add_argument('source', type=lambda s: unicode(s, 'utf-8'))
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
    if args.operation == u'encode':
        print(core_value_encode(args.source))
    else:
        print(core_value_decode(args.source))

