from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List, Optional,Type
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from Schemas.extraction_schemas import get_sec_filings

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def EXTRACT(tool,data):
    Extractor = DataExtractorAgent(llm,tool)
    return Extractor.extract(data)

class DataExtractorAgent:
    """extracts structured text from unstructured data using a given pydantic schema"""
    def __init__(self,llm,model):
        self.classes= {"get_sec_filings":get_sec_filings}
        self.model = self.classes[model]
        self.llm = llm.with_structured_output(self.model)
        self.extracts= None
        self.all_extracts = []
        self.prompt = ChatPromptTemplate.from_messages([ 
            ("system", """You are a precise information extraction assistant. 
                Your job is to read text documents and extract structured data according to the provided JSON schema:{schema}.
                Always return output that matches the schema exactly — do not add explanations or commentary."""),
            ("user", "Here is what you Extracted previously:{extracts}, now provide the schema again using your previous extracts and the data from this document using the schema provided. chunk:\n\n{chunk}")
        ])
    
    
    def extract(self, text: str)->List[BaseModel]:
        """Extract structured financial data from a filing chunk"""
        chain = self.prompt | self.llm
        chunks = self.chunking_express(text)
        if len(text) > 500:
            for chunk in chunks:
                self.extracts = chain.invoke({"chunk":chunk,
                                            "extracts":self.extracts,
                                            "schema":self.model.model_json_schema()
                                            })
                self.all_extracts.append(self.extracts)
            return self.extracts
        else :
            self.extracts = chain.invoke({"chunk":chunk,
                                            "extracts":self.extracts,
                                            "schema":self.model.model_json_schema()
                                            })
            return self.extracts

        
       
    def chunking_express(self,doc) ->List[str]:
        """chunks the text and returns a list of texts""" 
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " "]
        )   
        return splitter.split_text(doc)
