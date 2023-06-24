import os

from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone, VectorStore

from prepare_db import PINECONE_INDEX_NAME, get_embeddings

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # platform.openai.com/account/api-keys
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

TEMPERATURE = 0.7  ## default temperature from langchain source code
MAX_TOKENS = -1  ## default max_token is 256 but -1 allows to set the max
MODEL_NAME = "gpt4"  ## default model name from langchain source code
CHAIN_TYPE = "stuff"  # one off "map_reduce", "map_rerank", and "refine".


def db_from_pinecone() -> VectorStore:
    return Pinecone.from_existing_index(
        index_name=PINECONE_INDEX_NAME, embedding=get_embeddings()
    )


# https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa.html
def retrieval_qa(doc_db: VectorStore) -> RetrievalQA:
    # llm_chat = ChatOpenAI()  # ChatGPT
    llm_openai = OpenAI(
        model_name=MODEL_NAME, temperature=TEMPERATURE, max_tokens=MAX_TOKENS
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm_openai,
        chain_type=CHAIN_TYPE,
        retriever=doc_db.as_retriever(),
    )
    return qa


def main():
    print(PINECONE_INDEX_NAME)
    doc_db = db_from_pinecone()
    qa = retrieval_qa(doc_db)
    query = "What is the most important aspect of crypto?"
    result = qa.run(query)
    # print(result)

    # query = "What were the most important events for Google in 2021?"
    # search_docs = doc_db.similarity_search(query)
    # search_docs


if __name__ == "__main__":
    main()
