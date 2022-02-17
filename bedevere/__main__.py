import json
import os
import re

TITLE_RE = re.compile(r'\s*\[(?P<branch>\d+\.\d+)\].+\((?:GH-|#)(?P<pr>\d+)\)')

def normalize_title(title, body):
    """Normalize the title if it spills over into the PR's body."""
    if not (title.endswith("…") and body.startswith("…")):
        return title
    else:
        # Being paranoid in case \r\n is used.
        return title[:-1] + body[1:].partition("\r\n")[0]

def manage_labels(event, gh, *args, **kwargs):
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)
        if event["action"] == "edited" and "title" not in event["changes"]:
            return
        pull_request = event["pull_request"]
        title = normalize_title(pull_request['title'],
                                 pull_request['body'])
        title_match = TITLE_RE.match(title)
        if title_match is None:
            return
        branch = title_match.group('branch')
        original_pr_number = title_match.group('pr')

        print(pull_request)
        print(title_match)
        print(branch)
        print(original_pr_number)

manage_labels(None, None)