import streamlit as st
import login

login.generarLogin()
if 'usuario' in st.session_state:
    st.header('Página :blue[1]')