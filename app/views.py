from .items import *
from .models import *
from .recognition import *
from .summary import *
from .tools import *

from django.shortcuts import render
from youtube_transcript_api import YouTubeTranscriptApi

DEFAULT_VIDEO_ID = "G9-urSR19SI"

summarizer = Summarizer()
keywordFinder = KeywordFinder()
cache = dict()

def summarize(request, video_id=None):
    if not video_id:
        video_id = DEFAULT_VIDEO_ID

    if video_id in cache:
        print("Response cached.")
        context = cache[video_id]
    else:
        time_to_label = dict()
        thread = fetch_highlights_thread(video_id, time_to_label)
        thread.start()
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en',])
        subtitles = get_subtitles(transcript)
        joined_subtitles = get_joined_subtitles(transcript)
        summary = summarizer.summarize(joined_subtitles)
        keywords_to_sentence_indices = keywordFinder.keywords(subtitles) 
        thread.join()
        items = get_items(transcript, keywords_to_sentence_indices, time_to_label)
        intervals_to_skip = get_intervals_to_skip(items)
        context = {'video_id': video_id, 'summary': summary, 'items': items, 'intervals_to_skip': intervals_to_skip }
        cache[video_id] = context

    return render(request, 'summary.html', context)
