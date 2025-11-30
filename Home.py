import streamlit as st
import sys
import os

from PIL import Image
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from app.services.user_service import login_user, register_user

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if "show_login" not in st.session_state:
    st.session_state.show_login = False

if "show_register" not in st.session_state:
    st.session_state.show_register = False




if not st.session_state.logged_in:
    
        st.markdown(
            """
          <h1 style="text-align:center; 
                    font-size:43px; 
                    font-weight:bold; 
                    color:#1E90FF; 
                    margin-top:5px;">
                Multi-Domain Intelligence Platform
           </h1>
           <p style="text-align:center; 
              font-size:22px; 
              font-family:'Segoe UI', 'Helvetica Neue', sans-serif; 
              font-weight:500; 
              background: linear-gradient(90deg, #00C9FF, #92FE9D); 
              -webkit-background-clip: text; 
              -webkit-text-fill-color: transparent; 
              margin-top:10px; 
              text-shadow: 1px 1px 2px rgba(0,0,0,0.15);">
        Unlock insights across multiple domains with ease
            </p>

            """,
            unsafe_allow_html=True
        )



        st.markdown(
            """
            <div style="width:100%; text-align:center; margin-top:px;">
                <h1 style="color:#1E90FF; font-size: 35px; text-align:center;">Access Your Dashboard</h1>
            </div>
            """,
            unsafe_allow_html=True
        )


        # Button for login/registration
      
        col= st.columns(1)[0]
        
        with col: 
                 

            col1,col2, col3= st.columns([2,2,2])

            with col2:
                b1,b2= st.columns([1,1])
                with b1:
                  if st.button("Login", key="login_button"):
                    st.session_state.show_login = True
                    st.session_state.show_register = False

                with b2:
                  if st.button("Register", key="register_button"):
                    st.session_state.show_register = True
                    st.session_state.show_login = False



        if st.session_state.show_login and not st.session_state.logged_in:
            st.subheader("User Login")
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
        
            if st.button("Login", key="login_submit"):
                sucess, msg= login_user(username, password)
                if sucess: 
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(msg)
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error(msg)


        if st.session_state.show_register and not st.session_state.logged_in:
            st.subheader("User Register")
            new_user = st.text_input("New Username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", key="reg_pass")
            user_role = st.selectbox("Select Role", options=["user", "admin","analyst"], key="reg_role")
        
            if st.button("Register", key="reg_submit"):
                sucess, msg= register_user(new_user, new_pass, user_role)
                if sucess: 
                    st.success(msg)
                    st.session_state.show_register = False
                else:
                    st.error(msg)
elif st.session_state.logged_in: 
    st.markdown(f"""
    <div style="
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        margin-top: 10px;
    ">
        <h1 style="
            font-size: 45px;
            font-weight: 700;
            color: #1E90FF;
            margin-bottom: 10px;
        ">
            Welcome, {st.session_state.username}
        </h1>
        <p style="
            font-size: 20px;
            color: #80CBC4;
            line-height: 1.5;
        ">
            You are now logged in. Select a dashboard from the sidebar to explore your domains.
        </p>
    </div>
    """, unsafe_allow_html=True)
    img = Image.open("app\Dashboard.jpg")  
    st.image(img, use_container_width=True)

      
if st.session_state.logged_in:
    st.sidebar.title(f"Welcome, {st.session_state.username} 👋")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.show_login = False
        st.session_state.show_register = False
        st.rerun()  




            

