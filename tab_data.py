import pandas as pd
import streamlit as st
import youtube_db as ytdb
import time
from streamlit_player import st_player

def get_hhmmss(value):
    return time.strftime('%H:%M:%S', time.gmtime(pd.Timedelta(value['Duration']).seconds))

def load():
    
    all_channels = pd.DataFrame(ytdb.channel_data(), columns=['Channel ID', 'Channel Name', 'Views', 'Description', 'Status'])

    all_videos = pd.DataFrame(ytdb.all_videos(), columns=['Video ID', 'Channel ID', 'Channel Name', 'Video Name', 'Video Description', 'Published Date', 'View Count', 'Like Count', 'Dislike Count', 'Favorite Count', 'Comment Count', 'Duration', 'Caption Status'])
    all_videos['Video Duration'] = all_videos.apply(get_hhmmss, axis=1)

    selected_channel = st.multiselect(label='Select a channel to filter', options = all_channels['Channel Name'])
    
    video_filter = st.text_input('Filter by video name or description')
    
    if selected_channel:
        selected_videos = all_videos[all_videos['Channel Name'].isin(selected_channel)]
    else:
        selected_videos = all_videos
        
    if video_filter:
        selected_videos = selected_videos[selected_videos['Video Name'].str.contains(video_filter, case=False) | selected_videos['Video Description'].str.contains(video_filter, case=False)]
        
    selected_video = st.dataframe(selected_videos[['Channel Name', 'Video Name', 'Video Description', 'Video Duration', 'View Count', 'Comment Count']], selection_mode="single-row", on_select="rerun", hide_index=True)

    if selected_video:
        play_video = st.button("Play Video")
    
    if play_video:
        url = selected_videos.iloc[selected_video['selection']['rows'][0]]['Video ID']
        video_url = f"https://youtu.be/{url}"
        st_player(video_url, playing=True)