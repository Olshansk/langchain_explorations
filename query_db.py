import os

# from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone, VectorStore

from prepare_db import PINECONE_INDEX_NAME, pinecone_db

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # platform.openai.com/account/api-keys
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

TEMPERATURE = 0.7  ## default temperature from langchain source code
MAX_TOKENS = 600  ##
MODEL_NAME = "gpt-4"  ## default model name from langchain source code
CHAIN_TYPE = "stuff"  # one off "map_reduce", "map_rerank", and "refine".

# Hardcoded for vitalik-index
prompt_template = """
Assuming the role, knowledge, and responsibilities of Vitalik Buterin, co-founder of Ethereum, please answer the following question based on your inherent knowledge.
If you don't have the answer, please clearly state that you don't know, rather than guessing or inventing information.
Your response should be concise, clear, and honest, aiming to educate.
If appropriate, have a small sentence followed by bullet points and simple sentences, avoiding jargon whenever possible.

Context: {context}

Question: {question}

Answer:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


# https://python.langchain.com/en/latest/modules/chains/index_examples/vector_db_qa.html
def retrieval_qa(doc_db: VectorStore) -> RetrievalQA:
    chain_type_kwargs = {"prompt": PROMPT}
    llm = ChatOpenAI(
        model_name=MODEL_NAME, temperature=TEMPERATURE, max_tokens=MAX_TOKENS
    )  # ChatGPT
    # llm_openai = OpenAI()

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=CHAIN_TYPE,
        retriever=doc_db.as_retriever(),
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True,
    )

    return qa


def main():
    print(PINECONE_INDEX_NAME)
    doc_db = pinecone_db()
    qa = retrieval_qa(doc_db)

    query = "What are zero knowledge proofs?"
    result = qa({"query": query})

    # doc_db.similarity_search(query)
    # result = qa.run(query)
    print(result)


if __name__ == "__main__":
    main()
