import streamlit as st
import pandas as pd
import youtube_client_df as yt_df
import youtube_db as ytdb
import time
import os

def save_data(channel, playlists, videos, comments):
    with st.container():
        ytdb.save_all_data(channel, playlists, videos, comments)
        st.success("Save complete!")
        if (st.button("Close")):
            close()

def get_hhmmss(value):
    return time.strftime('%H:%M:%S', time.gmtime(pd.Timedelta(value['duration']).seconds))

def load():

    channel_id = st.text_input("Enter channel id")

    if channel_id:
        # Get data from youtube data API and convert to dataframe
        #channel_df = pd.DataFrame([channel])
        channel = yt_df.get_channel_details(channel_id)
        
        if 'error' in channel:
            st.error("Invalid channel ID")
            return
       
        # Display Channel information
        st.header("Channel")
        st.dataframe(pd.DataFrame([channel])[["name","description","subscriber_count","view_count","status"]])

        # Get playlists data and display
        st.header("Playlists")
        playlists = yt_df.get_playlist_details(channel_id)
        st.dataframe(pd.DataFrame(playlists, columns=['id','channelId','title','status','count'])[["title","status","count"]])

        # Get videos
        st.header("Videos")
        videos = yt_df.get_video_details(channel_id, channel['upload_playlist_id'])
        videos_df = pd.DataFrame(videos)
        # Convert duration from ISO format to seconds
        videos_df['hhmmss'] = videos_df.apply(get_hhmmss, axis=1)
        st.dataframe(videos_df.drop(['id','channelid','duration'], axis=1))

        # Get comments
        st.header("Comments")
        comments = yt_df.get_comments(channel_id)
        st.dataframe(pd.DataFrame(comments).drop(['id','videoId'], axis=1))
        
        if st.button("Save"):
            save_data(channel, playlists, videos, comments)
