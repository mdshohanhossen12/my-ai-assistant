import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Shohan AI Assistant", page_icon="🤖", layout="centered")

# ২. এপিআই কী সেটআপ
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Error: Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# ৩. মডেল এবং চ্যাট সেশন ইনিশিয়ালাইজেশন
# এখানে system_instruction যোগ করা হয়েছে যাতে এআই সবসময় আপনার নির্দেশ মেনে চলে
model = genai.GenerativeModel(
    model = genai.GenerativeModel("gemini-1.5-flash-latest"),
    system_instruction="You are Shohan's AI Assistant. Always be helpful and friendly."
)

# চ্যাট হিস্ট্রি স্টোর করার জন্য Session State ব্যবহার
if "chat_session" not in st.session_state:
    st.session_state.chat_session = [] # এখানে আগের মেসেজগুলো জমা থাকবে

# ৪. ইউআই ডিজাইন (সাইডবার)
st.sidebar.title("⚙️ Configuration")
target_language = st.sidebar.selectbox(
    "Response Language:",
    ["English", "Bengali (বাংলা)", "Hindi", "Arabic"]
)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_session = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("**Developer:** Shohan (CST Student)")

# ৫. মেইন ইউআই
st.title("🤖 Shohan's AI Assistant")
st.info("ইমেজ অ্যানালাইসিস এবং ট্রান্সলেশন সাপোর্ট সহ উন্নত এআই।")

# ৬. ইমেজ আপলোড
uploaded_file = st.file_uploader("Upload an image (Optional)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# ৭. আগের চ্যাটগুলো স্ক্রিনে দেখানো
for message in st.session_state.chat_session:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ৮. নতুন চ্যাট ইনপুট এবং প্রসেসিং
user_query = st.chat_input("আপনার প্রশ্ন লিখুন...")

if user_query:
    # ইউজারের মেসেজ স্ক্রিনে দেখানো এবং সেভ করা
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.chat_session.append({"role": "user", "content": user_query})

    # এআই রেসপন্স তৈরি
    with st.chat_message("assistant"):
        with st.spinner("চিন্তা করছি..."):
            try:
                # প্রম্পটের সাথে ভাষা যোগ করা
                final_prompt = f"Response Language: {target_language}. Question: {user_query}"
                
                # ইমেজ থাকলে ইমেজসহ, না থাকলে শুধু টেক্সট পাঠানো
                if image:
                    response = model.generate_content([final_prompt, image], stream=True)
                else:
                    response = model.generate_content(final_prompt, stream=True)

                # স্ট্রিমিং ইফেক্ট (লেখা টাইপ হওয়ার মতো দেখাবে)
                placeholder = st.empty()
                full_text = ""
                for chunk in response:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
                placeholder.markdown(full_text)

                # এআই এর উত্তর হিস্ট্রিতে সেভ করা
                st.session_state.chat_session.append({"role": "assistant", "content": full_text})

            except Exception as e:
                st.error(f"Error: {e}")
