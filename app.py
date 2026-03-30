import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Configuration
st.set_page_config(page_title="Shohan AI Assistant", page_icon="🤖", layout="centered")

# 2. API Key Setup from Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Error: Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# 3. Model Initialization (Fixes the 404/v1beta error)
model = genai.GenerativeModel("gemini-1.5-flash")

# 4. UI Design
st.title("🤖 Shohan's AI Assistant")
st.info("Created by Shohan, a CST Student. This AI supports Image Analysis and Translation.")

# 5. Sidebar - Language Translation Settings
st.sidebar.title("Configuration")
target_language = st.sidebar.selectbox(
    "Choose Response Language:",
    ["English", "Bengali (বাংলা)", "Hindi", "Arabic"]
)

st.sidebar.markdown("---")
st.sidebar.write("**Developer:** Shohan")
st.sidebar.write("**Department:** CST")

# 6. Image Upload Section
uploaded_file = st.file_uploader("Upload an image (Optional)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Preview", use_container_width=True)

# 7. Chat Input & Processing
user_query = st.chat_input("Type your message here...")

if user_query:
    # Adding a translation instruction to the prompt
    final_prompt = f"User Question: {user_query}. Please provide the response strictly in {target_language}."

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if image:
                    # Vision + Text response
                    response = model.generate_content([final_prompt, image])
                else:
                    # Text only response
                    response = model.generate_content(final_prompt)
                
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Tip: Try rebooting the app from Streamlit Dashboard.")
