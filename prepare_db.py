import os

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

### API Keys


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # platform.openai.com/account/api-keys
if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

### Data Sources

ALL_PDFS_PATTERN = "**/*.pdf"  # only retrieve PDFs
VITALIK_ARTICLES_DIR = "data/vitalik_articles"

### Constants

CHUNK_SIZE = 1000  # number of characters per chunk
CHUNK_OVERLAP = 0  # number of characters to overlap between chunks
OPEN_AI_EMBEDDING = "text-embedding-ada-002"  # Default embedding from https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
OPEN_AI_EMBEDDING_CTX_LENGTH = 8191  # Default context length from source code


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # app.pinecone.io
PINECONE_ENV = os.getenv(
    "PINECONE_ENV", "us-west4-gcp-free"
)  # next to api key in console
PINECONE_INDEX_NAME = "vitalik-index"  # https://app.pinecone.io/organizations/-NXb73w99AnTOSga21uA/projects/us-west4-gcp-free:5be2215/indexes


def get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model=OPEN_AI_EMBEDDING, embedding_ctx_length=OPEN_AI_EMBEDDING_CTX_LENGTH
    )


def pinecone_init():
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)


def pinecone_db() -> VectorStore:
    pinecone_init()
    return Pinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME, embedding=get_embeddings()
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
def prepare_db(data_source: str, pattern: str) -> VectorStore:
    loader = DirectoryLoader(
        data_source,
        glob=pattern,
        show_progress=True,
    )
    docs = loader.load()
    # print("docs", docs)

    # Split PDFs into chunks (1 chunk = 1 embedding)
    # text_splitter = CharacterTextSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP,
    #     # length_function=len,
    #     # keep_separator=True,
    #     # add_start_index=True,
    # )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[" ", ",", "\n"]
        # length_function=len,
        # keep_separator=True,
        # add_start_index=True,
    )

    docs_split = text_splitter.split_documents(docs)
    # print("Split docs", docs_split)

    embeddings = get_embeddings()
    pinecone_init()
    doc_db = Pinecone.from_documents(
        docs_split, embeddings, index_name=PINECONE_INDEX_NAME
    )
    # print("doc_db", doc_db)
    return doc_db


def main():
    doc_db = prepare_db(VITALIK_ARTICLES_DIR, ALL_PDFS_PATTERN)
    print(f"doc_db for {VITALIK_ARTICLES_DIR} initialized", doc_db)


if __name__ == "__main__":
    main()
