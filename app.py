import streamlit as st
import pandas as pd
import os
from pathlib import Path

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Financial Contagion Network",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# PROJECT TITLE
# ============================================================

st.title("📊 Financial Contagion Network Analysis")

st.markdown("""
### SVD-Based Cross-Market Contagion Analysis with DeFi Extension

This dashboard presents the results of a financial contagion analysis
using rolling correlation networks, Singular Value Decomposition (SVD),
Marchenko–Pastur filtering, contagion centrality and TradFi–DeFi comparison.
""")

st.divider()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

BASE_DIR = Path(__file__).parent


def load_csv(filename):
    """Load a CSV file safely."""
    path = BASE_DIR / filename

    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return None

    return None


def show_image(filename, caption=None):
    """Display an image if it exists."""
    path = BASE_DIR / filename

    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"{filename} not found.")


# ============================================================
# LOAD DATA
# ============================================================

final_summary = load_csv("final_summary.csv")
final_events = load_csv("final_event_results.csv")
final_centrality = load_csv("final_centrality_summary.csv")

normalized_data = load_csv("normalized_tradfi_vs_defi.csv")
event_comparison = load_csv("normalized_event_comparison.csv")

contagion = load_csv("contagion_centrality.csv")
spectral_summary = load_csv("spectral_network_summary.csv")

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Analysis",
    [
        "Overview",
        "Systemic Risk",
        "Contagion Centrality",
        "TradFi vs DeFi",
        "Event Validation",
        "Project Results"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    # Number of assets
    num_assets = 25

    # Number of observations
    observations = "—"

    if normalized_data is not None:
        observations = len(normalized_data)

    col1.metric(
        "Assets",
        num_assets
    )

    col2.metric(
        "Analysis Observations",
        observations
    )

    col3.metric(
        "TradFi Assets",
        12
    )

    col4.metric(
        "DeFi/Crypto Assets",
        13
    )

    st.divider()

    st.subheader("Methodology")

    st.markdown("""
    The analysis follows these major stages:

    **1. Data Collection**
    
    Daily financial-market and DeFi data are collected.

    **2. Preprocessing**
    
    Price series are transformed into returns and DeFi TVL series
    into growth measures.

    **3. GARCH Filtering**
    
    Volatility clustering is filtered before correlation estimation.

    **4. Rolling Correlation**
    
    A 90-day rolling correlation structure is estimated.

    **5. SVD / Spectral Decomposition**
    
    Singular Value Decomposition identifies dominant systemic modes.

    **6. Marchenko–Pastur Filtering**
    
    Noise-dominated singular modes are removed.

    **7. Spectral Network**
    
    The retained modes are used to construct the financial contagion network.

    **8. Contagion Centrality**
    
    Assets are evaluated according to their position in the systemic network.

    **9. DeFi Extension**
    
    Crypto assets, stablecoins and DeFi TVL variables are incorporated.

    **10. Event Validation**
    
    The framework is evaluated around major financial and crypto stress events.
    """)

    st.divider()

    st.subheader("Project Architecture")

    st.code("""
    Financial Data
          ↓
    Preprocessing
          ↓
    GARCH Filtering
          ↓
    Rolling Correlation
          ↓
    SVD
          ↓
    Marchenko–Pastur Filtering
          ↓
    Spectral Network
          ↓
    Contagion Centrality
          ↓
    Event Validation
          ↓
    TradFi vs TradFi + DeFi
          ↓
    Final Results
    """, language="text")


# ============================================================
# SYSTEMIC RISK
# ============================================================

elif page == "Systemic Risk":

    st.header("📈 Systemic Risk Analysis")

    st.write(
        "The leading singular value represents the dominant systemic "
        "mode of the financial network."
    )

    # Leading singular value plot
    show_image(
        "final_leading_singular_value.png",
        "Leading Singular Value Over Time"
    )

    st.divider()

    st.subheader("Systemic Mode")

    show_image(
        "final_systemic_mode.png",
        "Systemic Mode Contribution"
    )

    st.divider()

    st.subheader("Network Strength")

    show_image(
        "final_network_strength.png",
        "Financial Network Strength Over Time"
    )

    if spectral_summary is not None:

        st.subheader("Spectral Network Summary")

        st.dataframe(
            spectral_summary,
            use_container_width=True
        )


# ============================================================
# CONTAGION CENTRALITY
# ============================================================

elif page == "Contagion Centrality":

    st.header("🔗 Contagion Centrality")

    st.write("""
    Contagion centrality measures the importance of each asset
    within the spectral financial network.
    """)

    if contagion is not None:

        st.subheader("Centrality Data")

        st.dataframe(
            contagion.head(100),
            use_container_width=True
        )

        # Find asset columns
        numeric_columns = contagion.select_dtypes(
            include="number"
        ).columns.tolist()

        if len(numeric_columns) > 0:

            st.subheader("Average Contagion Centrality")

            mean_values = (
                contagion[numeric_columns]
                .mean()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                mean_values.head(15)
            )

    else:

        st.warning(
            "contagion_centrality.csv was not found."
        )


# ============================================================
# TRADFI VS DEFI
# ============================================================

elif page == "TradFi vs DeFi":

    st.header("🌐 TradFi vs TradFi + DeFi")

    st.markdown("""
    This section compares the financial network using:

    - TradFi assets only
    - TradFi + Crypto/DeFi assets

    The comparison helps evaluate the incremental effect of
    DeFi-related variables on the systemic network.
    """)

    if normalized_data is not None:

        st.subheader("Comparison Data")

        st.dataframe(
            normalized_data.head(100),
            use_container_width=True
        )

        # Identify important columns automatically
        cols = normalized_data.columns.tolist()

        st.subheader("Normalized Comparison")

        numeric_cols = normalized_data.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            selected_cols = st.multiselect(
                "Select variables",
                numeric_cols,
                default=numeric_cols[:min(3, len(numeric_cols))]
            )

            if selected_cols:

                st.line_chart(
                    normalized_data[selected_cols]
                )

    else:

        st.warning(
            "normalized_tradfi_vs_defi.csv was not found."
        )

    st.divider()

    st.subheader("Leading Mode Comparison")

    show_image(
        "normalized_leading_mode.png",
        "Normalized Leading Systemic Mode"
    )

    st.subheader("Network Strength Comparison")

    show_image(
        "normalized_network_strength.png",
        "Normalized Network Strength"
    )

    st.subheader("Systemic Mode Comparison")

    show_image(
        "normalized_systemic_mode.png",
        "Normalized Systemic Mode"
    )


# ============================================================
# EVENT VALIDATION
# ============================================================

elif page == "Event Validation":

    st.header("🚨 Historical Event Validation")

    st.markdown("""
    The model is evaluated around major stress events used in the project,
    including:

    - Terra/LUNA collapse
    - FTX collapse
    - USDC depeg
    """)

    if final_events is not None:

        st.subheader("Event Results")

        st.dataframe(
            final_events,
            use_container_width=True
        )

    if event_comparison is not None:

        st.subheader("Normalized Event Comparison")

        st.dataframe(
            event_comparison,
            use_container_width=True
        )

    st.divider()

    st.subheader("Leading Singular Value During Events")

    show_image(
        "event_leading_singular_value.png",
        "Event-Based Leading Singular Value"
    )

    st.subheader("Network Strength During Events")

    show_image(
        "event_network_strength.png",
        "Event-Based Network Strength"
    )

    st.subheader("Systemic Mode During Events")

    show_image(
        "event_systemic_mode.png",
        "Event-Based Systemic Mode"
    )

    st.subheader("Top Contagion Assets")

    show_image(
        "event_top_centrality_assets.png",
        "Top Contagion Assets During Events"
    )


# ============================================================
# PROJECT RESULTS
# ============================================================

elif page == "Project Results":

    st.header("📋 Final Project Results")

    if final_summary is not None:

        st.subheader("Final Summary")

        st.dataframe(
            final_summary,
            use_container_width=True
        )

    if final_centrality is not None:

        st.subheader("Final Centrality Summary")

        st.dataframe(
            final_centrality,
            use_container_width=True
        )

    st.divider()

    st.subheader("Final Report")

    report_path = BASE_DIR / "final_results_report.txt"

    if report_path.exists():

        with open(
            report_path,
            "r",
            encoding="utf-8"
        ) as f:

            report_text = f.read()

        st.text_area(
            "Analysis Report",
            report_text,
            height=500
        )

    else:

        st.warning(
            "final_results_report.txt was not found."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Financial Contagion Networks — SVD of Cross-Market Correlation "
    "with DeFi Extension"
)