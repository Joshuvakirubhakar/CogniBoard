import pandas as pd
import streamlit as st

from app import run_chatbot

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Employee Onboarding Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# EXCEL FILES
# =========================================================

SECURITY_FILE = "security.xlsx"

DATA_FILE = "employee_data.xlsx"

# =========================================================
# SESSION STATE
# =========================================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False

# =========================================================
# LOGIN FUNCTION
# =========================================================

def login(employee_id, password):

    try:

        security_df = pd.read_excel(
            SECURITY_FILE
        )

        user = security_df[

            (security_df["employee_id"] == employee_id)

            &

            (security_df["password"] == password)
        ]

        return not user.empty

    except Exception as e:

        st.error(
            f"Login Error: {str(e)}"
        )

        return False

# =========================================================
# GET EMPLOYEE DATA
# =========================================================

def get_employee_data(employee_id):

    try:

        employee_df = pd.read_excel(
            DATA_FILE
        )

        employee = employee_df[

            employee_df["employee_id"] == employee_id
        ]

        if employee.empty:

            return None

        return employee.iloc[0].to_dict()

    except Exception as e:

        st.error(
            f"Employee Data Error: {str(e)}"
        )

        return None

# =========================================================
# RESET PASSWORD
# =========================================================

def reset_password(
    employee_id,
    mobile,
    new_password
):

    try:

        security_df = pd.read_excel(
            SECURITY_FILE
        )

        user_index = security_df[

            (security_df["employee_id"] == employee_id)

            &

            (security_df["mobile"] == mobile)

        ].index

        if len(user_index) == 0:

            return False

        security_df.loc[
            user_index,
            "password"
        ] = new_password

        security_df.to_excel(
            SECURITY_FILE,
            index=False
        )

        return True

    except Exception as e:

        st.error(
            f"Password Reset Error: {str(e)}"
        )

        return False

# =========================================================
# LOGIN SCREEN
# =========================================================

if not st.session_state.authenticated:

    # =====================================================
    # HIDE SIDEBAR ONLY DURING LOGIN
    # =====================================================

    hide_streamlit_style = """
    <style>

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    </style>
    """

    st.markdown(
        hide_streamlit_style,
        unsafe_allow_html=True
    )

    st.title(
        "Employee Onboarding Assistant"
    )

    tab1, tab2 = st.tabs([
        "Login",
        "Forgot Password"
    ])

    # =====================================================
    # LOGIN TAB
    # =====================================================

    with tab1:

        employee_id = st.text_input(
            "Employee ID",
            key="login_employee_id"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
        ):

            if login(
                employee_id,
                password
            ):

                employee_data = get_employee_data(
                    employee_id
                )

                if employee_data is None:

                    st.error(
                        "Employee data not found"
                    )

                else:

                    st.session_state.authenticated = True

                    st.session_state.employee_id = (
                        employee_id
                    )

                    st.session_state.employee_data = (
                        employee_data
                    )

                    st.success(
                        "Login successful"
                    )

                    st.rerun()

            else:

                st.error(
                    "Invalid Employee ID or Password"
                )

    # =====================================================
    # FORGOT PASSWORD TAB
    # =====================================================

    with tab2:

        forgot_employee_id = st.text_input(
            "Employee ID",
            key="forgot_employee_id"
        )

        forgot_mobile = st.text_input(
            "Registered Mobile Number",
            key="forgot_mobile"
        )

        new_password = st.text_input(
            "New Password",
            type="password",
            key="forgot_new_password"
        )

        if st.button(
            "Reset Password",
            key="reset_password_button"
        ):

            success = reset_password(
                forgot_employee_id,
                forgot_mobile,
                new_password
            )

            if success:

                st.success(
                    "Password updated successfully"
                )

            else:

                st.error(
                    "Invalid Employee ID or Mobile Number"
                )

# =========================================================
# LOAD CHATBOT APPLICATION
# =========================================================

else:

    run_chatbot()