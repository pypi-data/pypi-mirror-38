import re

def parse(dsn):
    pattern = re.compile(r'^([\w\+]+)://([\w]+):([\S]+)@([\S]+)/([\w]+)')
    m = pattern.search(dsn)
    return m.group

