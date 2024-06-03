from langchain_openai import ChatOpenAI
from langchain import hub
from dotenv import load_dotenv
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from main import text_from_file
from langchain_community.tools import DuckDuckGoSearchRun


load_dotenv()
model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.7)

filepath = ".\\input\\Biblioteca.java"
text = text_from_file(filepath)

message = [
   SystemMessage(
      content = "A user will give you a class in java, you will output a .yaml file with the class swagger written on it"
   ),
   HumanMessage(
      content="{text}"
   ),
]



search = DuckDuckGoSearchRun()
print(search.run(message))
"""
tools = [search]
agent = create_openai_functions_agent(llm=model,tools= tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent,tools=tools, verbose=True)
agent_executor.invoke({})
"""
