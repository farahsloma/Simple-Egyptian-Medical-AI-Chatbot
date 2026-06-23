import streamlit as st
from models import State
from workflow import WorkFlow
from dotenv import load_dotenv
load_dotenv()

st.title('Gen AI Assistant')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'workflow' not in st.session_state:
    st.session_state.workflow = WorkFlow()

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

query = st.chat_input('Ask any question about Egyptain Medical')

if query:
    st.session_state.messages.append({'role':'user','content':query})
    with st.chat_message('user'):
        st.write(query)
    with st.chat_message('assistant'):
        with st.spinner('thinking....'):
            intial_state = State({
                'query' : 'give me 4 exmples about egyptian medical',
                'messages':[],
                'content':None,
                'response':None,
                'rewritten_query':None,
                'user_web_search' : None
            })
        result = st.session_state.workflow.run(intial_state)
        responce = result.get('response')
        source = 'Web Search' if result.get('user_web_search') else 'knowledge base'
        st.caption(f'source : {source}')
        st.write(responce)
    st.session_state.messages.append({'role' : 'assistant','content':responce})

