# Summarize

Summarize extracts highlights from video and provides context using information from the video’s subtitles and the video frame data itself. Users specify a Youtube URL in the input field and Summarize will display the highlights of the video, keywords with definitions, and a summary of the video. This is done through different artificial intelligence techniques such as TextRank, K-Means, and Google’s Cloud Vision. The app is written with the Django framework and runs on Python 3. 

### Prerequisites
- Python 3 with venv
- Google Cloud Vision API credentials. Place the credentials.json in app/credentials

### Instructions to run

1. Create a virtual environment to isolate dependencies.
`python3 -m venv env`

2. Enter the virtual environment.
`source env/bin/activate`

3. Install dependencies.
`pip install -r requirements.txt`

4. Run the app on localhost:8080/
`python3 manage.py runserver 8080`
