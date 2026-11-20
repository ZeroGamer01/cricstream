
import streamlit as st

st.set_page_config(
    page_title="CricStream",
    page_icon="🏏",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: white;
}
h1, h2, h3, p {
    color: white;
}
div.stButton > button {
    background-color: #16a34a;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

st.title("🏏 CricStream")
st.caption("Your cricket streaming hub")

st.markdown("---")

st.subheader("📺 Live Cricket")

st.info("Live matches and authorized streams will appear here.")

st.markdown("---")

st.subheader("🏆 Match Center")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🇮🇳 India")
    st.write("Live scores and match updates")

with col2:
    st.markdown("### 🌍 International")
    st.write("Fixtures and match information")

st.markdown("---")

st.subheader("🔴 Watch Live")

stream_url = st.text_input(
    "Enter an authorized live stream URL",
    placeholder="Paste an authorized stream URL here"
)

if stream_url:
    st.video(stream_url)

st.caption("CricStream | Free-to-use streaming hub")
