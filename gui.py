import streamlit as st
from sqlalchemy import true

from sidebar import render_employee_profile


class AssistantGUI:

    def __init__(self, assistant):

        self.assistant = assistant

        self.messages = assistant.messages

        self.employee_information = (
            assistant.employee_information
        )

    # =====================================================
    # GET RESPONSE
    # =====================================================

    def get_response(self, user_input):

        return self.assistant.get_response(
            user_input
        )

    # =====================================================
    # RENDER CHAT MESSAGES
    # =====================================================

    def render_messages(self):

        for message in self.messages:

            role = message.get(
                "role",
                ""
            )

            content = message.get(
                "content",
                ""
            )

            if role == "user":

                with st.chat_message("human"):

                    st.markdown(content)

            elif role == "ai":

                with st.chat_message("ai"):

                    st.markdown(content)

    # =====================================================
    # SAVE SESSION STATE
    # =====================================================

    def set_state(self, key, value):

        st.session_state[key] = value

    # =====================================================
    # USER INPUT
    # =====================================================

    def render_user_input(self):

        user_input = st.chat_input(
            "Type here...",
            key="chat_input"
        )

        if (
            user_input
            and
            user_input.strip() != ""
        ):

            # ---------------------------------------------
            # USER MESSAGE
            # ---------------------------------------------

            with st.chat_message("human"):

                st.markdown(user_input)

            # ---------------------------------------------
            # AI RESPONSE
            # ---------------------------------------------

            with st.chat_message("ai"):

                with st.status("Fetching Response...", expanded=True):

                    response_generator = (
                        self.get_response(user_input)
                    )

                    response = st.write_stream(
                        response_generator
                    )

            # ---------------------------------------------
            # SAVE HISTORY
            # ---------------------------------------------

            self.messages.append({

                "role": "user",

                "content": user_input
            })

            self.messages.append({

                "role": "ai",

                "content": response
            })

            self.set_state(
                "messages",
                self.messages
            )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self):

        with st.sidebar:

            # =============================================
            # COMPANY LOGO
            # =============================================

            st.markdown(
                """
                <div style="
                    background-color:white;
                    padding:15px;
                    border-radius:10px;
                    display:flex;
                    justify-content:center;
                    margin-bottom:20px;
                ">
                    <img 
                        src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Logo_of_Lehman_Brothers.svg/1920px-Logo_of_Lehman_Brothers.svg.png"
                        width="220"
                    >
                </div>
                """,
                unsafe_allow_html=True
            )

            # =============================================
            # EMPLOYEE PROFILE
            # =============================================

            render_employee_profile(
                self.employee_information
            )

    # =====================================================
    # MAIN GUI
    # =====================================================

    def render(self):

        if self.employee_information is None:

            st.error(
                "Employee information not found."
            )

            return

        self.render_sidebar()

        self.render_messages()

        self.render_user_input()