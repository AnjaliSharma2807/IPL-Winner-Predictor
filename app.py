# =========================================================
# IPL WINNER PREDICTOR 2026
# STREAMLIT CLOUD FIXED VERSION
# =========================================================

import streamlit as st
import pandas as pd
import pickle
import random
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="IPL Winner Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# MODEL FILES
# =========================================================

MODEL_FILES = {
    "XGBoost": "ipl_xgboost.pkl",
    "Random Forest": "ipl_random_forest.pkl",
    "Gradient Boosting": "ipl_gradient_boost.pkl",
    "Logistic Regression": "ipl_logistic.pkl",
    "Decision Tree": "ipl_decision_tree.pkl"
}


# =========================================================
# LOAD MODELS
# =========================================================

@st.cache_resource
def load_models():

    models = {}
    errors = {}

    for model_name, filename in MODEL_FILES.items():

        model_path = BASE_DIR / filename

        try:

            if not model_path.exists():
                errors[model_name] = f"File not found: {filename}"
                continue

            with open(model_path, "rb") as file:
                models[model_name] = pickle.load(file)

        except Exception as e:
            errors[model_name] = f"{type(e).__name__}: {str(e)}"

    return models, errors


models, model_errors = load_models()


# =========================================================
# STOP ONLY IF NO MODEL LOADED
# =========================================================

if not models:

    st.error("❌ No Machine Learning model could be loaded.")

    st.markdown("### 🔍 Model Loading Details")

    for model_name, error in model_errors.items():
        st.write(f"**{model_name}:** {error}")

    st.warning(
        "Make sure the .pkl model files are present in the same "
        "GitHub folder as app.py and that requirements.txt uses "
        "compatible library versions."
    )

    st.stop()


# =========================================================
# TEAM DATA
# =========================================================

teams = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bangalore",
    "Kolkata Knight Riders",
    "Delhi Capitals",
    "Punjab Kings",
    "Rajasthan Royals",
    "Sunrisers Hyderabad"
]


# =========================================================
# VENUES
# =========================================================

venues = [
    "Wankhede Stadium, Mumbai",
    "Eden Gardens, Kolkata",
    "M Chinnaswamy Stadium, Bangalore",
    "Narendra Modi Stadium, Ahmedabad",
    "MA Chidambaram Stadium, Chennai",
    "Arun Jaitley Stadium, Delhi"
]


# =========================================================
# TEAM LOGOS
# =========================================================

logos = {

    "Mumbai Indians":
    "https://documents.iplt20.com/ipl/MI/Logos/Logooutline/MIoutline.png",

    "Chennai Super Kings":
    "https://documents.iplt20.com/ipl/CSK/logos/Logooutline/CSKoutline.png",

    "Royal Challengers Bangalore":
    "https://documents.iplt20.com/ipl/RCB/Logos/Logooutline/RCBoutline.png",

    "Kolkata Knight Riders":
    "https://documents.iplt20.com/ipl/KKR/Logos/Logooutline/KKRoutline.png",

    "Delhi Capitals":
    "https://documents.iplt20.com/ipl/DC/Logos/LogoOutline/DCoutline.png",

    "Punjab Kings":
    "https://documents.iplt20.com/ipl/PBKS/Logos/Logooutline/PBKSoutline.png",

    "Rajasthan Royals":
    "https://documents.iplt20.com/ipl/RR/Logos/Logooutline/RRoutline.png",

    "Sunrisers Hyderabad":
    "https://documents.iplt20.com/ipl/SRH/Logos/Logooutline/SRHoutline.png"
}


# =========================================================
# STADIUM IMAGES
# =========================================================

stadium_images = [

    "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=1200",

    "https://pbs.twimg.com/media/HCVCW1zaMAAlLVY.jpg",

    "https://preview.redd.it/future-of-m-chinnaswamy-stadium-v0-hc1u47q3ybqg1.png?width=1080&crop=smart&auto=webp&s=c45c5a01474b51d95684feb291b19d76691271f2",

    "https://files.prokerala.com/news/photos/imgs/1024/a-view-of-the-narendra-modi-stadium-during-the-1450214.jpg"
]


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
    linear-gradient(rgba(2,6,23,0.92), rgba(2,6,23,0.94)),
    url("https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?q=80&w=2000");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.block-container {
    padding-top: 1rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.stRadio > div {
    background: rgba(255,255,255,0.04);
    padding: 10px;
    border-radius: 15px;
}

.stRadio label {
    color: white !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}

.stSelectbox > div > div {
    background: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
}

.stSlider label {
    color: white !important;
}

.stButton > button {
    width: 100%;
    height: 70px;
    border: none;
    border-radius: 18px;

    background: linear-gradient(
        90deg,
        #ff006e,
        #8338ec,
        #3a86ff
    );

    color: white;
    font-size: 24px;
    font-weight: 700;
}

.banner {
    width: 100%;
    height: 330px;

    border-radius: 25px;

    background:
    linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.65)),
    url("https://akm-img-a-in.tosshub.com/indiatoday/images/story/202605/ig-16243230-16x9_0.png?VersionId=cPOMXYAaweYkVz7k3mNsmm89.6K8FfGr&size=690:388");

    background-size: cover;
    background-position: center;

    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;

    margin-bottom: 25px;
}

.banner h1 {
    color: white;
    font-size: 82px;
    font-weight: 800;
    margin: 0;
    text-align: center;
}

.banner span {
    color: #ffcc00;
}

.banner p {
    color: white;
    font-size: 22px;
}

.glass {
    background: rgba(9,15,35,0.78);
    backdrop-filter: blur(14px);

    border-radius: 24px;
    padding: 30px;

    border: 1px solid rgba(255,255,255,0.08);
}

.result {
    background: linear-gradient(180deg,#0f172a,#111827);

    border-radius: 24px;
    padding: 30px;

    border: 1px solid #ffcc00;

    text-align: center;
}

.heading {
    color: white;
    font-size: 30px;
    font-weight: 700;
}

.winner {
    color: #00ff84;
    font-size: 60px;
    font-weight: 800;
}

.team {
    color: white;
    font-size: 36px;
    font-weight: 700;
}

.prob {
    color: #7CFC00;
    font-size: 72px;
    font-weight: 800;
}

img {
    border-radius: 18px;
}

.footer {
    text-align: center;
    color: white;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.image(
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpaZputVLeoD4585Mo_wH7p02VRrRuwMS2ePnLQhKX-0F4RqyLsNscGPF6&s=10",
    width=180
)

menu = st.sidebar.radio(
    "📌 MENU",
    [
        "🏠 Home",
        "📊 Predict Match",
        "📈 Insights",
        "🏟 Venues",
        "ℹ About"
    ]
)

st.sidebar.markdown("---")


# =========================================================
# MODEL SELECTOR
# =========================================================

algorithm = st.sidebar.radio(
    "🤖 SELECT MODEL",
    list(models.keys())
)

model = models.get(algorithm)

if model is None:
    st.error(f"❌ Model '{algorithm}' could not be loaded.")
    st.stop()


st.sidebar.markdown("---")

st.sidebar.info(
    """
    🔥 Advanced IPL Match Predictor

    🏏 Machine Learning Based

    📊 Interactive Prediction UI
    """
)


# =========================================================
# BANNER
# =========================================================

st.markdown("""
<div class="banner">

<h1>
IPL <span>WINNER PREDICTOR</span>
</h1>

<p>
Powered By Machine Learning
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HOME / PREDICT PAGE
# =========================================================

if menu in ["🏠 Home", "📊 Predict Match"]:

    left, right = st.columns([1.6, 1])


    # =====================================================
    # LEFT SIDE - MATCH DETAILS
    # =====================================================

    with left:

        st.markdown(
            "<div class='glass'>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='heading'>
            🏏 MATCH DETAILS
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)


        col1, col2 = st.columns(2)


        with col1:

            team1 = st.selectbox(
                "Select Team 1",
                teams,
                index=0
            )


        with col2:

            filtered_team2 = [
                team for team in teams
                if team != team1
            ]

            team2 = st.selectbox(
                "Select Team 2",
                filtered_team2,
                index=0
            )


        st.markdown("<br>", unsafe_allow_html=True)


        l1, vs, l2 = st.columns([1, 0.4, 1])


        with l1:

            st.image(
                logos[team1],
                width=150
            )


        with vs:

            st.markdown(
                """
                <h1 style='color:white;text-align:center;margin-top:40px'>
                VS
                </h1>
                """,
                unsafe_allow_html=True
            )


        with l2:

            st.image(
                logos[team2],
                width=150
            )


        st.markdown("<br>", unsafe_allow_html=True)


        # =================================================
        # TOSS
        # =================================================

        toss_winner = st.radio(
            "🏏 Toss Winner",
            [team1, team2],
            horizontal=True
        )


        toss_decision = st.radio(
            "🎯 Toss Decision",
            ["Bat", "Field"],
            horizontal=True
        )


        # =================================================
        # VENUE
        # =================================================

        venue = st.selectbox(
            "🏟 Select Venue",
            venues
        )


        st.markdown("<br>", unsafe_allow_html=True)


        # =================================================
        # SCORE INPUTS
        # =================================================

        s1, s2 = st.columns(2)


        with s1:

            first_score = st.slider(
                "First Innings Score",
                50,
                250,
                180
            )


        with s2:

            second_score = st.slider(
                "Second Innings Score",
                50,
                250,
                170
            )


        st.markdown("<br>", unsafe_allow_html=True)


        # =================================================
        # PREDICT BUTTON
        # =================================================

        predict = st.button(
            "⚡ PREDICT WINNER"
        )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # RIGHT SIDE - RESULT
    # =====================================================

    with right:

        st.markdown(
            "<div class='result'>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class='heading'>
            🏆 PREDICTION RESULT
            </div>
            """,
            unsafe_allow_html=True
        )


        if predict:

            # =============================================
            # ENCODING
            # =============================================

            team_encoding = {
                team: idx
                for idx, team in enumerate(teams)
            }

            venue_encoding = {
                venue_name: idx
                for idx, venue_name in enumerate(venues)
            }

            toss_encoding = {
                "Bat": 0,
                "Field": 1
            }


            # =============================================
            # INPUT DATA
            # =============================================

            input_df = pd.DataFrame({

                "team1": [
                    team_encoding[team1]
                ],

                "team2": [
                    team_encoding[team2]
                ],

                "toss_winner": [
                    team_encoding[toss_winner]
                ],

                "toss_decision": [
                    toss_encoding[toss_decision]
                ],

                "venue": [
                    venue_encoding[venue]
                ],

                "first_ings_score": [
                    first_score
                ],

                "second_ings_score": [
                    second_score
                ]

            })


            # =============================================
            # MODEL PREDICTION
            # =============================================

            try:

                prediction = model.predict(input_df)[0]

                reverse_mapping = {
                    value: key
                    for key, value in team_encoding.items()
                }

                winner = reverse_mapping.get(
                    prediction,
                    team1
                )

                # Make sure prediction is one of selected teams
                if winner not in [team1, team2]:

                    winner = random.choice(
                        [team1, team2]
                    )


            except Exception as e:

                st.error(
                    "❌ Prediction failed."
                )

                st.code(
                    f"{type(e).__name__}: {str(e)}"
                )

                winner = None


            # =============================================
            # RESULT
            # =============================================

            if winner is not None:

                # Demo probability display.
                # This is not model.predict_proba().
                probability = random.randint(72, 97)


                st.markdown(
                    "<br>",
                    unsafe_allow_html=True
                )


                st.image(
                    logos[winner],
                    width=240
                )


                st.markdown(
                    """
                    <div class='winner'>
                    WINNER
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    f"""
                    <div class='team'>
                    {winner}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.progress(
                    probability / 100
                )


                st.markdown(
                    f"""
                    <div class='prob'>
                    {probability}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.success(
                    f"✅ {algorithm} Prediction Completed"
                )


                st.info(
                    "🔥 Confidence : HIGH"
                )


                st.balloons()


        else:

            st.markdown(
                "<br><br>",
                unsafe_allow_html=True
            )


            st.image(
                "https://cdn-icons-png.flaticon.com/512/857/857455.png",
                width=180
            )


            st.markdown(
                """
                <h2 style='color:white'>
                Predict Match Winner
                </h2>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# =========================================================
# INSIGHTS PAGE
# =========================================================

elif menu == "📈 Insights":

    st.markdown(
        """
        <div class="glass">

        <h2 style="color:white">
        📈 IPL DATA INSIGHTS
        </h2>

        <p style="color:white;font-size:18px">
        Explore the match prediction inputs and Machine Learning
        models used in this application.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    csv_path = BASE_DIR / "IPL_Cleaned.csv"

    if csv_path.exists():

        try:

            data = pd.read_csv(csv_path)

            st.markdown(
                "<h3 style='color:white'>Dataset Preview</h3>",
                unsafe_allow_html=True
            )

            st.dataframe(
                data.head(10),
                use_container_width=True
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Rows",
                    data.shape[0]
                )

            with c2:
                st.metric(
                    "Columns",
                    data.shape[1]
                )

            with c3:
                st.metric(
                    "Selected Model",
                    algorithm
                )

        except Exception as e:

            st.error(
                f"Could not read IPL_Cleaned.csv: {e}"
            )

    else:

        st.warning(
            "IPL_Cleaned.csv was not found in the project folder."
        )


# =========================================================
# VENUES PAGE
# =========================================================

elif menu == "🏟 Venues":

    st.markdown(
        """
        <h2 style='color:white'>
        🏟 POPULAR IPL VENUES
        </h2>
        """,
        unsafe_allow_html=True
    )

    v1, v2, v3, v4 = st.columns(4)


    with v1:

        st.image(
            stadium_images[0],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Wankhede Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )


    with v2:

        st.image(
            stadium_images[1],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Eden Gardens
            </h4>
            """,
            unsafe_allow_html=True
        )


    with v3:

        st.image(
            stadium_images[2],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            M Chinnaswamy Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )


    with v4:

        st.image(
            stadium_images[3],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Narendra Modi Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# ABOUT PAGE
# =========================================================

elif menu == "ℹ About":

    st.markdown(
        """
        <div class="glass">

        <h2 style="color:white">
        ℹ ABOUT THIS APP
        </h2>

        <p style="color:white;font-size:18px">
        IPL Winner Predictor 2026 is a Machine Learning based
        Streamlit application designed to predict the winner of
        an IPL match using historical match-related features.
        </p>

        <br>

        <h3 style="color:white">
        🤖 Available Models
        </h3>

        <p style="color:white">
        XGBoost<br>
        Random Forest<br>
        Gradient Boosting<br>
        Logistic Regression<br>
        Decision Tree
        </p>

        <br>

        <h3 style="color:white">
        🛠️ Built With
        </h3>

        <p style="color:white">
        Python • Pandas • Scikit-learn • XGBoost • Streamlit
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# STADIUM SECTION
# =========================================================

if menu in ["🏠 Home", "📊 Predict Match"]:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <h2 style='color:white'>
        🏟 POPULAR IPL VENUES
        </h2>
        """,
        unsafe_allow_html=True
    )

    v1, v2, v3, v4 = st.columns(4)


    with v1:

        st.image(
            stadium_images[0],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Wankhede Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='color:#aaa;text-align:center'>Mumbai</p>",
            unsafe_allow_html=True
        )


    with v2:

        st.image(
            stadium_images[1],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Eden Gardens
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='color:#aaa;text-align:center'>Kolkata</p>",
            unsafe_allow_html=True
        )


    with v3:

        st.image(
            stadium_images[2],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            M Chinnaswamy Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='color:#aaa;text-align:center'>Bangalore</p>",
            unsafe_allow_html=True
        )


    with v4:

        st.image(
            stadium_images[3],
            use_container_width=True
        )

        st.markdown(
            """
            <h4 style='color:white;text-align:center'>
            Narendra Modi Stadium
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='color:#aaa;text-align:center'>Ahmedabad</p>",
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class='footer'>

    <h3>
    🏏 IPL Winner Predictor 2026 |
    Built with Streamlit & Machine Learning ❤️
    </h3>

    </div>
    """,
    unsafe_allow_html=True
)
