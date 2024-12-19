import streamlit as st
from instaloader import Instaloader, Post
import random
import re

# Add a background image (replace the URL with your own if desired)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://images.pexels.com/photos/1252890/pexels-photo-1252890.jpeg?cs=srgb&dl=pexels-krisof-1252890.jpg&fm=jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Instagram Comment Picker")

post_url = st.text_input("Enter the Instagram post URL.")

if st.button("Choose winner"):
    # Extract the shortcode from the URL
    match = re.search(r"instagram\.com/p/([^/]+)/?", post_url)
    if not match:
        st.error("Invalid URL format. Make sure it looks like https://www.instagram.com/p/shortcode/")
        st.stop()
    shortcode = match.group(1)

    loader = Instaloader()
    # Load your saved session (replace "_space42_" with the username you used to login)
    loader.load_session_from_file("_space42_")

    try:
        post = Post.from_shortcode(loader.context, shortcode)
    except Exception as e:
        st.error(f"Failed to load post: {e}")
        st.stop()

    # Gather unique usernames from comments
    usernames = set(comment.owner.username for comment in post.get_comments())

    if not usernames:
        st.write("No comments found on this post.")
    else:
        # Select 3 distinct winners
        if len(usernames) < 3:
            st.warning("Not enough unique commenters to pick 3 winners.")
        else:
            winners = random.sample(list(usernames), 3)
            for i, winner in enumerate(winners, start=1):
                st.success(f"Winner {i}: {winner}")
