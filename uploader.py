import datetime
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


def upload_video(filename, title, description, tags):
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)

    now = datetime.datetime.now()
    upload_date_time = datetime.datetime(
        now.year, now.month, now.day, now.hour, now.minute + 5, int(now.second)).isoformat() + '.000Z'

    request_body = {
        'snippet': {
            'categoryID': 23,
            'title': title,
            'description': description,
            'tags': tags,
        },
        'status': {
            'privacyStatus': 'public',
            # 'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    media_file = MediaFileUpload(filename)

    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
