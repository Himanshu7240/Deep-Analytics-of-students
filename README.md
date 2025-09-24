# Snowball Deep Analytics API

A comprehensive FastAPI application that provides predictive analytics, insights, and recommendations for student data analysis.

## 🚀 Features

This API provides 10 main endpoints covering:

### Predictions
1. **Academic Performance Prediction** - Predicts if a student is at-risk for poor academic performance
2. **Dropout Risk Detection** - Predicts the probability of a student dropping out or transferring

### Analysis
3. **Teacher Effectiveness Analysis** - Ranks teachers based on student score growth
4. **Talent Discovery** - Identifies students with non-curricular talents
5. **Behavioral & Emotional Analysis** - Generates confidential list of students showing signs of concern
6. **External Factors Impact** - Analyzes how external factors correlate with performance
7. **Peer Influence Tracking** - Provides student peer network data for analysis

### Recommendations
8. **Personalized Learning Pathways** - Generates customized learning recommendations for students
9. **Intervention Recommendations** - Suggests interventions for student problems
10. **Career Suggestions** - Recommends future career paths for students

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your data files are in the `data/` directory:**
   - `academic_performance.csv`
   - `engagement_behavioral.csv`
   - `student_master.csv`
   - `surveys_qualitative.csv`
   - `interventions_outcomes.csv`
   - `relational_social.csv`
   - `staff_faculty.csv`

## 🚀 Running the API

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Documentation (ReDoc):** http://localhost:8000/redoc
- **API Root:** http://localhost:8000/

## 🔗 API Endpoints

### Predictions (`/api/v1/predict`)

#### 1. Academic Risk Prediction
```
GET /api/v1/predict/academic-risk/{student_id}
```
Predicts if a student is at-risk for poor academic performance.

**Example:**
```bash
curl http://localhost:8000/api/v1/predict/academic-risk/STU-001
```

#### 2. Dropout Risk Detection
```
GET /api/v1/predict/dropout-risk/{student_id}
```
Predicts the probability of a student dropping out or transferring.

**Example:**
```bash
curl http://localhost:8000/api/v1/predict/dropout-risk/STU-001
```

#### 3. Batch Academic Risk Prediction
```
POST /api/v1/predict/batch-academic-risk
```
Predicts academic risk for multiple students at once.

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/predict/batch-academic-risk" \
     -H "Content-Type: application/json" \
     -d '["STU-001", "STU-002", "STU-003"]'
```

### Analysis (`/api/v1/analysis`)

#### 4. Teacher Effectiveness Analysis
```
GET /api/v1/analysis/teacher-effectiveness
```
Returns a ranked list of teachers based on student score growth.

#### 5. Talent Discovery
```
GET /api/v1/analysis/talent-discovery
```
Identifies students with non-curricular talents based on activities and performance.

#### 6. Behavioral Concerns Analysis
```
GET /api/v1/analysis/behavioral-concerns
```
Generates a confidential list of students showing signs of concern.

#### 7. External Factors Analysis
```
GET /api/v1/analysis/external-factors
```
Provides a summary of how external factors correlate with performance.

#### 8. Peer Network Analysis
```
GET /api/v1/analysis/peer-network
```
Returns the student peer network data for analysis.

### Recommendations (`/api/v1/recommend`)

#### 9. Personalized Learning Pathway
```
GET /api/v1/recommend/learning-pathway/{student_id}
```
Generates a personalized learning pathway for a student.

**Example:**
```bash
curl http://localhost:8000/api/v1/recommend/learning-pathway/STU-001
```

#### 10. Intervention Recommendations
```
GET /api/v1/recommend/intervention?problem=Low attendance
```
Recommends interventions for given student problems.

**Example:**
```bash
curl "http://localhost:8000/api/v1/recommend/intervention?problem=Low%20attendance"
```

#### 11. Career Suggestions
```
GET /api/v1/recommend/career-suggestion/{student_id}
```
Suggests future career paths for a student to explore.

**Example:**
```bash
curl http://localhost:8000/api/v1/recommend/career-suggestion/STU-001
```

#### 12. Batch Career Suggestions
```
POST /api/v1/recommend/batch-career-suggestions
```
Generates career suggestions for multiple students at once.

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/recommend/batch-career-suggestions" \
     -H "Content-Type: application/json" \
     -d '["STU-001", "STU-002", "STU-003"]'
```

## 📊 Response Examples

### Academic Risk Prediction Response
```json
{
  "student_id": "STU-001",
  "prediction": "At-Risk",
  "risk_probability": 0.65,
  "confidence_score": 0.85,
  "key_factors": ["Low final scores", "Poor attendance"],
  "timestamp": "2024-01-15T10:30:00"
}
```

### Teacher Effectiveness Response
```json
{
  "report_date": "2024-01-15T10:30:00",
  "effectiveness_ranking": [
    {
      "teacher_id": "TCH-001",
      "teacher_name": "Sunita Rao",
      "mean_score_growth": 5.5,
      "student_count": 30,
      "growth_consistency": 2.1
    }
  ],
  "total_teachers": 5,
  "average_score_growth": 3.2
}
```

### Career Suggestion Response
```json
{
  "student_id": "STU-001",
  "student_name": "Aarav Sharma",
  "top_recommendations": [
    {
      "cluster": "Engineering & Technology",
      "match_score": 15,
      "strength_level": "Strong",
      "key_alignment": ["Math", "Science"]
    }
  ],
  "supporting_evidence": {
    "strong_subjects": ["Math", "Science"],
    "extracurricular_activities": ["Coding Club"],
    "stated_interests": ["Technology"],
    "total_evidence_points": 3
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🔧 Configuration

The API automatically loads data from the `data/` directory. Make sure all required CSV files are present:

- **academic_performance.csv** - Student academic scores and performance data
- **engagement_behavioral.csv** - Student engagement and behavioral data
- **student_master.csv** - Student demographic and personal information
- **surveys_qualitative.csv** - Student survey responses
- **interventions_outcomes.csv** - Intervention history and outcomes
- **relational_social.csv** - Student relationships and social data
- **staff_faculty.csv** - Teacher and staff information

## 🚨 Error Handling

The API includes comprehensive error handling:

- **404 Not Found** - When a student ID doesn't exist
- **500 Internal Server Error** - When data loading or processing fails
- **Validation Errors** - When request parameters are invalid

## 🔒 Security Considerations

- The behavioral concerns endpoint returns confidential information
- Consider implementing authentication for production use
- Data should be properly secured in production environments

## 🧪 Testing

You can test the API using:

1. **The interactive Swagger UI** at http://localhost:8000/docs
2. **curl commands** as shown in the examples above
3. **Any HTTP client** like Postman or Insomnia

## 📈 Performance

- The API is optimized for quick responses
- Data is loaded once per request for simplicity
- For production use, consider implementing caching
- Batch endpoints are available for processing multiple students efficiently

## 🤝 Contributing

To extend the API:

1. Add new endpoints to the appropriate router files
2. Update the Pydantic models for request/response validation
3. Add proper error handling
4. Update this README with new endpoint documentation

## 📝 License

This project is for educational and demonstration purposes.

## 🆘 Support

If you encounter issues:

1. Check that all data files are present in the `data/` directory
2. Verify that all dependencies are installed correctly
3. Check the console output for error messages
4. Ensure the API server is running on the correct port

---

**Happy Analyzing! 🎓📊**
