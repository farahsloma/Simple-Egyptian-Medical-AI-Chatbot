from typing import Annotated, Optional
from pydantic import BaseModel
from typing_extensions import TypedDict
from langgraph.graph import add_messages

class State(TypedDict):
    query : str
    rewritten_query : Optional[str]
    messages : Annotated[list,add_messages]
    response : Optional[str]
    content : Optional[list[str]]
    user_web_search : Optional[bool]

class RouteDecision(BaseModel):
    user_web_search : bool