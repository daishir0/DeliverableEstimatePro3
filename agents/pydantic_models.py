"""
Pydantic Model Definitions - For Structured Output
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DeliverableEstimate(BaseModel):
    """Deliverable Estimate"""
    name: str = Field(description="Deliverable name")
    description: str = Field(description="Deliverable description")
    base_effort_days: float = Field(description="Base effort (person-days)")
    complexity_multiplier: float = Field(description="Complexity multiplier")
    risk_multiplier: float = Field(description="Risk multiplier")
    final_effort_days: float = Field(description="Final effort (person-days)")
    cost: float = Field(description="Cost in configured currency")
    confidence_score: float = Field(description="Confidence score (0-1)")
    rationale: str = Field(description="Estimation rationale")


class FinancialSummary(BaseModel):
    """Financial Summary"""
    total_effort_days: float = Field(description="Total effort (person-days)")
    subtotal: float = Field(description="Subtotal in configured currency")
    tax: float = Field(description="Tax in configured currency")
    total: float = Field(description="Total amount in configured currency")


class TechnicalAssumptions(BaseModel):
    """Technical Assumptions"""
    engineer_level: str = Field(description="Engineer level")
    daily_rate: float = Field(description="Daily rate in configured currency")
    currency: str = Field(description="Currency code (USD, JPY, EUR, etc.)")
    development_stack: str = Field(description="Assumed technology stack")
    team_size: int = Field(description="Assumed team size")
    project_duration_months: int = Field(description="Assumed duration (months)")


class EstimationResult(BaseModel):
    """Estimation Result"""
    deliverable_estimates: List[DeliverableEstimate] = Field(description="List of deliverable estimates")
    financial_summary: FinancialSummary = Field(description="Financial summary")
    technical_assumptions: TechnicalAssumptions = Field(description="Technical assumptions")
    overall_confidence: float = Field(description="Overall confidence (0-1)")
    key_risks: List[str] = Field(description="Key risk factors")
    recommendations: List[str] = Field(description="Recommendations")


class BusinessEvaluationDetail(BaseModel):
    """Business Evaluation Detail"""
    clarity_score: int = Field(description="Clarity score (0-100)")
    assessment: str = Field(description="Assessment comment")
    missing_elements: List[str] = Field(description="Missing elements")


class ImprovementQuestion(BaseModel):
    """Improvement Question"""
    category: str = Field(description="Question category")
    question: str = Field(description="Specific question")
    purpose: str = Field(description="Purpose of question")
    impact_on_estimation: str = Field(description="Impact on estimation")


class BusinessEvaluationResult(BaseModel):
    """Business & Functional Requirements Evaluation Result"""
    overall_score: int = Field(description="Overall evaluation score (0-100)")
    business_purpose: BusinessEvaluationDetail = Field(description="Business purpose evaluation")
    functional_requirements: BusinessEvaluationDetail = Field(description="Functional requirements evaluation")
    user_stories: BusinessEvaluationDetail = Field(description="User stories evaluation")
    business_value: BusinessEvaluationDetail = Field(description="Business value evaluation")
    stakeholders: BusinessEvaluationDetail = Field(description="Stakeholders evaluation")
    business_flow: BusinessEvaluationDetail = Field(description="Business flow evaluation")
    improvement_questions: List[ImprovementQuestion] = Field(description="List of improvement questions")
    risk_factors: List[str] = Field(description="Business risk factors")
    recommendations: List[str] = Field(description="Improvement recommendations")


class QualityEvaluationDetail(BaseModel):
    """Quality Evaluation Detail"""
    definition_score: int = Field(description="Definition score (0-100)")
    assessment: str = Field(description="Assessment comment")
    missing_elements: List[str] = Field(description="Missing elements")
    effort_impact_percentage: float = Field(description="Effort impact percentage (%)")


class QualityEvaluationResult(BaseModel):
    """Quality & Non-functional Requirements Evaluation Result"""
    overall_score: int = Field(description="Overall evaluation score (0-100)")
    performance_requirements: QualityEvaluationDetail = Field(description="Performance requirements evaluation")
    security_requirements: QualityEvaluationDetail = Field(description="Security requirements evaluation")
    availability_reliability: QualityEvaluationDetail = Field(description="Availability & reliability evaluation")
    scalability_maintainability: QualityEvaluationDetail = Field(description="Scalability & maintainability evaluation")
    usability: QualityEvaluationDetail = Field(description="Usability evaluation")
    operational_monitoring: QualityEvaluationDetail = Field(description="Operational monitoring evaluation")
    improvement_questions: List[ImprovementQuestion] = Field(description="List of improvement questions")
    total_effort_impact: float = Field(description="Total effort impact percentage (%)")
    risk_factors: List[str] = Field(description="Quality risk factors")
    recommendations: List[str] = Field(description="Quality improvement recommendations")


class ConstraintsEvaluationDetail(BaseModel):
    """Constraints Evaluation Detail"""
    clarity_score: int = Field(description="Clarity score (0-100)")
    assessment: str = Field(description="Assessment comment")
    identified_constraints: List[str] = Field(description="Identified constraints")
    missing_elements: List[str] = Field(description="Missing elements")
    effort_impact_percentage: float = Field(description="Effort impact percentage (%)")


class ConstraintsEvaluationResult(BaseModel):
    """Constraints & External Integration Requirements Evaluation Result"""
    overall_score: int = Field(description="Overall evaluation score (0-100)")
    technical_constraints: ConstraintsEvaluationDetail = Field(description="Technical constraints evaluation")
    external_integrations: ConstraintsEvaluationDetail = Field(description="External integrations evaluation")
    compliance_regulations: ConstraintsEvaluationDetail = Field(description="Compliance & regulations evaluation")
    infrastructure_constraints: ConstraintsEvaluationDetail = Field(description="Infrastructure constraints evaluation")
    resource_constraints: ConstraintsEvaluationDetail = Field(description="Resource constraints evaluation")
    operational_constraints: ConstraintsEvaluationDetail = Field(description="Operational constraints evaluation")
    improvement_questions: List[ImprovementQuestion] = Field(description="List of improvement questions")
    total_effort_impact: float = Field(description="Total effort impact percentage (%)")
    feasibility_risks: List[str] = Field(description="Feasibility risks")
    mitigation_strategies: List[str] = Field(description="Risk mitigation strategies")
    recommendations: List[str] = Field(description="Constraint handling recommendations")