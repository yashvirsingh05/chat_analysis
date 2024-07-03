import streamlit as st
import preprocessor,helper

st.sidebar.title("whatsapp chat")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'OverAll')
    user_list.remove('group_notification')
    selected_list=st.sidebar.selectbox("Show users List",user_list)
    if st.sidebar.button("Show Analysis"):
        num_message,words,num_media_messages=helper.fetch_stats(selected_list,df)
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


