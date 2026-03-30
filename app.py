import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Shohan AI Assistant", page_icon="🤖", layout="centered")

# ২. এপিআই কী সেটআপ (Streamlit Secrets থেকে)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Error: Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# ৩. মডেল ইনিশিয়ালাইজেশন (সংশোধিত)
# এখানে model_name এবং system_instruction সঠিকভাবে ব্যবহার করা হয়েছে
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are Shohan's AI Assistant, created by a CST student. Always be helpful, concise, and friendly."
)

# ৪. চ্যাট হিস্ট্রি বা মেমোরি সেটআপ
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

# ৫. সাইডবার কনফিগারেশন
st.sidebar.title("⚙️ Configuration")
target_language = st.sidebar.selectbox(
    "Response Language:",
    ["English", "Bengali (বাংলা)", "Hindi", "Arabic"]
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_session = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("**Developer:** Shohan")
st.sidebar.write("**Department:** CST")

# ৬. মেইন ইউআই (Title & Info)
st.title("🤖 Shohan's AI Assistant")
st.info("CST স্টুডেন্ট সোহান দ্বারা তৈরি। এটি ইমেজ অ্যানালাইসিস এবং চ্যাট সাপোর্ট করে।")

# ৭. ইমেজ আপলোড সেকশন
uploaded_file = st.file_uploader("Upload an image (Optional)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image Preview", use_container_width=True)

# ৮. আগের মেসেজগুলো স্ক্রিনে দেখানো (History Display)
for message in st.session_state.chat_session:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৯. চ্যাট ইনপুট এবং প্রসেসিং
user_query = st.chat_input("আপনার প্রশ্নটি এখানে লিখুন...")

if user_query:
    # ইউজারের প্রশ্ন স্ক্রিনে দেখানো এবং মেমোরিতে রাখা
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_session.append({"role": "user", "content": user_query})

    # এআই রেসপন্স তৈরি
    with st.chat_message("assistant"):
        with st.spinner("চিন্তা করছি..."):
            try:
                # প্রম্পট তৈরি করা (ভাষা নির্ধারণ সহ)
                final_prompt = f"Target Language: {target_language}. User Query: {user_query}"
                
                # ইমেজ থাকলে ইমেজসহ প্রম্পট পাঠানো
                content_list = [final_prompt]
                if image:
                    content_list.append(image)
                
                # জেনারেট কন্টেন্ট (Streaming অন করা হয়েছে)
                response = model.generate_content(content_list, stream=True)
                
                # স্ট্রিমিং টাইপিং ইফেক্ট
                placeholder = st.empty()
                full_response = ""
                
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                
                placeholder.markdown(full_response)

                # এআই এর উত্তর মেমোরিতে সেভ করা
                st.session_state.chat_session.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"একটি সমস্যা হয়েছে: {e}")
                st.info("টিপস: আপনার API Key এবং ইন্টারনেট কানেকশন চেক করুন।")
