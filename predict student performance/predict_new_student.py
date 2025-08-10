import pandas as pd
import joblib
import numpy as np

def predict_student_risk(student_data):
    """
    Predict whether a student is at risk based on early indicators.
    
    Args:
        student_data (dict): Dictionary containing student features:
            - mid_term_score: float
            - attendance_percentage: float  
            - lms_logins_per_week: float
            - disciplinary_incidents: int
            - parental_education: str (High School, Bachelors, Masters, PhD)
    
    Returns:
        dict: Prediction results with risk probability and recommendation
    """
    
    # Load the saved model and features
    try:
        model = joblib.load('student_risk_model.pkl')
        features = joblib.load('model_features.pkl')
        print("Model loaded successfully!")
    except FileNotFoundError:
        print("Error: Model files not found. Please run predict_performance.py first from this directory.")
        return None
    
    # Create a DataFrame with the student data
    df_student = pd.DataFrame([student_data])
    
    # Handle categorical variables (parental education)
    df_student = pd.get_dummies(df_student, columns=['parental_education'], drop_first=True)
    
    # Ensure all required features are present
    for feature in features:
        if feature not in df_student.columns:
            if feature.startswith('parental_education_'):
                # Add missing parental education columns with 0
                df_student[feature] = 0
            else:
                print(f"Warning: Missing required feature: {feature}")
                return None
    
    # Select only the features used by the model
    X = df_student[features]
    
    # Make prediction
    risk_probability = model.predict_proba(X)[0][1]  # Probability of being at-risk
    risk_prediction = model.predict(X)[0]
    
    # Create recommendation
    if risk_prediction == 1:
        risk_level = "HIGH RISK"
        recommendation = "Immediate intervention recommended. Consider:"
        actions = [
            "Schedule meeting with student and parents",
            "Assign academic mentor/tutor",
            "Increase monitoring of attendance and engagement",
            "Provide additional academic support resources"
        ]
    else:
        risk_level = "LOW RISK"
        recommendation = "Student appears to be on track. Continue monitoring:"
        actions = [
            "Regular check-ins to maintain progress",
            "Encourage continued engagement",
            "Monitor for any changes in performance"
        ]
    
    return {
        'risk_prediction': risk_prediction,
        'risk_probability': risk_probability,
        'risk_level': risk_level,
        'recommendation': recommendation,
        'actions': actions
    }

def main():
    """Demo function showing how to use the prediction model."""
    
    print("=== Student Risk Prediction System ===\n")
    
    # Example 1: High-risk student
    print("Example 1: High-Risk Student Profile")
    print("-" * 40)
    high_risk_student = {
        'mid_term_score': 65,           # Below average
        'attendance_percentage': 75,    # Poor attendance
        'lms_logins_per_week': 2,      # Low online engagement
        'disciplinary_incidents': 3,    # Multiple behavioral issues
        'parental_education': 'High School'
    }
    
    result = predict_student_risk(high_risk_student)
    if result:
        print(f"Risk Level: {result['risk_level']}")
        print(f"Risk Probability: {result['risk_probability']:.1%}")
        print(f"Recommendation: {result['recommendation']}")
        for action in result['actions']:
            print(f"  • {action}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Low-risk student
    print("Example 2: Low-Risk Student Profile")
    print("-" * 40)
    low_risk_student = {
        'mid_term_score': 88,           # Above average
        'attendance_percentage': 95,    # Excellent attendance
        'lms_logins_per_week': 8,      # High online engagement
        'disciplinary_incidents': 0,    # No behavioral issues
        'parental_education': 'Masters'
    }
    
    result = predict_student_risk(low_risk_student)
    if result:
        print(f"Risk Level: {result['risk_level']}")
        print(f"Risk Probability: {result['risk_probability']:.1%}")
        print(f"Recommendation: {result['recommendation']}")
        for action in result['actions']:
            print(f"  • {action}")
    
    print("\n" + "="*50 + "\n")
    
    # Interactive prediction
    print("Interactive Prediction")
    print("-" * 40)
    print("Enter student data to get a prediction (or press Enter to skip):")
    
    try:
        mid_term = input("Mid-term score (0-100): ").strip()
        if mid_term:
            attendance = input("Attendance percentage (0-100): ").strip()
            lms_logins = input("LMS logins per week: ").strip()
            incidents = input("Disciplinary incidents: ").strip()
            education = input("Parental education (High School/Bachelors/Masters/PhD): ").strip()
            
            if all([mid_term, attendance, lms_logins, incidents, education]):
                student_data = {
                    'mid_term_score': float(mid_term),
                    'attendance_percentage': float(attendance),
                    'lms_logins_per_week': float(lms_logins),
                    'disciplinary_incidents': int(incidents),
                    'parental_education': education
                }
                
                result = predict_student_risk(student_data)
                if result:
                    print(f"\nPrediction Results:")
                    print(f"Risk Level: {result['risk_level']}")
                    print(f"Risk Probability: {result['risk_probability']:.1%}")
                    print(f"Recommendation: {result['recommendation']}")
                    for action in result['actions']:
                        print(f"  • {action}")
    except (ValueError, KeyboardInterrupt):
        print("\nInput cancelled or invalid. Exiting...")

if __name__ == "__main__":
    main() 