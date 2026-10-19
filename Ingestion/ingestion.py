import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings

from Ingestion.pdf2markdown import PDFToMarkdownConverter
from Ingestion.semanticchunker import SemanticChunker
