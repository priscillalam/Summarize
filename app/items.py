import sys

from .models import *
from .tools import *
from .wiki import *

INTERVAL_MARGIN_SECONDS = 2

def get_items(transcript, keywords_to_sentence_indices, time_to_label):
    items = []
    keywords = keywords_to_sentence_indices.keys()
    term_to_wikipedia_response = fetch_wikipedia_for_terms(keywords)
    for keyword in keywords:
        sentence_index = keywords_to_sentence_indices[keyword]
        interval_start, interval_end = get_interval(transcript, sentence_index)
        previous_time = interval_end
        wikipedia_response = term_to_wikipedia_response[keyword]
        items.append( \
            Link( \
                keyword, \
                wikipedia_response.wikipedia_link, \
                wikipedia_response.definition, \
                interval_start, \
                interval_end \
                ) \
            )
    for time in time_to_label:
        items.append(Highlight(time_to_label[time], time))
    items.sort(key=lambda link: link.time_start)
    return items

def get_intervals_to_skip(items):
    raw_intervals = []

    for item in items:
        time_start = max(0, item.time_start - INTERVAL_MARGIN_SECONDS)
        time_end = item.time_end + INTERVAL_MARGIN_SECONDS
        raw_intervals.append((time_start, time_end))

    intervals_to_play = non_overlapping_intervals(raw_intervals)
    previous_time = 0
    intervals_to_skip = []
    for interval in intervals_to_play:
        if previous_time != interval[0]:
            intervals_to_skip.append((previous_time, interval[0]))
        previous_time = interval[1]
    intervals_to_skip.append((previous_time, 2 ** 32));
    return intervals_to_skip

def non_overlapping_intervals(intervals):
    sorted_by_lower_bound = sorted(intervals, key=lambda interval: interval[0])
    merged_intervals = []

    for higher in sorted_by_lower_bound:
        if not merged_intervals:
            merged_intervals.append(higher)
        else:
            lower = merged_intervals[-1]
            if higher[0] <= lower[1]:
                upper_bound = max(lower[1], higher[1])
                merged_intervals[-1] = (lower[0], upper_bound)
            else:
                merged_intervals.append(higher)
    return merged_intervals
