"""Automatically close PR that tries to merge maintenance branch into main."""
import asyncio
import json
import os
import re
import traceback

import aiohttp
from gidgethub.aiohttp import GitHubAPI


PYTHON_MAINT_BRANCH_RE = re.compile(r'^\w+:\d+\.\d+$')

INVALID_PR_COMMENT = """\
PRs attempting to merge a maintenance branch into the \
main branch are deemed to be spam and automatically closed. \
If you were attempting to report a bug, please go to bugs.python.org; \
see devguide.python.org for further instruction as needed."""


async def close_invalid_pr(gh, *args, **kwargs):
    """Close the invalid PR, add 'invalid' label, and post a message.

    PR is considered invalid if:
    * base_label is 'python:main'
    * head_label is '<username>:<maint_branch>'
    """
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)
        head_label = event["pull_request"]["head"]["label"]
        base_label = event["pull_request"]["base"]["label"]

    if PYTHON_MAINT_BRANCH_RE.match(head_label) and \
        base_label == "python:main":
        data = {'state': 'closed'}
        await gh.patch(event["pull_request"]["url"], data=data)
        await gh.post(
            f'{event["pull_request"]["issue_url"]}/labels',
            data=["invalid"]
        )
        await gh.post(
            f'{event["pull_request"]["issue_url"]}/comments',
            data={'body': INVALID_PR_COMMENT}
        )

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            gh = GitHubAPI(session, "sabderemane", oauth_token=os.getenv("GH_AUTH"))
            await close_invalid_pr(gh)  
    except Exception:
        traceback.print_exc()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())