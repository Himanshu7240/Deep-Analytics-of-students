from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

# Data loading function
def load_data():
    """Load all necessary datasets"""
    try:
        base_path = "data/"
        df_academic = pd.read_csv(base_path + 'academic_performance.csv')
        df_engagement = pd.read_csv(base_path + 'engagement_behavioral.csv')
        df_student = pd.read_csv(base_path + 'student_master.csv')
        df_surveys = pd.read_csv(base_path + 'surveys_qualitative.csv')
        df_interventions = pd.read_csv(base_path + 'interventions_outcomes.csv')
        df_relational = pd.read_csv(base_path + 'relational_social.csv')
        df_staff = pd.read_csv(base_path + 'staff_faculty.csv')
        return df_academic, df_engagement, df_student, df_surveys, df_interventions, df_relational, df_staff
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

# Pydantic models for responses
class LearningPathwayResponse(BaseModel):
    student_id: str
    student_name: str
    areas_for_improvement: List[Dict[str, Any]]
    areas_for_enrichment: List[Dict[str, Any]]
    overall_recommendations: List[str]
    timestamp: str

class InterventionRecommendationResponse(BaseModel):
    problem: str
    recommended_interventions: List[Dict[str, Any]]
    success_rate: float
    confidence_level: str
    timestamp: str

class CareerSuggestionResponse(BaseModel):
    student_id: str
    student_name: str
    top_recommendations: List[Dict[str, Any]]
    supporting_evidence: Dict[str, Any]
    timestamp: str

# Career clusters knowledge base
CAREER_CLUSTERS = {
    'Engineering & Technology': {
        'strong_subjects': ['Math', 'Science'],
        'relevant_activities': ['Coding Club', 'Robotics', 'Science Olympiad', 'Physics'],
        'stated_interests': ['STEM', 'Technology', 'Engineer', 'IT', 'Software'],
        'weight': {'subject': 3, 'activity': 2, 'interest': 5}
    },
    'Medicine & Healthcare': {
        'strong_subjects': ['Science'],
        'relevant_activities': ['Volunteering', 'Science Club', 'Biology'],
        'stated_interests': ['Healthcare', 'Doctor', 'Nurse', 'Medical', 'Pharmacist'],
        'weight': {'subject': 4, 'activity': 3, 'interest': 5}
    },
    'Business & Finance': {
        'strong_subjects': ['Math', 'Economics'],
        'relevant_activities': ['Debate Club', 'Student Government', 'Economics Club'],
        'stated_interests': ['Business', 'Management', 'Finance', 'Sales', 'Marketing', 'Entrepreneur', 'Analyst'],
        'weight': {'subject': 3, 'activity': 3, 'interest': 5}
    },
    'Arts, Humanities & Law': {
        'strong_subjects': ['English', 'History'],
        'relevant_activities': ['Debate Club', 'Model UN', 'School Newspaper', 'Art Club', 'Drama Club', 'Author'],
        'stated_interests': ['Writing', 'History', 'Arts', 'Law', 'Journalist'],
        'weight': {'subject': 3, 'activity': 3, 'interest': 5}
    }
}

# --- Endpoint 3: Personalized Learning Pathways ---
@router.get("/learning-pathway/{student_id}", response_model=LearningPathwayResponse)
def get_learning_pathway(student_id: str):
    """
    Generates a personalized learning pathway for a student.
    
    - **student_id**: The ID of the student (e.g., STU-001)
    """
    try:
        df_academic, df_engagement, df_student, df_surveys, _, _, _ = load_data()
        
        # Check if student exists
        if student_id not in df_student['student_id'].values:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        # Get student data
        student_info = df_student[df_student['student_id'] == student_id].iloc[0]
        student_name = f"{student_info['first_name']} {student_info['last_name']}"
        
        student_academic = df_academic[df_academic['student_id'] == student_id]
        student_engagement = df_engagement[df_engagement['student_id'] == student_id]
        student_surveys = df_surveys[df_surveys['student_id'] == student_id]
        
        if student_academic.empty:
            raise HTTPException(status_code=404, detail=f"No academic data found for student {student_id}")
        
        # Analyze performance by subject
        subject_performance = student_academic.groupby('subject').agg({
            'final_score': ['mean', 'count'],
            'mid_term_score': 'mean'
        }).reset_index()
        
        subject_performance.columns = ['subject', 'avg_final_score', 'term_count', 'avg_mid_score']
        
        areas_for_improvement = []
        areas_for_enrichment = []
        overall_recommendations = []
        
        # Identify areas for improvement (subjects with scores < 75)
        weak_subjects = subject_performance[subject_performance['avg_final_score'] < 75]
        for _, subject in weak_subjects.iterrows():
            improvement_score = 75 - subject['avg_final_score']
            areas_for_improvement.append({
                "subject": subject['subject'],
                "current_score": round(subject['avg_final_score'], 1),
                "target_score": 75,
                "improvement_needed": round(improvement_score, 1),
                "recommendation": f"Focus on {subject['subject']} fundamentals and seek additional support"
            })
        
        # Identify areas for enrichment (subjects with scores > 85)
        strong_subjects = subject_performance[subject_performance['avg_final_score'] > 85]
        for _, subject in strong_subjects.iterrows():
            areas_for_enrichment.append({
                "subject": subject['subject'],
                "current_score": round(subject['avg_final_score'], 1),
                "enrichment_opportunity": f"Advanced {subject['subject']} courses or competitions",
                "recommendation": f"Explore advanced topics in {subject['subject']} and consider leadership roles"
            })
        
        # Engagement analysis
        if not student_engagement.empty:
            avg_attendance = student_engagement['attendance_percentage'].mean()
            avg_lms_logins = student_engagement['lms_logins_per_week'].mean()
            
            if avg_attendance < 90:
                overall_recommendations.append("Improve attendance to enhance learning consistency")
            
            if avg_lms_logins < 4:
                overall_recommendations.append("Increase online engagement through LMS platform")
        
        # Survey-based recommendations
        if not student_surveys.empty:
            learning_style_surveys = student_surveys[student_surveys['survey_type'] == 'Learning Style']
            if not learning_style_surveys.empty:
                learning_preferences = learning_style_surveys['response'].tolist()
                overall_recommendations.append(f"Leverage learning preferences: {', '.join(learning_preferences[:2])}")
        
        # Add general recommendations if none specific
        if not areas_for_improvement and not areas_for_enrichment:
            overall_recommendations.append("Maintain current performance and explore new subjects")
        
        if not overall_recommendations:
            overall_recommendations.append("Continue current study habits and seek feedback from teachers")
        
        return LearningPathwayResponse(
            student_id=student_id,
            student_name=student_name,
            areas_for_improvement=areas_for_improvement,
            areas_for_enrichment=areas_for_enrichment,
            overall_recommendations=overall_recommendations,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning pathway: {str(e)}")

# --- Endpoint 9: Intervention Recommendation Engine ---
@router.get("/intervention", response_model=InterventionRecommendationResponse)
def get_intervention_recommendation(problem: str):
    """
    Recommends interventions for given student problems.
    
    - **problem**: The issue observed (e.g., "Low attendance", "Falling grades", "Behavioral issues")
    """
    try:
        _, _, _, _, df_interventions, _, _ = load_data()
        
        # Define intervention strategies based on problem types
        intervention_strategies = {
            "low attendance": [
                {
                    "intervention": "Parent-Teacher Meeting",
                    "description": "Schedule meeting to discuss attendance issues and develop action plan",
                    "success_rate": 0.85,
                    "timeframe": "1-2 weeks",
                    "resources_needed": ["Teacher", "Parent", "Counselor"]
                },
                {
                    "intervention": "Attendance Monitoring Program",
                    "description": "Implement daily check-ins and attendance tracking",
                    "success_rate": 0.75,
                    "timeframe": "Ongoing",
                    "resources_needed": ["Administrator", "Teacher"]
                }
            ],
            "falling grades": [
                {
                    "intervention": "Academic Support Program",
                    "description": "Provide tutoring and additional academic resources",
                    "success_rate": 0.80,
                    "timeframe": "4-8 weeks",
                    "resources_needed": ["Tutor", "Teacher", "Study Materials"]
                },
                {
                    "intervention": "Study Skills Workshop",
                    "description": "Teach effective study techniques and time management",
                    "success_rate": 0.70,
                    "timeframe": "2-4 weeks",
                    "resources_needed": ["Counselor", "Study Materials"]
                }
            ],
            "behavioral issues": [
                {
                    "intervention": "Behavioral Intervention Plan",
                    "description": "Develop structured behavior management approach",
                    "success_rate": 0.75,
                    "timeframe": "6-12 weeks",
                    "resources_needed": ["Counselor", "Teacher", "Parent"]
                },
                {
                    "intervention": "Social Skills Training",
                    "description": "Provide guidance on appropriate social interactions",
                    "success_rate": 0.65,
                    "timeframe": "8-12 weeks",
                    "resources_needed": ["Counselor", "Peer Mentors"]
                }
            ],
            "low engagement": [
                {
                    "intervention": "Personalized Learning Plan",
                    "description": "Create customized learning activities based on student interests",
                    "success_rate": 0.80,
                    "timeframe": "Ongoing",
                    "resources_needed": ["Teacher", "Technology"]
                },
                {
                    "intervention": "Extracurricular Involvement",
                    "description": "Encourage participation in clubs and activities",
                    "success_rate": 0.70,
                    "timeframe": "Ongoing",
                    "resources_needed": ["Activity Coordinators"]
                }
            ]
        }
        
        # Find matching interventions
        problem_lower = problem.lower()
        recommended_interventions = []
        
        for key, interventions in intervention_strategies.items():
            if key in problem_lower or any(word in problem_lower for word in key.split()):
                recommended_interventions.extend(interventions)
        
        # If no specific match, provide general recommendations
        if not recommended_interventions:
            recommended_interventions = [
                {
                    "intervention": "Student Assessment",
                    "description": "Conduct comprehensive assessment to identify root causes",
                    "success_rate": 0.90,
                    "timeframe": "1-2 weeks",
                    "resources_needed": ["Counselor", "Teacher"]
                },
                {
                    "intervention": "Parent Consultation",
                    "description": "Meet with parents to discuss concerns and develop support plan",
                    "success_rate": 0.75,
                    "timeframe": "1 week",
                    "resources_needed": ["Teacher", "Parent"]
                }
            ]
        
        # Calculate overall success rate
        avg_success_rate = np.mean([intervention['success_rate'] for intervention in recommended_interventions])
        
        # Determine confidence level
        if avg_success_rate >= 0.8:
            confidence_level = "High"
        elif avg_success_rate >= 0.6:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
        
        return InterventionRecommendationResponse(
            problem=problem,
            recommended_interventions=recommended_interventions,
            success_rate=round(avg_success_rate, 2),
            confidence_level=confidence_level,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error recommending interventions: {str(e)}")

# --- Endpoint 10: Future Career or Stream Suggestion ---
@router.get("/career-suggestion/{student_id}", response_model=CareerSuggestionResponse)
def get_career_suggestion(student_id: str):
    """
    Suggests future career paths for a student to explore.
    
    - **student_id**: The ID of the student (e.g., STU-001)
    """
    try:
        df_academic, df_engagement, df_student, df_surveys, _, _, _ = load_data()
        
        # Check if student exists
        if student_id not in df_student['student_id'].values:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        # Get student data
        student_info = df_student[df_student['student_id'] == student_id].iloc[0]
        student_name = f"{student_info['first_name']} {student_info['last_name']}"
        
        student_academic = df_academic[df_academic['student_id'] == student_id]
        student_engagement = df_engagement[df_engagement['student_id'] == student_id]
        student_surveys = df_surveys[df_surveys['student_id'] == student_id]
        
        # Get student profile
        strong_subjects = []
        if not student_academic.empty:
            # Get subjects where student scores above 80
            subject_scores = student_academic.groupby('subject')['final_score'].mean()
            strong_subjects = subject_scores[subject_scores > 80].index.tolist()
        
        # Get activities
        activities = []
        if not student_engagement.empty:
            activities = student_engagement['extracurricular_activity'].unique()
            activities = [act for act in activities if act != 'None' and pd.notna(act)]
        
        # Get stated interests from surveys
        interests = []
        if not student_surveys.empty:
            career_surveys = student_surveys[student_surveys['survey_type'] == 'Career Interest']
            interests = career_surveys['response'].unique().tolist()
        
        # Score career clusters
        scores = {}
        for cluster_name, attributes in CAREER_CLUSTERS.items():
            score = 0
            
            # Score based on strong subjects
            for subject in strong_subjects:
                if subject in attributes['strong_subjects']:
                    score += attributes['weight']['subject']
            
            # Score based on activities
            for activity in activities:
                if any(keyword.lower() in activity.lower() for keyword in attributes['relevant_activities']):
                    score += attributes['weight']['activity']
            
            # Score based on stated interests
            for interest in interests:
                if any(keyword.lower() in interest.lower() for keyword in attributes['stated_interests']):
                    score += attributes['weight']['interest']
            
            if score > 0:
                scores[cluster_name] = score
        
        # Sort by score and get top recommendations
        ranked_recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_recommendations = []
        
        for cluster, score in ranked_recommendations[:3]:  # Top 3 recommendations
            top_recommendations.append({
                "cluster": cluster,
                "match_score": score,
                "strength_level": "Strong" if score >= 10 else "Moderate" if score >= 5 else "Weak",
                "key_alignment": CAREER_CLUSTERS[cluster]['strong_subjects']
            })
        
        # Prepare supporting evidence
        supporting_evidence = {
            "strong_subjects": strong_subjects,
            "extracurricular_activities": activities,
            "stated_interests": interests,
            "total_evidence_points": len(strong_subjects) + len(activities) + len(interests)
        }
        
        return CareerSuggestionResponse(
            student_id=student_id,
            student_name=student_name,
            top_recommendations=top_recommendations,
            supporting_evidence=supporting_evidence,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating career suggestions: {str(e)}")

# --- Batch Career Suggestions Endpoint ---
class BatchCareerRequest(BaseModel):
    student_ids: List[str]

@router.post("/batch-career-suggestions")
def get_batch_career_suggestions(payload: BatchCareerRequest):
    """
    Generates career suggestions for multiple students at once.
    
    - **student_ids**: List of student IDs
    """
    try:
        results = []
        for student_id in payload.student_ids:
            try:
                result = get_career_suggestion(student_id)
                results.append(result.dict())
            except HTTPException as e:
                results.append({
                    "student_id": student_id,
                    "error": e.detail,
                    "status": "failed"
                })
        
        return {
            "suggestions": results,
            "total_students": len(payload.student_ids),
            "successful_suggestions": len([r for r in results if "error" not in r]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch career suggestions: {str(e)}")
