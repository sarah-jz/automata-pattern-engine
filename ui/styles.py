
import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* Application hero header */

        .hero-header {
            padding: 12px 0 25px 0;
            margin-bottom: 12px;
        }

        .hero-accent {
            width: 48px;
            height: 4px;
            background: #DC2626;
            border-radius: 4px;
            margin-bottom: 22px;
        }

        .hero-eyebrow {
            color: #EF4444;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }

        .hero-title {
            color: #F5F5F5;
            font-size: 36px;
            font-weight: 750;
            line-height: 1.2;
            margin-bottom: 14px;
        }

        .hero-description {
            color: #A1A1AA;
            font-size: 15px;
            line-height: 1.7;
            max-width: 700px;
        }

        .hero-meta {
            color: #71717A;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 1.4px;
            margin-top: 20px;
        }

        /* Main background */

        .stApp {
            background-color: #0B0B0D;
            color: #F5F5F5;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        /* Sidebar */

        [data-testid="stSidebar"] {
            background-color: #0B0B0D;
            border-right: 1px solid #303036;
        }

        [data-testid="stSidebar"] * {
            color: #E4E4E7;
        }

        /* Headings */

        h1, h2, h3 {
            color: #F5F5F5 !important;
            font-weight: 650 !important;
        }

        /* General text */

        p, label {
            color: #D4D4D8;
        }

        /* Metric cards */

        [data-testid="stMetric"] {
            background-color: #171719;
            border: 1px solid #303036;
            padding: 18px;
            border-radius: 10px;
        }

        [data-testid="stMetricLabel"] {
            color: #A1A1AA !important;
        }

        [data-testid="stMetricValue"] {
            color: #F5F5F5 !important;
        }

        /* Buttons */

        .stButton > button {
            background-color: #B91C1C;
            color: #FFFFFF;
            border: 1px solid #B91C1C;
            border-radius: 7px;
            font-weight: 600;
        }

        .stButton > button:hover {
            background-color: #DC2626;
            color: #FFFFFF;
            border-color: #DC2626;
        }

        /* Input fields */

        .stTextInput input,
        .stTextArea textarea {
            background-color: #171719;
            color: #F5F5F5;
            border: 1px solid #3F3F46;
            border-radius: 7px;
        }

        /* Tabs */

        .stTabs [data-baseweb="tab"] {
            color: #A1A1AA;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            color: #EF4444 !important;
        }

        /* Dividers */

        hr {
            border-color: #303036;
        }

        /* Sidebar pattern builder */

        .sidebar-heading {
            padding: 10px 0 20px 0;
        }

        .sidebar-eyebrow {
            color: #EF4444;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .sidebar-title {
           color: #F5F5F5;
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .sidebar-description {
            color: #A1A1AA;
            font-size: 12px;
            line-height: 1.6;
        }

        .syntax-card {
            background: #171719;
            border: 1px solid #303036;
            border-radius: 9px;
            padding: 14px;
            margin: 8px 0 18px 0;
        }

        .syntax-title {
            color: #71717A;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.2px;
            margin-bottom: 12px;
        }

        .syntax-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 9px 0;
            color: #D4D4D8;
            font-size: 12px;
        }

        .syntax-row code {
            color: #F87171;
            background: #2A1719;
            border-radius: 4px;
            padding: 3px 8px;
            min-width: 35px;
            text-align: center;
        }

        /* Automata visualization */
        .visualization-heading {
            margin: 12px 0 18px 0;
        }

        .visualization-title {
            color: #F5F5F5;
            font-size: 21px;
            font-weight: 700;
           margin-bottom: 6px;
        }

        .visualization-description {
            color: #A1A1AA;
            font-size: 13px;
            line-height: 1.6;
        }


        </style>
        """,
        unsafe_allow_html=True
    )
