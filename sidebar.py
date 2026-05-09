import streamlit as st


def render_employee_profile(employee_information):

    # =====================================================
    # PROFILE TITLE
    # =====================================================

    st.title("👤 Employee Profile")

    st.markdown("---")

    # =====================================================
    # FULL NAME
    # =====================================================

    firstname = employee_information.get(
        "firstname",
        ""
    )

    lastname = employee_information.get(
        "lastname",
        ""
    )

    st.markdown(
        f"### {firstname} {lastname}"
    )

    # =====================================================
    # POSITION
    # =====================================================

    st.caption(
        employee_information.get(
            "position",
            "N/A"
        )
    )

    st.markdown("---")

    # =====================================================
    # ICON MAPPING
    # =====================================================

    field_icons = {

        "employee_id": "🆔",

        "email": "📧",

        "phone_number": "📱",

        "mobile": "📱",

        "department": "🏢",

        "location": "📍",

        "supervisor": "👨‍💼",

        "hire_date": "📅",

        "salary": "💰",

        "position": "💼",

        "firstname": "👤",

        "lastname": "👤",

        "skills": "🛠"
    }

    # =====================================================
    # DISPLAY ALL FIELDS
    # =====================================================

    for key, value in employee_information.items():

        # -------------------------------------------------
        # SKIP NAME FIELDS
        # -------------------------------------------------

        if key in [
            "firstname",
            "lastname"
        ]:
            continue

        # -------------------------------------------------
        # SKILLS
        # -------------------------------------------------

        if key == "skills":

            st.markdown("### 🛠 Skills")

            if isinstance(value, list):

                for skill in value:

                    st.markdown(
                        f"- {skill}"
                    )

            else:

                st.markdown(
                    str(value)
                )

            st.markdown("---")

            continue

        # -------------------------------------------------
        # FORMAT KEY
        # -------------------------------------------------

        formatted_key = (
            key.replace("_", " ")
            .title()
        )

        icon = field_icons.get(
            key,
            "📌"
        )


        # -------------------------------------------------
        # FORMAT DATETIME
        # -------------------------------------------------

        if "date" in key.lower():

            try:

                value = str(value).split(" ")[0]

            except Exception:

                pass

        # -------------------------------------------------
        # DISPLAY FIELD
        # -------------------------------------------------

        st.markdown(
            f"**{icon} {formatted_key}:**  \n"
            f"{value}"
        )

    st.markdown("---")

    # =====================================================
    # LOGOUT BUTTON
    # =====================================================

    if st.button("Logout"):

        st.session_state.authenticated = (
            False
        )

        st.session_state.messages = []

        st.rerun()