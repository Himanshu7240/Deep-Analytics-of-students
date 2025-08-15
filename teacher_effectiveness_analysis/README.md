## Teacher Effectiveness Analysis

### Overview
This module analyzes teacher effectiveness using student performance and course-teacher mappings. It computes growth metrics, aggregates results at the teacher level, and produces clear visualizations.

### Inputs (CSV files in `data/`)
- **`academic_performance.csv`**: per-student course outcomes
  - Key columns: `student_id`, `course_id`, `term`, `subject`, `mid_term_score`, `final_score`, `standardized_test_score`
- **`relational_social.csv`**: maps students/courses/terms to teachers
  - Key columns: `student_id`, `course_id`, `term`, `subject`, `teacher_id`
- **`staff_faculty.csv`**: teacher metadata
  - Key columns: `teacher_id`, `first_name`, `last_name`, `qualification`, `years_experience`, `specialization`, `effectiveness_rating_5`

Notes:
- The script auto-detects `data/` whether you run it from the repo root or from `teacher_effectiveness_analysis/`.
- String values like `NULL` in score columns are treated as missing values.

### Methodology
- **Load**: Read the three CSVs.
- **Join scores ↔ teacher mapping**: inner-join `academic_performance` with `relational_social` on `['student_id','course_id','term','subject']`.
- **Add teacher details**: left-join with `staff_faculty` on `teacher_id`.
- **Type handling**: coerce `mid_term_score`, `final_score`, `years_experience`, `effectiveness_rating_5` to numeric.
- **Filter**: drop rows with missing `mid_term_score` or `final_score`.
- **Metric**: compute `score_growth = final_score - mid_term_score`.
- **Aggregate by teacher**: compute
  - `mean_score_growth`, `mean_final_score`, `mean_midterm_score`
  - `std_score_growth`
  - `student_record_count`
- **Labels**: create `First Last (TCH-XX)` for plot readability.

### Visualizations (saved in this folder)
- `teacher_effectiveness_ranking.png`: bar chart of mean score growth per teacher
- `experience_vs_effectiveness.png`: experience vs growth (bubble size = student count, color = specialization)
- `score_growth_distribution.png`: distribution (box plots) of student score growth by teacher

### Requirements
- Python 3.10+
- Packages: pandas, seaborn, matplotlib

Install dependencies:
```bash
pip install pandas seaborn matplotlib
```

### How to Run (Windows PowerShell or any shell)
From the repository root:
```bash
python "teacher_effectiveness_analysis\analyze_teacher_effectiveness.py"
```
From inside `teacher_effectiveness_analysis/`:
```bash
python analyze_teacher_effectiveness.py
```

The script prints a teacher summary table and saves the charts listed above.

### Output Example (summary columns)
- `teacher_id`, `first_name`, `last_name`, `specialization`, `years_experience`, `effectiveness_rating_5`
- `mean_midterm_score`, `mean_final_score`, `mean_score_growth`, `std_score_growth`, `student_record_count`

Only teachers present in both the mapping and performance data (and with complete scores) will appear in the summary.

### Customization
- Filter by subject or term by subsetting the dataframes before aggregation.
- Export the summary to CSV:
  - Add: `teacher_effectiveness.to_csv('teacher_effectiveness_summary.csv', index=False)` at the end of the script.

### Troubleshooting
- **Data directory not found**: Ensure a `data/` folder exists at repo root next to `teacher_effectiveness_analysis/`.
- **Missing columns**: Confirm the CSV headers match the expected names listed above.
- **No teachers in output**: Verify that `relational_social.csv` has matching `student_id/course_id/term/subject` pairs present in `academic_performance.csv`, and that scores are not missing.

