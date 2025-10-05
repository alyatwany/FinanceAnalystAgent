import yfinance as yf
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from  yahooquery import Ticker
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from DataExtraction.DataExtractor import DataExtractorAgent
from langchain.memory import ConversationBufferMemory
from tools.sec_filings import get_sec_filings
from tools.news_sentiment import get_all_news
from tools.stock_data import get_stock_data


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

class DataCollectorAgent:
    def __init__(self):
        self.tools = [get_stock_data
                      ,get_all_news,
                      get_sec_filings,
                      get_financial_ratios]
        
        self.prompt = ChatPromptTemplate.from_messages([
                ("system","You are a Data Collector for a Financial Analyst"),
                MessagesPlaceholder(variable_name="chat history"),
                ("human","{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
        self.agent = create_openai_functions_agent(llm,
                                                   self.tools)
        self.memory = ConversationBufferMemory(memory_key="chat_history",
                                               return_messages=True)
        self.executor = AgentExecutor(self.agent,
                                      tools=self.tools,
                                      max_iter = 5,
                                      verbose = True,
                                      memory=self.memory)

    def run(self,query):
        return self.executor.invoke({input:query})        


@tool
def get_financial_ratios(ticker: str) -> dict:
    """fetch key financial ratios for a stock ticker."""
    t = Ticker(ticker)
    ratios = t.key_stats 
    if not ratios:
        return {"error": "No data found for ticker"}
    
    important_ratios = {
        "pe_ratio": ratios.get("trailingPE"),
        "pb_ratio": ratios.get("priceToBook"),
        "roe": ratios.get("returnOnEquity"),
        "current_ratio": ratios.get("currentRatio"),
        "debt_to_equity": ratios.get("debtToEquity")
    }
    return important_ratios

