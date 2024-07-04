import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analysis")
font_path = 'NotoEmoji-VariableFont_wght.ttf'  # Update this to the correct path
prop = FontProperties(fname=font_path)
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'OverAll')
    user_list.remove('group_notification')
    selected_list=st.sidebar.selectbox("Show Users List",user_list)
    if st.sidebar.button("Show Analysis"):
        num_message,words,num_media_messages,urls=helper.fetch_stats(selected_list,df)
        st.title("Top Statistics")

        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Link Shared")
            st.title(urls)
        #finding the busiest users in the group(group level)
        if selected_list=='OverAll':
            st.title('Most Busy Users')
            x,new_df=helper.most_busy_users(df)
            col1,col2=st.columns(2)
            fig,ax=plt.subplots()

            with col1:
                st.header("Link Shared")
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Link Shared")
                st.dataframe(new_df)
        #Create wordcloud
        st.title("WordCloud")
        df_wc=helper.create_worldcould(selected_list,df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most Common Words")
        df_mc = helper.most_common_words(selected_list,df)
        fig,ax=plt.subplots()
        ax.barh(df_mc[0],df_mc[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig)
        st.dataframe(df_mc)


        #most common emojii
        st.title("Most Common Emoji")
        emoji_df = helper.emoji_helper(selected_list, df)
        autopct = lambda p: '{:.2f}%'.format(p)

        col1, col2 = st.columns(2)
        fig, ax = plt.subplots()

        with col2:
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(), textprops={'fontproperties': prop})
            st.pyplot(fig)
        with col1:
            st.dataframe(emoji_df)

        #Timeline
        st.title("Monthly timeline")
        timeline=helper.monthly_timeline(selected_list,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_list, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity Map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.title("Most busy day")
            busy_day = helper.week_activity_map(selected_list, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            # ax.plot(busy_day['day_name'], busy_day['count'], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title("Most busy Month")
            month_day = helper.month_activity_map(selected_list, df)
            fig, ax = plt.subplots()
            ax.bar(month_day.index, month_day.values,color='orange')
            #ax.plot(month_day['month'], month_day['count'], color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Daily Timeline
        st.title("Heatmap")
        user_heat = helper.activity_heatmap(selected_list, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heat,ax=ax, cmap='coolwarm')
        st.pyplot(fig)








