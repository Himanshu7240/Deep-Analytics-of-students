import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# --- Step 1: Load the Necessary Data ---
print("Step 1: Loading data...")
# Load the data
print("Loading student data...")
df_academic = pd.read_csv('../data/academic_performance.csv')
df_engagement = pd.read_csv('../data/engagement_behavioral.csv')
df_student = pd.read_csv('../data/student_master.csv')
df_surveys = pd.read_csv('../data/surveys_qualitative.csv')
df_interventions = pd.read_csv('../data/interventions_outcomes.csv')
df_relational = pd.read_csv('../data/relational_social.csv')
df_staff = pd.read_csv('../data/staff_faculty.csv')

# --- Step 2: Preprocess and Merge the Data ---
print("\nStep 2: Preprocessing and merging data...")

# For this model, we only need a few key columns from the student master file
df_students_subset = df_student[['student_id', 'parental_education']]

# Merge academic and engagement data
df_merged = pd.merge(df_academic, df_engagement, on=['student_id', 'term'])
# Merge with the student subset data
df_merged = pd.merge(df_merged, df_students_subset, on='student_id')

# --- Step 3: Feature Engineering ---
# Let's use a different approach: predict risk within the same term using early indicators
print("\nStep 3: Engineering features to predict risk within the same term...")

# We'll use mid-term scores and other early indicators to predict final performance
# This gives us more data to work with

# Create a copy of the merged data
df_model_data = df_merged.copy()

# Define our "At-Risk" condition based on final scores within each term
# Using the median score of each term to create balanced classes
df_model_data['is_at_risk'] = df_model_data.groupby('term')['final_score'].transform(
    lambda x: (x < x.median()).astype(int)
)

# Remove rows where we don't have final scores (future terms)
df_model_data = df_model_data.dropna(subset=['final_score'])

print(f"Total records available for modeling: {len(df_model_data)}")
print(f"Terms available: {df_model_data['term'].unique()}")
print(f"Risk distribution:")
print(df_model_data['is_at_risk'].value_counts())

# Handle categorical variables like 'parental_education' using one-hot encoding
df_model_data = pd.get_dummies(df_model_data, columns=['parental_education'], drop_first=True)

# Get the base features (non-categorical)
# We'll use early indicators to predict final performance
base_features = [
    'mid_term_score',        # Early academic indicator
    'attendance_percentage',  # Engagement indicator
    'lms_logins_per_week',   # Online engagement
    'disciplinary_incidents' # Behavioral indicator
]

# Get the dynamically created parental education columns
parental_education_cols = [col for col in df_model_data.columns if col.startswith('parental_education_')]

# Combine base features with dynamic parental education features
features = base_features + parental_education_cols

print(f"Available features: {features}")
print(f"DataFrame columns: {list(df_model_data.columns)}")

# Our target variable
target = 'is_at_risk'

X = df_model_data[features]
y = df_model_data[target]

# Debug: Check the data distribution
print(f"\nData shape: {df_model_data.shape}")
print(f"Features shape: {X.shape}")
print(f"Target distribution:")
print(y.value_counts())
print(f"Target values: {y.unique()}")

# --- Step 4: Train the Machine Learning Model ---
print("\nStep 4: Training the Random Forest Classifier...")

# Split the data into training and testing sets to evaluate performance
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the RandomForestClassifier
# `class_weight='balanced'` is important when one class is rarer than another (at-risk students might be a minority)
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

# Train the model
model.fit(X_train, y_train)

# --- Step 5: Evaluate the Model ---
print("\nStep 5: Evaluating model performance...")

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Print a detailed classification report
print("\nClassification Report:")
# Check if we have multiple classes
if len(y.unique()) > 1:
    print(classification_report(y_test, y_pred, target_names=['Not At-Risk', 'At-Risk']))
else:
    print(f"Warning: Only one class found in target variable: {y.unique()}")
    print("Cannot generate classification report with single class.")
    print("Consider adjusting the risk threshold or checking data quality.")

# Display the confusion matrix
print("\nConfusion Matrix:")
if len(y.unique()) > 1:
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not At-Risk', 'At-Risk'], yticklabels=['Not At-Risk', 'At-Risk'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()
else:
    print("Cannot display confusion matrix with single class.")

# --- Step 6: Interpret the Model and Make Predictions ---
print("\nStep 6: Interpreting model and identifying key risk factors...")

# Get feature importances
importances = model.feature_importances_
feature_importance_df = pd.DataFrame({'feature': features, 'importance': importances}).sort_values('importance', ascending=False)

print("Top Risk Factors Identified by the Model:")
print(feature_importance_df)

# Plot feature importances
plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance_df)
plt.title('Feature Importances for At-Risk Prediction')
plt.tight_layout()
plt.show()

print("\n--- Process Complete ---")
print("You can now use this trained model to predict which students might be at-risk in the current term.")
print("\nKey Insights:")
print(f"- Model uses {len(features)} features to predict at-risk status")
print(f"- Most important predictor: {feature_importance_df.iloc[0]['feature']} ({feature_importance_df.iloc[0]['importance']:.1%})")
print(f"- Data covers {len(df_model_data['term'].unique())} terms: {', '.join(df_model_data['term'].unique())}")
print(f"- Total students analyzed: {len(df_model_data)}")
print("\nTo use this model:")
print("1. Collect early-term data (mid-term scores, attendance, engagement)")
print("2. Feed the data through the model to get risk predictions")
print("3. Use predictions to target interventions for at-risk students")

# Save the trained model for future use
print("\nSaving the trained model...")
joblib.dump(model, 'student_risk_model.pkl')
joblib.dump(features, 'model_features.pkl')
print("Model saved as 'student_risk_model.pkl'")
print("Features list saved as 'model_features.pkl'")
print("Files saved in current directory")
print("\nTo load and use the model in the future:")
print("model = joblib.load('student_risk_model.pkl')")
print("features = joblib.load('model_features.pkl')")