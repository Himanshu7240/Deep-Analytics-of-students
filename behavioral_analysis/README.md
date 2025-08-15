# Behavioral Analysis: Early Warning System

## Overview
The Behavioral Analysis module is an **early warning system** designed to identify students who may benefit from supportive check-ins from counselors or teachers. It analyzes behavioral and academic changes between terms to flag students who may need additional support or intervention.

## ⚠️ **Important Disclaimer**
**This is NOT a diagnostic tool.** It is an early warning system to identify students who may benefit from a supportive check-in. All results must be handled with **confidentiality and care**.

## What It Does

### 🎯 **Core Functionality**
- **Monitors student behavior** across multiple terms
- **Tracks academic performance** changes over time
- **Identifies attendance patterns** and drops
- **Flags disciplinary incidents** and changes
- **Monitors extracurricular engagement** changes
- **Tracks self-reported stress levels** from surveys
- **Logs counselor visit patterns**

### 📊 **Risk Assessment System**
The module uses a **point-based scoring system** to identify students at risk:

#### **Risk Factors & Scoring:**
- **📉 Academic Drop** (≥15 points): **3 points**
- **📉 Attendance Drop** (≥10%): **3 points**
- **🚨 New Disciplinary Incidents**: **2 points**
- **🚫 Withdrew from Activities**: **2 points**
- **😰 High Self-Reported Stress** (≥4/5): **4 points**
- **👥 Counselor Visit**: **1 point**

#### **Threshold:**
- **Students flagged** when total concern score ≥ **5 points**
- **Lower scores** indicate minor concerns
- **Higher scores** suggest need for immediate attention

### 🔍 **Analysis Process**
1. **Data Loading**: Reads engagement, academic, survey, and student data
2. **Term Comparison**: Compares Fall 2024 vs Spring 2025 data
3. **Risk Calculation**: Applies scoring rules to each student
4. **Threshold Filtering**: Identifies students meeting concern criteria
5. **Report Generation**: Creates confidential check-in list

## Data Requirements

### 📁 **Required CSV Files** (in `data/` folder)
- **`engagement_behavioral.csv`**: Attendance, disciplinary incidents, activities, counselor visits
- **`academic_performance.csv`**: Student course scores and performance data
- **`surveys_qualitative.csv`**: Student self-reported stress and well-being data
- **`student_master.csv`**: Student demographic and basic information

### 📋 **Expected Columns**
- **Engagement**: `student_id`, `term`, `attendance_percentage`, `disciplinary_incidents`, `extracurricular_activity`, `counselor_visit`
- **Academic**: `student_id`, `term`, `final_score`
- **Surveys**: `student_id`, `term`, `survey_type`, `question`, `response`
- **Student Master**: `student_id`, `first_name`, `last_name`

### 🔍 **Data Quality Features**
- **Handles missing data** gracefully (NULL, NaN values)
- **Converts data types** automatically (strings to numeric)
- **Validates term availability** (requires Fall 2024 and Spring 2025)
- **Robust error handling** for file access and data processing

## Usage

### 🚀 **Run the Complete Analysis**
```bash
# From repository root
python "behavioral_analysis\identify_concern_students.py"

# From inside the module directory
python identify_concern_students.py
```

### 🎓 **Custom Analysis**
```python
from behavioral_analysis.identify_concern_students import find_data_directory

# Use the path detection function in other scripts
data_path = find_data_directory()
```

## Output Examples

### 📈 **Sample Data Processing**
```
Step 2: Loading and preparing student data...
Found data directory at: data/
Data loaded successfully.
Step 3: Comparing Spring 2025 data against Fall 2024 baseline...
Academic records: 33
Engagement records: 24
Available terms: ['Fall 2024' 'Spring 2025' 'Fall 2025']
Merged records: 37
Records for required terms: 24
Terms found: ['Fall 2024' 'Spring 2025']
Data prepared. 12 students found with data for both terms.
```

### 🎯 **Report Output**
```
--- Confidential Student Check-in List ---
Report Date: 2025-08-15
Flagging students with Concern Score >= 5

Student ID  Name          Concern Score  Reasons for Flag
STU-001     Aarav Sharma  6              Academic Drop (>15 pts); Attendance Drop (>10%)
STU-002     Priya Patel   5              New Disciplinary Incident; Withdrew from Activities
```

## Configuration

### ⚙️ **Customizable Risk Thresholds**
```python
CONCERN_SCORE_THRESHOLDS = {
    'ACADEMIC_DROP': {'points': 3, 'threshold': 15},      # Score drop of 15+ points
    'ATTENDANCE_DROP': {'points': 3, 'threshold': 10},    # Attendance drop of 10%+
    'NEW_DISCIPLINARY_INCIDENT': {'points': 2},
    'WITHDREW_FROM_ACTIVITY': {'points': 2},
    'HIGH_STRESS_REPORT': {'points': 4, 'threshold': 4},  # Self-reported stress >= 4/5
    'COUNSELOR_VISIT': {'points': 1}                      # Support indicator
}
FINAL_SCORE_THRESHOLD = 5  # Students flagged when score >= this
```

### 📍 **Path Detection**
Automatically detects data directory from multiple locations:
- `data/` (if running from root)
- `../data/` (if running from behavioral_analysis subdirectory)
- `./data/` (if data is in current directory)

## Use Cases

### 👨‍🏫 **For Educators**
- **Counselors** identifying students needing support
- **Teachers** recognizing behavioral changes early
- **Administrators** monitoring student well-being trends
- **Student support teams** prioritizing interventions

### 🏫 **For Institutions**
- **Early intervention** programs
- **Student retention** strategies
- **Resource allocation** for support services
- **Compliance** with student welfare requirements

### 👨‍👩‍👧‍👦 **For Parents**
- **Understanding** their child's school experience
- **Supporting** academic and social development
- **Communication** with teachers and counselors
- **Early awareness** of potential issues

## Technical Details

### 🐍 **Requirements**
- Python 3.7+
- pandas
- Standard library modules (os, datetime)

### 🔍 **Algorithm Details**
- **Term-based comparison** (Fall 2024 vs Spring 2025)
- **Point-based scoring** system for risk assessment
- **Data validation** and type conversion
- **Missing data handling** with graceful degradation

### 🛡️ **Error Handling**
- **File validation** before processing
- **Data quality checks** during analysis
- **Graceful degradation** for missing data
- **Informative error messages** for troubleshooting

## Example Analysis

### 📊 **Data Processing Flow**
1. **Load 33 academic records** and **24 engagement records**
2. **Merge datasets** to create **37 combined records**
3. **Filter for required terms** (Fall 2024, Spring 2025)
4. **Process 12 students** with complete data for both terms
5. **Calculate concern scores** based on defined risk factors
6. **Generate confidential report** for flagged students

### 🎯 **Risk Detection Examples**
- **Academic Drop**: Student's final score dropped from 85 to 65 (20-point drop = 3 points)
- **Attendance Issues**: Student's attendance dropped from 95% to 80% (15% drop = 3 points)
- **Behavioral Changes**: New disciplinary incidents in Spring term (2 points)
- **Social Withdrawal**: Student stopped participating in extracurriculars (2 points)
- **Stress Indicators**: Self-reported stress level of 4/5 (4 points)

## Customization

### 📚 **Adding New Risk Factors**
```python
CONCERN_SCORE_THRESHOLDS['NEW_RISK_FACTOR'] = {
    'points': 2,
    'threshold': 5  # if applicable
}
```

### ⚖️ **Adjusting Scoring Weights**
```python
# Increase academic drop sensitivity
CONCERN_SCORE_THRESHOLDS['ACADEMIC_DROP']['threshold'] = 10  # Flag smaller drops

# Adjust final threshold
FINAL_SCORE_THRESHOLD = 3  # More sensitive flagging
```

### 📊 **Enhanced Analysis Features**
- Add **confidence scores** for risk assessments
- Implement **trend analysis** across multiple terms
- Create **intervention recommendations** based on risk factors
- Add **peer comparison** and benchmarking

## Troubleshooting

### ❌ **Common Issues**
- **"Data directory not found"**: Ensure `data/` folder exists at repository root
- **"No data for required terms"**: Verify Fall 2024 and Spring 2025 data exists
- **"No students flagged"**: Check if concern thresholds are too high
- **"File not found"**: Verify CSV files exist and are accessible

### 🔧 **Solutions**
- Verify CSV file structure matches expected columns
- Check for data consistency across terms
- Ensure student IDs match across all datasets
- Validate that required terms exist in the data

## Contributing

### 📝 **Adding New Features**
- **New risk factors** with appropriate scoring
- **Enhanced data validation** and quality checks
- **Visualization options** for risk trends
- **Export functionality** (CSV, PDF reports)
- **Integration** with other analysis modules

### 🧪 **Testing**
- Test with various student profiles and risk levels
- Verify risk factor detection accuracy
- Check error handling with missing/invalid data
- Validate scoring calculations and thresholds
- Test path detection from various locations

## Future Enhancements

### 🚀 **Planned Features**
- **Machine learning** for improved risk prediction
- **Confidence scoring** for risk assessments
- **Intervention tracking** and outcome measurement
- **Peer benchmarking** and comparison
- **Integration** with academic performance data
- **Visual dashboards** for risk monitoring
- **Automated alerts** for high-risk students

## Ethical Considerations

### 🔒 **Confidentiality**
- **All results are confidential** and should be handled with care
- **Student privacy** must be protected at all times
- **Access should be limited** to authorized personnel only

### 🎯 **Purpose**
- **Not for punishment** or negative labeling
- **Designed for support** and early intervention
- **Focus on student well-being** and success
- **Professional judgment** required for interpretation

---

**Note**: This module is designed to work with the Snowball educational data analysis project and provides a foundation for proactive student support and intervention strategies. 