import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import os

print("--- Dropout or Transfer Risk Detection Model ---")

# --- Step 1: Load and Prepare Data ---
print("\nStep 1: Loading and preparing student data...")

# Robust path detection for data directory
def find_data_directory():
    """Find the data directory from various possible locations"""
    possible_paths = [
        'data/',           # If running from root directory
        '../data/',        # If running from dropout_risk_detection subdirectory
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
df_academic = pd.read_csv(base_path + 'academic_performance.csv')
df_engagement = pd.read_csv(base_path + 'engagement_behavioral.csv')
df_students = pd.read_csv(base_path + 'student_master.csv')

# Merge the key data sources
df_merged = pd.merge(df_academic, df_engagement, on=['student_id', 'term'])
df_merged = pd.merge(df_merged, df_students[['student_id', 'parental_education']], on='student_id')
print("Data loaded and prepared.")


# --- Step 2: Synthesize the Target Variable (did_dropout) ---
# CRITICAL STEP: As we don't have real dropout data, we create it based on severe risk factors from Spring 2025.
print("\nStep 2: Synthesizing historical dropout data for demonstration...")

# Isolate Spring 2025 data to create labels from
spring25_data = df_merged[df_merged['term'] == 'Spring 2025'].copy()

# Define the rules for a synthetic dropout event
# A student is considered to have "dropped out" if they met these criteria in their last term
def synthesize_dropout(row):
    # More realistic dropout criteria - lower thresholds to ensure some dropouts
    if row['final_score'] < 70 and row['attendance_percentage'] < 90:
        return 1
    if row['attendance_percentage'] < 85 and row['lms_logins_per_week'] < 3:
        return 1
    if row['final_score'] < 60:  # Very low performance
        return 1
    if row['disciplinary_incidents'] > 2:  # Multiple behavioral issues
        return 1
    return 0

spring25_data['did_dropout'] = spring25_data.apply(synthesize_dropout, axis=1)
print(f"Synthesized {spring25_data['did_dropout'].sum()} dropout events for model training.")


# --- Step 3: Feature Engineering ---
# We will use the Spring 2025 data as the features (X) to predict the 'did_dropout' outcome (y)
print("\nStep 3: Engineering features...")
df_model_data = spring25_data.copy()

# Handle categorical variables
df_model_data = pd.get_dummies(df_model_data, columns=['parental_education'], drop_first=True)

# Debug: Show available columns
print("Available columns after one-hot encoding:")
print(df_model_data.columns.tolist())

# Define our base features (these should always exist)
base_features = [
    'final_score',
    'attendance_percentage',
    'lms_logins_per_week',
    'disciplinary_incidents'
]

# Dynamically add parental education columns that exist
parental_education_features = [col for col in df_model_data.columns if col.startswith('parental_education_')]
print(f"Found parental education features: {parental_education_features}")

# Combine all available features
features = base_features + parental_education_features
print(f"Final feature set: {features}")

target = 'did_dropout'

# Verify all features exist
missing_features = [f for f in features if f not in df_model_data.columns]
if missing_features:
    print(f"Warning: Missing features: {missing_features}")
    # Remove missing features
    features = [f for f in features if f in df_model_data.columns]
    print(f"Adjusted feature set: {features}")

X = df_model_data[features]
y = df_model_data[target]

print(f"Feature matrix shape: {X.shape}")
print(f"Target vector shape: {y.shape}")

# --- Step 4: Train the Logistic Regression Model ---
print("\nStep 4: Training the prediction model...")

# Split data for training and testing
# For small datasets, we need to handle the case where stratification isn't possible
if len(y) < 10:
    # Very small dataset - use simple split without stratification
    test_size = min(0.3, 1/len(y))  # Ensure at least 1 sample in test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    print(f"Small dataset detected ({len(y)} samples). Using simple split: {len(X_train)} train, {len(X_test)} test")
else:
    # Larger dataset - use stratified split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"Dataset size: {len(y)} samples. Using stratified split: {len(X_train)} train, {len(X_test)} test")

# Scale features - Important for Logistic Regression
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model
# We use class_weight='balanced' to handle the fact that dropouts are rare
model = LogisticRegression(random_state=42, class_weight='balanced')
model.fit(X_train_scaled, y_train)
print("Model training complete.")


# --- Step 5: Evaluate the Model ---
print("\nStep 5: Evaluating model performance...")
y_pred = model.predict(X_test_scaled)

# Check if we have both classes in the test set
unique_classes = set(y_test)
print(f"Classes in test set: {unique_classes}")

if len(unique_classes) == 1:
    print("Warning: Test set contains only one class. Model evaluation will be limited.")
    print(f"All test samples belong to class: {list(unique_classes)[0]}")
    print("Model accuracy: 100% (but this is not meaningful with single class)")
else:
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Stayed', 'Dropped Out']))

    # Display the confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', 
                xticklabels=['Stayed', 'Dropped Out'], 
                yticklabels=['Stayed', 'Dropped Out'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.show()


# --- Step 6: Generate Actionable Risk List for Fall 2025 ---
print("\nStep 6: Generating a prioritized risk list for the current term...")

# We use the trained model to predict the *probability* of dropout for ALL students based on their Spring 2025 data
all_students_scaled = scaler.transform(X)
dropout_probabilities = model.predict_proba(all_students_scaled)[:, 1] # Get probability of the '1' class (dropout)

# Create a final report
df_risk_report = df_students.copy()
df_risk_report = pd.merge(df_risk_report, df_model_data[['student_id', 'final_score', 'attendance_percentage']], on='student_id')
df_risk_report['dropout_risk_probability'] = dropout_probabilities

# Sort by the highest risk
df_risk_report = df_risk_report.sort_values('dropout_risk_probability', ascending=False)

print("\n--- Confidential Dropout Risk List for Fall 2025 ---")
print("This list should be used by counselors to prioritize outreach.")
print(df_risk_report[['first_name', 'last_name', 'dropout_risk_probability', 'final_score', 'attendance_percentage']].head(15).to_string())


print("\n--- Process Complete ---")