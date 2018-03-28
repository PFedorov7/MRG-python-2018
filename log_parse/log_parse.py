# -*- encoding: utf-8 -*-
import re
import collections

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
    for line in f:
        pattern = re.search(r':\/\/[^\s]*', line)
        if(pattern):
            key = pattern.group()
            total_dict[ key ] += 1
    return sorted(total_dict.values(), reverse = True)[:5:]
