# Student Risk Prediction System

This system uses machine learning to predict whether students are at risk of poor academic performance based on early indicators.

## Overview

The system analyzes student data including:
- **Academic Performance**: Mid-term scores
- **Engagement**: Attendance percentage, LMS logins per week
- **Behavior**: Disciplinary incidents
- **Background**: Parental education level

## Files

- `predict_performance.py` - Main script to train the model
- `predict_new_student.py` - Script to make predictions for new students
- `student_risk_model.pkl` - Trained machine learning model
- `model_features.pkl` - List of features used by the model
- `../data/` - Directory containing student data files (relative to script location)

## Quick Start

### 1. Navigate to the Project Directory

```bash
cd "predict student performance"
```

### 2. Train the Model

```bash
# Make sure you're in the "predict student performance" directory
python predict_performance.py
```

This will:
- Load and preprocess student data
- Train a Random Forest classifier
- Save the trained model to `student_risk_model.pkl`
- Display model performance metrics and feature importance

### 3. Make Predictions

```bash
python predict_new_student.py
```

This provides:
- Example predictions for sample students
- Interactive input for new student data
- Risk assessment and intervention recommendations

## Data Requirements

To make predictions, you need the following student data:

| Feature | Type | Description | Example |
|---------|------|-------------|---------|
| `mid_term_score` | float | Student's mid-term score (0-100) | 75.0 |
| `attendance_percentage` | float | Attendance rate (0-100) | 85.0 |
| `lms_logins_per_week` | float | Weekly LMS logins | 5.0 |
| `disciplinary_incidents` | int | Number of behavioral issues | 1 |
| `parental_education` | string | Education level | "Masters" |

## Model Performance

The current model achieves:
- **Accuracy**: 100% (on training data)
- **Key Predictors**:
  - Mid-term score (56.9% importance)
  - LMS logins per week (13.8% importance)
  - Disciplinary incidents (12.5% importance)
  - Attendance percentage (10.5% importance)

## Risk Levels

- **LOW RISK**: Student appears on track, continue monitoring
- **HIGH RISK**: Immediate intervention recommended

## Intervention Recommendations

### For High-Risk Students:
- Schedule meeting with student and parents
- Assign academic mentor/tutor
- Increase monitoring of attendance and engagement
- Provide additional academic support resources

### For Low-Risk Students:
- Regular check-ins to maintain progress
- Encourage continued engagement
- Monitor for any changes in performance

## Technical Details

- **Algorithm**: Random Forest Classifier
- **Features**: 6 engineered features
- **Data Source**: Academic performance, engagement, and demographic data
- **Training Data**: 13 student records across Fall 2024 and Spring 2025

## Usage Examples

### Python API

```python
import joblib

# Load the model
model = joblib.load('student_risk_model.pkl')
features = joblib.load('model_features.pkl')

# Prepare student data
student_data = {
    'mid_term_score': 70,
    'attendance_percentage': 80,
    'lms_logins_per_week': 3,
    'disciplinary_incidents': 2,
    'parental_education': 'High School'
}

# Make prediction
risk_probability = model.predict_proba([student_data])[0][1]
risk_prediction = model.predict([student_data])[0]
```

### Command Line

```bash
# Train model
python predict_performance.py

# Make predictions
python predict_new_student.py
```

## Data Sources

The system uses data from:
- `academic_performance.csv` - Grades and test scores
- `engagement_behavioral.csv` - Attendance and behavioral data
- `student_master.csv` - Demographic and background information

## Limitations

- **Small Dataset**: Currently trained on 13 student records
- **Limited Terms**: Data covers only Fall 2024 and Spring 2025
- **Overfitting Risk**: 100% accuracy suggests potential overfitting
- **Feature Dependencies**: Some features may be correlated

## Future Improvements

1. **Expand Dataset**: Include more students and terms
2. **Feature Engineering**: Add more predictive variables
3. **Model Validation**: Implement cross-validation and holdout testing
4. **Real-time Updates**: Integrate with live student data systems
5. **Intervention Tracking**: Monitor effectiveness of recommended actions

## Requirements

- Python 3.7+
- pandas
- scikit-learn
- matplotlib
- seaborn
- joblib

## Installation

```bash
pip install pandas scikit-learn matplotlib seaborn joblib
```

## Support

For questions or issues, please check:
1. Data file formats and structure
2. Python package versions
3. File permissions for model saving
4. Input data validation

## License

This project is for educational and research purposes. 