from models import *
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from promots import * 
from langchain_tavily import TavilyResearch
import os
load_dotenv()
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.0,api_key=os.getenv('OPENAI_API_KEY'), base_url="https://openrouter.ai/api/v1")
embedding = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2') 
vdb = Chroma(persist_directory='gen-ai',embedding_function=embedding)
def reweitten_query_agent(state : State):
    query = state.get('query')
    chat_history = state.get('messages')
    messages = [SystemMessage(content=REWRITE_PROMPT),
                HumanMessage(query_rewrite_extend(query,chat_history))]
    try :
        responce = llm.invoke(messages)
        reweitten_query = responce.content

        return{
            'rewritten_query' : reweitten_query
        }
    except Exception as e:
        print(f'Error in rewritten_query : {e}')
        return None

def reterivel_agent(state : State)->dict:
    rewritten_query = state.get('rewritten_query')
    retrever = vdb.as_retriever(search_kwargs = {'k':10})
    results = retrever.invoke(rewritten_query)
    return{
        'content' : results
    }

def responce_agent(state: State)-> str:
    rewritten_query = state.get('rewritten_query')
    content = state.get('content')
    chat_history = state.get('messages')
    message = [SystemMessage(content=SYSTEM_PROMPT),
               HumanMessage(system_prompt_extend(rewritten_query,chat_history,content))]
    try : 
        responce = llm.invoke(message)
        answer = responce.content
        return{
            'response' : answer
        }
    except Exception as e:
        print(f'Error in responce_agent : {e}')
        return None
router = llm.with_structured_output(RouteDecision)
def router_agent(state:State):
    query = state.get('rewritten_query') or state.get('query')
    message = [SystemMessage(content='you are a router for Egyptian medical knowlage base'
                             'Set user_web_search = true if the query asks about recent medical , modern medical or anything changes frequently'
                             'Set user_web_search = false if the query asks about Eyptian medical or old Egyptian treatment '),
                             HumanMessage(content=query)]
    result :RouteDecision = router.invoke(message)
    return{
        'user_web_search' : result.user_web_search
    }


def tavily_search_agent(state: State):
    query = state.get('rewritten_query')
    tool= TavilyResearch(max_result = 4)
    result = tool.invoke(query)
    return{
        'content' : result
    }
