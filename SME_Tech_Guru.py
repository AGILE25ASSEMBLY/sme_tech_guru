# SME_Tech_Guru.py
import streamlit as st
import pandas as pd
import pickle
import os
import re

# --- Configuration ---
PICKLE_FILENAME = 'faculty_data.pkl'
APP_NAME = "SME Tech Guru"
COMPANY_NAME = "Agile Assembly"
MOTTO = "A Prince Campus Company"

# --- Streamlit Page Configuration ---
st.set_page_config(
    layout="wide", # Use wide layout for more content space
    page_title=APP_NAME,
    page_icon="💡",
    initial_sidebar_state="collapsed" # Start with sidebar collapsed
)

# --- Data Loading and Processing Function ---
@st.cache_data(ttl=3600) # Cache data for 1 hour to reduce file reads and processing
def load_faculty_data():
    """
    Loads faculty data from a pickle file and extracts unique specializations.
    Returns: Tuple (DataFrame, List of unique specializations)
    """
    if not os.path.exists(PICKLE_FILENAME):
        st.error(f"⚠️ Data file '{PICKLE_FILENAME}' not found. Please run `01_prepare_data.py`.")
        return pd.DataFrame(), []

    try:
        with open(PICKLE_FILENAME, 'rb') as f:
            df = pickle.load(f)

        # --- Extract Unique Specializations ---
        all_individual_specializations = set()
        if 'specialization' in df.columns:
            for specialization_str in df['specialization'].dropna():
                # Split by comma and optional spaces, handle potential empty strings after split
                specs = [s.strip() for s in re.split(r',\s*', specialization_str) if s.strip()]
                all_individual_specializations.update(specs)

        unique_specializations_list = sorted(list(all_individual_specializations))
        return df, unique_specializations_list
    except Exception as e:
        st.error(f"🐛 Error loading data: {e}. Try regenerating `faculty_data.pkl`.")
        return pd.DataFrame(), []

# --- Custom Styling (Inline CSS for finer control) ---
st.markdown("""
<style>
/* Adjusts spacing around main content */
.st-emotion-cache-nahz7x { /* This class name is specific to Streamlit's internal CSS */
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* Adjusts block container padding */
.st-emotion-cache-czk5ss { /* This class name is specific to Streamlit's internal CSS */
    padding: 1.5rem 2rem 1rem;
    border-radius: 10px; /* Slightly rounded corners for containers */
    box-shadow: 0 4px 8px rgba(0,0,0,0.05); /* Subtle shadow */
}
/* Main titles */
.main-title {
    font-size: 3.8rem;
    font-weight: 800;
    color: #4CAF50; /* Primary green from theme */
    text-align: center;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.15); /* More prominent shadow */
    margin-bottom: 0.8rem;
    letter-spacing: 0.05em; /* Slightly spaced letters */
}
.tagline {
    font-size: 1.6rem;
    font-weight: 600;
    color: #FFC107; /* Secondary yellow/gold */
    text-align: center;
    margin-top: -0.5rem;
    margin-bottom: 2.5rem;
    font-style: italic;
}
/* Section headers */
.section-header {
    font-size: 2.2rem; /* Larger section headers */
    font-weight: 700;
    color: #2196F3; /* A bright blue for emphasis */
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    border-bottom: 3px solid #E0E0E0; /* Thicker, subtle underline */
    padding-bottom: 0.8rem;
    text-align: center; /* Center section headers */
}
/* Widget labels */
.stMultiSelect label, .stCheckbox label, .stTextInput label {
    font-weight: bold;
    color: #3F51B5; /* Indigo for labels */
    font-size: 1.1rem; /* Slightly larger labels */
}
/* Table styling for better readability */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1.5rem;
    margin-bottom: 2.5rem; /* ADDED: More space after each table */
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08); /* Shadow for the table */
    border-radius: 8px; /* Rounded corners for the table */
    overflow: hidden; /* Ensures rounded corners apply to content */
}
th {
    background-color: #e0e0e0; /* Light gray from theme's secondary background */
    color: #333;
    font-weight: bold;
    padding: 12px 18px; /* More padding */
    text-align: left;
    border-bottom: 2px solid #bdbdbd; /* Slightly darker border */
    font-size: 1.05rem; /* Slightly larger header font */
}
td {
    padding: 12px 18px; /* More padding */
    border-bottom: 1px solid #eeeeee;
    font-size: 0.98rem; /* Slightly larger content font */
    color: #444;
    vertical-align: top; /* Align content to top for multi-line cells */
    line-height: 1.4; /* Better line spacing for text */
}
tr:nth-child(even) {
    background-color: #fcfcfc; /* Very light subtle zebra striping */
}
tr:hover {
    background-color: #e3f2fd; /* Light blue on hover for rows */
}
/* Specific fix for the first empty header cell if index is not named correctly by to_html */
.dataframe th:first-child {
    background-color: #e0e0e0 !important; /* Ensure first header cell has background */
}
/* Hide Streamlit footer and menu button for a cleaner look */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# --- Main Application Logic ---
def main():
    # --- Header Section ---
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:#607D8B; font-weight: 500;'>Prince Campus Company </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:#607D8B; font-weight: 500;'> AGILE ASSEMBLY </p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:1.2rem; color:#607D8B; font-weight: 500;'>Proudly presents </p>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='main-title'> {APP_NAME} </h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='tagline'>✨ Driving Innovation, Empowering Minds ✨</p>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px; font-size: 1.15rem; color: #555;">
        Welcome, brilliant minds! This platform connects you with our esteemed faculty experts.<br>
        Find your perfect mentor for research, projects, or just sparking new ideas!
    </div>
    """, unsafe_allow_html=True)

    #st.markdown("---") # Visual separator

    # --- Load Data ---
    faculty_df, unique_specializations = load_faculty_data()

    if faculty_df.empty:
        st.error("🚨 Critical Error: Faculty data could not be loaded. Please check your data source and `01_prepare_data.py` script.")
        return # Exit if no data is loaded

    # --- Search & Filter Section (Encased in a container for visual grouping) ---
    with st.container(border=True): # Use a container with a border
        st.markdown("<h2 class='section-header'>🔍 Discover Your Expert!</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns([3, 1])

        with col1:
            selected_specializations = st.multiselect(
                "📚 **Filter by Specialization** (Choose one or more areas of expertise):",
                options=unique_specializations,
                placeholder="Select specializations...",
                help="Start typing or select specific technology areas to find faculty.",
                key="specialization_selector" # Unique key for widget
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True) # Space for alignment
            filter_currently_teaching = st.checkbox(
                "✅ Show only faculty currently teaching in their specialization",
                value=True,
                help="Toggle to include faculty who may not be actively teaching in their specialization.",
                key="teaching_checkbox" # Unique key for widget
            )

        faculty_name_search = st.text_input(
            "👤 **Search by Faculty Name** :",
            placeholder="Enter faculty name or part of it...",
            key="name_search_input" # Unique key for widget
        ).lower().strip()

        st.markdown("---") # Separator within the search container
        st.info("💡 **Tip:** Combine specialization filters with a faculty name search for precise results. Results will match ALL active criteria.")

    # --- Data Filtering Logic ---
    filtered_results_df = faculty_df.copy()

    # Apply 'currently_teaching' filter
    if filter_currently_teaching:
        filtered_results_df = filtered_results_df[
            filtered_results_df['currently_teaching'] == 'Yes'
        ]

    # Apply multi-select specialization filter
    if selected_specializations:
        selected_specs_lower = [s.lower() for s in selected_specializations]
        mask_specialization = filtered_results_df['specialization'].apply(
            lambda x: any(s_lower in str(x).lower() for s_lower in selected_specs_lower)
        )
        filtered_results_df = filtered_results_df[mask_specialization]

    # Apply faculty name search filter
    if faculty_name_search:
        filtered_results_df = filtered_results_df[
            filtered_results_df['faculty_name'].str.contains(faculty_name_search, case=False, na=False)
        ]

    # --- Display Results ---
    st.markdown("<h2 class='section-header'>Accelerate Your Research/Idea!</h2>", unsafe_allow_html=True)

    if not filtered_results_df.empty:
        unique_departments = sorted(filtered_results_df['department'].unique())

        for dept in unique_departments:
            st.markdown(f"### ✨ **{dept.upper()} Department Faculty** ✨")
            dept_df = filtered_results_df[filtered_results_df['department'] == dept].copy()

            # Define columns for display with user-friendly names
            display_column_map = {
                'faculty_name': 'Faculty Name',
                'specialization': 'Specialization',
                'research_papers': 'Research Papers',
                'experience': 'Experience',
                'currently_teaching': 'Currently Teaching',
                'google_scholar_link': 'Google Scholar'
            }

            actual_df_columns = [col for col in display_column_map.keys() if col in dept_df.columns]
            display_df = dept_df[actual_df_columns].copy()
            display_df = display_df.rename(columns=display_column_map)

            # Customize 'Google Scholar' column to be clickable HTML
            def make_clickable_link(url):
                if pd.isna(url) or not isinstance(url, str) or not url.strip():
                    return "🚫 N/A"
                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url
                return f'<a href="{url}" target="_blank" style="text-decoration: none; color: #4CAF50; font-weight: bold;">🔗 View Profile</a>'

            if 'Google Scholar' in display_df.columns:
                display_df['Google Scholar'] = display_df['Google Scholar'].apply(make_clickable_link)

            # Display the DataFrame as HTML for styling and clickable links
            st.markdown(
                display_df.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
            # REMOVED: st.markdown("<br>") - This was causing the visible <br> tag.

        st.markdown(f"<p style='text-align:center; font-size:1.1rem; color:#333; margin-top: 20px;'>🎉 Success!!! Found {len(filtered_results_df)} faculty members matching your criteria. Keep exploring! 🎉</p>", unsafe_allow_html=True)

    else:
        st.info("😔 No faculty members found matching your selected criteria. Try broadening your search or adjusting filters.")

    st.markdown("---")
    st.markdown(f"<p style='text-align:center; font-size:1rem; color:#607D8B;'>💡 Powered by <span style='font-weight: bold;'>{COMPANY_NAME}</span>, A Prince Campus Company 💡</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.8rem; color:#B0BEC5;'>Copyright © 2025 Agile Assembly. All rights reserved.</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
