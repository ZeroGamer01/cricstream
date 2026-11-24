
import streamlit as st
import requests

st.set_page_config(
    page_title="CricStream",
    page_icon="🏏",
    layout="wide"
)

# ----------- DESIGN -----------
st.markdown("""
<style>
.stApp {
    background: #0b1120;
    color: white;
}
.block-container {
    max-width: 1100px;
    padding-top: 1.5rem;
}
h1, h2, h3, p {
    color: white !important;
}
.match-card {
    background: #172338;
    border: 1px solid #293952;
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ----------- HEADER -----------
st.title("🏏 CricStream")
st.caption("Your cricket streaming hub")

st.markdown("---")
st.subheader("🔴 Live Cricket")

# ----------- API CONFIG -----------
API_BASE = "https://cricket.sportmonks.com/api/v2.0"

# ----------- API FUNCTION -----------
@st.cache_data(ttl=60)
def get_live_matches(token):

    url = f"{API_BASE}/livescores"

    params = {
        "api_token": token,
        "include": "localteam,visitorteam,runs"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    return result.get("data", [])

# ----------- HELPERS -----------
def team_name(team):

    if isinstance(team, dict):
        return team.get("name", "Unknown team")

    return "Unknown team"


def show_match(match):

    local = team_name(match.get("localteam"))
    visitor = team_name(match.get("visitorteam"))

    status = match.get("status", "Live")

    runs_data = match.get("runs", [])

    score_text = ""

    if isinstance(runs_data, list):
        for innings in runs_data:
            score = innings.get("score")
            wickets = innings.get(" wickets")

            if wickets is None:
                wickets = innings.get("wickets")

            overs = innings.get("overs")

            if score is not None:
                line = str(score)

                if wickets is not None:
                    line += "/" + str(wickets)

                if overs is not None:
                    line += " (" + str(overs) + " overs)"

                score_text += line + "\n"

    if not score_text:
        score_text = "Score details unavailable"

    st.markdown(
        f"""
        <div class="match-card">
            <h3>{local} vs {visitor}</h3>
            <p><b>Status:</b> {status}</p>
            <p><b>Score:</b></p>
            <pre>{score_text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

# ----------- LOAD DATA -----------
if "SPORTMONKS_API_TOKEN" not in st.secrets:
    st.error("API token is missing. Add it in Streamlit Secrets.")

else:

    token = st.secrets["SPORTMONKS_API_TOKEN"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.caption("Live match data from Sportmonks")

    with col2:
        if st.button("🔄 Refresh scores"):
            st.cache_data.clear()
            st.rerun()

    try:

        matches = get_live_matches(token)

        if matches:

            st.success(f"{len(matches)} match record(s) received")

            for match in matches:
                show_match(match)

        else:

            st.info("No live matches returned by the API right now.")

    except requests.exceptions.HTTPError as e:

        st.error("The API returned an HTTP error.")
        st.caption(str(e))

    except requests.exceptions.RequestException as e:

        st.error("Unable to connect to the cricket API.")
        st.caption(str(e))

    except Exception as e:

        st.error("Something went wrong while loading matches.")
        st.caption(str(e))

# ----------- FOOTER -----------
st.markdown("---")
st.caption("CricStream | Cricket Live Match Center")
st.caption("Live data powered by Sportmonks")
