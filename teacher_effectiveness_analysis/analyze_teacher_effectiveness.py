import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("--- Teacher Effectiveness Analysis ---")

# Ensure all outputs save to this script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Step 1: Define Paths and Load Data ---
print("\nStep 1: Loading data...")

# Try multiple possible paths for the data directory
possible_paths = [
    'data/',           # If running from root directory
    '../data/',        # If running from teacher_effectiveness_analysis subdirectory
    './data/'          # If data is in current directory
]

base_path = None
for path in possible_paths:
    if os.path.exists(path):
        base_path = path
        break

if base_path is None:
    print("Error: Data directory not found!")
    print("Tried the following paths:")
    for path in possible_paths:
        print(f"  - {path}")
    print("Please ensure the 'data' folder is accessible from one of these locations.")
    exit()

print(f"Found data directory at: {base_path}")

df_academic = pd.read_csv(base_path + 'academic_performance.csv')
df_relational = pd.read_csv(base_path + 'relational_social.csv')
df_staff = pd.read_csv(base_path + 'staff_faculty.csv')
print("Data loaded successfully.")

# --- Step 2: Merge Data to Link Scores with Teachers ---
print("Step 2: Merging data to create a unified analysis set...")

# Merge academic records with relational data to link scores to teacher_id
df_merged = pd.merge(df_academic, df_relational, on=['student_id', 'course_id', 'term', 'subject'])

# Merge in teacher/staff details
# Ensure numeric fields are properly typed in staff dataframe
for col in ['years_experience', 'effectiveness_rating_5']:
    if col in df_staff.columns:
        df_staff[col] = pd.to_numeric(df_staff[col], errors='coerce')

df_merged = pd.merge(df_merged, df_staff, on='teacher_id', how='left')

print("Data merged successfully.")

# --- Step 3: Calculate Student Score Growth (Value-Added Metric) ---
print("Step 3: Calculating student score growth...")

# Coerce score columns to numeric (handles 'NULL' strings as NaN)
for col in ['mid_term_score', 'final_score']:
    if col in df_merged.columns:
        df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')

# Filter out records where final_score or mid_term_score is NaN
df_analysis = df_merged.dropna(subset=['final_score', 'mid_term_score']).copy()

# Compute growth on the filtered copy to avoid SettingWithCopyWarning
df_analysis['score_growth'] = df_analysis['final_score'] - df_analysis['mid_term_score']

# Display a sample of the prepared data to verify
print("\nSample of the prepared analysis data:")
cols_to_show = [
    c for c in ['student_id', 'term', 'subject', 'teacher_id', 'first_name', 'last_name', 'mid_term_score', 'final_score', 'score_growth']
    if c in df_analysis.columns
]
print(df_analysis[cols_to_show].head())

# --- Step 4: Analyze Effectiveness by Aggregating per Teacher ---
print("\nStep 4: Aggregating results by teacher...")

# Group by teacher and calculate key metrics
group_cols = [c for c in ['teacher_id', 'first_name', 'last_name', 'years_experience', 'specialization', 'effectiveness_rating_5'] if c in df_analysis.columns]

teacher_effectiveness = df_analysis.groupby(group_cols).agg(
    mean_score_growth=('score_growth', 'mean'),
    mean_final_score=('final_score', 'mean'),
    mean_midterm_score=('mid_term_score', 'mean'),
    student_record_count=('student_id', 'count'), # Count of student-term records
    std_score_growth=('score_growth', 'std')  # Standard deviation of score growth
).reset_index()

# Sort teachers by their mean score growth
teacher_effectiveness = teacher_effectiveness.sort_values('mean_score_growth', ascending=False)

# Create a human-readable label for plots
if {'first_name', 'last_name', 'teacher_id'}.issubset(teacher_effectiveness.columns):
    teacher_effectiveness['teacher_label'] = (
        teacher_effectiveness['first_name'].fillna('') + ' ' +
        teacher_effectiveness['last_name'].fillna('') +
        ' (' + teacher_effectiveness['teacher_id'] + ')'
    ).str.strip()
else:
    teacher_effectiveness['teacher_label'] = teacher_effectiveness.get('teacher_id', '')

print("\n--- Teacher Effectiveness Summary ---")
summary_cols = [
    c for c in ['teacher_id', 'first_name', 'last_name', 'specialization', 'years_experience', 'effectiveness_rating_5',
                'mean_midterm_score', 'mean_final_score', 'mean_score_growth', 'std_score_growth', 'student_record_count']
    if c in teacher_effectiveness.columns
]
print(teacher_effectiveness[summary_cols].round(2))

# --- Step 5: Visualize the Results ---
print("\nStep 5: Generating visualizations...")
sns.set_theme(style="whitegrid")

# Visualization 1: Bar chart comparing Mean Score Growth per Teacher
plt.figure(figsize=(12, 8))
barplot = sns.barplot(
    x='mean_score_growth', 
    y='teacher_label', 
    data=teacher_effectiveness, 
    orient='h', 
    hue='teacher_label',  # assign y to hue to satisfy seaborn 0.14+ and color bars distinctly
    legend=False
)
plt.xlabel('Mean Score Growth (Final Score - Midterm Score)')
plt.ylabel('Teacher')
plt.title('Teacher Effectiveness based on Average Student Score Growth')
plt.bar_label(barplot.containers[0], fmt='%.2f') # Add labels to bars
plt.tight_layout()
# Save the figure
_out1 = os.path.join(script_dir, 'teacher_effectiveness_ranking.png')
plt.savefig(_out1)
print(f"Saved chart: {_out1}")
plt.show()

# Visualization 2: Scatter plot of experience vs. effectiveness (if experience available)
if 'years_experience' in teacher_effectiveness.columns and 'specialization' in teacher_effectiveness.columns:
    plt.figure(figsize=(12, 8))
    scatterplot = sns.scatterplot(
        x='years_experience', 
        y='mean_score_growth', 
        size='student_record_count', 
        sizes=(50, 600), 
        hue='specialization', 
        data=teacher_effectiveness
    )
    plt.xlabel('Years of Experience')
    plt.ylabel('Mean Score Growth')
    plt.title('Teacher Experience vs. Student Score Growth')
    plt.legend(title='Specialization & Student Count', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    # Save the figure
    _out2 = os.path.join(script_dir, 'experience_vs_effectiveness.png')
    plt.savefig(_out2)
    print(f"Saved chart: {_out2}")
    plt.show()
else:
    print("Skipping experience vs effectiveness scatter (missing columns)")

# Visualization 3: Box plot of score growth by teacher
plt.figure(figsize=(14, 8))
# Prepare data for box plot
box_data = []
teacher_labels = []
for _, teacher in teacher_effectiveness.iterrows():
    t_id = teacher.get('teacher_id')
    if t_id is None:
        continue
    teacher_data = df_analysis[df_analysis['teacher_id'] == t_id]['score_growth']
    if len(teacher_data) > 0:
        box_data.append(teacher_data)
        teacher_labels.append(teacher.get('teacher_label', t_id))

if box_data:
    plt.boxplot(box_data, tick_labels=teacher_labels)
    plt.xlabel('Teacher')
    plt.ylabel('Score Growth')
    plt.title('Distribution of Student Score Growth by Teacher')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the figure
    _out3 = os.path.join(script_dir, 'score_growth_distribution.png')
    plt.savefig(_out3)
    print(f"Saved chart: {_out3}")
    plt.show()
else:
    print("Not enough data for box plot visualization.")

print("\n--- Process Complete ---")