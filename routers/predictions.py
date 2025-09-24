from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime

router = APIRouter(
    prefix="/predict",
    tags=["Predictions"]
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

# Pydantic models for request/response
class StudentPredictionRequest(BaseModel):
    student_id: str

class AcademicRiskResponse(BaseModel):
    student_id: str
    prediction: str
    risk_probability: float
    confidence_score: float
    key_factors: List[str]
    timestamp: str

class DropoutRiskResponse(BaseModel):
    student_id: str
    dropout_risk_probability: float
    risk_level: str
    key_factors: List[str]
    recommendations: List[str]
    timestamp: str

# --- Endpoint 1: Academic Performance Prediction ---
@router.get("/academic-risk/{student_id}", response_model=AcademicRiskResponse)
def predict_academic_risk(student_id: str):
    """
    Predicts if a student is at-risk for poor academic performance.
    
    - **student_id**: The ID of the student to predict (e.g., STU-001)
    """
    try:
        # Load data
        df_academic, df_engagement, df_student, _, _, _, _ = load_data()
        
        # Check if student exists
        if student_id not in df_student['student_id'].values:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        # Get student's latest data
        student_academic = df_academic[df_academic['student_id'] == student_id]
        student_engagement = df_engagement[df_engagement['student_id'] == student_id]
        
        if student_academic.empty:
            raise HTTPException(status_code=404, detail=f"No academic data found for student {student_id}")
        
        # Get latest term data
        latest_term = sorted(student_academic['term'].unique())[-1]
        latest_academic = student_academic[student_academic['term'] == latest_term]
        latest_engagement = student_engagement[student_engagement['term'] == latest_term]
        
        if latest_engagement.empty:
            # Use average engagement if no specific term data
            latest_engagement = student_engagement.mean(numeric_only=True).to_dict()
        else:
            latest_engagement = latest_engagement.iloc[0].to_dict()
        
        # Calculate risk factors
        avg_final_score = latest_academic['final_score'].mean()
        avg_mid_score = latest_academic['mid_term_score'].mean()
        attendance = latest_engagement.get('attendance_percentage', 85)
        lms_logins = latest_engagement.get('lms_logins_per_week', 5)
        disciplinary = latest_engagement.get('disciplinary_incidents', 0)
        
        # Simple risk calculation (in a real app, you'd use a trained model)
        risk_score = 0
        key_factors = []
        
        if avg_final_score < 70:
            risk_score += 0.3
            key_factors.append("Low final scores")
        
        if avg_mid_score < 65:
            risk_score += 0.2
            key_factors.append("Low mid-term scores")
        
        if attendance < 90:
            risk_score += 0.2
            key_factors.append("Poor attendance")
        
        if lms_logins < 3:
            risk_score += 0.15
            key_factors.append("Low online engagement")
        
        if disciplinary > 1:
            risk_score += 0.15
            key_factors.append("Behavioral issues")
        
        # Determine prediction
        if risk_score > 0.5:
            prediction = "At-Risk"
        elif risk_score > 0.3:
            prediction = "Moderate Risk"
        else:
            prediction = "Low Risk"
        
        confidence_score = min(0.95, 0.7 + (risk_score * 0.25))
        
        return AcademicRiskResponse(
            student_id=student_id,
            prediction=prediction,
            risk_probability=risk_score,
            confidence_score=confidence_score,
            key_factors=key_factors if key_factors else ["No significant risk factors identified"],
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting academic risk: {str(e)}")

# --- Endpoint 7: Dropout Risk Detection ---
@router.get("/dropout-risk/{student_id}", response_model=DropoutRiskResponse)
def predict_dropout_risk(student_id: str):
    """
    Predicts the probability of a student dropping out or transferring.
    
    - **student_id**: The ID of the student to predict (e.g., STU-001)
    """
    try:
        # Load data
        df_academic, df_engagement, df_student, _, _, _, _ = load_data()
        
        # Check if student exists
        if student_id not in df_student['student_id'].values:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        
        # Get student's data
        student_academic = df_academic[df_academic['student_id'] == student_id]
        student_engagement = df_engagement[df_engagement['student_id'] == student_id]
        
        if student_academic.empty and student_engagement.empty:
            raise HTTPException(status_code=404, detail=f"No data found for student {student_id}")
        
        # Calculate dropout risk factors
        latest_term = None
        if not student_academic.empty:
            latest_term = sorted(student_academic['term'].unique())[-1]
            latest_academic = student_academic[student_academic['term'] == latest_term]
        else:
            latest_academic = pd.DataFrame()
        latest_engagement = student_engagement
        if latest_term is not None and 'term' in latest_engagement.columns:
            le = latest_engagement[latest_engagement['term'] == latest_term]
            latest_engagement = le if not le.empty else latest_engagement
        
        if latest_engagement.empty:
            latest_engagement = student_engagement.mean(numeric_only=True).to_dict()
        else:
            latest_engagement = latest_engagement.iloc[0].to_dict()
        
        # Risk calculation
        final_score = latest_academic['final_score'].mean() if not latest_academic.empty else np.nan
        attendance = latest_engagement.get('attendance_percentage', 85)
        lms_logins = latest_engagement.get('lms_logins_per_week', 5)
        disciplinary = latest_engagement.get('disciplinary_incidents', 0)
        
        # Dropout risk algorithm
        dropout_risk = 0
        key_factors = []
        recommendations = []
        
        # Academic factors
        if not np.isnan(final_score) and final_score < 60:
            dropout_risk += 0.4
            key_factors.append("Very low academic performance")
            recommendations.append("Immediate academic intervention needed")
        elif not np.isnan(final_score) and final_score < 70:
            dropout_risk += 0.2
            key_factors.append("Below average academic performance")
            recommendations.append("Academic support and tutoring recommended")
        
        # Attendance factors
        if attendance < 80:
            dropout_risk += 0.3
            key_factors.append("Poor attendance record")
            recommendations.append("Address attendance issues with student and parents")
        elif attendance < 90:
            dropout_risk += 0.15
            key_factors.append("Below average attendance")
            recommendations.append("Monitor attendance patterns")
        
        # Engagement factors
        if lms_logins < 2:
            dropout_risk += 0.2
            key_factors.append("Very low online engagement")
            recommendations.append("Encourage LMS usage and online participation")
        elif lms_logins < 4:
            dropout_risk += 0.1
            key_factors.append("Low online engagement")
            recommendations.append("Improve online learning engagement")
        
        # Behavioral factors
        if disciplinary > 2:
            dropout_risk += 0.25
            key_factors.append("Multiple behavioral incidents")
            recommendations.append("Behavioral intervention and counseling recommended")
        elif disciplinary > 0:
            dropout_risk += 0.1
            key_factors.append("Some behavioral issues")
            recommendations.append("Monitor behavioral patterns")
        
        # Determine risk level
        if dropout_risk > 0.7:
            risk_level = "High Risk"
        elif dropout_risk > 0.4:
            risk_level = "Moderate Risk"
        else:
            risk_level = "Low Risk"
        
        return DropoutRiskResponse(
            student_id=student_id,
            dropout_risk_probability=min(0.95, dropout_risk),
            risk_level=risk_level,
            key_factors=key_factors if key_factors else ["No significant dropout risk factors identified"],
            recommendations=recommendations if recommendations else ["Continue monitoring student progress"],
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting dropout risk: {str(e)}")

# --- Batch Prediction Endpoint ---
from pydantic import BaseModel

class BatchStudentsRequest(BaseModel):
    student_ids: List[str]

@router.post("/batch-academic-risk")
def predict_batch_academic_risk(payload: BatchStudentsRequest):
    """
    Predicts academic risk for multiple students at once.
    
    - **student_ids**: List of student IDs to predict
    """
    try:
        results = []
        for student_id in payload.student_ids:
            try:
                result = predict_academic_risk(student_id)
                results.append(result.dict())
            except HTTPException as e:
                results.append({
                    "student_id": student_id,
                    "error": e.detail,
                    "status": "failed"
                })
        
        return {
            "predictions": results,
            "total_students": len(payload.student_ids),
            "successful_predictions": len([r for r in results if "error" not in r]),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch prediction: {str(e)}")
