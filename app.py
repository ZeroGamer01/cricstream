import streamlit as st
import requests
from datetime import datetime, timedelta, timezone

st.set_page_config(page_title="CricStream", page_icon="🏏", layout="wide")

st.title("🏏 CricStream")
st.caption("Your cricket live score and match schedule hub")

# Read the API key securely from Streamlit Secrets
try:
    API_TOKEN = st.secrets["SPORTMONKS_API_TOKEN"]
except Exception:
    st.error("SportMonks API token not found in Streamlit Secrets.")
    st.stop()

BASE_URL = "https://cricket.sportmonks.com/api/v2.0"

def fetch_matches(endpoint, params=None):
    params = params or {}
    params["api_token"] = API_TOKEN

    try:
        response = requests.get(
            f"{BASE_URL}/{endpoint}",
            params=params,
            timeout=20
        )
        response.raise_for_status()
        result = response.json()
        return result.get("data", [])
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {e}")
        return []
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return []

def get_name(team):
    if isinstance(team, dict):
        return team.get("name", "Unknown team")
    return "Unknown team"

def display_match(match):
    local = get_name(match.get("localteam"))
    visitor = get_name(match.get("visitorteam"))
    league = match.get("league") or {}
    league_name = league.get("name", "Competition") if isinstance(league, dict) else "Competition"

    fixture_date = match.get("starting_at", "Date unavailable")
    status = match.get("status", "Scheduled")

    with st.container(border=True):
        st.subheader(f"{local} vs {visitor}")
        st.caption(f"🏆 {league_name}")
        st.write(f"📅 {fixture_date}")
        st.write(f"📌 Status: {status}")

st.divider()

tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Upcoming Matches"])

# LIVE MATCHES
with tab1:
    st.subheader("🔴 Live Cricket")

    if st.button("🔄 Refresh Live Matches", key="live"):
        st.cache_data.clear()

    live_matches = fetch_matches("livescores", {
        "include": "localteam,visitorteam,league"
    })

    if live_matches:
        for match in live_matches:
            display_match(match)
    else:
        st.info("No live matches currently available.")

# UPCOMING MATCHES
with tab2:
    st.subheader("📅 Upcoming Cricket Matches")

    if st.button("🔄 Refresh Upcoming Matches", key="upcoming"):
        st.cache_data.clear()

    today = datetime.now(timezone.utc).date()
    end_date = today + timedelta(days=14)

    date_range = f"{today},{end_date}"

    upcoming_matches = fetch_matches("fixtures", {
    "filter[starts_between]": date_range,
    "include": "localteam,visitorteam,league"
})

    if upcoming_matches:
        for match in upcoming_matches:
            display_match(match)
    else:
        st.info(
            "No upcoming matches returned. "
            "The API may have restrictions on fixtures or the filter format."
        )

st.divider()

st.caption("CricStream | Cricket Match Center")
st.caption("Live and fixture data powered by SportMonks")
