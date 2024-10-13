import streamlit as st
from skrapy import scrapeWeb, cleanBody, splitDomContent
from llm import parseLocal

st.title('skrapy')
url = st.text_input('URL: ')

if st.button('Scrape site'):
    st.write(f'Scraping {url}...')

    content = scrapeWeb(url)
    content = cleanBody(content)
    
    st.session_state.dom_content = content
    
    with st.expander("View DOM Content"):
        st.text_area('DOM Content', content, height=400)

if "dom_content" in st.session_state:
    prompt = st.text_area('Prompt: ')

    if st.button('Parse'):
        if prompt:
            st.write('Parsing...')
            
            dom_list = splitDomContent(st.session_state.dom_content)
            result = parseLocal(dom_list, prompt)
            st.write(result)