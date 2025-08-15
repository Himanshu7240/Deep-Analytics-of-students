import pandas as pd
import os
from collections import defaultdict
from datetime import datetime

print("--- Non-Curricular Skill & Talent Discovery ---")

# --- Step 1: Define Talent Signatures ---
# This section acts as the "brain" of our talent scout.
# We define keywords to categorize activities and identify leadership roles.

TALENT_CLUSTERS = {
    'Athletic': ['Sports', 'Cricket', 'Football', 'Basketball', 'Athlete'],
    'Artistic/Creative': ['Art Club', 'Music', 'Violin', 'Drama Club', 'Newspaper', 'Literary', 'Writer', 'Author'],
    'STEM/Analytical': ['Science Club', 'Coding Club', 'Robotics', 'Science Olympiad', 'Chess Club', 'Physics', 'Chemist'],
    'Leadership/Public Speaking': ['Debate Club', 'Model UN', 'Student Government', 'Economics Club', 'Editor', 'Captain', 'Leader', 'Mentor']
}

LEADERSHIP_KEYWORDS = ['Captain', 'Leader', 'Mentor', 'Editor']

# --- Step 2: Path Detection Function ---
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from talent_discovery subdirectory
        './data/'          # If data is in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

# --- Step 3: Load and Prepare Data ---
print("\nStep 2: Loading and preparing student engagement data...")

# Auto-detect data path
base_path = find_data_directory()
if base_path is None:
    print("Error: Data directory not found!")
    print("Please ensure the 'data' folder is accessible.")
    exit()

print(f"Found data directory at: {base_path}")

try:
    df_engagement = pd.read_csv(base_path + 'engagement_behavioral.csv')
    df_students = pd.read_csv(base_path + 'student_master.csv')
    print("Data loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: Could not find required data files. Please check the data directory.")
    print(f"Details: {e}")
    exit()

# Merge to get student names
df_analysis = pd.merge(df_engagement, df_students[['student_id', 'first_name', 'last_name']], on='student_id')

# Filter out records with no activity and handle NaN values
df_analysis = df_analysis.dropna(subset=['extracurricular_activity'])
df_analysis = df_analysis[df_analysis['extracurricular_activity'] != 'None'].copy()
df_analysis = df_analysis[df_analysis['extracurricular_activity'] != ''].copy()

print(f"Data prepared. {len(df_analysis)} valid activity records found.")

if df_analysis.empty:
    print("No valid extracurricular activities found. Exiting.")
    exit()

# --- Step 4: Analyze Each Student's Activity History ---
print("\nStep 3: Analyzing student records for talent signals...")

# A dictionary to hold our findings for each student
student_talents = defaultdict(lambda: {
    'name': '',
    'activities': set(),
    'potential_talents': set(),
    'leadership_evidence': [],
    'consistency_evidence': []
})

# Process each record
for _, row in df_analysis.iterrows():
    student_id = row['student_id']
    name = f"{row['first_name']} {row['last_name']}"
    activity = str(row['extracurricular_activity']).strip()

    if not activity or activity.lower() in ['none', 'nan', '']:
        continue

    student_talents[student_id]['name'] = name
    student_talents[student_id]['activities'].add(activity)

    # Check for talent clusters
    for talent, keywords in TALENT_CLUSTERS.items():
        if any(keyword.lower() in activity.lower() for keyword in keywords):
            student_talents[student_id]['potential_talents'].add(talent)

    # Check for leadership keywords
    for keyword in LEADERSHIP_KEYWORDS:
        if keyword.lower() in activity.lower():
            student_talents[student_id]['leadership_evidence'].append(f"'{activity}'")

# Check for consistency (participation over multiple terms)
consistency_check = df_analysis.groupby('student_id')['extracurricular_activity'].nunique()
for student_id, count in consistency_check.items():
    # This is a simple check; a more complex one could track the same activity over time
    if count > 1 or len(student_talents[student_id]['activities']) > 1:
         student_talents[student_id]['consistency_evidence'].append("Shows consistent engagement in extracurriculars.")

print("Analysis complete.")

# --- Step 5: Generate the Final Report ---
print("\nStep 4: Generating Talent Discovery Report...")

report_data = []
for student_id, data in student_talents.items():
    if not data['potential_talents']:
        continue

    evidence = []
    if data['leadership_evidence']:
        evidence.append(f"Leadership Role(s): {', '.join(data['leadership_evidence'])}")
    if data['consistency_evidence']:
        evidence.append(data['consistency_evidence'][0])
    
    report_data.append({
        'Student ID': student_id,
        'Name': data['name'],
        'Potential Talent(s)': ', '.join(sorted(list(data['potential_talents']))),
        'Evidence': '; '.join(evidence) if evidence else 'General Participation'
    })

if not report_data:
    print("No specific non-curricular talents were identified based on the defined rules.")
else:
    df_report = pd.DataFrame(report_data)
    df_report = df_report.sort_values('Name').reset_index(drop=True)
    print("\n--- Non-Curricular Talent & Skill Report ---")
    print(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(df_report.to_string(index=False))

print("\n--- Process Complete ---")