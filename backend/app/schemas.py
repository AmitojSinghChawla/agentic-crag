from typing import Annotated, Literal, TypedDict
from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AppState(TypedDict):
    message: Annotated[list[AnyMessage], add_messages]
    session_id : str
    has_docs : strrou