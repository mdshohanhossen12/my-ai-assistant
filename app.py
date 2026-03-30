import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ সেটআপ (টাইটেল এবং আইকন)
st.set_page_config(page_title="Shohan AI Assistant", page_icon="🤖")

st.title("🤖 আমার AI অ্যাসিস্ট্যান্ট")
st.write("CST স্টুডেন্ট শোয়ানের তৈরি প্রথম এআই। আপনি এখানে চ্যাট করতে পারেন এবং ছবি আপলোড করে প্রশ্ন করতে পারেন।")

# ২. এপিআই কি (API Key) সেটআপ - এটি Streamlit Secrets থেকে আসবে
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("দয়া করে Streamlit Settings > Secrets-এ আপনার API Key যুক্ত করুন।")
    st.stop()

# ৩. এআই মডেল সেটআপ (ইন্সট্রাকশন দেওয়া হয়েছে যেন সে শুধু কোড না দেয়)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are a helpful and friendly AI assistant. Answer the user's questions clearly in the language they use (Bengali or English). Avoid giving only code unless the user specifically asks for it."
)

# ৪. ছবি আপলোড করার অপশন
uploaded_file = st.file_uploader("একটি ছবি আপলোড করুন (ঐচ্ছিক)", type=["jpg", "jpeg", "png"])

# ৫. ইউজার ইনপুট বক্স
user_input = st.chat_input("এখানে আপনার প্রশ্ন লিখুন...")

if user_input:
    # ইউজারের মেসেজ দেখানো
    with st.chat_message("user"):
        st.write(user_input)

    # এআই-এর উত্তর তৈরি করা
    with st.chat_message("assistant"):
        with st.spinner("AI চিন্তা করছে..."):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([user_input, img])
                else:
                    response = model.generate_content(user_input)
                
                # উত্তরটি সুন্দরভাবে দেখানো
                st.write(response.text)
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

# সাইডবার বা নিচে ক্রেডিট
st.sidebar.markdown("---")
st.sidebar.write("Developed by **MD Shohan Hossen**")
st.sidebar.write("Department: CST")
