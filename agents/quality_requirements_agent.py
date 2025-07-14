"""
Quality & Non-functional Requirements Agent - How Well Evaluation
"""

from typing import Dict, Any, List
from .base_ai_agent import BaseAIAgent


class QualityRequirementsAgent(BaseAIAgent):
    """Quality & Non-functional Requirements Agent - How Well Perspective Evaluation"""
    
    def __init__(self):
        system_prompt = """
You are an experienced quality and non-functional requirements analysis specialist.
Your primary role is to evaluate quality and non-functional requirements for system development projects from the "How well (what level of quality to build)" perspective.

[RESPONSIBILITIES]
1. Evaluate validity of performance requirements
2. Evaluate completeness of security requirements
3. Evaluate availability and scalability
4. Evaluate operability and maintainability

[EVALUATION PERSPECTIVES]
- Performance requirements (response time, throughput, concurrent connections)
- Security level (authentication, authorization, encryption, vulnerability countermeasures)
- Availability and reliability (uptime, failure recovery time, data backup)
- Scalability and maintainability (future expansion, maintenance ease)
- Usability (operability, accessibility, multi-language support)
- Operational monitoring (logs, monitoring, alerts)

[EVALUATION CRITERIA]
- High rating (Score: 80-100): Specific and measurable quality standards are set
- Medium rating (Score: 50-79): Basic quality requirements are included but need detailed elaboration
- Low rating (Score: 0-49): Quality requirements are unclear and need concretization

[QUALITY REQUIREMENTS EFFORT IMPACT]
- Performance optimization: +20-40% effort increase
- Advanced security implementation: +30-50% effort increase
- High availability design: +25-45% effort increase
- Internationalization support: +15-30% effort increase
- Accessibility support: +10-25% effort increase

[QUESTION GENERATION PERSPECTIVES]
- Expected concurrent access numbers and peak load
- Response time and processing performance requirements
- Security level and compliance requirements
- Availability and uptime target values
- Future expansion plans and growth prospects
- Operational structure and monitoring requirements

Please respond in the following JSON format:
{
  "success": true,
  "quality_evaluation": {
    "overall_score": overall_evaluation_score(0-100),
    "performance_requirements": {
      "definition_score": definition_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "security_requirements": {
      "completeness_score": completeness_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "availability_reliability": {
      "specification_score": specification_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "scalability_maintainability": {
      "consideration_score": consideration_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "usability": {
      "requirement_score": requirement_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "operational_monitoring": {
      "planning_score": planning_score(0-100),
      "assessment": "evaluation_comment",
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "improvement_questions": [
      {
        "category": "question_category",
        "question": "specific_question",
        "purpose": "question_purpose",
        "impact_on_estimation": "impact_on_estimation"
      }
    ],
    "total_effort_impact": total_effort_impact,
    "risk_factors": ["quality_risk_factors"],
    "recommendations": ["quality_improvement_recommendations"]
  }
}
"""
        super().__init__("QualityRequirementsAgent", system_prompt)
    
    def evaluate_quality_requirements(self, project_requirements: str, 
                                    deliverables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate quality and non-functional requirements"""
        
        deliverables_context = ""
        if deliverables:
            deliverables_context = "\n[DELIVERABLES LIST]\n" + "\n".join([
                f"- {d.get('name', '')}: {d.get('description', '')}" 
                for d in deliverables
            ])
        
        user_input = f"""
[PROJECT REQUIREMENTS]
{project_requirements}
{deliverables_context}

Please evaluate the above project requirements from the perspective of "How well (what level of quality to build)" in terms of quality and non-functional requirements.

Items to evaluate:
1. Are performance requirements specifically defined?
2. Are security requirements adequately set?
3. Are availability and reliability targets clear?
4. Are scalability and maintainability considered?
5. Are usability requirements appropriately set?
6. Are operational monitoring plans included?

Also, please evaluate the impact of each quality requirement on estimation effort and generate quality-related questions necessary for improving estimation accuracy.
"""
        
        result = self.execute_with_ai(user_input)
        
        # Response validation
        required_keys = ["quality_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("Invalid format for quality requirements evaluation results")
        
        return result
    
    def analyze_performance_impact(self, performance_requirements: str, 
                                 current_architecture: str = None) -> Dict[str, Any]:
        """Analyze effort impact of performance requirements"""
        
        architecture_context = ""
        if current_architecture:
            architecture_context = f"\n[ASSUMED ARCHITECTURE]\n{current_architecture}"
        
        user_input = f"""
[PERFORMANCE REQUIREMENTS]
{performance_requirements}
{architecture_context}

Please analyze the above performance requirements and evaluate in detail the impact on implementation effort.
Please analyze particularly from the following perspectives:

1. Necessity of database optimization
2. Need for cache strategy implementation
3. Load balancing and scaling design
4. Scope of performance testing
5. Construction of monitoring and measurement systems
"""
        
        result = self.execute_with_ai(user_input)
        
        # Response validation
        required_keys = ["quality_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("Invalid format for performance impact analysis results")
        
        return result