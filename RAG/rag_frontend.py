import streamlit as st
import rag_backend as rag

st.set_page_config(page_title="Biblio Search")

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">Biblio Search </p>'
st.markdown(new_title, unsafe_allow_html=True)

if 'vector_index' not in st.session_state:
    with st.spinner("Indexing document..."):
        st.session_state.vector_index = rag.rag_index()

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")

if go_button:
    with st.spinner("Searching document..."):
        response = rag.rag_response(question=input_text, index=st.session_state.vector_index)
        st.write(response)