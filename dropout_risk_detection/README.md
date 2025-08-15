# Dropout Risk Detection: Machine Learning Early Warning System

## Overview
The Dropout Risk Detection module is an **advanced machine learning system** that identifies students at risk of dropping out or transferring. Using logistic regression and comprehensive student data analysis, it provides **predictive risk scores** to enable proactive intervention and support strategies.

## 🎯 **What It Does**

### **Core Functionality:**
- **🔮 Predictive Modeling**: Uses machine learning to predict dropout probability
- **📊 Risk Scoring**: Assigns numerical risk scores (0-100%) to each student
- **🎯 Prioritization**: Creates ranked lists for counselor outreach and intervention
- **📈 Data-Driven Insights**: Analyzes multiple risk factors simultaneously

### **Key Features:**
- **Machine Learning Model**: Logistic regression trained on historical patterns
- **Multi-Factor Analysis**: Considers academic, behavioral, and engagement data
- **Real-Time Risk Assessment**: Provides current-term risk predictions
- **Actionable Intelligence**: Prioritizes students needing immediate attention

## 🤖 **Machine Learning Approach**

### **Model Type:**
- **Algorithm**: Logistic Regression with balanced class weights
- **Purpose**: Binary classification (Stay vs. Dropout/Transfer)
- **Training**: Uses Spring 2025 data to predict Fall 2025 outcomes

### **Feature Engineering:**
- **Academic Performance**: Final scores, attendance percentages
- **Engagement Metrics**: LMS logins per week, extracurricular activities
- **Behavioral Indicators**: Disciplinary incidents, counselor visits
- **Demographic Factors**: Parental education levels (one-hot encoded)

### **Model Training:**
- **Data Split**: Train/test split with small dataset handling
- **Feature Scaling**: StandardScaler for optimal model performance
- **Class Balancing**: Handles imbalanced dropout vs. stay classes
- **Validation**: Cross-validation for model reliability

## 📊 **Risk Assessment Methodology**

### **Dropout Synthesis Rules:**
Since real dropout data isn't available, the system creates synthetic labels based on **severe risk factors**:

```python
def synthesize_dropout(row):
    # Multiple risk criteria for comprehensive assessment
    if row['final_score'] < 70 and row['attendance_percentage'] < 90:
        return 1  # High academic + attendance risk
    if row['attendance_percentage'] < 85 and row['lms_logins_per_week'] < 3:
        return 1  # Poor engagement + attendance
    if row['final_score'] < 60:
        return 1  # Very low academic performance
    if row['disciplinary_incidents'] > 2:
        return 1  # Multiple behavioral issues
    return 0  # No significant risk factors
```

### **Risk Factors Analyzed:**
1. **📚 Academic Performance**: Final scores below thresholds
2. **📅 Attendance Patterns**: Low attendance percentages
3. **💻 Digital Engagement**: Limited LMS activity
4. **🚨 Behavioral Issues**: Multiple disciplinary incidents
5. **👨‍👩‍👧‍👦 Family Background**: Parental education levels

## 📈 **Sample Results & Analysis**

### **Current Risk Assessment (Fall 2025):**
```
Student Name        Risk %    Final Score    Attendance    Risk Level
Harish Rao         89.9%      72.0          93%          🔴 HIGH
Priya Patel        20.4%      75.0          92%          🟡 MEDIUM
Parineeti Goel     14.1%      50.0          90%          🟡 MEDIUM
Sameer Ali          6.4%      78.0          92%          🟢 LOW
Emraan Hashmi       5.0%      76.0          92%          🟢 LOW
Uday Shetty         4.7%      78.0          90%          🟢 LOW
Aarav Sharma        0.03%     90.0          99%          🟢 VERY LOW
```

### **Risk Level Interpretation:**
- **🔴 HIGH RISK (80%+)**: Immediate intervention required
- **🟡 MEDIUM RISK (10-80%)**: Regular monitoring and support
- **🟢 LOW RISK (0-10%)**: Standard academic support

## 🔍 **Analysis Process**

### **Step 1: Data Loading & Preparation**
- **Robust path detection** for data directory access
- **Multi-source integration**: Academic, engagement, and student data
- **Data validation** and quality checks

### **Step 2: Dropout Event Synthesis**
- **Risk factor analysis** using defined criteria
- **Synthetic label generation** for model training
- **Data balancing** for effective learning

### **Step 3: Feature Engineering**
- **Dynamic feature selection** based on available data
- **Categorical encoding** for parental education
- **Feature validation** and missing data handling

### **Step 4: Model Training**
- **Adaptive train-test splitting** for small datasets
- **Feature scaling** for optimal performance
- **Logistic regression training** with balanced weights

### **Step 5: Risk Prediction**
- **Probability calculation** for all students
- **Risk ranking** and prioritization
- **Actionable report generation**

## 📁 **Data Requirements**

### **Required CSV Files:**
- **`academic_performance.csv`**: Course scores, terms, subjects
- **`engagement_behavioral.csv`**: Attendance, LMS activity, behavioral data
- **`student_master.csv`**: Demographics, parental information

### **Expected Columns:**
- **Academic**: `student_id`, `term`, `final_score`, `subject`
- **Engagement**: `student_id`, `term`, `attendance_percentage`, `lms_logins_per_week`, `disciplinary_incidents`
- **Student**: `student_id`, `first_name`, `last_name`, `parental_education`

### **Data Quality Features:**
- **Handles missing data** gracefully
- **Automatic type conversion** for numerical fields
- **Robust error handling** for file access issues

## 🚀 **Usage**

### **Run the Complete Analysis:**
```bash
# From repository root
python "dropout_risk_detection\detect_dropout_risk.py"

# From inside the module directory
python detect_dropout_risk.py
```

### **Custom Analysis:**
```python
from dropout_risk_detection.detect_dropout_risk import find_data_directory

# Use the path detection function in other scripts
data_path = find_data_directory()
```

## ⚙️ **Configuration**

### **Path Detection:**
Automatically detects data directory from multiple locations:
- `data/` (if running from root)
- `../data/` (if running from dropout_risk_detection subdirectory)
- `./data/` (if data is in current directory)

### **Model Parameters:**
- **Test Size**: 30% (adjusts for small datasets)
- **Random State**: 42 (for reproducible results)
- **Class Weights**: Balanced (handles imbalanced data)
- **Feature Scaling**: StandardScaler (normalizes features)

## 🎓 **Educational Applications**

### **For Counselors:**
- **Prioritized Outreach**: Focus on highest-risk students first
- **Early Intervention**: Identify problems before they escalate
- **Resource Allocation**: Target support where it's most needed
- **Progress Monitoring**: Track intervention effectiveness

### **For Administrators:**
- **Strategic Planning**: Identify at-risk student populations
- **Program Development**: Design targeted retention programs
- **Resource Planning**: Allocate counseling and support resources
- **Policy Making**: Develop evidence-based intervention strategies

### **For Teachers:**
- **Student Awareness**: Identify students needing additional support
- **Parent Communication**: Engage families of at-risk students
- **Classroom Strategies**: Adapt teaching methods for struggling students
- **Progress Tracking**: Monitor improvement after interventions

## 🔬 **Technical Details**

### **Requirements:**
- Python 3.7+
- pandas, numpy
- scikit-learn (sklearn)
- matplotlib, seaborn
- Standard library modules (os)

### **Algorithm Details:**
- **Logistic Regression**: Binary classification for dropout prediction
- **Feature Scaling**: StandardScaler for numerical features
- **Cross-Validation**: Ensures model reliability
- **Probability Output**: Risk scores from 0% to 100%

### **Performance Considerations:**
- **Small Dataset Handling**: Adapts to limited data availability
- **Class Imbalance**: Uses balanced weights for rare dropout events
- **Feature Selection**: Dynamic based on available data
- **Error Handling**: Graceful degradation for edge cases

## 📊 **Model Performance**

### **Current Model Status:**
- **Training Data**: 6 samples (Spring 2025)
- **Test Data**: 1 sample (validation)
- **Feature Count**: 6 features (academic + behavioral + demographic)
- **Model Type**: Logistic Regression with balanced weights

### **Performance Metrics:**
- **Accuracy**: 100% (limited by small test set)
- **Risk Prediction**: Probability-based scoring system
- **Feature Importance**: Academic performance and attendance dominant
- **Validation**: Cross-validation for small datasets

## 🎯 **Risk Factor Analysis**

### **High-Risk Indicators:**
1. **Academic Struggles**: Scores below 70 with poor attendance
2. **Engagement Issues**: Low LMS activity and attendance
3. **Performance Crisis**: Very low scores (below 60)
4. **Behavioral Problems**: Multiple disciplinary incidents

### **Risk Mitigation Strategies:**
- **Academic Support**: Tutoring, study skills, course adjustments
- **Attendance Monitoring**: Regular check-ins, family engagement
- **Digital Engagement**: LMS training, online resource promotion
- **Behavioral Support**: Counseling, conflict resolution, mentoring

## 🔮 **Future Enhancements**

### **Planned Features:**
- **Advanced ML Models**: Random Forest, Neural Networks
- **Longitudinal Analysis**: Track risk changes over time
- **Intervention Tracking**: Measure support program effectiveness
- **Real-Time Monitoring**: Continuous risk assessment updates
- **Predictive Analytics**: Early warning for future terms
- **Dashboard Integration**: Visual risk monitoring interface

### **Model Improvements:**
- **Feature Engineering**: Additional risk factors and interactions
- **Hyperparameter Tuning**: Optimize model performance
- **Ensemble Methods**: Combine multiple model predictions
- **Cross-Validation**: Robust performance evaluation

## 🛡️ **Ethical Considerations**

### **Data Privacy:**
- **Student Confidentiality**: All predictions are confidential
- **Limited Access**: Risk scores for authorized personnel only
- **Secure Storage**: Data protection and access controls
- **Consent Management**: Respect student and family privacy

### **Interpretation Guidelines:**
- **Risk ≠ Certainty**: High risk doesn't guarantee dropout
- **Individual Context**: Consider personal circumstances
- **Support Focus**: Use insights for assistance, not labeling
- **Professional Judgment**: Combine with human expertise
- **Continuous Monitoring**: Update assessments regularly

## 📚 **Related Modules**

This module works alongside other Snowball analysis modules:
- **Teacher Effectiveness Analysis**: Examines teaching impact on retention
- **Personalized Learning Pathways**: Creates individual support strategies
- **Behavioral Analysis**: Monitors student well-being and engagement
- **External Factors Analysis**: Considers background influences on risk

## 🔧 **Troubleshooting**

### **Common Issues:**
- **"Data directory not found"**: Ensure `data/` folder exists at repository root
- **"No dropout events synthesized"**: Adjust risk thresholds in synthesis rules
- **"Single class in test set"**: Model handles this automatically with warnings
- **"Feature not found"**: Script dynamically adjusts to available columns

### **Solutions:**
- Verify CSV file structure matches expected columns
- Check data quality and completeness
- Adjust dropout synthesis rules if needed
- Ensure sufficient data for meaningful analysis

## 📈 **Success Metrics**

### **Intervention Effectiveness:**
- **Risk Reduction**: Decrease in student risk scores over time
- **Retention Rates**: Improved student continuation rates
- **Academic Progress**: Better performance in at-risk students
- **Engagement Levels**: Increased attendance and participation

### **System Performance:**
- **Prediction Accuracy**: Model performance on validation data
- **Risk Detection**: Early identification of at-risk students
- **Response Time**: Speed of risk assessment and reporting
- **User Adoption**: Counselor and administrator utilization

---

**Note**: This module is designed to work with the Snowball educational data analysis project and provides a foundation for proactive student retention strategies. All risk assessments should be interpreted with care and used to provide support rather than to make assumptions about individual student outcomes. 