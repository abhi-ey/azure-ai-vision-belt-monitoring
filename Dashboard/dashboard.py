import streamlit as st
import pandas as pd
import altair as alt

# Set page configuration
st.set_page_config(page_title="Conveyor Belt Analytics", layout="wide")

# Load and preprocess data
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except FileNotFoundError:
        st.error(f"File not found at {file_path}. Please upload a valid file.")
        st.stop()
    return df


file_path = "conveyor_belt_carryback_dataset.xlsx"
uploaded_file = st.sidebar.file_uploader("Upload Conveyor Data", type=["xlsx"])
df = load_data(uploaded_file if uploaded_file else file_path)

# Sidebar Navigation with Buttons
st.sidebar.title("Navigation")

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "Overview"

# Navigation buttons
if st.sidebar.button("Overview"):
    st.session_state.page = "Overview"
if st.sidebar.button("Analytics"):
    st.session_state.page = "Analytics"

# --- Overview Page ---
if st.session_state.page == "Overview":
    st.title("Overview: Conveyor Belt Carryback")
    
    # Calculate aggregate info
    total_sections = df["Section_ID"].nunique()
    carryback_sections = df[df["Carryback_Area"] > 0]["Section_ID"].nunique()
    carryback_coverage = (carryback_sections / total_sections) * 100
    
    # Display summary metrics
    st.markdown(
        """
        <div style="padding: 10px; background-color: #f1f1f1; border-radius: 10px; text-align: center;">
            <h3 style="color: #0078D7;">Aggregate Metrics</h3>
            <p><strong>Total Sections:</strong> {total_sections}</p>
            <p><strong>Sections with Carryback:</strong> {carryback_sections}</p>
            <p><strong>Carryback Coverage:</strong> {carryback_coverage:.2f}%</p>
        </div>
        """.format(
            total_sections=total_sections,
            carryback_sections=carryback_sections,
            carryback_coverage=carryback_coverage,
        ),
        unsafe_allow_html=True,
    )

    # Optional chart
    st.subheader("Carryback Distribution")
    carryback_chart = alt.Chart(df[df["Carryback_Area"] > 0]).mark_bar().encode(
        x=alt.X("Section_ID:N", title="Section ID"),
        y=alt.Y("Carryback_Area:Q", title="Total Carryback Area"),
        tooltip=["Section_ID", "Carryback_Area"]
    ).properties(
        width=800,
        height=400,
        title="Total Carryback Area by Section"
    )
    st.altair_chart(carryback_chart)

# --- Analytics Page ---
elif st.session_state.page == "Analytics":
    st.title("Analytics: Belt and Section Insights")
    
        # Hardcoded belt options
    st.subheader("Select a Belt")

    # Styling for buttons
    st.markdown(
        """
        <style>
            .button-container {
                display: flex;
                gap: 10px;
            }
            .button {
                padding: 10px 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
                border: none;
                cursor: pointer;
            }
            .red-button {
                background-color: #FF4B4B;
            }
            .green-button {
                background-color: #4CAF50;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Define belt options
    belt_options = [
        {"name": "Crusher-Transport Belt", "color": "red"},
        {"name": "South Transport Belt", "color": "green"},
        {"name": "North Transport Belt", "color": "green"},
    ]

    # Initialize selected belt
    selected_belt = None

    # Render buttons for each belt
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    for belt in belt_options:
        if st.button(
            label=belt["name"],
            key=belt["name"],  # Unique key for each button
        ):
            selected_belt = belt["name"]
    st.markdown("</div>", unsafe_allow_html=True)

    # Display the selected belt
    if selected_belt:
        st.markdown(
            f"""
            <div style="padding: 10px; background-color: #e8f4fc; border-radius: 10px; text-align: center;">
                <h4 style="color: #0078D7;">{selected_belt}</h4>
                <p>This data pertains to Belt 1 (hardcoded).</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Filter sections with carryback
    carryback_sections = df[df["Carryback_Area"] > 0]["Section_ID"].unique()

    st.subheader("Sections with Carryback")
    if len(carryback_sections) > 0:
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
            {''.join([f'<div style="padding: 10px; background-color: #e8f4fc; border-radius: 5px; border: 1px solid #cce7ff; text-align: center;">Section {section}</div>' for section in carryback_sections])}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.write("No sections with carryback detected.")

    # Analytics for sections
    st.subheader("Section Insights")
    sections = df["Section_ID"].unique()
    selected_section = st.selectbox("Select Section", [None] + list(sections))
    
    if selected_section:
        if selected_section:
            section_df = df[df["Section_ID"] == selected_section]
            st.subheader(f"Carryback Analytics for Section {selected_section}")
            
            # Define the threshold value
            threshold_value = 300  # Replace with your desired threshold

            # Base chart for carryback data
            carryback_chart = alt.Chart(section_df).mark_line().encode(
                x="Timestamp:T",
                y="Carryback_Area:Q",
                tooltip=["Timestamp", "Carryback_Area"]
            ).properties(
                width=800,
                height=400,
                title=f"Carryback Area Over Time for Section {selected_section}"
            )

            # Add a horizontal rule for the threshold
            threshold_line = alt.Chart(pd.DataFrame({"Threshold": [threshold_value]})).mark_rule(color="red", strokeDash=[4, 4]).encode(
                y="Threshold:Q"
            )

            # Combine the carryback chart and the threshold line
            combined_chart = carryback_chart + threshold_line

            st.altair_chart(combined_chart)

    else:
        st.write("Select a section to view detailed analytics.")
