import psycopg2
import os


def get_connection():
    return psycopg2.connect(user=os.environ['pg_user'],
        password=os.environ['pg_password'],
        host=os.environ['pg_host'],
        port=os.environ['pg_port'],
        dbname=os.environ['pg_dbname']
    )

def save_channel(channel, cursor):
    query = "INSERT INTO YT_CHANNEL(CHANNEL_ID, CHANNEL_NAME, CHANNEL_VIEWS, CHANNEL_DESC, CHANNEL_STATUS) VALUES (%(id)s, %(name)s, %(view_count)s, %(description)s, %(status)s) ON CONFLICT(CHANNEL_ID) DO UPDATE SET CHANNEL_NAME = %(name)s, CHANNEL_VIEWS=%(view_count)s, CHANNEL_DESC=%(description)s, CHANNEL_STATUS=%(status)s";

    cursor.execute(query, channel)


def save_playlists(playlists, cursor):
    query = "INSERT INTO YT_PLAYLIST(PLAYLIST_ID, CHANNEL_ID, PLAYLIST_TITLE, PLAYLIST_STATUS, ITEM_COUNT) VALUES (%(id)s, %(channelId)s, %(title)s, %(status)s, %(count)s) ON CONFLICT(PLAYLIST_ID) DO UPDATE SET PLAYLIST_TITLE = %(title)s, PLAYLIST_STATUS=%(status)s, ITEM_COUNT=%(count)s";
    
    for playlist in playlists:
        cursor.execute(query, playlist)


def save_videos(videos, cursor):
    query = "INSERT INTO YT_VIDEO(VIDEO_ID, CHANNEL_ID, VIDEO_NAME, VIDEO_DESC, PUBLISHED_DATE, VIEW_COUNT, LIKE_COUNT, DISLIKE_COUNT, FAV_COUNT, COMMENT_COUNT, DURATION, CAPTION_STATUS) VALUES (%(id)s, %(channelid)s, %(name)s, %(description)s, %(publishedDate)s, %(viewCount)s, %(likeCount)s, %(dislikeCount)s, %(favoriteCount)s, %(commentCount)s, %(duration)s, %(caption_status)s) ON CONFLICT(VIDEO_ID) DO UPDATE SET VIDEO_NAME = %(name)s, VIDEO_DESC=%(description)s, PUBLISHED_DATE=%(publishedDate)s, VIEW_COUNT=%(viewCount)s, LIKE_COUNT=%(likeCount)s, DISLIKE_COUNT=%(dislikeCount)s, FAV_COUNT=%(favoriteCount)s, COMMENT_COUNT=%(commentCount)s, DURATION=%(duration)s, CAPTION_STATUS=%(caption_status)s";
    
    for video in videos:
        cursor.execute(query, video)

def save_comments(comments, cursor):
    query = "INSERT INTO YT_COMMENT(COMMENT_ID, VIDEO_ID, COMMENT_TEXT, AUTHOR, PUBLISHED_DATE) VALUES (%(id)s, %(videoId)s, %(text)s, %(author)s, %(publishedDate)s) ON CONFLICT(COMMENT_ID) DO UPDATE SET VIDEO_ID = %(videoId)s, COMMENT_TEXT=%(text)s, AUTHOR=%(author)s, PUBLISHED_DATE=%(publishedDate)s";
    
    for comment in comments:
        cursor.execute(query, comment)
        

def save_all_data(channel, playlists, videos, comments):
    connection = get_connection()
    cursor = connection.cursor()

    save_channel(channel, cursor)
    save_playlists(playlists, cursor)
    save_videos(videos, cursor)
    save_comments(comments, cursor)
    
    connection.commit()
    cursor.close()
    connection.close()
    

def executeQuery(query):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()   
    return result
    
def get_videos_count_by_channel():
    query = "select channel_name, count(video_name) as video_count from (select v.video_name as video_name, c.channel_name as channel_name from yt_video v inner join yt_channel c on v.channel_id = c.channel_id) group by channel_name order by video_count desc"
    
    return executeQuery(query)


def get_top10_videos():
    query = "with ranked_videos as (select v.video_id, v.video_name, c.channel_id, c.channel_name, v.view_count, rank() over (partition by v.channel_id order by v.view_count desc) as ranking  from yt_video v inner join yt_channel c on v.channel_id = c.channel_id) select * from ranked_videos where ranking <= 10"
    return executeQuery(query)

def get_videos_and_channels():
    query = "select v.video_name, c.channel_name from yt_video v inner join yt_channel c on v.channel_id = c.channel_id"
    return executeQuery(query)

def get_videos_and_comments_count():
    query = "with video_comments_count as (select video_id, count(*) from yt_comment group by video_id) select v.video_name, c.count from yt_video v inner join video_comments_count c on v.video_id = c.video_id"
    return executeQuery(query)

def top_10_videos_by_likes():
    query = "select v.video_name, c.channel_name, v.like_count from yt_video v inner join yt_channel c on v.channel_id = c.channel_id  order by like_count desc limit 10"
    return executeQuery(query)

def video_like_count():
    query = "select video_name, like_count, dislike_count from yt_video"
    return executeQuery(query)

def channel_data():
    query = "select channel_id, channel_name, channel_views, channel_desc, channel_status from yt_channel"
    return executeQuery(query)

def active_channels_2022():
    query = "select distinct c.channel_name from yt_video v inner join yt_channel c on v.channel_id = c.channel_id where extract(year from v.published_date) = 2022"
    return executeQuery(query)

def top_100_videos_by_comments():
    query = "with video_comments_count as (select video_id, count(video_id) as comments_count from yt_comment group by video_id order by comments_count desc limit 100) select yt_video.video_name, video_comments_count.comments_count from yt_video inner join video_comments_count on yt_video.video_id = video_comments_count.video_id order by comments_count desc"
    return executeQuery(query)

def videos_with_duration():
    query = "select c.channel_name as channel_name, v.duration as duration from yt_video v inner join yt_channel c on v.channel_id = c.channel_id"
    return executeQuery(query)

def all_videos():
    query = "select video_id, yt_channel.channel_id, channel_name, video_name, video_desc, published_date, view_count, like_count, dislike_count, fav_count, comment_count, duration, caption_status from yt_video inner join yt_channel on yt_video.channel_id = yt_channel.channel_id"
    return executeQuery(query)