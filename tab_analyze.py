import streamlit as st
import youtube_client_df as yt_df
import youtube_db as ytdb
import pandas as pd
import plotly.express as px
import time

def seconds(row):
    return pd.Timedelta(row['Duration']).seconds

def load():
    option = st.selectbox("Select from below", ('Videos Count by Channel', 'Top 10 Videos', 'Videos and Channels', 'Videos and Comments', 'Top 10 videos by likes', 'Video Like Counts', 'Channel Views', '2022 Active Channels', 'Top 100 Videos by Comments', 'Videos by Duration'), index=None)
            
    if (option == 'Videos Count by Channel'):
        output = pd.DataFrame(ytdb.get_videos_count_by_channel(), columns=['Channel','Videos count'])
        st.write(output)
        st.bar_chart(output, x='Channel', y='Videos count', horizontal = True)
    elif(option == 'Top 10 Videos'):
        top_10_videos = pd.DataFrame(ytdb.get_top10_videos(), columns=['Video ID','Video Name', 'Channel ID', 'Channel Name', 'Views', 'Rank']).drop(['Video ID','Channel ID'], axis=1)
        st.write(top_10_videos)
        
        option = st.selectbox('Select a channel', top_10_videos['Channel Name'].unique(), index=None)
        if option:
            st.bar_chart(top_10_videos.loc[top_10_videos['Channel Name'] == option], x='Video Name', y='Views', horizontal = True)
    elif(option == 'Videos and Channels'):
        output = pd.DataFrame(ytdb.get_videos_and_channels(), columns=['Video Name','Channel Name'])
        st.write(output)
    elif(option == 'Videos and Comments'):
        output = pd.DataFrame(ytdb.get_videos_and_comments_count(), columns=['Video Name','Comments count'])
        st.write(output)        
    elif(option == 'Top 10 videos by likes'):
        output = pd.DataFrame(ytdb.top_10_videos_by_likes(), columns=['Video Name','Channel Name', 'Like Count'])
        st.write(output)
    elif(option == 'Video Like Counts'):
        output = pd.DataFrame(ytdb.video_like_count(), columns=['Video Name','Like Count', 'Dislike Count'])
        st.write(output)
    elif(option == 'Channel Views'):
        output = pd.DataFrame(ytdb.channel_data(), columns=['channel_id', 'channel_name', 'channel_views', 'channel_desc', 'channel_status'])[['channel_name','channel_views']]
        st.write(output)
        px_line = px.scatter(output, x='channel_views', y='channel_name', size_max=60, log_x=True)
        st.plotly_chart(px_line)
    elif(option == '2022 Active Channels'):
        output = pd.DataFrame(ytdb.active_channels_2022(), columns=['Channel Names'])
        st.write(output)
    elif(option == 'Top 100 Videos by Comments'):
        output = pd.DataFrame(ytdb.top_100_videos_by_comments(), columns=['Video Names', 'Comments Count'])
        st.write(output)
    elif(option == 'Videos by Duration'):
        output = pd.DataFrame(ytdb.videos_with_duration(), columns=['Channel Name', 'Duration'])
        output['Average Duration'] = output.apply(seconds, axis=1)
        st.write(output.groupby('Channel Name')['Average Duration'].mean())
