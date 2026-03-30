import streamlit as st
import google.generativeai as genai
from PIL import Image

# ১. পেজ সেটআপ (টাইটেল এবং আইকন)
st.set_page_config(page_title="Shohan AI Assistant", page_icon="🤖")

# ২. এপিআই কি (API Key) কানেক্ট করা
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("দয়া করে Streamlit Settings > Secrets-এ আপনার API Key যুক্ত করুন।")
    st.stop()

# ৩. এআই মডেল সেটআপ
model = genai.GenerativeModel('gemini-1.5-flash')

# ৪. ইন্টারফেস ডিজাইন
st.title("🤖 আমার AI অ্যাসিস্ট্যান্ট")
st.write("CST স্টুডেন্ট শোয়ানের তৈরি প্রথম এআই। আপনি এখানে চ্যাট করতে পারেন এবং ছবি আপলোড করে প্রশ্ন করতে পারেন।")

# ৫. ছবি আপলোড অপশন
uploaded_file = st.file_uploader("একটি ছবি আপলোড করুন (ঐচ্ছিক)", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="আপনার আপলোড করা ছবি", use_container_width=True)

# ৬. চ্যাট ইনপুট
user_input = st.chat_input("এখানে আপনার প্রশ্ন লিখুন...")

if user_input:
    # ইউজারের মেসেজ দেখানো
    with st.chat_message("user"):
        st.markdown(user_input)

    # এআই-এর উত্তর তৈরি করা
    with st.chat_message("assistant"):
        with st.spinner("AI ভাবছে..."):
            try:
                if image:
                    # ছবিসহ উত্তর
                    response = model.generate_content([user_input, image])
                else:
                    # শুধু টেক্সট উত্তর
                    response = model.generate_content(user_input)
                
                st.markdown(response.text)
            except Exception as e:
                st.error(f"দুঃখিত, একটি সমস্যা হয়েছে: {e}")

# সাইডবার
st.sidebar.title("ডেভেলপার ইনফো")
st.sidebar.info("নাম: শোয়ান\nবিভাগ: CST\nলক্ষ্য: ২০২৯ সালে ডিপ্লোমা সম্পন্ন করা।")
