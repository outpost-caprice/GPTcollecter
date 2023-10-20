
import streamlit as st
from main import main

st.title('Text Summarization App')

col1, col2 = st.columns(2)

with col1:
  query = st.text_input('Enter search query')
  num_results = st.number_input('Number of results', min_value=1, max_value=10, value=5)
  
  if st.button('Search and Summarize'):
    with st.spinner('Processing...'):
      full_texts = main(query, num_results)

with col2:  
  st.subheader('Logs')
  for text in full_texts:
    st.write(text)