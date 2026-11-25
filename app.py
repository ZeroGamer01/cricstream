
import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="CricStream", page_icon="🏏", layout="wide")

st.title("🏏 CricStream")
st.caption("Your cricket live score and match schedule hub")

try:
    API_TOKEN = st.secrets["SPORTMONKS_API_TOKEN"]
except Exception:
    st.error("API token missing from Streamlit Secrets.")
    st.stop()

BASE_URL = "https://cricket.sportmonks.com/api/v2.0"

def fetch_data(endpoint, params=None):
    params = params or {}
    params["api_token"] = API_TOKEN

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=20
        )
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        st.error(f"API error: {e}")
        return []

def team_name(team):
    return team.get("name", "Unknown") if isinstance(team, dict) else "Unknown"

def format_date(date_string):
    if not date_string:
        return "Date unavailable"

    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y | %I:%M %p UTC")
    except Exception:
        return date_string

def match_card(match, index):
    local = team_name(match.get("localteam"))
    visitor = team_name(match.get("visitorteam"))
    league = match.get("league") or {}
    venue = match.get("venue") or {}

    league_name = league.get("name", "Unknown competition") if isinstance(league, dict) else "Unknown competition"
    venue_name = venue.get("name", "Venue not available") if isinstance(venue, dict) else "Venue not available"

    match_date = format_date(match.get("starting_at"))
    status = match.get("status", "Unknown")
    match_id = match.get("id", "N/A")

    with st.expander(f"🏏 {local} vs {visitor} | {match_date}"):
        st.markdown(f"**🏆 Competition:** {league_name}")
        st.markdown(f"**📅 Date:** {match_date}")
        st.markdown(f"**📌 Status:** {status}")
        st.markdown(f"**🏟️ Venue:** {venue_name}")
        st.markdown(f"**🆔 Match ID:** {match_id}")

        if match.get("note"):
            st.markdown(f"**ℹ️ Note:** {match['note']}")

        st.caption("More match details will be added in future upgrades.")

st.divider()

tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Upcoming Matches"])

# LIVE MATCHES
with tab1:
    st.subheader("🔴 Live Cricket")

    if st.button("🔄 Refresh Live Matches", key="refresh_live"):
        st.rerun()

    live_matches = fetch_data(
        "livescores",
        {"include": "localteam,visitorteam,league,venue"}
    )

    if live_matches:
        for i, match in enumerate(live_matches):
            match_card(match, i)
    else:
        st.info("No live matches currently available.")

# UPCOMING MATCHES
with tab2:
    st.subheader("📅 Upcoming Cricket Matches")

    if st.button("🔄 Refresh Upcoming Matches", key="refresh_upcoming"):
        st.rerun()

    today = datetime.now(timezone.utc).date()
    end_date = today + timedelta(days=14)
    date_range = f"{today},{end_date}"

    upcoming_matches = fetch_data(
    "fixtures",
    {
        "filter[starts_between]": date_range,
        "include": "localteam,visitorteam,league,venue"
    }
)

# Fetch WBBL fixtures (League ID 65)
wbbl_matches = fetch_data(
    "fixtures",
    {
        "filter[league_id]": 65,
        "filter[starts_between]": date_range,
        "include": "localteam,visitorteam,league,venue"
    }
)

# Combine matches and remove duplicates
all_matches = {m.get("id"): m for m in upcoming_matches}
for match in wbbl_matches:
    all_matches[match.get("id")] = match

upcoming_matches = list(all_matches.values())
    if upcoming_matches:

        formats = ["All"]

        for match in upcoming_matches:
            type_name = match.get("type")
            if type_name and type_name not in formats:
                formats.append(type_name)

        selected_format = st.selectbox(
            "Filter by match format",
            formats
        )

        filtered_matches = upcoming_matches

        if selected_format != "All":
            filtered_matches = [
                m for m in upcoming_matches
                if m.get("type") == selected_format
            ]

        st.write(f"Matches found: {len(filtered_matches)}")

        for i, match in enumerate(filtered_matches):
            match_card(match, i)

    else:
        st.info("No upcoming matches returned by the API.")

st.divider()
st.caption("CricStream | Cricket Match Center")
st.caption("Live and fixture data powered by SportMonks")
