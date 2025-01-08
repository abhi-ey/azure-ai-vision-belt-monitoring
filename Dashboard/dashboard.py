import streamlit as st
import pandas as pd
import altair as alt

############## NOTES ################
# Run this script with: streamlit run dashboard.py
# Install streamlit: pip install streamlit
#####################################

# Page layout
st.set_page_config(page_title="Conveyor Belt Analytics", layout="wide")

# Header
st.markdown(
    """
    <style>
    .header {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
        color: #4a4a4a;
    }
    .sub-header {
        font-size: 18px;
        text-align: center;
        margin-bottom: 30px;
        color: #a1a1a1;
    }
    </style>
    <div class="header">Conveyor Belt Analytics</div>
    <div class="sub-header">Live Monitoring and Predictive Analysis</div>
    """,
    unsafe_allow_html=True,
)

# Add a horizontal line for separation
st.markdown("---")

# Create a three-column layout
left_column, spacer_column, middle_column, right_column = st.columns([1, 0.2, 3, 1.5])

# Left Column: File upload and metrics
with left_column:
    file_path = "conveyor_belt_carryback_dataset.xlsx"  # Default file path
    # Styled file uploader button
    st.markdown(
        """
        <style>
        .file-uploader {
            display: inline-block;
            font-size: 14px;
            padding: 5px 10px;
            background-color: #0078D7;
            color: white;
            border-radius: 5px;
            cursor: pointer;
            text-align: center;
            transition: background-color 0.3s;
        }
        .file-uploader:hover {
            background-color: #005a9e;
        }
        .file-uploader input {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # File uploader
    # File uploader
    uploaded_file = st.file_uploader(" ", type=["xlsx"], label_visibility="collapsed")
    st.markdown(
        """
        <style>
        div.stButton > button {
            padding: 4px 8px;
            font-size: 12px;
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        div.stButton > button:hover {
            background-color: #005a9e;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



    if uploaded_file:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    else:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
        except FileNotFoundError:
            st.error(f"File not found at {file_path}. Please ensure the file exists.")
            st.stop()

    # Filter conveyor belts with carryback
    carryback_df = df[df["Carryback_Area"] > 0]

    # Display box for total sections with carryback
    total_sections_with_carryback = len(carryback_df["Section_ID"].unique())

    st.markdown(
        f"""
        <div style="
            padding: 10px;
            margin-bottom: 10px;
            background-color: #e8f4fc;
            border: 2px solid #cce7ff;
            border-radius: 10px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h5 style="margin: 0; color: #0078D7;">Sections with Carryback</h5>
            <p style="margin: 0; font-size: 16px; font-weight: bold; color: #0078D7;">{total_sections_with_carryback}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # the Section IDs with carryback
    st.write("**Section IDs with Carryback:**")
    sections_with_carryback = carryback_df["Section_ID"].unique()

    if len(sections_with_carryback) > 0:
        # Use markdown to create a styled box
        st.markdown(
            f"""
            <div style="
                padding: 10px;
                margin-bottom: 10px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
            ">
                {'<br>'.join([f"Section {section_id}" for section_id in sections_with_carryback])}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="
                padding: 10px;
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.1);
                color: #555;
            ">
                No sections with carryback.
            </div>
            """,
            unsafe_allow_html=True,
        )


# Middle Column: Graph
with middle_column:
    st.subheader("Belt Analytics")
    if not carryback_df.empty:
        carryback_chart = alt.Chart(carryback_df).mark_line().encode(
            x="Timestamp:T",
            y="Carryback_Area:Q",
            color="Section_ID:N",
            tooltip=["Timestamp", "Section_ID", "Carryback_Area"]
        ).properties(
            width=450,
            height=300,
            title="Carryback Area Over Time"
        )
        st.altair_chart(carryback_chart)
    else:
        st.write("No carryback detected on any conveyor sections.")

# Right Column: Insights
with right_column:
    st.subheader("Insights")
    st.write("- **Days to repair**: 10")
    st.write("- **High-risk sections**: Section 6, Section 10")
    st.write("- **Suggested actions**: Regular inspections")
