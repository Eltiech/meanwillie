# coding=utf8

"""
youtube.py - Willie YouTube v3 Module
Copyright (c) 2015 Calvin Montgomery, All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list
of conditions and the following disclaimer. Redistributions in binary form must
reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the
distribution. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
OF SUCH DAMAGE.

Behavior based on the original YouTube module by the following authors:
Dimitri Molenaars, Tyrope.nl.
Elad Alfassa, <elad@fedoraproject.org>
Edward Powell, embolalia.net

Usage:

    1. Go to https://console.developers.google.com/project
    2. Create a new API project
    3. On the left sidebar, click "Credentials" under "APIs & auth"
    4. Click "Create new Key" under "Public API access"
    5. Click "Server key"
    6. Under "APIs & auth" click "YouTube Data API" and then click "Enable API"

Once the key has been generated, add the following to your willie config
(replace dummy_key with the key obtained from the API console):

[youtube]
api_key = dummy_key

"""

import datetime
import json
import re
import sys
from willie import web, tools
from willie.module import rule, commands, example

URL_REGEX = re.compile(r'(youtube.com/watch\S*v=|youtu.be/)([\w-]+)')
INFO_URL = ('https://www.googleapis.com/youtube/v3/videos'
            '?key={}&part=contentDetails,status,snippet,statistics&id={}')
SEARCH_URL = ('https://www.googleapis.com/youtube/v3/search'
              '?key={}&part=id&maxResults=1&q={}&type=youtube%23video')

class YouTubeError(Exception):
    pass

def setup(bot):
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.WillieMemory()
    bot.memory['url_callbacks'][URL_REGEX] = youtube_info

def shutdown(bot):
    del bot.memory['url_callbacks'][URL_REGEX]

def get_api_key(bot):
    if not bot.config.has_option('youtube', 'api_key'):
        raise KeyError('Missing YouTube API key')
    return bot.config.youtube.api_key

def configure(config):
    if config.option('Configure YouTube v3 API', False):
        config.interactive_add('youtube', 'api_key', 'Google Developers '
                'Console API key (Server key)')

def convert_date(date):
    """Parses an ISO 8601 datestamp and reformats it to be a bit nicer"""
    date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    return date.strftime('%Y-%m-%d %H:%M:%S UTC')

def convert_duration(duration):
    """Converts an ISO 8601 duration to a human-readable duration"""
    units = {
        'hour': 0,
        'minute': 0,
        'second': 0
    }
    for symbol, unit in zip(('H', 'M', 'S'), ('hour', 'minute', 'second')):
        match = re.search(r'(\d+)' + symbol, duration)
        if match:
            units[unit] = int(match.group(1))

    time = datetime.time(**units)
    output = str(time)
    match = re.search('(\d+)D', duration)
    if match:
        output = match.group(1) + ' days, ' + output
    return output

def fetch_video_info(bot, id):
    """Retrieves video metadata from YouTube"""
    url = INFO_URL.format(get_api_key(bot), id)
    result = json.loads(web.get(url))

    if 'error' in result:
        raise YouTubeError(result['error']['message'])

    if len(result['items']) == 0:
        raise YouTubeError('YouTube API returned empty result')

    video = result['items'][0]
    info = {
        'title': video['snippet']['title'],
        'uploader': video['snippet']['channelTitle'],
        'uploaded': convert_date(video['snippet']['publishedAt']),
        'duration': convert_duration(video['contentDetails']['duration']),
        'views': video['statistics']['viewCount'],
        'comments': video['statistics']['commentCount'],
        'likes': video['statistics']['likeCount'],
        'dislikes': video['statistics']['dislikeCount'],
        'link': 'https://youtu.be/' + video['id']
    }

    return info

def fix_count(count):
    """Adds commas to a number representing a count"""
    return '{:,}'.format(int(count))

def format_info(tag, info, include_link=False):
    """Formats video information for sending to IRC.

    If include_link is True, then the video link will be included in the
    output (this is useful for search results), otherwise it is not (no
    reason to include a link if we are simply printing information about
    a video that was already linked in chat).
    """
    output = [
        '[{}] Title: {}'.format(tag, info['title']),
        'Uploader: ' + info['uploader'],
        'Uploaded: ' + info['uploaded'],
        'Duration: ' + info['duration'],
        'Views: ' + fix_count(info['views']),
        'Comments: ' + fix_count(info['comments']),
        'Likes: ' + fix_count(info['likes']),
        'Dislikes: ' + fix_count(info['dislikes'])
    ]

    if include_link:
        output.append('Link: ' + info['link'])

    return ' | '.join(output)

@rule('.*(youtube.com/watch\S*v=|youtu.be/)([\w-]+).*')
def youtube_info(bot, trigger, found_match=None):
    """Catches youtube links said in chat and fetches video information"""
    match = found_match or trigger
    try:
        info = fetch_video_info(bot, match.group(2))
    except YouTubeError as e:
        bot.say('[YouTube] Lookup failed: {}'.format(e))
        return
    bot.say(format_info('YouTube', info))

@commands('yt', 'youtube')
@example('.yt Mystery Skulls - Ghost')
def ytsearch(bot, trigger):
    """Allows users to search for YouTube videos with .yt <search query>"""
    if not trigger.group(2):
        return

    # Note that web.get() quotes the query parameters, so the
    # trigger is purposely left unquoted (double-quoting breaks things)
    url = SEARCH_URL.format(get_api_key(bot), trigger.group(2))
    result = json.loads(web.get(url))
    if 'error' in result:
        bot.say('[YouTube Search] ' + result['error']['message'])
        return

    if len(result['items']) == 0:
        bot.say('[YouTube Search] No results for ' + trigger.group(2))
        return

    # YouTube v3 API does not include useful video metadata in search results.
    # Searching gives us the video ID, now we have to do a regular lookup to
    # get the information we want.
    try:
        info = fetch_video_info(bot, result['items'][0]['id']['videoId'])
    except YouTubeError as e:
        bot.say('[YouTube] Lookup failed: {}'.format(e))
        return

    bot.say(format_info('YouTube Search', info, include_link=True))
