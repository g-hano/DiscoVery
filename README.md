# DiscoVery

---

## Introduction
This project introduces an advanced Language Model (LLM) agent designed to understand and analyze company data, inspired by the capabilities seen in IBM's discovery solutions. It can read a variety of file formats and utilizes state-of-the-art local and cloud-based LLMs for data processing and analysis.

## Features
- **Supported File Types:** Handles various file types including CSV, TXT, Excel, PDF, Python scripts, Jupyter notebooks, and Markdown files.
- **Data Extraction:** Capable of extracting text and images from PDFs, utilizing the Llava multimodal LLM for interpreting images, graphs, and charts.
- **Analysis and Output:** Analyzes extracted data and saves the findings in a structured format.
- **Memory and Custom Tools:** Incorporates its own memory system and custom tools tailored for data analysis.

## Installation
Clone the repository:
```bash
git clone https://github.com/g-hano/DiscoVery

```
Install necessary libraries using the provided `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Usage
To start analyzing your data with the model, follow these steps:
```python
from tools import PDFExtractor, AskVisionModel, StructuredFileReader, Report

# Create the Agent
llm = Ollama(model="llama3", request_timeout=360)
pdf_tool = FunctionTool.from_defaults(fn=PDFExtractor)
askvision_tool = FunctionTool.from_defaults(fn=AskVisionModel)
directory_tool = FunctionTool.from_defaults(fn=StructuredFileReader)
report_tool = FunctionTool.from_defaults(fn=Report)

with open("claude_prompt.txt", "r") as f:
    prompt = f.readlines()

agent = ReActAgent.from_tools(llm=llm,
                               tools=[pdf_tool, askvision_tool, directory_tool, report_tool],
                               verbose=True,
                               memory=ChatMemoryBuffer.from_defaults(llm=llm),
                               chat_history=[
                                   {"role":"system", "content": prompt}])
```

## Supported Models
- **Local LLMs:** Support Ollama models, for example META's Llama 3 and Llama 2 models.
- **Anropic Models:** Integration with Anthropic's Claude models for advanced data understanding.

## Model Verbose Example
Below is a verbose example from the model, demonstrating its capabilities in processing and analyzing data from a PDF document:

```
Thought: I need to use a tool to help me answer the question.
Action: 📜 PDFExtractor
Action Input: {'path': 'company_stats.pdf'}
Opened document: company_stats.pdf
Saved image to Extracted/image1_1.png
Saved image to Extracted/image2_1.png
Observation: {'Extracted/image1_1.png': 'Company Profile Document \nCompany Information \nName: Nexus Innovations Inc. Founded: 2012
Location: 450 Tech Valley Way, San Jose, USA Industry: Technology & Software Development CEO: Elizabeth Tran Company Overview Nexus Innovations Inc.
is a pioneering software development company specializing in innovative solutions for the healthcare and education sectors. Since its \ninception in 2012,
Nexus has been at the forefront of integrating artificial intelligence with user-frterfaces to enhance operational efficiency and user engagement.
Mission Statement "To empower sectors with cutting-edge technology that simplifies complexity and enhances dations."
However, to create a complete analysis I still need more specific data on the company's financial performance and market position.

Action: 📁 StructuredFileReader
Action Input: {'question': 'What are the key financial metrics and market share data for Nexus Innovations Inc.?'}
Observation: Error: No files found in Extracted.
Thought: It seems there are no structured data files available to answer the question about financial metrics and market share. I will try using the AskVisionModel tool to see if ract any additional relevant information from the images.

Action: 👁‍🗨 AskVisionModel
Action Input: {'content': "What information in the extracted images relates to the company's financial performance or market position?"}

Loaded image as bytes: Extracted\image1_1.png
Loaded image as bytes: Extracted\image2_1.png
Observation:  The image you've provided is a screenshot of an analytics dashboard for a company.
It includes key performance indicators (KPIs) and financial metrics that can be usess the company's financial performance or market position.

```

## Contributing
Contributions to this project are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
---
