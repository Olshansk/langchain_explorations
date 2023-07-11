import os

import streamlit as st
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSerperAPIWrapper

from query_db import pinecone_db, retrieval_qa

PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_INDEX_NAME = st.secrets["PINECONE_INDEX_NAME"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

with st.sidebar:
    if PINECONE_API_KEY:
        pinecone_api_key = st.text_input(
            "Pinecone API Key",
            key="langchain_search_api_key_pinecone",
            value="ALREADY SET VIA ENV",
        )
    else:
        pinecone_api_key = st.text_input(
            "Pinecone API Key", key="langchain_search_api_key_pinecone"
        )
    if OPENAI_API_KEY:
        openai_api_key = st.text_input(
            "OpenAI API Key",
            key="openai_key",
            value="ALREADY SET VIA ENV",
        )
    else:
        openai_api_key = st.text_input("OpenAI API Key", key="openai_key")
    "[View the source code](https://github.com/Olshansk/langchain_explorations)"

st.title(f"❓ AMA w/ index: {PINECONE_INDEX_NAME} 🧑‍🎓")
question = st.text_input(
    # "What would you like to know?", placeholder="What are zero knowledge proofs?"
    "What would you like to know?",
    placeholder="What data would you like to retrieve from your index?",
)

if question:
    if not pinecone_api_key and not openai_api_key:
        st.info("Please add your Pinecone and OpenAI API keys to continue.")
    elif not pinecone_api_key:
        st.info("Please add your Pinecone API key to continue.")
    elif not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif pinecone_api_key and openai_api_key:
        os.environ["OPENAI_API_KEY"] = (
            OPENAI_API_KEY if OPENAI_API_KEY else openai_api_key
        )
        os.environ["PINECONE_API_KEY"] = (
            PINECONE_API_KEY if PINECONE_API_KEY else pinecone_api_key
        )
        doc_db = pinecone_db(PINECONE_INDEX_NAME)
        qa = retrieval_qa(doc_db)
        result = qa({"query": question})
        st.header("Answer")
        st.write(result["result"])
        st.subheader("Source Documents")
        st.text(
            "Click to expand each file to see the most relevant info we found in that document."
        )
        for doc in result["source_documents"]:
            with st.expander(doc.metadata["source"]):
                st.write(doc.page_content)
                # st.image("https://static.streamlit.io/examples/dice.jpg")


# TODO: Improve this in the future
# st.write("### Answer")
# st.write(result)

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
#         llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.secrets.openai_api_key)
# search = GoogleSerperAPIWrapper(serper_api_key=pinecone_api_key)
#         search = GoogleSerperAPIWrapper(serper_api_key=st.secrets.serper_api_key)
# search_tool = Tool(
#     name="Intermediate Answer",
#     func=search.run,
#     description="useful for when you need to ask with search",
# )
# search_agent = initialize_agent(
#     [search_tool],
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
# )
# response = search_agent.run(question)
# st.write("### Answer")
# st.write(response)
