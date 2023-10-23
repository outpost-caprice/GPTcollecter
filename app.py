import streamlit as st
from main import main

st.title('Text Summarization App')

col1, col2 = st.columns(2)

full_texts = []  # このリストに要約を保存します

with col1:
    query = st.text_input('Enter search query')
    num_results = st.number_input('Number of results', min_value=1, max_value=10, value=5)

    if st.button('Search and Summarize'):
        with st.spinner('Processing...'):
            # main関数を呼び出し、結果をfull_textsに保存
            # 注意: main関数がfull_textsを返すように修正する必要があります
            full_texts = main(query, num_results)

with col2:
    st.subheader('Logs')
    # full_textsに保存された要約を表示
    for text in full_texts:
        st.write(text)
