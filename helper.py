def fetch_stats(selected_list,df):
    if selected_list=='OverAll':
        #fetch number of messages
        num_messages=df.shape[0]
        #fetch number of words
        words = []
        for message in df['message']:
            words.extend(message.split())
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        return num_messages,len(words),num_media_messages
    else:
        # fetch number of messages
        new_df =df[df['user'] == selected_list]
        nuw_messages=new_df.shape[0]
        # fetch number of words
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        return nuw_messages,len(words),num_media_messages

