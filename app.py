
import streamlit as st
import requests
from datetime import date, timedelta

st.set_page_config(
    page_title="CricStream",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 CricStream")
st.caption("Your cricket live score and match schedule hub")

API_BASE = "https://cricket.sportmonks.com/api/v2.0"

def get_token():
    try:
        return st.secrets["SPORTMONKS_API_TOKEN"]
    except Exception:
        return None

def fetch_api(endpoint, params=None):
    token = get_token()

    if not token:
        st.error("API token missing. Check Streamlit Secrets.")
        return None

    if params is None:
        params = {}

    params["api_token"] = token

    try:
        response = requests.get(
            f"{API_BASE}/{endpoint}",
            params=params,
            timeout=25
        )

        if response.status_code == 503:
            st.warning("SportMonks is temporarily unavailable (503).")
            return None

        if response.status_code == 429:
            st.warning("API rate limit reached. Please wait.")
            return None

        if response.status_code in (401, 403):
            st.error("Token or API plan access problem.")
            return None

        response.raise_for_status()
        return response.json().get("data", [])

    except requests.exceptions.Timeout:
        st.warning("Request timed out. Try again.")
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to SportMonks.")
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e.response.status_code}")
    except Exception:
        st.error("Unexpected API error.")

    return None


def team_name(team):
    if isinstance(team, dict):
        return team.get("name", "Unknown team")
    return "Unknown team"


def match_date(match):
    value = match.get("starting_at", "")

    if value:
        return value.replace("T", " ")[:16]

    return "Time not available"


def show_match(match, upcoming=False):
    local = team_name(match.get("localteam"))
    visitor = team_name(match.get("visitorteam"))

    league = match.get("league") or {}
    venue = match.get("venue") or {}

    league_name = league.get("name", "Cricket")
    venue_name = venue.get("name", "Venue not available")

    status = match.get("status", "Scheduled")
    match_type = match.get("type", "Match")

    st.subheader(f"{local} vs {visitor}")

    st.write(f"🏆 **Tournament:** {league_name}")
    st.write(f"🏏 **Format:** {match_type}")
    st.write(f"📅 **Date:** {match_date(match)}")
    st.write(f"📍 **Venue:** {venue_name}")
    st.write(f"📌 **Status:** {status}")

    if match.get("note"):
        st.write(f"ℹ️ {match.get('note')}")

    st.divider()


@st.cache_data(ttl=60)
def live_matches():
    return fetch_api(
        "livescores",
        {
            "include": "localteam,visitorteam,league,scoreboards"
        }
    )


@st.cache_data(ttl=600)
def upcoming_matches(start_date, end_date):
    return fetch_api(
        "fixtures",
        {
            "filter[starts_between]": f"{start_date},{end_date}",
            "include": "localteam,visitorteam,league,venue",
            "sort": "starting_at"
        }
    )


if st.button("🔄 Refresh All Data"):
    st.cache_data.clear()

today = date.today()
end_day = today + timedelta(days=14)

tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Upcoming Matches"])

with tab1:
    st.header("🔴 Live Cricket")

    live = live_matches()

    if live is None:
        st.info("Live data could not be retrieved right now.")
    elif len(live) == 0:
        st.info("No live matches currently available.")
    else:
        st.success(f"{len(live)} live matches found")

        for match in live:
            show_match(match)


with tab2:
    st.header("📅 Upcoming Cricket Matches")
    st.caption("Fixtures scheduled over the next 14 days.")

    upcoming = upcoming_matches(
        today.isoformat(),
        end_day.isoformat()
    )

    if upcoming is None:
        st.info("Upcoming fixtures could not be retrieved.")
    elif len(upcoming) == 0:
        st.info("No upcoming fixtures returned by the API.")
    else:
        st.success(f"{len(upcoming)} fixtures retrieved")

        for match in upcoming:
            show_match(match, upcoming=True)


st.divider()
st.caption("CricStream | Cricket Match Center")
st.caption("Powered by SportMonks")
