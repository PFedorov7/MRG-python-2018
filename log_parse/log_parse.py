# -*- encoding: utf-8 -*-
from datetime import datetime
from math import floor
from time import strptime
import collections
import re
import os


def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at= None,
    stop_at = None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):

    f = open('log.log')
    total_dict = collections.defaultdict(int)
    time_dict = collections.defaultdict(int)

    for line in f:
        if(start_at or stop_at):
            period = re.search(r'\d+\/\w+\/\d+\s[\d+:]+', line)
            if(period):

                dt = datetime.strptime(period.group(), "%d/%b/%Y %H:%M:%S")
                if (stop_at and dt > stop_at):
                    break
                if (start_at and dt < start_at):
                    continue 
                if (start_at and dt >= start_at):
                    start_at = 0
            else:
                continue
        pattern = re.search(r':\/\/[^\s]*', line)

        if (pattern):
            pattern = pattern.group()[3:]
            filename, file_extension = os.path.splitext(pattern)
            if (ignore_www and re.search(r'^www.', pattern)):
                pattern = pattern[4:]
            if(request_type and line.find("\"" + request_type + ' ') == -1):
                continue
            if (ignore_files and file_extension):
                continue
            if (ignore_urls and ignore(ignore_urls, pattern)):
                continue

            total_dict[ pattern ] += 1
            time = re.search(r'\d+$',line)
            if(time):
                time_dict[ pattern ] += int(time.group())  

    if (slow_queries):
        return calc(time_dict, total_dict)
    else:
        return sorted(total_dict.values(), reverse = True)[:5]

def ignore(ignore_urls, pattern):
    for url in ignore_urls:
        if (re.match('^http[s]?', url)):
            url = re.search(r':\/\/[^\s]*', url)
            url = url.group()[3:]
            if(url == pattern):
                return 1
    return 0

def calc(time_dict, total_dict):
    return_list = []
    for key in sorted(time_dict.items(), key=lambda x: x[1]):
        for key2 in total_dict:
            if (key[0] == key2):
                value = floor(key[1] / total_dict[key2])
                return_list.append(value)
    return sorted(return_list, reverse = True)[:5]



