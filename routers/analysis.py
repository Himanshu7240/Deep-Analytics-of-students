from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
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
class TeacherEffectivenessResponse(BaseModel):
    report_date: str
    effectiveness_ranking: List[Dict[str, Any]]
    total_teachers: int
    average_score_growth: float

class TalentDiscoveryResponse(BaseModel):
    report_date: str
    talents: List[Dict[str, Any]]
    total_talents_identified: int

class BehavioralConcernResponse(BaseModel):
    report_date: str
    concern_list: List[Dict[str, Any]]
    total_concerns: int
    confidentiality_level: str

class ExternalFactorsResponse(BaseModel):
    report_date: str
    summary: str
    correlations: List[Dict[str, Any]]
    recommendations: List[str]

class PeerNetworkResponse(BaseModel):
    report_date: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    network_metrics: Dict[str, Any]

# --- Endpoint 2: Teacher Effectiveness Analysis ---
@router.get("/teacher-effectiveness", response_model=TeacherEffectivenessResponse)
def get_teacher_effectiveness():
    """
    Returns a ranked list of teachers based on student score growth.
    No query parameters are required or accepted.
    """
    try:
        df_academic, _, _, _, _, df_relational, df_staff = load_data()
        
        # Merge academic data with teacher information
        df_merged = pd.merge(df_academic, df_relational, on=['student_id', 'term'])

        # Defaults: no filtering, include all data; require at least 1 student
        min_students = 1
        df_merged = pd.merge(df_merged, df_staff, on='teacher_id')
        
        # Calculate score growth for each student-teacher combination
        teacher_effectiveness = []
        
        for teacher_id in df_staff['teacher_id'].unique():
            teacher_data = df_merged[df_merged['teacher_id'] == teacher_id]
            
            if len(teacher_data) > 0:
                # Calculate average score growth
                score_growth = []
                for student_id in teacher_data['student_id'].unique():
                    student_data = teacher_data[teacher_data['student_id'] == student_id]
                    if len(student_data) >= 2:
                        # Calculate growth between terms
                        terms = sorted(student_data['term'].unique())
                        for i in range(1, len(terms)):
                            current_term = student_data[student_data['term'] == terms[i]]['final_score'].mean()
                            previous_term = student_data[student_data['term'] == terms[i-1]]['final_score'].mean()
                            growth = current_term - previous_term
                            score_growth.append(growth)
                
                if score_growth and len(teacher_data['student_id'].unique()) >= min_students:
                    mean_growth = np.mean(score_growth)
                    row = df_staff[df_staff['teacher_id'] == teacher_id].iloc[0]
                    teacher_name = f"{row['first_name']} {row['last_name']}"
                    student_count = len(teacher_data['student_id'].unique())
                    
                    teacher_effectiveness.append({
                        "teacher_id": teacher_id,
                        "teacher_name": teacher_name,
                        "mean_score_growth": round(mean_growth, 2),
                        "student_count": student_count,
                        "growth_consistency": round(np.std(score_growth), 2) if len(score_growth) > 1 else 0
                    })
        
        # Sort by effectiveness (score growth)
        teacher_effectiveness.sort(key=lambda x: x['mean_score_growth'], reverse=True)
        
        # Calculate overall metrics
        total_teachers = len(teacher_effectiveness)
        average_growth = np.mean([t['mean_score_growth'] for t in teacher_effectiveness]) if teacher_effectiveness else 0
        
        return TeacherEffectivenessResponse(
            report_date=datetime.now().isoformat(),
            effectiveness_ranking=teacher_effectiveness,
            total_teachers=total_teachers,
            average_score_growth=round(average_growth, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing teacher effectiveness: {str(e)}")


# --- Endpoint 4: Skill & Talent Discovery ---
@router.get("/talent-discovery", response_model=TalentDiscoveryResponse)
def get_talent_discovery(
    min_confidence: float = 0.6,
    talent: Optional[str] = None
):
    """
    Identifies students with non-curricular talents based on activities and performance.
    Minimal parameters: optionally set a confidence threshold or filter by a single talent.
    """
    try:
        # Validate confidence bounds
        if min_confidence < 0 or min_confidence > 1:
            raise HTTPException(status_code=422, detail="min_confidence must be between 0 and 1")

        # Correctly unpack from load_data():
        # returns (df_academic, df_engagement, df_student, df_surveys, df_interventions, df_relational, df_staff)
        _, df_engagement, df_student, df_surveys, _, _, _ = load_data()
        
        # Merge data
        df_merged = pd.merge(df_engagement, df_student, on='student_id')
        
        # Define talent categories and their indicators
        talent_categories = {
            "Leadership": {
                "activities": ["Student Government", "Debate Club", "Model UN"],
                "indicators": ["leadership", "president", "captain", "coordinator"]
            },
            "Creative Arts": {
                "activities": ["Art Club", "Drama Club", "Music Club", "Creative Writing"],
                "indicators": ["art", "creative", "drama", "music", "writing"]
            },
            "Sports & Athletics": {
                "activities": ["Basketball", "Football", "Swimming", "Track"],
                "indicators": ["sports", "athletic", "fitness", "team"]
            },
            "STEM & Technology": {
                "activities": ["Coding Club", "Robotics", "Science Olympiad", "Math Club"],
                "indicators": ["coding", "robotics", "science", "technology", "math"]
            },
            "Community Service": {
                "activities": ["Volunteering", "Community Service", "Social Work"],
                "indicators": ["volunteer", "community", "service", "social"]
            }
        }
        
        talents = []
        
        for student_id in df_merged['student_id'].unique():
            student_data = df_merged[df_merged['student_id'] == student_id]
            student_name = f"{student_data['first_name'].iloc[0]} {student_data['last_name'].iloc[0]}"
            
            # Get student's activities
            activities = student_data['extracurricular_activity'].unique()
            activities = [act for act in activities if act != 'None' and pd.notna(act)]
            
            # Check for talents
            for talent_category, criteria in talent_categories.items():
                # Check activities
                matching_activities = [act for act in activities if any(
                    indicator.lower() in act.lower() for indicator in criteria['indicators']
                )]
                
                if matching_activities:
                    # Check survey responses for additional evidence
                    student_surveys = df_surveys[df_surveys['student_id'] == student_id]
                    survey_evidence = []
                    
                    for _, survey in student_surveys.iterrows():
                        if any(indicator.lower() in survey['response'].lower() for indicator in criteria['indicators']):
                            survey_evidence.append(survey['response'])
                    
                    evidence = matching_activities + survey_evidence
                    
                    record = {
                        "student_id": student_id,
                        "student_name": student_name,
                        "potential_talent": talent_category,
                        "evidence": evidence,
                        "confidence_score": min(0.95, 0.6 + (len(evidence) * 0.1))
                    }

                    # Apply minimal filters: optional single talent and confidence threshold
                    if (talent is None or record["potential_talent"].lower() == talent.lower()) and record["confidence_score"] >= min_confidence:
                        talents.append(record)

        return TalentDiscoveryResponse(
            report_date=datetime.now().isoformat(),
            talents=talents,
            total_talents_identified=len(talents)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error discovering talents: {str(e)}")

# --- Endpoint 5: Behavioral & Emotional Analysis ---
@router.get("/behavioral-concerns", response_model=BehavioralConcernResponse)
def get_behavioral_concerns(
    min_concern_score: int = 3,
    grade_level: Optional[int] = None,
    limit: Optional[int] = None
):
    """
    Generates a confidential list of students showing signs of concern.
    """
    try:
        df_academic, df_engagement, df_student, df_surveys, _, _, _ = load_data()
        
        # Merge data
        df_merged = pd.merge(df_academic, df_engagement, on=['student_id', 'term'])
        df_merged = pd.merge(df_merged, df_student, on='student_id')

        if grade_level is not None:
            col_name = 'grade_level_in_fall_2024' if 'grade_level_in_fall_2024' in df_merged.columns else 'grade'
            if col_name in df_merged.columns:
                df_merged = df_merged[df_merged[col_name] == grade_level]
        
        concern_list = []
        
        for student_id in df_merged['student_id'].unique():
            student_data = df_merged[df_merged['student_id'] == student_id]
            student_name = f"{student_data['first_name'].iloc[0]} {student_data['last_name'].iloc[0]}"
            
            # Calculate concern indicators
            concern_score = 0
            reasons = []
            
            # Academic decline
            if len(student_data) >= 2:
                terms = sorted(student_data['term'].unique())
                latest_scores = student_data[student_data['term'] == terms[-1]]['final_score'].mean()
                previous_scores = student_data[student_data['term'] == terms[-2]]['final_score'].mean()
                
                if latest_scores < previous_scores - 10:  # Significant drop
                    concern_score += 3
                    reasons.append(f"Academic decline: {previous_scores:.1f} → {latest_scores:.1f}")
            
            # Attendance issues
            avg_attendance = student_data['attendance_percentage'].mean()
            if avg_attendance < 85:
                concern_score += 2
                reasons.append(f"Poor attendance: {avg_attendance:.1f}%")
            
            # Behavioral issues
            total_incidents = student_data['disciplinary_incidents'].sum()
            if total_incidents > 2:
                concern_score += 2
                reasons.append(f"Multiple behavioral incidents: {total_incidents}")
            
            # Low engagement
            avg_lms_logins = student_data['lms_logins_per_week'].mean()
            if avg_lms_logins < 3:
                concern_score += 1
                reasons.append(f"Low online engagement: {avg_lms_logins:.1f} logins/week")
            
            # Survey responses indicating distress
            student_surveys = df_surveys[df_surveys['student_id'] == student_id]
            distress_keywords = ['stress', 'anxiety', 'depression', 'lonely', 'overwhelmed', 'struggling']
            distress_responses = []
            
            for _, survey in student_surveys.iterrows():
                if any(keyword in survey['response'].lower() for keyword in distress_keywords):
                    distress_responses.append(survey['response'])
            
            if distress_responses:
                concern_score += 2
                reasons.append(f"Distress indicators in surveys: {len(distress_responses)} responses")
            
            # Add to concern list if score is significant
            if concern_score >= min_concern_score:
                concern_list.append({
                    "student_id": student_id,
                    "student_name": student_name,
                    "concern_score": concern_score,
                    "reasons": reasons,
                    "urgency_level": "High" if concern_score >= 6 else "Medium" if concern_score >= 4 else "Low"
                })
        
        # Sort by concern score
        concern_list.sort(key=lambda x: x['concern_score'], reverse=True)
        
        if limit is not None and limit > 0:
            concern_list = concern_list[:limit]

        return BehavioralConcernResponse(
            report_date=datetime.now().isoformat(),
            concern_list=concern_list,
            total_concerns=len(concern_list),
            confidentiality_level="High - For authorized personnel only"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing behavioral concerns: {str(e)}")

# --- Endpoint 6: Impact of External Factors ---
@router.get("/external-factors", response_model=ExternalFactorsResponse)
def get_external_factors_summary(
    factor: Optional[str] = None,
    min_count: int = 1
):
    """
    Provides a summary of how external factors correlate with performance.
    """
    try:
        df_academic, _, df_student, _, _, _, _ = load_data()
        
        # Merge academic data with student demographics
        df_merged = pd.merge(df_academic, df_student, on='student_id')
        
        correlations = []
        recommendations = []
        
        # Analyze parental education impact
        if (factor is None or factor.lower() in ['parental_education','parental education']) and 'parental_education' in df_merged.columns:
            education_impact = df_merged.groupby('parental_education')['final_score'].agg(['mean', 'count']).reset_index()
            education_impact = education_impact.sort_values('mean', ascending=False)
            education_impact = education_impact[education_impact['count'] >= min_count]
            
            correlations.append({
                "factor": "Parental Education",
                "correlation_type": "Positive",
                "details": education_impact.to_dict('records'),
                "insight": "Higher parental education correlates with better student performance"
            })
            
            if len(education_impact) > 1:
                max_education = education_impact.iloc[0]['parental_education']
                min_education = education_impact.iloc[-1]['parental_education']
                score_diff = education_impact.iloc[0]['mean'] - education_impact.iloc[-1]['mean']
                
                if score_diff > 10:
                    recommendations.append(f"Provide additional support for students from {min_education} backgrounds")
        
        # Analyze gender impact
        if (factor is None or factor.lower() == 'gender') and 'gender' in df_merged.columns:
            gender_impact = df_merged.groupby('gender')['final_score'].agg(['mean', 'count']).reset_index()
            gender_impact = gender_impact[gender_impact['count'] >= min_count]
            correlations.append({
                "factor": "Gender",
                "correlation_type": "Minimal",
                "details": gender_impact.to_dict('records'),
                "insight": "Gender shows minimal correlation with academic performance"
            })
        
        # Analyze age/grade impact
        if (factor is None or factor.lower() == 'age') and 'age' in df_merged.columns:
            age_impact = df_merged.groupby('age')['final_score'].agg(['mean', 'count']).reset_index()
            age_impact = age_impact.sort_values('age')
            age_impact = age_impact[age_impact['count'] >= min_count]
            correlations.append({
                "factor": "Age",
                "correlation_type": "Variable",
                "details": age_impact.to_dict('records'),
                "insight": "Age shows variable correlation with performance"
            })
        
        summary = "Analysis of external factors reveals key correlations with student performance. Parental education shows the strongest positive correlation, while other factors show varying degrees of impact."
        
        return ExternalFactorsResponse(
            report_date=datetime.now().isoformat(),
            summary=summary,
            correlations=correlations,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing external factors: {str(e)}")

# --- Endpoint 8: Peer Influence Tracking ---
@router.get("/peer-network", response_model=PeerNetworkResponse)
def get_peer_network(
    peer_group: Optional[str] = None,
    include_metrics: bool = True,
    limit_nodes: Optional[int] = None
):
    """
    Returns the student peer network data for analysis.
    """
    try:
        df_relational, df_student, df_academic, _, _, _, _ = load_data()
        
        # Create network nodes (students)
        nodes = []
        for _, student in df_student.iterrows():
            # Get student's academic performance
            student_academic = df_academic[df_academic['student_id'] == student['student_id']]
            avg_score = student_academic['final_score'].mean() if not student_academic.empty else 75
            
            # Determine performance category
            if avg_score >= 85:
                performance = "High-Performing"
            elif avg_score >= 70:
                performance = "Average"
            else:
                performance = "At-Risk"
            
            nodes.append({
                "id": student['student_id'],
                "name": f"{student['first_name']} {student['last_name']}",
                "performance": performance,
                "avg_score": round(avg_score, 1),
                "grade": student.get('grade', 'Unknown')
            })
        
        # Create network edges (peer relationships)
        edges = []
        for _, relation in df_relational.iterrows():
            if relation['peer_group'] != 'None' and pd.notna(relation['peer_group']):
                if peer_group is not None and str(relation['peer_group']).lower() != peer_group.lower():
                    continue
                # Find other students in the same peer group
                same_group = df_relational[
                    (df_relational['peer_group'] == relation['peer_group']) & 
                    (df_relational['student_id'] != relation['student_id'])
                ]
                
                for _, peer in same_group.iterrows():
                    edge = {
                        "source": relation['student_id'],
                        "target": peer['student_id'],
                        "group": relation['peer_group'],
                        "strength": "Strong" if relation['peer_group'] in ['Study Group', 'Project Team'] else "Moderate"
                    }
                    
                    # Avoid duplicate edges
                    if not any(e['source'] == edge['target'] and e['target'] == edge['source'] for e in edges):
                        edges.append(edge)
        
        if limit_nodes is not None and limit_nodes > 0:
            node_ids = set([n['id'] for n in nodes[:limit_nodes]])
            edges = [e for e in edges if e['source'] in node_ids and e['target'] in node_ids]

        # Calculate network metrics
        network_metrics = {}
        if include_metrics:
            total_students = len(nodes)
            total_connections = len(edges)
            high_performers = len([n for n in nodes if n['performance'] == 'High-Performing'])
            at_risk = len([n for n in nodes if n['performance'] == 'At-Risk'])

            network_metrics = {
                "total_students": total_students,
                "total_connections": total_connections,
                "high_performers": high_performers,
                "at_risk_students": at_risk,
                "network_density": round(total_connections / (total_students * (total_students - 1) / 2), 3) if total_students > 1 else 0,
                "performance_distribution": {
                    "high_performing": round(high_performers / total_students * 100, 1),
                    "average": round((total_students - high_performers - at_risk) / total_students * 100, 1),
                    "at_risk": round(at_risk / total_students * 100, 1)
                }
            }
        
        return PeerNetworkResponse(
            report_date=datetime.now().isoformat(),
            nodes=nodes,
            edges=edges,
            network_metrics=network_metrics
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing peer network: {str(e)}")
