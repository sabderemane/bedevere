"""Checks related to filepaths on a pull request."""
import asyncio
import json
import os
import traceback

import aiohttp
from gidgethub.aiohttp import GitHubAPI

from . import news
from . import prtype
from . import util


async def check_file_paths(gh, *args, **kwargs):
    with open(os.environ["GITHUB_EVENT_PATH"]) as f:
        event = json.load(f)
        pull_request = event['pull_request']
    files = await util.files_for_PR(gh, pull_request)
    filenames = [file['file_name'] for file in files]
    await news.check_news(gh, pull_request, files)
    if event['action'] == 'opened':
        await prtype.classify_by_filepaths(gh, pull_request, filenames)

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            gh = GitHubAPI(session, "sabderemane", oauth_token=os.getenv("GH_AUTH"))
            await check_file_paths(gh)  
    except Exception:
        traceback.print_exc()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())