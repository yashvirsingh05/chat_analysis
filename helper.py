from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji

def fetch_stats(selected_list,df):
    if selected_list=='OverAll':
        num_messages=df.shape[0]
        words = []
        urls=[]
        extractor = URLExtract()
        for message in df['message']:
            words.extend(message.split())
            urls.extend(extractor.find_urls(message))
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        return num_messages,len(words),num_media_messages,len(urls)
    else:
        # fetch number of messages
        new_df =df[df['user'] == selected_list]
        nuw_messages=new_df.shape[0]
        extractor = URLExtract()
        # fetch number of words
        words = []
        urls = []
        for message in new_df['message']:
            words.extend(message.split())
            urls.extend(extractor.find_urls(message))
        num_media_messages = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        return nuw_messages,len(words),num_media_messages,len(urls)

#crate most busy users List
def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,new_df


#create world cloud
def create_worldcould(selected_list,df):
    if selected_list == 'OverAll':
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(df['message'].str.cat(sep=" "))
        return df_wc

    else:
        new_df = df[df['user'] == selected_list]
        wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        df_wc=wc.generate(new_df['message'].str.cat(sep=" "))
        return df_wc

#most common words
def most_common_words(selected_list,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_list == 'OverAll':
        temp = df[df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
        words = []
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words and string.punctuation:
                    words.append(word)
        return pd.DataFrame(Counter(words).most_common(20))
    else:
        new_df = df[df['user'] == selected_list]
        temp = new_df[new_df['user'] != 'group_notification']
        temp = temp[temp['message'] != '<Media omitted>\n']
        words = []
        for message in temp['message']:
            for word in message.lower().split():
                if word not in stop_words and string.punctuation:
                    words.append(word)
        return pd.DataFrame(Counter(words).most_common(10))


# temp = df[df['user'] != 'group_notification']
# temp = temp[temp['message'] != '<Media omitted>\n']
# def remove_stop_words(message):
#   words = []
#   for word in message.lower().split():
#       if word not in stop_words and string.punctuation:
#           words.append(word)
#   return " ".join(words)
# temp['message']=temp['message'].apply(remove_stop_words)


def emoji_helper(selected_list,df):
    emojis = []
    if selected_list == 'OverAll':

        for message in df['message']:
            for c in message:
                if emoji.is_emoji(c):
                    emojis.append(c)
    else:
        new_df = df[df['user'] == selected_list]
        for message in new_df['message']:
            for c in message:
                if emoji.is_emoji(c):
                    emojis.append(c)
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#monthly timeline
def monthly_timeline(selected_list,df):
    time = []
    if selected_list == 'OverAll':
        timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
        timeline['time'] = time

    else:
        new_df = df[df['user'] == selected_list]
        timeline = new_df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

        for i in range(timeline.shape[0]):
            time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
        timeline['time'] = time

    return timeline

#check daily timeline
def daily_timeline(selected_list,df):
    if selected_list == 'OverAll':
        daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    else:
        new_df = df[df['user'] == selected_list]
        daily_timeline = new_df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

#check for most activit week
def week_activity_map(selected_list,df):
    if selected_list == 'OverAll':
       week_activity= df['day_name'].value_counts()
    else:
        new_df = df[df['user'] == selected_list]
        week_activity= df['day_name'].value_counts()
    return week_activity

#check for most activit month
def month_activity_map(selected_list,df):
    if selected_list == 'OverAll':
       month_activity= df['month'].value_counts()
    else:
        new_df = df[df['user'] == selected_list]
        month_activity= df['month'].value_counts()
    return month_activity


#
def activity_heatmap(selected_list,df):
    if selected_list == 'OverAll':
      activity_heatmap= df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    else:
        new_df = df[df['user'] == selected_list]
        activity_heatmap= new_df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_heatmap

