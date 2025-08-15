import pandas as pd
import os
from collections import defaultdict
from datetime import datetime

print("--- Future Career & Stream Suggestion Engine ---")

# --- Step 1: Define the Career Cluster "Knowledge Base" ---
# This is the core of our expert system. It defines the attributes for different career paths.
# We assign weights to different signals (e.g., stated interest is more important than a single high grade).
CAREER_CLUSTERS = {
    'Engineering & Technology': {
        'strong_subjects': ['Math', 'Science'],
        'relevant_activities': ['Coding Club', 'Robotics', 'Science Olympiad', 'Physics'],
        'stated_interests': ['STEM', 'Technology', 'Engineer', 'IT', 'Software'],
        'weight': {'subject': 3, 'activity': 2, 'interest': 5}
    },
    'Medicine & Healthcare': {
        'strong_subjects': ['Science'],
        'relevant_activities': ['Volunteering', 'Science Club', 'Biology'],
        'stated_interests': ['Healthcare', 'Doctor', 'Nurse', 'Medical', 'Pharmacist'],
        'weight': {'subject': 4, 'activity': 3, 'interest': 5}
    },
    'Business & Finance': {
        'strong_subjects': ['Math', 'Economics'],
        'relevant_activities': ['Debate Club', 'Student Government', 'Economics Club'],
        'stated_interests': ['Business', 'Management', 'Finance', 'Sales', 'Marketing', 'Entrepreneur', 'Analyst'],
        'weight': {'subject': 3, 'activity': 3, 'interest': 5}
    },
    'Arts, Humanities & Law': {
        'strong_subjects': ['English', 'History'],
        'relevant_activities': ['Debate Club', 'Model UN', 'School Newspaper', 'Art Club', 'Drama Club', 'Author'],
        'stated_interests': ['Writing', 'History', 'Arts', 'Law', 'Journalist'],
        'weight': {'subject': 3, 'activity': 3, 'interest': 5}
    }
}
SUBJECT_STRENGTH_THRESHOLD = 80 # A final score above this is considered a strong subject

# --- Step 2: Load All Relevant Student Data ---
print("\nStep 2: Loading holistic student data...")

# Robust path detection for data directory
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from career_suggester subdirectory
        './data/'          # If data is in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found data directory at: {path}")
            return path
    
    raise FileNotFoundError("Data directory not found. Please ensure the 'data/' folder exists.")

# Find the data directory
base_path = find_data_directory()

# Load the datasets
df_students = pd.read_csv(base_path + 'student_master.csv')
df_academic = pd.read_csv(base_path + 'academic_performance.csv')
df_engagement = pd.read_csv(base_path + 'engagement_behavioral.csv')
df_surveys = pd.read_csv(base_path + 'surveys_qualitative.csv')
print("Data loaded.")


# --- Step 3: Define Profiling and Recommendation Functions ---
print("Step 3: Building profiling and recommendation logic...")

def get_student_profile(student_id: str):
    """Creates a holistic profile for a single student."""
    profile = {
        'name': '',
        'strong_subjects': [],
        'activities': [],
        'interests': []
    }
    
    # Get Name
    profile['name'] = df_students.loc[df_students['student_id'] == student_id, 'first_name'].iloc[0]

    # Get Strong Subjects from the latest term
    student_academic = df_academic[df_academic['student_id'] == student_id]
    if not student_academic.empty:
        latest_term = sorted(student_academic['term'].unique())[-1]
        latest_records = student_academic[student_academic['term'] == latest_term]
        profile['strong_subjects'] = list(latest_records[latest_records['final_score'] > SUBJECT_STRENGTH_THRESHOLD]['subject'])
        
    # Get Activities
    student_engagement = df_engagement[df_engagement['student_id'] == student_id]
    profile['activities'] = list(student_engagement[student_engagement['extracurricular_activity'] != 'None']['extracurricular_activity'].unique())

    # Get Stated Interests
    student_surveys = df_surveys[(df_surveys['student_id'] == student_id) & (df_surveys['survey_type'] == 'Career Interest')]
    profile['interests'] = list(student_surveys['response'].unique())
    
    return profile

def generate_recommendations(student_id: str):
    """Scores a student profile against career clusters and provides recommendations."""
    student_profile = get_student_profile(student_id)
    scores = defaultdict(int)

    print("\n" + "="*60)
    print(f"Generating Career & Stream Suggestions for: {student_profile['name']} ({student_id})")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"  -> Academic Strengths: {student_profile['strong_subjects'] or ['None identified']}")
    print(f"  -> Extracurriculars: {student_profile['activities'] or ['None']}")
    print(f"  -> Stated Interests: {student_profile['interests'] or ['None provided']}")
    print("="*60)

    # Score the profile against each career cluster
    for cluster_name, attributes in CAREER_CLUSTERS.items():
        # Score based on strong subjects
        for subject in student_profile['strong_subjects']:
            if subject in attributes['strong_subjects']:
                scores[cluster_name] += attributes['weight']['subject']
        
        # Score based on activities
        for activity in student_profile['activities']:
            if any(keyword.lower() in activity.lower() for keyword in attributes['relevant_activities']):
                scores[cluster_name] += attributes['weight']['activity']
        
        # Score based on stated interests
        for interest in student_profile['interests']:
            if any(keyword.lower() in interest.lower() for keyword in attributes['stated_interests']):
                scores[cluster_name] += attributes['weight']['interest']
    
    if not scores:
        print("Not enough data to generate a specific recommendation. Encourage student to complete career interest surveys.")
        return

    # Sort clusters by score
    ranked_recommendations = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    
    print("\n--- Top Recommended Paths for Exploration ---\n")
    for i, (cluster, score) in enumerate(ranked_recommendations):
        if score > 0:
            print(f"{i+1}. {cluster} (Match Score: {score})")
            print(f"   Why? This path aligns with your strengths in subjects like '{', '.join(CAREER_CLUSTERS[cluster]['strong_subjects'])}'")
            print(f"   and your involvement in activities like '{', '.join(CAREER_CLUSTERS[cluster]['relevant_activities'])}'.\n")
            
# --- Step 4: Run for Sample Students ---
if __name__ == "__main__":
    # Use students that are more likely to have complete data
    test_students = ['STU-001', 'STU-002', 'STU-003']
    
    for student_id in test_students:
        try:
            generate_recommendations(student_id=student_id)
            print("\n" + "-"*60 + "\n")
        except Exception as e:
            print(f"Error processing {student_id}: {str(e)}")
            print("\n" + "-"*60 + "\n")
            continue

    print("\n--- Process Complete ---")