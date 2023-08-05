""" Simple util package"""
import re
import json

def load_dirty_json(dirty_json):
    """Takes JSON returned from ADT and makes it valid python JSON"""
    regex_replace = [(r"(\\)", r'\\\\'), (r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for req, sub in regex_replace:
        dirty_json = re.sub(req, sub, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json
