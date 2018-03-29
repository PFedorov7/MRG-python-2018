# -*- encoding: utf-8 -*-
import collections
import math
import re
import os

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    f = open('log.log')
    total_dict = collections.defaultdict(int)
    time_dict = collections.defaultdict(int)
    stop = 0

    for line in f:

        if (stop):
            break
        if (start_at):
            if(line.find(start_at) != -1):
                start_at = 0
            else:
                continue
        if (stop_at and line.find(stop_at) == 1):
            stop = 1

        pattern = re.search(r':\/\/[^\s]*', line)
        if (pattern):

            pattern = pattern.group()
            filename, file_extension = os.path.splitext(pattern)

            if (ignore_www and re.search(r':\/\/www', pattern)):
                pattern = pattern.replace('www.', '')
            if(request_type and line.find(request_type) == -1):
                continue
            if (ignore_files and file_extension):
                continue
            if (ignore_urls and ignore(ignore_urls, line)):
                continue

            add(pattern, total_dict)
            sum(pattern, time_dict, line)

    if (slow_queries):
        return calc(time_dict, total_dict)
    else:
        return sorted(total_dict.values(), reverse = True)[:5:]

def ignore(ignore_urls, line):
    for url in ignore_urls:
        if (line.find(url) != -1):
            return 1
    return 0

def add(key, total_dict):
    total_dict[ key ] += 1

def sum(key, time_dict, line):
    time = re.search(r'\d+$',line)
    time_dict[ key ] += int(time.group())

def calc(time_dict, total_dict):
    return_list = []
    for key in sorted(time_dict.items(), key=lambda x: x[1])[-5::]:
        for key2 in total_dict:
            if (key[0] == key2):
                value = math.floor(key[1] / total_dict[key2])
                return_list.append(value)
    return sorted(return_list, reverse = True)