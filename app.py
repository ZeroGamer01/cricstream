
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="CricStream",
    page_icon="🏏",
    layout="wide"
)

# ---------------- DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: white;
}
.block-container {
    padding-top: 1.5rem;
    max-width: 1100px;
}
h1, h2, h3, p, label {
    color: white !important;
}
.match-card {
    background: #172338;
    border: 1px solid #293952;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 14px;
}
.live {
    color: #ff4b4b;
    font-weight: bold;
}
.upcoming {
    color: #38bdf8;
    font-weight: bold;
}
.completed {
    color: #a3a3a3;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("🏏 CricStream")
st.caption("Your cricket streaming hub")

st.markdown("---")

# ---------------- SAMPLE MATCH DATA ----------------
matches = [
    {
        "team1": "India",
        "team2": "Australia",
        "score": "185/4",
        "overs": "32.4 overs",
        "status": "LIVE",
        "format": "ODI",
        "info": "India batting"
    },
    {
        "team1": "England",
        "team2": "Pakistan",
        "score": "Upcoming",
        "overs": "Not started",
        "status": "UPCOMING",
        "format": "T20",
        "info": "Today"
    },
    {
        "team1": "South Africa",
        "team2": "New Zealand",
        "score": "241/8",
        "overs": "50 overs",
        "status": "COMPLETED",
        "format": "ODI",
        "info": "Match finished"
    },
    {
        "team1": "Australia",
        "team2": "England",
        "score": "Upcoming",
        "overs": "Not started",
        "status": "UPCOMING",
        "format": "TEST",
        "info": "Tomorrow"
    }
]

# ---------------- FILTERS ----------------
st.subheader("📺 Match Center")

filter_col, refresh_col = st.columns([3, 1])

with filter_col:
    selected_format = st.selectbox(
        "Filter by format",
        ["All", "T20", "ODI", "TEST"]
    )

with refresh_col:
    st.write("")
    st.write("")
    st.button("🔄 Refresh", use_container_width=True)

tab_live, tab_upcoming, tab_completed = st.tabs(
    ["🔴 Live", "📅 Upcoming", "🏁 Completed"]
)

# ---------------- MATCH CARD ----------------
def show_match(match):

    status = match["status"]

    if status == "LIVE":
        status_color = "#ff4b4b"
    elif status == "UPCOMING":
        status_color = "#38bdf8"
    else:
        status_color = "#a3a3a3"

    st.markdown(
        f"""
        <div class="match-card">
            <div style="color:{status_color};font-weight:bold">
                {status} | {match["format"]}
            </div>
            <h3>{match["team1"]} vs {match["team2"]}</h3>
            <h2>{match["score"]}</h2>
            <p>{match["overs"]}</p>
            <p>{match["info"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if status == "LIVE":
        st.button(
            "▶ Watch Live",
            key="watch_" + match["team1"] + match["team2"],
            disabled=True,
            help="A streaming source will be connected in a future step."
        )

# ---------------- LIVE ----------------
with tab_live:
    live_matches = [
        m for m in matches
        if m["status"] == "LIVE"
        and (selected_format == "All" or m["format"] == selected_format)
    ]

    if live_matches:
        for match in live_matches:
            show_match(match)
    else:
        st.info("No sample live matches in this category.")

# ---------------- UPCOMING ----------------
with tab_upcoming:
    upcoming_matches = [
        m for m in matches
        if m["status"] == "UPCOMING"
        and (selected_format == "All" or m["format"] == selected_format)
    ]

    if upcoming_matches:
        for match in upcoming_matches:
            show_match(match)
    else:
        st.info("No sample upcoming matches in this category.")

# ---------------- COMPLETED ----------------
with tab_completed:
    completed_matches = [
        m for m in matches
        if m["status"] == "COMPLETED"
        and (selected_format == "All" or m["format"] == selected_format)
    ]

    if completed_matches:
        for match in completed_matches:
            show_match(match)
    else:
        st.info("No sample completed matches in this category.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("CricStream | Live Cricket Hub")
st.caption("Sample matches only — real match data will be connected later.")
