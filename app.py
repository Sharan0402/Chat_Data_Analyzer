import streamlit as st
import matplotlib.pyplot as plt
import preprocessor,helper
import seaborn as sns
st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    #Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("Show analysis w.r.t",user_list)

    if st.sidebar.button("Show Analysis"):
        #Stats area
        st.title("Top Statistics")
        num_messages,total_words, num_media_msg, len_links= helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(total_words)
        with col3:
            st.header("#Media Shared")
            st.title(num_media_msg)

        with col4:
            st.header("#Links Shared")
            st.title(len_links)

        #TIME LINE

        #Monthly TImeline
        st.title('Monthly Timeline')
        timeline = helper.monthy_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = 'black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig , ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        # finding the most active user in the group(Not for single user)
        if selected_user == 'Overall':
            st.title("Most Active users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()



            col1,col2 = st.columns(2)
            with col1:
                plt.xticks(rotation='vertical')
                ax.bar(x.index, x.values, color='red')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        most_common_df = helper.most_common_words(selected_user,df)
        st.title("Most common words")
        fig, ax = plt.subplots()
        plt.xticks(rotation='vertical')
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        #Emoji analysis
        st.title("Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user,df)

        col1 , col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            if(emoji_df.empty):
                st.write("No emojis used")
            else:
                plt.xlabel('Emoji')
                plt.ylabel('# of occurances')
                ax.bar(emoji_df[0].head(),emoji_df[1].head(),color='green')
                st.pyplot(fig)
