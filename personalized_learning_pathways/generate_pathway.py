import pandas as pd
import os
from datetime import datetime

# --- Step 1: Setup and Configuration ---

# Define thresholds for identifying strengths and weaknesses
STRENGTH_THRESHOLD = 85  # Final scores above this are a strength
WEAKNESS_THRESHOLD = 70  # Final scores below this are a weakness

# Define a "Knowledge Base" for recommendations
# This maps strong subjects to potential advanced subjects or activities
STRENGTH_RECOMMENDATIONS = {
    'Math': ['Consider joining the Coding Club', 'Explore Advanced Placement (AP) Calculus', 'Look into competitive programming'],
    'Science': ['Join the Science Olympiad team', 'Propose a project for the school science fair', 'Consider robotics or astronomy clubs'],
    'English': ['Join the Debate Club or Model UN', 'Contribute to the school newspaper or literary magazine', 'Explore creative writing workshops'],
    'History': ['Participate in the History Bowl team', 'Explore local museum volunteer opportunities', 'Join the Model UN'],
    'Economics': ['Start an investment club', 'Participate in a business case competition', 'Read The Economist or Wall Street Journal'],
}

# Define generic recommendations for weak subjects
WEAKNESS_RECOMMENDATIONS = {
    'Math': ['Focus on practicing foundational concepts', 'Seek peer tutoring or attend academic support sessions', 'Use online resources like Khan Academy for extra practice'],
    'Science': ['Review lab reports and fundamental theories', 'Form a study group to discuss complex topics', 'Seek extra help from the teacher during office hours'],
    'English': ['Work on essay structure and outlining', 'Read more widely to improve vocabulary and comprehension', 'Request feedback on drafts before submission'],
    'History': ['Create timelines to better understand context', 'Use flashcards for key dates and events', 'Practice writing thesis-driven essays'],
    'Economics': ['Review core principles of micro and macroeconomics', 'Connect theories to current news events', 'Seek help on quantitative aspects'],
}

# --- Step 2: Path Detection Function ---

def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from personalized_learning_pathways subdirectory
        './data/'          # If data is in current directory
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

# --- Step 3: Main Function to Generate Pathway ---

def generate_learning_pathway(student_id: str, data_path: str = None):
    """
    Analyzes a student's record and generates a personalized learning pathway.
    """
    print("="*60)
    print(f"Generating Personalized Learning Pathway for: {student_id}")
    print(f"Report Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    try:
        # Auto-detect data path if not provided
        if data_path is None:
            data_path = find_data_directory()
            if data_path is None:
                print("Error: Data directory not found!")
                print("Please ensure the 'data' folder is accessible.")
                return
            print(f"Found data directory at: {data_path}")
        
        # Load relevant data
        df_academic = pd.read_csv(data_path + 'academic_performance.csv')
        df_engagement = pd.read_csv(data_path + 'engagement_behavioral.csv')
        df_students = pd.read_csv(data_path + 'student_master.csv')

        # Validate that student exists
        if student_id not in df_students['student_id'].values:
            print(f"Error: Student ID '{student_id}' not found in student records.")
            return

        # Get student's name and latest records
        student_name = df_students.loc[df_students['student_id'] == student_id, 'first_name'].iloc[0]
        student_academic = df_academic[df_academic['student_id'] == student_id].copy()
        student_engagement = df_engagement[df_engagement['student_id'] == student_id]

        if student_academic.empty:
            print(f"No academic records found for {student_id}.")
            return

        # Handle missing final scores (NULL values)
        student_academic['final_score'] = pd.to_numeric(student_academic['final_score'], errors='coerce')
        student_academic = student_academic.dropna(subset=['final_score'])

        if student_academic.empty:
            print(f"No complete academic records with final scores found for {student_id}.")
            return

        # Get the most recent term's data for analysis
        latest_term = student_academic['term'].unique()[-1]
        latest_records = student_academic[student_academic['term'] == latest_term]

        print(f"Analysis based on the latest available term: {latest_term}\n")
        
        strengths = []
        weaknesses = []

        # Identify strengths and weaknesses from the latest academic records
        for _, row in latest_records.iterrows():
            if row['final_score'] >= STRENGTH_THRESHOLD:
                strengths.append(row['subject'])
            elif row['final_score'] < WEAKNESS_THRESHOLD:
                weaknesses.append(row['subject'])

        # --- Generate Recommendations ---

        # 1. Recommendations for Weaknesses (Areas for Improvement)
        print("--- Areas for Improvement ---\n")
        if not weaknesses:
            print(f"Great work, {student_name}! No specific academic weaknesses identified in the last term.\n")
        else:
            for subject in weaknesses:
                print(f"-> In {subject}:")
                for rec in WEAKNESS_RECOMMENDATIONS.get(subject, ["Seek teacher guidance for a custom study plan."]):
                    print(f"   - {rec}")
                print("") # Newline for readability

        # 2. Recommendations for Strengths (Areas for Enrichment)
        print("--- Areas for Enrichment ---\n")
        if not strengths:
            print(f"{student_name}, let's work on building up your strengths! Keep working hard.\n")
        else:
            for subject in strengths:
                print(f"-> You excelled in {subject}! Consider these challenges:")
                for rec in STRENGTH_RECOMMENDATIONS.get(subject, ["Explore advanced topics in this area."]):
                    print(f"   - {rec}")
                print("")

        # 3. Holistic Recommendation based on Extracurriculars
        print("--- Holistic Pathway Note ---\n")
        if not student_engagement.empty:
            # Filter out NaN values and ensure all activities are strings
            student_activities = student_engagement['extracurricular_activity'].dropna().astype(str).unique()
            
            # Filter out 'None' and 'nan' string values
            valid_activities = [activity for activity in student_activities 
                              if activity not in ['None', 'nan', '']]
            
            if not valid_activities:
                print("Consider joining an extracurricular activity. It's great for both personal growth and college applications.")
            else:
                print(f"Your participation in {', '.join(valid_activities)} is fantastic.")
                print("Try to find links between your academic strengths and your activities for a powerful combination.")
        else:
            print("No engagement data available. Consider joining extracurricular activities for holistic development.")

        print("\n" + "="*60)

    except FileNotFoundError as e:
        print(f"Error: Could not find required data files. Please check the data directory.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"An error occurred while processing data for student '{student_id}'.")
        print(f"Details: {e}")

# --- Step 4: Run the Analysis for Sample Students ---

if __name__ == "__main__":
    print("Personalized Learning Pathways Generator")
    print("="*60)
    
    # Example 1: A high-achieving student strong in STEM
    print("\n1. Analyzing STU-041 (High-achieving STEM student):")
    generate_learning_pathway(student_id='STU-041')

    # Example 2: A student who improved but still has a clear weakness
    print("\n2. Analyzing STU-002 (Student with improvement areas):")
    generate_learning_pathway(student_id='STU-002')

    # Example 3: A student with strengths in humanities
    print("\n3. Analyzing STU-025 (Humanities-focused student):")
    generate_learning_pathway(student_id='STU-025')