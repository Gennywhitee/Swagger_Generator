from langchain_openai import ChatOpenAI
from langchain.runnables import hub
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from main import text_from_file, out_on_file

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults, Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages

load_dotenv()
url = "https://swagger.io/docs/specification"

file_out = ".\\output\\User_feed_agent.yml"
filepath = ".\\input\\User_feed.java"
text = text_from_file(filepath)

ddg_search = DuckDuckGoSearchResults()

# Creazione di un nuovo Tool utile per la ricerca
duckapi_tool = Tool(
    name="Search",
    func=ddg_search.run,
    description="useful for when you need to answer questions about current events",
)

# Defining Headers for Web Requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Mobile Safari/537.36'
}

# Parsing HTML Content
def parse_html(content) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    text_content_with_links = soup.get_text()
    return text_content_with_links

# Fetching Web Page Content
def fetch_web_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    return parse_html(response.content)


web_fetch_tool = Tool.from_function(
    func=fetch_web_page,
    name="WebFetcher",
    description="Fetches the content of a web page"
)

# Use the appropriate function to create the summarizer
prompt_template = "Summarize the following content: {content}"
model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate.from_template(prompt_template)

llm_chain = prompt | model 

def summarize_content(content: str) -> str:
    return llm_chain.invoke({"content": content})

summarize_tool = Tool.from_function(
    func=summarize_content,
    name="Summarizer",
    description="Summarizes a web page"
)

tools = [duckapi_tool, web_fetch_tool, summarize_tool]



prompt = ChatPromptTemplate.from_template("Utilizzando se necessario i tool che hai a disposizione per cercare come creare uno Swagger che segue lo standard OPENAI 3.0."
                                          "Successivamente creami la documentazione dello Swagger, con annesse tutte le operazioni CRUD in maniera tale che possano essere richiamate come API RESTfull,"
                                          "della seguente classe Entity: {text}. Non scrivere altri commenti.")


llm_with_tools = model.bind_tools(tools)

output_parser = StrOutputParser()

chain = prompt | llm_with_tools



# Run the agent and output the result to a file
result = chain.invoke({"text": text})

out_on_file(result, file_out)
