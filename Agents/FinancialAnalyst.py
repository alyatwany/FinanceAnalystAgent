from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder
from Agents.DataCollectorAgent import DataCollectorAgent
from tools.valuation_tools import calculate_dcf,calculate_ddm,calculate_comparable_valuation
from tools.stock_data import get_complete_stock_info


llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)

class FinancialAnalyst():
    def __init__(self):
        self.tools=[use_data_collector_agent,
                    calculate_dcf,calculate_ddm,
                    calculate_comparable_valuation,
                    get_complete_stock_info]

        self.prompt = ChatPromptTemplate.from_messages([
                ("system","You are a Data Collector for a Financial Analyst"),
                MessagesPlaceholder(variable_name="chat history"),
                ("human","{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ])
        self.agent = create_openai_functions_agent(llm,self.tools)
        
        self.memory = ConversationBufferMemory(memory_key="chat_history",
                                               return_messages = True)

        self.executor = AgentExecutor(self.agent,
                                      tools=self.tools,
                                      max_iter=5,
                                      verbose=True)

        def run(self,query):
            return self.executor.invoke({input:query})
        
@tool 
def use_data_collector_agent(query:str)->str:
    """Use DataCollectorAgent to retrieve structured data about a company/stock/ticker.
    
    Examples:
    - "Get the latest 10-K for Apple"
    - "What's the current stock price for MSFT?"
    - "Get news sentiment for TSLA"
    """
    DataCollector = DataCollectorAgent()
    return DataCollector.run(query)


     
    