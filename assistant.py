from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.output_parsers import (
    StrOutputParser
)

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)


class Assistant:

    def __init__(
        self,
        system_prompt,
        llm,
        message_history=None,
        vector_store=None,
        employee_information=None,
    ):

        self.system_prompt = system_prompt

        self.llm = llm

        self.messages = (
            message_history or []
        )

        self.vector_store = vector_store

        self.employee_information = (
            employee_information or {}
        )

        self.chain = (
            self._get_conversation_chain()
        )

    # =====================================================
    # GET RESPONSE
    # =====================================================

    def get_response(self, user_input):

        return self.chain.stream(
            user_input
        )

    # =====================================================
    # CLEAN RETRIEVED DOCS
    # =====================================================

    def format_docs(self, docs):

        # ---------------------------------------------
        # ONLY RETURN PAGE CONTENT
        # ---------------------------------------------

        cleaned_docs = []

        for doc in docs:

            cleaned_docs.append(
                doc.page_content
            )

        return "\n\n".join(
            cleaned_docs
        )

    # =====================================================
    # CONVERSATION CHAIN
    # =====================================================

    def _get_conversation_chain(self):

        # =================================================
        # RETRIEVER
        # =================================================

        retriever = (
            self.vector_store.as_retriever(
                search_kwargs={"k": 5}
            )
        )

        # =================================================
        # PROMPT
        # =================================================

        prompt = ChatPromptTemplate.from_messages([

            (
                "system",

                self.system_prompt +

                """

                Employee Information:
                {employee_information}

                Retrieved Company Policies:
                {retrieved_policy_information}

                Instructions:
                - Answer professionally.
                - Use retrieved policies when relevant.
                - Do NOT mention vector IDs, UUIDs,
                  metadata IDs, chunk IDs, or source hashes.
                - Never expose internal retrieval details.
                - Be concise unless detailed explanation
                  is requested.
                """
            ),

            MessagesPlaceholder(
                variable_name="conversation_history"
            ),

            (
                "human",
                "{user_input}"
            ),
        ])

        # =================================================
        # OUTPUT PARSER
        # =================================================

        output_parser = (
            StrOutputParser()
        )

        # =================================================
        # CHAIN
        # =================================================

        chain = (

            {
                "retrieved_policy_information":

                    retriever
                    | RunnableLambda(
                        self.format_docs
                    ),

                "employee_information":

                    lambda x: (
                        self.employee_information
                    ),

                "user_input":

                    RunnablePassthrough(),

                "conversation_history":

                    lambda x: self.messages,
            }

            | prompt

            | self.llm

            | output_parser
        )

        return chain