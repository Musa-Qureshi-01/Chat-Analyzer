import streamlit as st

import seaborn as sns
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.set_page_config(
    page_title="Chat Analyzer by Ⓜ️",  # This is the website name in the browser tab
    page_icon="📈",                  # This is the favicon (can be emoji or image file)
    layout="wide"
)

st.sidebar.title('Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

st.title("Chat Analyzer 🗨️ - Currently for Whatsapp")
st.write("""
Welcome to the Chat Analyzer!  

Easily upload and explore your chat data to uncover valuable insights —  
like activity patterns, most active hours, frequent contacts, and more.  

Dive into detailed visualizations and summaries to understand your conversations better.  

Get started by uploading your chat file below!
""")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(bytes_data)
    df = preprocessor.preprocess(data)

    if st.button("📊 Show Dataset", use_container_width=True):
        st.dataframe(df)
        st.subheader('To return to the Analysis page , simply click the [ Show Analysis Results ]  button again. ')
        st.subheader('\n Thank you for exploring our Chat Analyzer! 🚀📊')


    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt',user_list)

    if st.sidebar.button('Show Analysis Results'):

        num_message, words, num_media_msg, links  = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_message)
        with col2:
            st.header('Total Words')
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_msg)
        with col4:
            st.header('Links Shared')
            st.title(links)

        # Month TimeLine
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(timeline['time'], timeline['message'], color='skyblue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig, use_container_width=True)

        # Daily Timeline
        st.title('Daily Timeline')
        daily_time = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(daily_time['only_date'], daily_time['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig, use_container_width=True)

        # ACticity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most Busy Days')
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation=45, ha='right')
            ax.bar(busy_day.index, busy_day.values, color='skyblue', edgecolor='black')
            st.pyplot(fig)

        with col2:
            st.header('Most Busy Months')
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation=45, ha='right')
            ax.bar(busy_month.index, busy_month.values, color='skyblue', edgecolor='black')
            st.pyplot(fig)

        # Heatmap
        st.title('Weekly Activity Map')
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, cmap='inferno')
        st.pyplot(fig)


        # finding the busiest user in the Group
        if selected_user == 'Overall':
            st.title('Most Busy User')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2, = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='skyblue', edgecolor='black')
                plt.xticks(rotation=45, ha='right')
                ax.set_title("Most Busy Users", fontsize=14, fontweight="bold")
                ax.set_ylabel("Message Count")
                ax.set_xlabel("Users")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        # Word Cloud
        st.title('Most Common Messages - WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")  # Cleaner look
        st.pyplot(fig)

        # Most Common words
        st.title('Most Common Words')
        col1, col2 = st.columns(2)

        with col1:
            most_common_df = helper.most_common_words(selected_user, df)

            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color="skyblue", edgecolor="black")

            ax.set_xlabel("Count")
            ax.set_ylabel("Word")
            ax.set_title("Most Common Words")
            ax.invert_yaxis()  # most common on top

            st.pyplot(fig)

        with col2:
            most_common_df = helper.most_common_words(selected_user, df)
            st.dataframe(most_common_df)

        # Emoji Analysis
        emoji_df = helper.emojis_helper(selected_user, df)
        st.title('Emoji Analysis')

        col1, col2, col3 = st.columns(3)
        # with col1:
        #     # Keep only the top 10 emojis
        #     top_emojis = emoji_df.head(10)
        #
        #     fig, ax = plt.subplots()
        #     ax.barh(top_emojis[0], top_emojis[1], color="skyblue", edgecolor="black")
        #     ax.set_xlabel("Count")
        #     ax.set_ylabel("Emoji")
        #     ax.set_title("Top 10 Emojis Used")
        #
        #     # Invert y-axis so the most used emoji is at the top
        #     ax.invert_yaxis()
        #
        #     plt.tight_layout()
        #     st.pyplot(fig)
        with col3:
            # Keep only the top 10 emojis
            top_emojis = emoji_df.head(10)
            top_emojis.columns = ["Emoji", "Count"]

            fig = px.bar(
                top_emojis,
                x="Count",
                y="Emoji",
                orientation="h",
                text="Count",
                color_discrete_sequence=["skyblue"]
            )
            fig.update_layout(
                title="Top 10 Emojis Used",
                yaxis=dict(autorange="reversed"),
            )
            st.plotly_chart(fig, use_container_width=True, key="emoji_bar_chart")

        with col2:
            top_emojis = emoji_df.head(7)
            top_emojis.columns = ["Emoji", "Count"]

            fig = px.pie(
                top_emojis,
                names="Emoji",
                values="Count",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )

            fig.update_traces(textinfo="percent")

            st.plotly_chart(fig, use_container_width=True, key="emoji_pie_chart")

        with col1:
            st.dataframe(emoji_df)




# Excel file path
EXCEL_FILE = "contact_form_data.xlsx"

# Function to save form data to Excel
def save_to_excel(name, email, message):
    new_data = pd.DataFrame([[name, email, message]], columns=["Name", "Email", "Message"])

    if os.path.exists(EXCEL_FILE):
        existing_data = pd.read_excel(EXCEL_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_excel(EXCEL_FILE, index=False)

st.subheader("📬 Contact Us")

with st.form(key='contact_form'):
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    if not name or not email or not message:
        st.warning("⚠️ Please fill in all fields")
    else:
        save_to_excel(name, email, message)
        st.success("✅ Your message was saved successfully to Excel!")

st.markdown("---")  # horizontal line
st.markdown(
    "<p style='text-align: center; color: gray;'>💖 Thank you for using Chat Analyzer — you're amazing! 🌟</p>",
    unsafe_allow_html=True
)