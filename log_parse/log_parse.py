# -*- encoding: utf-8 -*-
import re
import collections
import math

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
    slow_dict = collections.defaultdict(int)
    count = 0
    counter = 0

    for line in f:

        if (counter == 2):
            break

        if(start_at and counter == 0):
            if(line.find(start_at) != -1):
                counter = 1
            else:
                continue

        if(stop_at):
            if(line.find(stop_at) == 1):
                counter = 2

        pattern = re.search(r':\/\/[^\s]*', line)
        if (pattern):

            pattern = pattern.group()

            if(ignore_www and re.search(r':\/\/www', pattern)):
                pattern = pattern.replace('www.', '')
            if(request_type):
                if (line.find(request_type) == -1):
                    continue
            if (ignore_files and re.search(r'\.[\w\d]+$', pattern)):
                continue
            if (ignore_urls):
                for url in ignore_urls:
                    if (line.find(url) != -1):
                        count = 1
                        break
            if (count == 1):
                count = 0
                continue

            add(pattern, total_dict)
            sum(pattern, slow_dict, line)


    if (slow_queries):
        return calc(slow_dict, total_dict)
    else:
        return sorted(total_dict.values(), reverse = True)[:5:]


def add(key, total_dict):
    total_dict[ key ] += 1

def sum(key, slow_dict, line):
    time = re.search(r'\d+$',line)
    slow_dict[ key ] += int(time.group())

def calc(slow_dict, total_dict):
    return_list = []
    for key in sorted(slow_dict.items(), key=lambda x: x[1])[-5::]:
        for key2 in total_dict:
            if (key[0] == key2):
                value = math.floor(key[1] / total_dict[key2])
                return_list.append(value)
    return sorted(return_list, reverse = True)