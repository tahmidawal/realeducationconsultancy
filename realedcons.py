import streamlit as st
import pandas as pd

# Load the course data
@st.cache_data
def load_data():
    df = pd.read_csv('Shuffled_Course_Details_UK_Ireland.csv')
    return df

df = load_data()

# Initialize session state
if 'loaded_count' not in st.session_state:
    st.session_state.loaded_count = 25

# Title and description
st.title('🎓 Course Finder App')
st.markdown("""
    Welcome to the Course Finder App! Use the filters in the sidebar to find courses 
    that match your preferences from various providers across the UK and Ireland.
""")

# Sidebar filters
st.sidebar.header('Filter Courses')
st.sidebar.markdown('Use the filters below to narrow down your search.')

majors = st.sidebar.multiselect(
    'Select Majors', 
    options=df['Subjects'].unique(), 
    default=None, 
    help='Choose one or more subjects of interest.'
)
providers = st.sidebar.multiselect(
    'Select Providers', 
    options=df['Provider'].unique(), 
    default=None, 
    help='Select the institutions providing the courses.'
)
study_options = st.sidebar.multiselect(
    'Select Study Options', 
    options=df['Study Options'].unique(), 
    default=None, 
    help='Pick your preferred study mode (e.g., Full-time, Part-time).'
)
academic_year = st.sidebar.multiselect(
    'Select Academic Year', 
    options=df['Academic Year'].unique(), 
    default=None, 
    help='Specify the academic year for the courses.'
)

# Apply filters
filtered_df = df

if majors:
    filtered_df = filtered_df[filtered_df['Subjects'].isin(majors)]

if providers:
    filtered_df = filtered_df[filtered_df['Provider'].isin(providers)]

if study_options:
    filtered_df = filtered_df[filtered_df['Study Options'].isin(study_options)]

if academic_year:
    filtered_df = filtered_df[filtered_df['Academic Year'].isin(academic_year)]

st.markdown(f'### Total Courses Found: {len(filtered_df)}')

# Display filtered data in a card format
def display_course_card(course):
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
        <h4>{course['Course Title']}</h4>
        <p><strong>Provider:</strong> {course['Provider']}</p>
        <p><strong>Subjects:</strong> {course['Subjects']}</p>
        <p><strong>Study Options:</strong> {course['Study Options']}</p>
        <p><strong>Academic Year:</strong> {course['Academic Year']}</p>
    </div>
    """, unsafe_allow_html=True)

# Determine the number of courses to display
num_courses_to_display = st.session_state.loaded_count

# Display courses in a grid format
num_cols = 3
cols = st.columns(num_cols)
for i, (index, course) in enumerate(filtered_df.iterrows()):
    if i >= num_courses_to_display:
        break
    col = cols[i % num_cols]
    with col:
        display_course_card(course)

# Load more button
if num_courses_to_display < len(filtered_df):
    if st.button('Load More'):
        st.session_state.loaded_count += 25
        st.experimental_rerun()

# Additional course details
with st.expander('Show Raw Data'):
    st.write(df)

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        Developed with ❤️ using Streamlit
    </div>
""", unsafe_allow_html=True)
