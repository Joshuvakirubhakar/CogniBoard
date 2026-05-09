import os
import logging

import streamlit as st

from langchain_chroma import Chroma

from langchain_ollama import (
    ChatOllama,
    OllamaEmbeddings
)

from langchain_community.document_loaders import (
    Docx2txtLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from assistant import Assistant

from gui import AssistantGUI

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE
)

# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO
)


# =========================================================
# CHATBOT FUNCTION
# =========================================================

def run_chatbot():
    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.title(
        "Lehman Brothers Holdings Inc."
    )

    st.caption(
        "Employee Onboarding Assistant"
    )

    # =====================================================
    # EMPLOYEE DATA
    # =====================================================

    customer_data = (
        st.session_state.get(
            "employee_data",
            {}
        )
    )

    # =====================================================
    # VECTOR STORE
    # =====================================================

    @st.cache_resource(
        ttl=3600,
        show_spinner="Loading Company Policies..."
    )
    def init_vector_store(docx_path):

        try:

            persistent_path = (
                "data/vectorstore"
            )

            # ---------------------------------------------
            # EMBEDDING MODEL
            # ---------------------------------------------

            embedding_function = (
                OllamaEmbeddings(
                    model="nomic-embed-text:latest"
                )
            )

            # ---------------------------------------------
            # LOAD EXISTING DB
            # ---------------------------------------------

            if os.path.exists(
                    persistent_path
            ):
                logging.info(
                    "Loading existing vector store..."
                )

                vectorstore = Chroma(

                    persist_directory=(
                        persistent_path
                    ),

                    embedding_function=(
                        embedding_function
                    )
                )

                return vectorstore

            # ---------------------------------------------
            # CREATE NEW VECTOR STORE
            # ---------------------------------------------

            logging.info(
                "Creating vector store..."
            )

            loader = Docx2txtLoader(
                docx_path
            )

            docs = loader.load()

            logging.info(
                f"Loaded {len(docs)} documents"
            )

            text_splitter = (
                RecursiveCharacterTextSplitter(

                    chunk_size=700,

                    chunk_overlap=100
                )
            )

            splits = (
                text_splitter.split_documents(
                    docs
                )
            )

            logging.info(
                f"Created {len(splits)} chunks"
            )

            vectorstore = (
                Chroma.from_documents(

                    documents=splits,

                    embedding=(
                        embedding_function
                    ),

                    persist_directory=(
                        persistent_path
                    ),
                )
            )

            logging.info(
                "Vector store created successfully"
            )

            return vectorstore

        except Exception as e:

            st.error(
                f"Vector Store Error: {str(e)}"
            )

            return None

    # =====================================================
    # INITIALIZE VECTOR STORE
    # =====================================================

    vector_store = init_vector_store(
        "data/Lehman_Brothers_Policies.docx"
    )

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    if "messages" not in st.session_state:
        st.session_state.messages = [

            {
                "role": "ai",

                "content": (
                    WELCOME_MESSAGE
                )
            }
        ]

    # =====================================================
    # LOCAL MODEL
    # =====================================================

    llm = ChatOllama(

        model="gemma3:4b",

        temperature=0.2,
    )

    # =====================================================
    # ASSISTANT
    # =====================================================

    assistant = Assistant(

        system_prompt=SYSTEM_PROMPT,

        llm=llm,

        message_history=(
            st.session_state.messages
        ),

        employee_information=(
            customer_data
        ),

        vector_store=(
            vector_store
        ),
    )

    # =====================================================
    # GUI
    # =====================================================

    gui = AssistantGUI(
        assistant
    )

    gui.render()
