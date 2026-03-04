import streamlit as st
import base64

def set_f1_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    
    # Professional CSS to cover the app background
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Make containers slightly transparent for readability */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: rgba(255, 255, 255, 0.1); 
        backdrop-filter: blur(10px);
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)