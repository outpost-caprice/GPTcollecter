import streamlit as st
import asyncio
from main import main  # main関数をインポート
from ErrorLogger import ErrorLogger, LogLevel

logger = ErrorLogger(log_file="streamlit_app_errors.log", log_level=LogLevel.INFO)

st.title("Web Search and Summarize App")

# 検索ワードと検索数の入力
query = st.text_input("Enter the search query:", "Example Query")
num_results = st.number_input("Number of results to fetch:", min_value=1, max_value=50, value=10)

# 検索ボタン
if st.button("Search and Summarize"):
    st.write("Starting the search...")

    progress_bar = st.progress(0)
    status_message = st.empty()

    try:
        # 非同期関数を同期的に呼び出す
        loop = asyncio.get_event_loop()
        summaries = loop.run_until_complete(main(query, num_results))

        for i, (url, summary) in enumerate(summaries):
            if summary is not None:
                st.write(f"### Summary for {url}")
                st.write(summary)
            else:
                st.write(f"### No summary available for {url}")

            progress_bar.progress((i + 1) / len(summaries))

        status_message.write("Search and summarization completed.")

    except Exception as e:
        logger.log(f"An error occurred: {e}", LogLevel.ERROR)
        status_message.write(f"An error occurred: {e}")

