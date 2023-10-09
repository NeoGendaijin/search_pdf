# Paper Downloader from ArXiv

This tool allows you to search for academic papers based on a query and download relevant papers from ArXiv in an automated manner. It uses a combination of Semantic Scholar for paper search and GPT-3 for query formulation and paper reranking to provide a list of relevant papers, which are then downloaded from ArXiv.

## Prerequisites

Ensure you have the following API keys:
- OpenAI API Key: For using GPT-3. Obtain it from [OpenAI Platform](https://beta.openai.com/signup/).
- Semantic Scholar API Key: For fetching paper details. Obtain it from [Semantic Scholar](https://www.semanticscholar.org/).

Store your API keys in `api_keys.json` in the following format:

```api_keys.json
{
    "openai": "your_openai_api_key",
    "semanticscholar": "your_semanticscholar_api_key"
}
```

## Installation

1. Clone this repository:
   ```sh
   git clone [your_repository_link]
   ```
2. Navigate to the project directory:
   ```sh
   cd [your_directory_name]
   ```
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## How to Use

Here's a quick start example on how to use this tool:

```quick_start.py
from src.main import download_relevent_papers

# How to use
your_question = "What is the best prompt to enhance LLM's math ability?"
save_dir = "./pdfs"
download_relevent_papers(your_question, save_dir=save_dir)
```

Replace `your_question` with the query for which you want to find and download papers. The papers will be downloaded to the directory specified in `save_dir`.

## Dependencies

- requests
- shutil
- os
- json
- openai
- sentence-transformers
- transformers
- faiss