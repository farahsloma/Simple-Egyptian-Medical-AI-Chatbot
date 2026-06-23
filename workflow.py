from langgraph.graph import START,END,StateGraph
from agents import *
from models import State

def route_decision(state:State)->str:
    return 'tavily_search' if state.get('user_web_search') else 'retrival_agent'


class WorkFlow:
    def __init__(self):
        self.rewritten_agent = reweitten_query_agent
        self.responce_agent = responce_agent
        self.retrival_agent = reterivel_agent
        self.tavily_search = tavily_search_agent
        self.router = router_agent
    def bulid_model(self):
        graph = StateGraph(State)

        graph.add_node('rewritten_query',self.rewritten_agent)
        graph.add_node('responce_agent' , self.responce_agent)
        graph.add_node('retrival_agent',self.retrival_agent)
        graph.add_node('tavily_search',self.tavily_search)
        graph.add_node('router',self.router)

        graph.add_edge(START,'rewritten_query')
        graph.add_edge('rewritten_query','router')
        graph.add_conditional_edges('router',route_decision,{
            'retrival_agent' :'retrival_agent',
            'tavily_search' : 'tavily_search'

        })
        graph.add_edge('retrival_agent','responce_agent')
        graph.add_edge('tavily_search','responce_agent')
        graph.add_edge('responce_agent',END)
        return graph.compile()

    def run(self , initial_state :State):
        graph = self.bulid_model()
        results = graph.invoke(initial_state)
        return results

