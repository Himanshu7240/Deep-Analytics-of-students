import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("--- Analysis of the Impact of External Factors on Student Performance ---")

# --- Step 1: Load and Prepare Data ---
print("\nStep 1: Loading and preparing student and academic data...")

# Robust path detection for data directory
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from external_factors_analysis subdirectory
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

# Merge the two essential datasets
df_analysis = pd.merge(df_students, df_academic, on='student_id')
print("Data loaded and merged successfully.")

# Get script directory for saving images
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Step 2: Feature Engineering for Analysis ---
# To analyze broad categories, we'll create some new, simplified columns.
print("Step 2: Engineering features for analysis...")

# 1. Create a binary feature for health notes
df_analysis['has_health_note'] = df_analysis['health_notes'].apply(lambda x: 'No' if x == 'None' else 'Yes')

# 2. Categorize diverse parental occupations into broader groups
def categorize_occupation(occupation):
    occupation = str(occupation).lower()
    if any(keyword in occupation for keyword in ['engineer', 'scientist', 'researcher', 'professor', 'it', 'software']):
        return 'STEM/Academia'
    elif any(keyword in occupation for keyword in ['manager', 'sales', 'business', 'architect', 'lawyer', 'banker', 'consultant', 'analyst', 'hr', 'marketing', 'author', 'entrepreneur']):
        return 'Business/Professional'
    elif any(keyword in occupation for keyword in ['doctor', 'pharmacist']):
        return 'Healthcare'
    elif any(keyword in occupation for keyword in ['technician', 'mechanic', 'electrician', 'contractor', 'driver', 'pilot']):
        return 'Skilled Trade/Technical'
    else:
        return 'Other'

df_analysis['occupation_category'] = df_analysis['parental_occupation'].apply(categorize_occupation)

print("Feature engineering complete.")
print("\n--- Data Analysis & Visualization ---")

# --- Analysis 1: Parental Education vs. Performance ---
print("\nAnalyzing impact of: Parental Education")

# Define a logical order for the education levels for plotting
education_order = ['High School', 'Bachelors', 'Masters', 'PhD']
df_analysis['parental_education'] = pd.Categorical(df_analysis['parental_education'], categories=education_order, ordered=True)

# Display the numerical summary
print(df_analysis.groupby('parental_education')['final_score'].describe().round(2))

# Visualize using a box plot
plt.figure(figsize=(12, 7))
sns.boxplot(x='parental_education', y='final_score', data=df_analysis, order=education_order)
plt.title('Impact of Parental Education on Student Final Scores')
plt.xlabel('Highest Level of Parental Education')
plt.ylabel('Final Score')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(os.path.join(script_dir, 'parental_education_impact.png'))
print("Saved chart: parental_education_impact.png")
plt.show()


# --- Analysis 2: Parental Occupation vs. Performance ---
print("\nAnalyzing impact of: Parental Occupation")

# Display the numerical summary
print(df_analysis.groupby('occupation_category')['final_score'].describe().round(2))

# Visualize using a box plot
plt.figure(figsize=(12, 7))
sns.boxplot(x='occupation_category', y='final_score', data=df_analysis)
plt.title('Impact of Parental Occupation Category on Student Final Scores')
plt.xlabel('Parental Occupation Category')
plt.ylabel('Final Score')
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(script_dir, 'parental_occupation_impact.png'))
print("Saved chart: parental_occupation_impact.png")
plt.show()


# --- Analysis 3: Health Notes vs. Performance ---
print("\nAnalyzing impact of: Recorded Health Notes")

# Display the numerical summary
print(df_analysis.groupby('has_health_note')['final_score'].describe().round(2))

# Visualize using a box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='has_health_note', y='final_score', data=df_analysis)
plt.title('Impact of Recorded Health Notes on Student Final Scores')
plt.xlabel('Does Student Have a Recorded Health Note?')
plt.ylabel('Final Score')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(os.path.join(script_dir, 'health_notes_impact.png'))
print("Saved chart: health_notes_impact.png")
plt.show()

print("\n--- Process Complete ---")