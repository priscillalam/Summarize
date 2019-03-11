from .tools import get_readable_time

HIGHLIGHT_DURATION_SECONDS = 5

class Link:
    def __init__(
        self,
        keyword,
        wikipedia_link,
        definition,
        time_start,
        time_end):
        self.keyword = keyword
        self.wikipedia_link = wikipedia_link
        self.definition = definition
        self.time_start = int(time_start)
        self.time_end = int(time_end)
        self.readable_time = get_readable_time(time_start)
        self.is_highlight = False
        
class Highlight:
    def __init__(
        self,
        description,
        time_start):
        self.description = description
        self.time_start = int(time_start)
        self.time_end = int(time_start + HIGHLIGHT_DURATION_SECONDS)
        self.readable_time = get_readable_time(time_start)
        self.is_highlight = True
