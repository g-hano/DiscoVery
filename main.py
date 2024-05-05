from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core.memory import ChatMemoryBuffer

from llama_index.llms.anthropic import Anthropic
from tools import PDFExtractor, AskVisionModel, StructuredFileReader, Report

CLAUDE_API_KEY="<ANTROPIC-API-KEY>"
llm = Anthropic(model="claude-3-opus-20240229", # you can change the model
                api_key=CLAUDE_API_KEY)

#llm = Ollama(model="llama3", request_timeout=360)

pdf_tool = FunctionTool.from_defaults(fn=PDFExtractor, name="PDFExtractor", description="""Extracts text and images from a PDF file located at the specified path. This function is designed to process PDF documents 
    comprehensively, capturing both textual and graphical information. Extracted images are automatically saved in a predefined 
    directory ('test') for further analysis.
    """)
askvision_tool = FunctionTool.from_defaults(fn=AskVisionModel, name="AskVisionModel", description="""
    Analyzes images using a multimodal LLM that can interpret visual content. This function processes images previously extracted
    and saved in the 'ExtractedImgs' directory, providing insights and detailed analysis based on the visual data. It is particularly 
    useful for extracting actionable information from images, supporting decision-making processes.
    """)
directory_tool = FunctionTool.from_defaults(fn=StructuredFileReader, name="StructuredFileReader", 
                                            description="""Extracts and analyzes information from structured files based on a specified query. 
                                            This function is adept at processing CSV files and other structured data formats, 
                                            answering questions and extracting specific data points that aid in data-driven analysis.""")
report_tool = FunctionTool.from_defaults(fn=Report, 
                                         name="Report", 
                                         description="""Useful when you are done with analysis and want to save the final version of the report.""")

with open("claude_prompt.txt", "r") as f:
    prompt = f.readlines()

agent = ReActAgent.from_tools(llm=llm,
                               max_iterations = 20,
                               tools=[pdf_tool, askvision_tool, directory_tool, report_tool],
                               verbose=True,
                               memory=ChatMemoryBuffer.from_defaults(llm=llm),
                               chat_history=[
                                   {"role":"system", "content": prompt}])

#text = "I want you to read files provided and create a complete analysis of my company's stats"
text = input("Ask: ")
print(agent.chat(text))