KEY_TEXT = "text"
KEY_START = "start"
KEY_DURATION = "duration"

def get_subtitles(transcript_data):
    return [item[KEY_TEXT] for item in transcript_data]

def get_joined_subtitles(transcript_data):
    return " ".join(get_subtitles(transcript_data))

def get_interval(transcript_data, index):
    item = transcript_data[index]
    return (item[KEY_START], item[KEY_START] + item[KEY_DURATION])

def get_readable_time(time_seconds):
    hours = int(time_seconds) // (60 ** 2)
    minutes = (int(time_seconds) // 60) % 60
    seconds = int(time_seconds) % 60

    readable_time = ""
    if hours > 0:
        readable_time += str(hours) + "h "
    if minutes > 0 or hours > 0:
        readable_time += str(minutes) + "m "
    readable_time += str(seconds) + "s"
    return readable_time
