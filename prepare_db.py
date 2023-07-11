import os
import sys

import pinecone

# So many different loader types!
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings

# See this for a discussion on the different splitters: https://github.com/hwchase17/langchain/discussions/3786
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
    TokenTextSplitter,
)
from langchain.vectorstores import Pinecone, VectorStore

### OpenAI API Keys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # platform.openai.com/account/api-keys
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# TODO: Improve in the future by using getpass
# os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

## Pinecone API Keys

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # app.pinecone.io
PINECONE_ENV = os.getenv(
    "PINECONE_ENV", "us-west4-gcp-free"
)  # next to api key in console


### Data Sources

# TODO: Extend to non pdf files in the future as well
ALL_PDFS_PATTERN = "**/*.pdf"  # only retrieve PDFs

### Constants

CHUNK_SIZE = 1000  # number of characters per chunk
CHUNK_OVERLAP = 0  # number of characters to overlap between chunks
OPEN_AI_EMBEDDING = "text-embedding-ada-002"  # Default embedding from https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
OPEN_AI_EMBEDDING_CTX_LENGTH = 8191  # Default context length from source code


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=OPEN_AI_EMBEDDING, embedding_ctx_length=OPEN_AI_EMBEDDING_CTX_LENGTH
    )


def pinecone_init():
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)


def pinecone_db(index_name) -> VectorStore:
    pinecone_init()
    return Pinecone.from_existing_index(
        index_name=index_name, embedding=get_embeddings()
    )


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=OPEN_AI_EMBEDDING, embedding_ctx_length=OPEN_AI_EMBEDDING_CTX_LENGTH
    )


# 1. Load documents from a directory matching the pattern provided
# 2. Split documents into chunks
# 3. Create embeddings for each chunk
# 4. Create a Pinecone index from the embeddings
# 5. Return the Pinecone index db
def prepare_db(data_source: str, index_name: str, pattern: str) -> VectorStore:
    loader = DirectoryLoader(
        data_source,
        glob=pattern,
        show_progress=True,
    )
    docs = loader.load()

    # Split PDFs into chunks (1 chunk = 1 embedding)
    # TODO: Investigate the difference between this and RecursiveCharacterTextSplitter
    # text_splitter = CharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP,
    #     # length_function=len,
    #     # keep_separator=True,
    #     # add_start_index=True,
    # )

    # Split PDFs into chunks (1 chunk = 1 embedding)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[" ", ",", "\n"]
        # length_function=len,
        # keep_separator=True,
        # add_start_index=True,
    )

    docs_split = text_splitter.split_documents(docs)

    embeddings = get_embeddings()
    pinecone_init()
    doc_db = Pinecone.from_documents(docs_split, embeddings, index_name=index_name)
    return doc_db


def main(datadir, index_name):
    print("args", datadir, index_name)
    doc_db = prepare_db(datadir, index_name, ALL_PDFS_PATTERN)
    print(f"doc_db for {datadir} initialized at index {index_name}", doc_db)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python prepare_db.py <data_source> <pattern>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
