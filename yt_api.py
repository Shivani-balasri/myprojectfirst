
from googleapiclient.discovery import build
from iteration_utilities import unique_everseen
from dotenv import load_dotenv

import csv
from datetime import datetime as dt

comments = []
today = dt.today().strftime('%d-%m-%Y')

def process_comments(response_items, csv_output=False):

    for res in response_items:
        if 'replies' in res.keys():
            for reply in res['replies']['comments']:
                comment = reply['snippet']
                comment['commentId'] = reply['id']
                comments.append(comment)
        else:
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']

            comments.append(comment['snippet'])

    if csv_output:
         make_csv(comments)
    
    print(f'Finished processing {len(comments)} comments.')
    return comments


def make_csv(comments, channelID=None):
    header = comments[0].keys()

    if channelID:
        filename = f'comments_{channelID}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    with open(filename, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(comments)
load_dotenv()
API_KEY = 


youtube = build("youtube", "v3", developerKey=API_KEY)

def search_result(query):
 
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=10,
    )

    return request.execute()

def channel_stats(channelID):
  
    request = youtube.channels().list(
        part="statistics",
        id=channelID
    )
    return request.execute()

def comment_threads(videoID, to_csv=False):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='id,replies,snippet',
        videoId=videoID,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=videoID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    comments_list = list(unique_everseen(comments_list))

    print(f"Finished fetching comments for {videoID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, videoID)
    
    return comments_list


def get_video_ids(channelId):

    videoIds = []
 
    request = youtube.search().list(
        part="snippet",
        channelId=channelId,
        type="video",
        maxResults=50,
        order="date"
    )

    response = request.execute()
    responseItems = response['items']

    videoIds.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])

    while response.get('nextPageToken', None):
        request = youtube.search().list(
            part="snippet",
            channelId=channelId,
        )
        response = request.execute()
        responseItems = response['items']

        videoIds.extend([item['id']['videoId'] for item in responseItems if item['id'].get('videoId', None) != None])
    
    print(f"videoIds {channelId}. {len(videoIds)} ")

    return videoIds



if __name__ == '__main__':

    response = comment_threads(videoID='Qo8dXyKXyME', to_csv=True)

    print(response)