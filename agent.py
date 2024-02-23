from langchain.agents import Tool, ConversationalChatAgent, AgentExecutor

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from tools.QnA import create_vector_db_tool

from utils import is_answer_formatted_in_json, output_response, _parse_source_docs
import os
import streamlit as st

from dotenv import load_dotenv

load_dotenv()
os.environ['OPENAI_API_KEY'] = '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'

CHAT_MODEL = 'gpt-3.5-turbo'
class Agent:

    def __init__(self, option):
        self.llm = ChatOpenAI(temperature=0, model_name=CHAT_MODEL, api_key=os.getenv('OPENAI_API_KEY'))
        self.agent_executor = self.create_agent_executor(option)

    def create_agent_executor(self, option):
        q_and_a_tool = create_vector_db_tool(option, llm=self.llm)
        tools = [
            Tool(
                name="Disability Services Office QA",
                return_direct=True,
                func=lambda query: _parse_source_docs(q_and_a_tool, query),
                description="useful for when you need to answer questions about DSO"
            )
        ]
        memory = ConversationBufferWindowMemory(llm=self.llm, k=10, memory_key="chat_history", return_messages=True,
                                                human_prefix="user", ai_prefix="assistant", input_key="input")
        custom_agent = ConversationalChatAgent.from_llm_and_tools(llm=self.llm,
                                                                  tools=tools,
                                                                  verbose=True,
                                                                  max_iterations=3,
                                                                  handle_parsing_errors=True,
                                                                  memory=memory,
                                                                  input_variables=["input", "chat_history",
                                                                                   "agent_scratchpad"],
                                                                  system_message=
                                                                  f"""
                                                                  Have a conversation with a human, answering the 
                                                                  following as best you can and try to use a tool to help. 
                                                                  You have access to the following tools: 
                                                                  Disability Services Office QA-useful for when you need to answer
                                                                  questions about Disability Services Office at UW. If you don't know the 
                                                                  answer don't make one up, just say "Hmm, I'm not sure 
                                                                  please contact dso@uw.edu for further assistance."
                                                                  """
                                                                  )
        return AgentExecutor.from_agent_and_tools(agent=custom_agent, tools=tools, memory=memory,
                                                  verbose=True)

    def query_agent(self, user_input):
        try:
            response = self.agent_executor.run(input=user_input)
            if is_answer_formatted_in_json(response):
                return response
            return f"""
            {{
                "result": "{response}"
            }}"""

        except ValueError as e:
            response = str(e)
            response_prefix = "Could not parse LLM output: `\nAI: "
            if not response.startswith(response_prefix):
                raise e
            response_suffix = "`"
            if response.startswith(response_prefix):
                response = response[len(response_prefix):]
            if response.endswith(response_suffix):
                response = response[:-len(response_suffix)]
            output_response(response)
            return response



