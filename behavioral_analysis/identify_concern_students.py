import pandas as pd
import os
from datetime import datetime

print("--- Behavioral & Emotional Analysis: Early Warning System ---")

# --- Ethical Disclaimer ---
print("""
IMPORTANT: This is not a diagnostic tool. It is an early warning system
to identify students who may benefit from a supportive check-in from a
counselor or teacher. All results must be handled with confidentiality
and care.
""")

# --- Step 1: Define Risk Factors and Scoring System ---
# This is the core logic. Points are assigned for negative changes or events.
# These weights can be adjusted based on professional experience.
CONCERN_SCORE_THRESHOLDS = {
    'ACADEMIC_DROP': {'points': 3, 'threshold': 15}, # Score drop of 15+ points
    'ATTENDANCE_DROP': {'points': 3, 'threshold': 10}, # Attendance drop of 10%+
    'NEW_DISCIPLINARY_INCIDENT': {'points': 2},
    'WITHDREW_FROM_ACTIVITY': {'points': 2},
    'HIGH_STRESS_REPORT': {'points': 4, 'threshold': 4}, # Self-reported stress >= 4 out of 5
    'COUNSELOR_VISIT': {'points': 1} # Not a negative, but indicates a need for support
}
FINAL_SCORE_THRESHOLD = 5 # Students with a total score >= this will be flagged.

# --- Step 2: Path Detection Function ---
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from behavioral_analysis subdirectory
        './data/'          # If data is in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

# --- Step 3: Load and Prepare Data ---
print("\nStep 2: Loading and preparing student data...")

# Auto-detect data path
base_path = find_data_directory()
if base_path is None:
    print("Error: Data directory not found!")
    print("Please ensure the 'data' folder is accessible.")
    exit()

print(f"Found data directory at: {base_path}")

try:
    df_engagement = pd.read_csv(base_path + 'engagement_behavioral.csv')
    df_academic = pd.read_csv(base_path + 'academic_performance.csv')
    df_surveys = pd.read_csv(base_path + 'surveys_qualitative.csv')
    df_students = pd.read_csv(base_path + 'student_master.csv')
    print("Data loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: Could not find required data files. Please check the data directory.")
    print(f"Details: {e}")
    exit()

# --- Step 4: Process Data for Comparison ---
# We need to compare Spring 2025 against Fall 2024
print("Step 3: Comparing Spring 2025 data against Fall 2024 baseline...")

# Handle missing values and ensure numeric columns are properly typed
df_academic['final_score'] = pd.to_numeric(df_academic['final_score'], errors='coerce')
df_engagement['attendance_percentage'] = pd.to_numeric(df_engagement['attendance_percentage'], errors='coerce')
df_engagement['disciplinary_incidents'] = pd.to_numeric(df_engagement['disciplinary_incidents'], errors='coerce')

print(f"Academic records: {len(df_academic)}")
print(f"Engagement records: {len(df_engagement)}")
print(f"Available terms: {df_academic['term'].unique()}")

# Combine key metrics into one dataframe
df_merged = pd.merge(df_academic[['student_id', 'term', 'final_score']],
                     df_engagement[['student_id', 'term', 'attendance_percentage', 'disciplinary_incidents', 'extracurricular_activity', 'counselor_visit']],
                     on=['student_id', 'term'], how='outer')

print(f"Merged records: {len(df_merged)}")

# Filter for the terms we need
df_merged = df_merged[df_merged['term'].isin(['Fall 2024', 'Spring 2025'])]

print(f"Records for required terms: {len(df_merged)}")
print(f"Terms found: {df_merged['term'].unique()}")

if df_merged.empty:
    print("Error: No data found for the required terms (Fall 2024, Spring 2025).")
    exit()

# Pivot the data to have terms as columns for easy comparison
df_pivot = df_merged.pivot_table(index='student_id', columns='term', aggfunc='first')

# Flatten the multi-index columns for easier access
df_pivot.columns = [f'{col[0]}_{col[1]}' for col in df_pivot.columns]
df_pivot.reset_index(inplace=True)

print(f"Data prepared. {len(df_pivot)} students found with data for both terms.")
print(f"Available columns: {df_pivot.columns.tolist()}")

# --- Step 5: Calculate Concern Score for Each Student ---
print("Step 4: Calculating 'Concern Score' for each student...")
results = []

for _, student in df_pivot.iterrows():
    student_id = student['student_id']
    score = 0
    reasons = []

    try:
        # Rule 1: Significant Academic Drop
        fall_score = student.get('final_score_Fall 2024')
        spring_score = student.get('final_score_Spring 2025')
        if pd.notna(fall_score) and pd.notna(spring_score):
            if fall_score - spring_score >= CONCERN_SCORE_THRESHOLDS['ACADEMIC_DROP']['threshold']:
                score += CONCERN_SCORE_THRESHOLDS['ACADEMIC_DROP']['points']
                reasons.append(f"Academic Drop (>{CONCERN_SCORE_THRESHOLDS['ACADEMIC_DROP']['threshold']} pts)")

        # Rule 2: Significant Attendance Drop
        fall_attendance = student.get('attendance_percentage_Fall 2024')
        spring_attendance = student.get('attendance_percentage_Spring 2025')
        if pd.notna(fall_attendance) and pd.notna(spring_attendance):
            if fall_attendance - spring_attendance >= CONCERN_SCORE_THRESHOLDS['ATTENDANCE_DROP']['threshold']:
                score += CONCERN_SCORE_THRESHOLDS['ATTENDANCE_DROP']['points']
                reasons.append(f"Attendance Drop (>{CONCERN_SCORE_THRESHOLDS['ATTENDANCE_DROP']['threshold']}%)")

        # Rule 3: New Disciplinary Incidents
        fall_incidents = student.get('disciplinary_incidents_Fall 2024')
        spring_incidents = student.get('disciplinary_incidents_Spring 2025')
        if pd.notna(fall_incidents) and pd.notna(spring_incidents):
            if spring_incidents > fall_incidents:
                score += CONCERN_SCORE_THRESHOLDS['NEW_DISCIPLINARY_INCIDENT']['points']
                reasons.append("New Disciplinary Incident")

        # Rule 4: Withdrew from Extracurriculars
        fall_activity = student.get('extracurricular_activity_Fall 2024')
        spring_activity = student.get('extracurricular_activity_Spring 2025')
        if pd.notna(fall_activity) and pd.notna(spring_activity):
            if (fall_activity != 'None' and fall_activity != 'nan') and (spring_activity == 'None' or spring_activity == 'nan'):
                score += CONCERN_SCORE_THRESHOLDS['WITHDREW_FROM_ACTIVITY']['points']
                reasons.append("Withdrew from Activities")

        # Rule 5: High Self-Reported Stress (from surveys)
        stress_report = df_surveys[(df_surveys['student_id'] == student_id) & 
                                 (df_surveys['survey_type'] == 'Well-being') & 
                                 (df_surveys['question'].str.contains('stress', na=False))]
        if not stress_report.empty:
            # Get the most recent stress report
            last_stress_value = pd.to_numeric(stress_report['response'].iloc[-1], errors='coerce')
            if pd.notna(last_stress_value) and last_stress_value >= CONCERN_SCORE_THRESHOLDS['HIGH_STRESS_REPORT']['threshold']:
                score += CONCERN_SCORE_THRESHOLDS['HIGH_STRESS_REPORT']['points']
                reasons.append(f"High Self-Reported Stress (Score: {int(last_stress_value)}/5)")

        # Rule 6: Counselor Visit
        spring_counselor = student.get('counselor_visit_Spring 2025')
        if pd.notna(spring_counselor) and spring_counselor == 'Yes':
            score += CONCERN_SCORE_THRESHOLDS['COUNSELOR_VISIT']['points']
            reasons.append("Counselor Visit Logged")
            
    except Exception as e:
        print(f"Warning: Error processing student {student_id}: {e}")
        continue
        
    if score > 0:
        results.append({
            'student_id': student_id,
            'concern_score': score,
            'reasons_for_flag': ', '.join(reasons)
        })

# --- Step 6: Generate the Final Report ---
print("\nStep 5: Generating confidential report of students to check in on...")

if not results:
    print("No students were flagged based on the current rules and data.")
else:
    df_report = pd.DataFrame(results)
    # Merge with student names
    df_report = pd.merge(df_report, df_students[['student_id', 'first_name', 'last_name']], on='student_id')
    # Filter for students meeting the final threshold
    df_report = df_report[df_report['concern_score'] >= FINAL_SCORE_THRESHOLD]
    
    if df_report.empty:
        print(f"No students met the concern threshold of {FINAL_SCORE_THRESHOLD} points.")
    else:
        # Reorder columns for clarity
        df_report = df_report[['student_id', 'first_name', 'last_name', 'concern_score', 'reasons_for_flag']]
        df_report = df_report.sort_values('concern_score', ascending=False).reset_index(drop=True)
        
        print("\n--- Confidential Student Check-in List ---")
        print(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Flagging students with Concern Score >= {FINAL_SCORE_THRESHOLD}")
        print(df_report.to_string(index=False))

print("\n--- Process Complete ---")