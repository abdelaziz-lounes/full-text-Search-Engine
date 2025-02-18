import streamlit as st
from main import load_data, build_inverted_index, search
from process_data import preprocess_text
from math import ceil

# File path
PROCESSED_DATA_FILE = "./data/processed_data.json"

# Load data and build index
data = load_data(PROCESSED_DATA_FILE)
inverted_index = build_inverted_index(data)

# Custom CSS for styling
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .result-box {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .pagination {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI
st.title("🔍 Full-Text Search Engine")

# Initialize session state for pagination
if "page" not in st.session_state:
    st.session_state.page = 1  # Stores the current page

# Search input
query = st.text_input("Enter search query:", placeholder="Type a word or phrase...", key="search")

# Pagination settings
RESULTS_PER_PAGE = 5  # Number of results per page

if query:
    results = search(query, inverted_index, data, preprocess_text)
    num_results = len(results)
    total_docs = len(data)
    match_percentage = (num_results / total_docs) * 100

    # Display results count and progress bar
    st.markdown(f"<div class='big-font'>Number of results found: {num_results}</div>", unsafe_allow_html=True)
    st.progress(match_percentage / 100)

    # Calculate total pages
    total_pages = ceil(num_results / RESULTS_PER_PAGE) # ceil function from the math module to round up to the nearest whole number

    # Pagination controls at the bottom
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("Previous"):
                if st.session_state.page > 1:
                    st.session_state.page -= 1

        with col2:
            st.markdown(f"<div class='pagination'>Page {st.session_state.page} of {total_pages}</div>", unsafe_allow_html=True)

        with col3:
            if st.button("Next"):
                if st.session_state.page < total_pages:
                    st.session_state.page += 1

    # Calculate start and end indices for the current page
    start = (st.session_state.page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    # Display results for the current page
    for res in results[start:end]:
        st.markdown(f"""
            <div class='result-box'>
                <h3>📄 Document ID: {res['id']}</h3>
                <p>{res['original']}</p>
            </div>
        """, unsafe_allow_html=True)
                                
# Add a footer
st.markdown("---")
st.markdown("Built with ❤️ by Abdelaziz LOUNES")
