import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- এখানে আপনার Gemini API Key দিন ---
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="My AI Assistant", layout="wide")
st.title("🤖 আমার AI ওয়েবসাইট")

option = st.sidebar.selectbox("কি করতে চান?", ("Chat & Coding", "Photo Analysis"))

if option == "Chat & Coding":
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("যেকোনো প্রশ্ন বা কোড লিখুন..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

elif option == "Photo Analysis":
    st.info("ছবি আপলোড করে AI-কে প্রশ্ন করুন।")
    uploaded_file = st.file_uploader("ছবি সিলেক্ট করুন...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="আপলোড করা ছবি", use_container_width=True)
        user_inst = st.text_input("এই ছবি নিয়ে আপনার প্রশ্ন লিখুন:")
        if st.button("Analyze Image"):
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([user_inst, image])
            st.write(response.text)