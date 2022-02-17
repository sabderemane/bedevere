import json
import os
import re

TITLE_RE = re.compile(r'\s*\[(?P<branch>\d+\.\d+)\].+\((?:GH-|#)(?P<pr>\d+)\)')

def manage_labels(event, gh, *args, **kwargs):
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)
        print(event)
        return True

manage_labels(None, None)