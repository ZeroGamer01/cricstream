
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="CricStream",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 CricStream")
st.caption("Your cricket live score hub")

API_URL = "https://cricket.sportmonks.com/api/v2.0/livescores"

def get_token():
    try:
        return st.secrets["SPORTMONKS_API_TOKEN"]
    except Exception:
        return None

def fetch_live_matches():
    token = get_token()

    if not token:
        st.error("API token is missing. Add it in Streamlit App Settings → Secrets.")
        return None

    params = {
        "api_token": token,
        "include": "localteam,visitorteam,league,scoreboards"
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=20
        )

        if response.status_code == 503:
            st.warning("SportMonks is temporarily unavailable (503). Please try again shortly.")
            return None

        if response.status_code == 429:
            st.warning("API rate limit reached. Please wait before refreshing.")
            return None

        if response.status_code == 401 or response.status_code == 403:
            st.error("API authentication or plan access error. Check your token and subscription.")
            return None

        response.raise_for_status()

        result = response.json()
        return result.get("data", [])

    except requests.exceptions.Timeout:
        st.warning("The API request timed out. Please try again.")
        return None

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to SportMonks. Check your internet connection.")
        return None

    except requests.exceptions.HTTPError as e:
        st.error(f"API HTTP error: {e.response.status_code}")
        return None

    except Exception:
        st.error("Something went wrong while retrieving match data.")
        return None


def get_team_name(team):
    if isinstance(team, dict):
        return team.get("name", "Unknown team")
    return "Unknown team"


def display_match(match):
    local = get_team_name(match.get("localteam"))
    visitor = get_team_name(match.get("visitorteam"))
    league = match.get("league") or {}
    league_name = league.get("name", "Cricket")

    scores = match.get("scoreboards") or []

    st.subheader(f"{local} vs {visitor}")
    st.caption(f"🏆 {league_name}")

    if scores:
        for score in scores:
            team_name = score.get("team", "")
            total = score.get("total", score.get("score", ""))
            wickets = score.get("wickets", "")
            overs = score.get("overs", "")

            if total != "":
                st.write(
                    f"**{team_name}**: {total}/{wickets} "
                    f"({overs} overs)"
                )
    else:
        st.info("Score details are not yet available.")

    st.divider()


st.header("🔴 Live Cricket")

if st.button("🔄 Refresh Live Scores"):
    st.cache_data.clear()

@st.cache_data(ttl=60)
def cached_matches():
    return fetch_live_matches()

matches = cached_matches()

if matches is not None:
    if len(matches) == 0:
        st.info("No live matches are currently returned by the API.")
    else:
        st.success(f"Live matches retrieved: {len(matches)}")

        for match in matches:
            display_match(match)

st.divider()
st.caption("CricStream | Cricket Live Match Center")
st.caption("Live data powered by SportMonks")
