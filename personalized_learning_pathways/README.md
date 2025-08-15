# Personalized Learning Pathways Generator

## Overview
This module generates **individualized learning recommendations** for students based on their academic performance, strengths, weaknesses, and extracurricular activities. It provides actionable insights to help students, teachers, and parents create personalized educational plans.

## What It Does

### 🎯 **Core Functionality**
- **Analyzes student performance** using intelligent thresholds
- **Identifies academic strengths** (scores ≥ 85) and **weaknesses** (scores < 70)
- **Generates subject-specific recommendations** for improvement and enrichment
- **Provides holistic guidance** based on extracurricular participation
- **Creates personalized reports** with actionable advice

### 📊 **Analysis Process**
1. **Data Loading**: Reads student academic, engagement, and demographic data
2. **Performance Assessment**: Evaluates scores against defined thresholds
3. **Recommendation Generation**: Creates subject-specific improvement and enrichment strategies
4. **Holistic Analysis**: Considers extracurricular activities and overall development

### 🔧 **Key Features**
- **Auto-detects data directory** (works from any location)
- **Handles missing data gracefully** (NULL values, incomplete records)
- **Subject-specific recommendations** for Math, Science, English, History, Economics
- **Personalized student reports** with actionable advice
- **Robust error handling** for various data scenarios

## Data Requirements

### 📁 **Required CSV Files** (in `data/` folder)
- **`academic_performance.csv`**: Student course scores and performance data
- **`engagement_behavioral.csv`**: Extracurricular activities and engagement metrics
- **`student_master.csv`**: Student demographic and basic information

### 📋 **Expected Columns**
- **Academic Performance**: `student_id`, `course_id`, `term`, `subject`, `mid_term_score`, `final_score`
- **Engagement**: `student_id`, `term`, `extracurricular_activity`
- **Student Master**: `student_id`, `first_name`, `last_name`

## Usage

### 🚀 **Run the Complete Analysis**
```bash
# From repository root
python "personalized_learning_pathways\generate_pathway.py"

# From inside the module directory
python generate_pathway.py
```

### 🎓 **Analyze Specific Students**
```python
from personalized_learning_pathways.generate_pathway import generate_learning_pathway

# Generate pathway for a specific student
generate_learning_pathway('STU-001')

# Or with custom data path
generate_learning_pathway('STU-001', data_path='path/to/data/')
```

## Output Examples

### 📈 **Areas for Improvement**
- **Math**: Focus on foundational concepts, seek peer tutoring, use Khan Academy
- **Science**: Review lab reports, form study groups, seek teacher help
- **English**: Work on essay structure, read widely, request feedback
- **History**: Create timelines, use flashcards, practice thesis writing
- **Economics**: Review core principles, connect to current events

### 🌟 **Areas for Enrichment**
- **Math**: Join Coding Club, explore AP Calculus, competitive programming
- **Science**: Science Olympiad, science fair projects, robotics clubs
- **English**: Debate Club, school newspaper, creative writing workshops
- **History**: History Bowl, museum volunteering, Model UN
- **Economics**: Investment clubs, business competitions, financial reading

### 🎯 **Holistic Pathway Notes**
- Extracurricular activity recommendations
- Links between academic strengths and activities
- Personal development suggestions

## Configuration

### ⚙️ **Customizable Thresholds**
```python
STRENGTH_THRESHOLD = 85    # Scores above this are strengths
WEAKNESS_THRESHOLD = 70    # Scores below this are weaknesses
```

### 📚 **Recommendation Customization**
- Modify `STRENGTH_RECOMMENDATIONS` and `WEAKNESS_RECOMMENDATIONS` dictionaries
- Add new subjects and recommendations
- Customize advice based on your institution's offerings

## Use Cases

### 👨‍🏫 **For Educators**
- **Academic advisors** creating personalized study plans
- **Teachers** identifying student needs and opportunities
- **Curriculum developers** understanding student strengths/weaknesses

### 👨‍🎓 **For Students**
- **Self-assessment** of academic performance
- **Goal setting** for improvement areas
- **Discovery** of enrichment opportunities

### 👨‍👩‍👧‍👦 **For Parents**
- **Understanding** their child's academic profile
- **Supporting** educational decisions
- **Identifying** areas for additional support

## Technical Details

### 🐍 **Requirements**
- Python 3.7+
- pandas
- Standard library modules (os, datetime)

### 🔍 **Path Detection**
The script automatically detects the data directory from multiple possible locations:
- `data/` (if running from root)
- `../data/` (if running from module directory)
- `./data/` (if data is in current directory)

### 🛡️ **Error Handling**
- Graceful handling of missing data files
- Validation of student IDs
- Proper handling of NULL/NaN values
- Informative error messages

## Example Output

```
============================================================
Generating Personalized Learning Pathway for: STU-002
Report Generated On: 2025-08-15 16:06:14
============================================================
Found data directory at: data/
Analysis based on the latest available term: Spring 2025

--- Areas for Improvement ---
Great work, Priya! No specific academic weaknesses identified in the last term.

--- Areas for Enrichment ---
Priya, let's work on building up your strengths! Keep working hard.

--- Holistic Pathway Note ---
Your participation in Art Club is fantastic.
Try to find links between your academic strengths and your activities for a powerful combination.
============================================================
```

## Troubleshooting

### ❌ **Common Issues**
- **"Data directory not found"**: Ensure `data/` folder exists at repository root
- **"Student ID not found"**: Verify the student ID exists in `student_master.csv`
- **"No academic records"**: Check that the student has performance data
- **"No complete records"**: Ensure final scores are not NULL/NaN

### 🔧 **Solutions**
- Verify CSV file structure matches expected columns
- Check for data consistency (no mixed data types)
- Ensure student IDs match across all files
- Validate that scores are numeric or properly formatted

## Contributing

### 📝 **Adding New Features**
- Add new subjects to recommendation dictionaries
- Implement additional analysis metrics
- Create new visualization options
- Add export functionality (CSV, PDF reports)

### 🧪 **Testing**
- Test with various student profiles
- Verify error handling with missing data
- Check path detection from different locations
- Validate recommendation quality and relevance

---

**Note**: This module is designed to work with the Snowball educational data analysis project and provides a foundation for personalized learning analytics. 