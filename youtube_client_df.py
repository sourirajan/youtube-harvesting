import requests
import datetime
import pandas as pd
import streamlit as st
import os

def yt_channel_url(channel_id, include, api_key=os.environ['API_KEY']):
  return f"https://www.googleapis.com/youtube/v3/channels?key={api_key}&id={channel_id}&part={include}"
  
def yt_playlist_url(channel_id, include, page_token=None, api_key=os.environ['API_KEY']):
  url = f"https://www.googleapis.com/youtube/v3/playlists?key={api_key}&channelId={channel_id}&part={include}&maxResults=50"
  if page_token is not None:
    url = f"{url}&pageToken={page_token}"
  return url

def yt_playlistitem_url(upload_playlist_id, include, page_token=None, api_key=os.environ['API_KEY']):
  url = f"https://www.googleapis.com/youtube/v3/playlistItems?key={api_key}&playlistId={upload_playlist_id}&part={include}&maxResults=50"
  if page_token is not None:
    url = f"{url}&pageToken={page_token}"
  return url
  
def yt_video_url(video_ids, include, page_token=None, api_key=os.environ['API_KEY']):
  url = f"https://www.googleapis.com/youtube/v3/videos?key={api_key}&id={video_ids}&part={include}&maxResults=50"
  if page_token is not None:
    url = f"{url}&pageToken={page_token}"
  return url
  
def yt_comment_threads_url(channel_id, include, page_token=None, api_key=os.environ['API_KEY']):
  url = f"https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&allThreadsRelatedToChannelId={channel_id}&part={include}&maxResults=50"
  if page_token is not None:
    url = f"{url}&pageToken={page_token}"
  return url

@st.cache_data  
def get_channel_details(channel_id):
  response = requests.get(yt_channel_url(channel_id, 'statistics,brandingSettings,status,contentDetails'))
  responseJson = response.json()
  if responseJson['pageInfo']['totalResults'] == 0:
    return {'error': 'Invalid Channel ID'}
    
  return {
      'id': responseJson['items'][0]['id'],
      "upload_playlist_id": responseJson['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
      'name': responseJson['items'][0]['brandingSettings']['channel']['title'],
      'description': repr(responseJson['items'][0]['brandingSettings']['channel']['description']) if 'description' in responseJson['items'][0]['brandingSettings'] else None,
      'type': repr(responseJson['items'][0]['brandingSettings']['channel']['keywords']) if 'keywords' in responseJson['items'][0]['brandingSettings']['channel'] else None,
      'subscriber_count': responseJson['items'][0]['statistics']['subscriberCount'],
      'view_count': responseJson['items'][0]['statistics']['viewCount'],
      'status': responseJson['items'][0]['status']['privacyStatus']
  }

@st.cache_data  
def get_playlist_details(channel_id):
  result = []
  nextPageToken = None

  while(True):
    response = requests.get(yt_playlist_url(channel_id, 'id, contentDetails,status,snippet', nextPageToken)).json()

    for item in response['items']:
      result.append({
          'id': item['id'],
          'channelId': item['snippet']['channelId'],
          'title': item['snippet']['title'],
          'status': item['status']['privacyStatus'],
          'count': item['contentDetails']['itemCount'],
      })

    if 'nextPageToken' in response:
      nextPageToken = response['nextPageToken']
    else:
      nextPageToken = None

    if nextPageToken is None:
      break

  return result

@st.cache_data
def get_video_details(channel_id, upload_playlist_id):
  videoIds = []
  videos = []

  nextPageToken = None

  while(True):    
    response = requests.get(yt_playlistitem_url(upload_playlist_id, 'contentDetails,status,snippet,id', nextPageToken)).json()

    for item in response['items']:
      videoIds.append(item['contentDetails']['videoId'])

    if 'nextPageToken' in response:
        nextPageToken = response['nextPageToken']
    else:
        nextPageToken = None

    if nextPageToken is None:
        break

  videoIdChunks = []
  for i in range(0, len(videoIds), 50):
    videoIdChunks.append(videoIds[i:i + 50])
  
  for chunk in videoIdChunks:
    ids = ','.join(chunk)
    i = i + 1
    
    response = requests.get(yt_video_url(ids, 'contentDetails,status,snippet,id,statistics')).json()

    for item in response['items']:
      videos.append({
          'id': item['id'],
          'name': item['snippet']['title'],
          'channelid': channel_id,
          'description': item['snippet']['description'][:255] if 'description' in item['snippet'] else None,
          'publishedDate': datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
          'viewCount': item['statistics']['viewCount'] if 'viewCount' in item['statistics'] else '0',
          'likeCount': item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else '0',
          'dislikeCount': item['statistics']['dislikeCount'] if 'dislikeCount' in item['statistics'] else '0',
          'favoriteCount': item['statistics']['favoriteCount'] if 'favoriteCount' in item['statistics'] else '0',
          'commentCount': item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else '0',
          'duration': item['contentDetails']['duration'] if 'duration' in item['contentDetails'] else '0',
          'caption_status': item['contentDetails']['caption'] if 'caption' in item['contentDetails'] else None
      })


  return videos

@st.cache_data
def get_comments(channel_id):
  result = []
  nextPageToken = None

  while(True):
    response = requests.get(yt_comment_threads_url(channel_id, 'id,snippet', nextPageToken)).json()

    for item in response['items']:
      result.append({
          'id': item['id'],
          'videoId': item['snippet']['videoId'],
          'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
          'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
          'publishedDate': datetime.datetime.strptime(item['snippet']['topLevelComment']['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
      })

    if 'nextPageToken' in response:
      nextPageToken = response['nextPageToken']
    else:
      nextPageToken = None

    if nextPageToken is None:
      break

  return result