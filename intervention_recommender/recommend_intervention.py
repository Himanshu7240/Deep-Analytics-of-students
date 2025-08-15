import pandas as pd
import os
from datetime import datetime

print("--- Intervention Recommendation Engine ---")

# --- Step 1: Load and Prepare Historical Data ---
print("\nStep 1: Loading intervention and academic history...")

# Robust path detection for data directory
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from intervention_recommender subdirectory
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
df_interventions = pd.read_csv(base_path + 'interventions_outcomes.csv')
df_academic = pd.read_csv(base_path + 'academic_performance.csv')
print("Data loaded successfully.")


# --- Step 2: Define and Calculate Intervention "Success" ---
# We define success as an improvement in the student's final score in the term following the intervention.
print("Step 2: Analyzing historical intervention success rates...")

# Create a helper function to get the term following a given term
def get_next_term(term):
    if term == 'Fall 2024':
        return 'Spring 2025'
    if term == 'Spring 2025':
        return 'Fall 2025'
    return None

# Find the term for each intervention
def get_intervention_term(date):
    intervention_date = pd.to_datetime(date)
    # Simple logic for our dataset's timeline
    if intervention_date < pd.to_datetime('2025-01-01'):
        return 'Fall 2024'
    else:
        return 'Spring 2025'

df_interventions['term'] = df_interventions['date'].apply(get_intervention_term)
df_interventions['next_term'] = df_interventions['term'].apply(get_next_term)

# Calculate success for each historical intervention
success_flags = []
for _, row in df_interventions.iterrows():
    student_id = row['student_id']
    term = row['term']
    next_term = row['next_term']
    
    if next_term is None:
        success_flags.append(None) # Can't determine success if there's no next term data
        continue
    
    # Get scores for the intervention term and the next term
    current_term_scores = df_academic[(df_academic['student_id'] == student_id) & (df_academic['term'] == term)]
    next_term_scores = df_academic[(df_academic['student_id'] == student_id) & (df_academic['term'] == next_term)]
    
    # Simple success metric: did the average score go up?
    if not current_term_scores.empty and not next_term_scores.empty:
        if next_term_scores['final_score'].mean() > current_term_scores['final_score'].mean():
            success_flags.append(1) # Success
        else:
            success_flags.append(0) # Not a success
    else:
        success_flags.append(None) # Not enough data

df_interventions['was_successful'] = success_flags
# Drop rows where we couldn't determine success
df_interventions.dropna(subset=['was_successful'], inplace=True)
df_interventions['was_successful'] = df_interventions['was_successful'].astype(int)

# --- Step 3: Build the Recommendation Logic ---
# The engine will find the intervention with the highest success rate for a given reason.
print("Step 3: Building the recommendation logic...")

# Calculate success rates for each (reason, intervention_type) pair
success_rates = df_interventions.groupby(['reason', 'intervention_type'])['was_successful'].agg(['mean', 'count']).reset_index()
success_rates.rename(columns={'mean': 'success_rate', 'count': 'sample_size'}, inplace=True)

def recommend_intervention(problem_reason: str):
    """Recommends the best intervention based on historical success rates."""
    
    # Find all historical interventions for this specific problem
    possible_interventions = success_rates[success_rates['reason'].str.contains(problem_reason, case=False)]
    
    if possible_interventions.empty:
        return "No historical data for this specific problem. Recommend standard counselor review.", 0, 0
    
    # Find the best intervention (highest success rate)
    best_recommendation = possible_interventions.sort_values('success_rate', ascending=False).iloc[0]
    
    return best_recommendation['intervention_type'], best_recommendation['success_rate'], best_recommendation['sample_size']

print("Recommendation engine is ready.")


# --- Step 4: Simulate Real-World Scenarios ---
print("\n--- Simulating Counselor Queries ---\n")

# A list of problems that might be flagged by our other analysis scripts
problems_to_solve = [
    "Falling grades", # A common academic issue
    "Low attendance", # A behavioral issue
    "ADHD management", # A specific health-related issue
    "Multiple disciplinary incidents" # A serious behavioral issue
]

# Get a recommendation for each problem
for problem in problems_to_solve:
    recommendation, rate, count = recommend_intervention(problem)
    print(f"Query: A student is showing signs of '{problem}'.")
    print(f"  -> Recommendation: '{recommendation}'")
    print(f"     (Based on {count} historical cases with a {rate:.0%} success rate.)\n")
    
print("\n--- Process Complete ---")