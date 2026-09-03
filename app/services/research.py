from typing import Tuple, List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.config import settings
from app.core.llm import get_llm
from app.tools.web_search import web_search_tool

class ResearchService:
    def __init__(self):
        # 1. Initialize the base LLM via factory
        # We need to extract the tool object
        self.web_search_tool = web_search_tool
        self.tools = [self.web_search_tool]
        
        # We bind the tools to the LLM directly via factory
        self.llm_with_tools = get_llm(tools=self.tools)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an intelligent research assistant. 
You have access to a web search tool. If the user's question requires up-to-date information, use the tool.
Otherwise, answer directly. Always cite your sources if you use the tool."""),
            ("placeholder", "{messages}")
        ])
        
        self.chain = self.prompt_template | self.llm_with_tools
        
    def research(self, question: str) -> Tuple[str, List[Dict[str, Any]]]:
        messages = [HumanMessage(content=question)]
        sources = []
        
        # 1. Initial LLM invocation
        response = self.chain.invoke({"messages": messages})
        messages.append(response)
        
        # 2. Check if LLM wants to call a tool (allow up to 3 tool calls)
        iterations = 0
        while response.tool_calls and iterations < 3:
            iterations += 1
            for tool_call in response.tool_calls:
                if tool_call["name"] == "web_search":
                    # Execute the tool
                    query = tool_call["args"]["query"]
                    try:
                        tool_result = web_search_tool.invoke({"query": query})
                        sources.extend(tool_result)
                        # The LLM needs the result back as a string for context
                        tool_msg_content = str(tool_result)
                    except Exception as e:
                        tool_msg_content = f"Error executing search: {str(e)}"
                    
                    # Add tool response to messages
                    messages.append(ToolMessage(
                        name=tool_call["name"],
                        content=tool_msg_content,
                        tool_call_id=tool_call["id"]
                    ))
            
            # Call LLM again with the tool results
            response = self.chain.invoke({"messages": messages})
            messages.append(response)
            
        answer = response.content
        # If no tools were called, just return the direct response
        answer = response.content
        if isinstance(answer, list) and len(answer) > 0 and isinstance(answer[0], dict):
            answer = answer[0].get("text", str(answer))
        elif isinstance(answer, list):
            answer = str(answer)
            
        return answer, sources
