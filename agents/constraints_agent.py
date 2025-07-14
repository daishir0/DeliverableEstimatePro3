"""
Constraints & External Integration Requirements Agent - Boundaries Evaluation
"""

from typing import Dict, Any, List
from .base_ai_agent import BaseAIAgent


class ConstraintsAgent(BaseAIAgent):
    """Constraints & External Integration Requirements Agent - Boundaries Perspective Evaluation"""
    
    def __init__(self):
        system_prompt = """
You are an experienced system constraints and integration analysis specialist.
Your primary role is to evaluate constraints and external integration requirements for system development projects from the "Boundaries (boundary and constraint conditions)" perspective.

[RESPONSIBILITIES]
1. Identify and evaluate technical constraints
2. Analyze external system integration requirements
3. Verify legal regulations and compliance requirements
4. Evaluate resource and schedule constraints

[EVALUATION PERSPECTIVES]
- Technical constraints (technology usage, platform, library restrictions)
- External system integration (API, database, authentication systems, payment systems)
- Legal regulations and compliance (personal information protection, industry regulations, standards)
- Infrastructure constraints (cloud, on-premises, network, security)
- Resource constraints (budget, personnel, schedule, environment)
- Operational constraints (support structure, maintenance windows, SLA)

[EVALUATION CRITERIA]
- High rating (Score: 80-100): Constraints are clear and feasibility is verified
- Medium rating (Score: 50-79): Major constraints are identified but detailed confirmation is needed
- Low rating (Score: 0-49): Constraints are unclear with high implementation risks

[CONSTRAINT EFFORT IMPACT]
- External API integration: +15-30% effort increase
- Legacy system integration: +25-50% effort increase
- Advanced security requirements: +20-40% effort increase
- Special compliance handling: +30-60% effort increase
- Complex infrastructure requirements: +20-35% effort increase
- Strict schedule constraints: +10-25% effort increase

[QUESTION GENERATION PERSPECTIVES]
- Detailed specifications of external systems to integrate
- Clarification of mandatory/prohibited technologies
- Concretization of legal regulations and compliance requirements
- Details of infrastructure and environment constraints
- Budget, schedule, and personnel constraints
- Operational and support structure requirements

Please respond in the following JSON format:
{
  "success": true,
  "constraints_evaluation": {
    "overall_score": overall_evaluation_score(0-100),
    "technical_constraints": {
      "clarity_score": clarity_score(0-100),
      "assessment": "evaluation_comment",
      "identified_constraints": ["identified_constraints"],
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "external_integrations": {
      "specification_score": specification_score(0-100),
      "assessment": "evaluation_comment",
      "identified_integrations": ["identified_integrations"],
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "compliance_regulations": {
      "coverage_score": coverage_score(0-100),
      "assessment": "evaluation_comment",
      "identified_requirements": ["identified_requirements"],
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "infrastructure_constraints": {
      "definition_score": definition_score(0-100),
      "assessment": "evaluation_comment",
      "identified_constraints": ["identified_constraints"],
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "resource_constraints": {
      "realism_score": realism_score(0-100),
      "assessment": "evaluation_comment",
      "identified_constraints": ["identified_constraints"],
      "missing_elements": ["missing_elements"],
      "effort_impact_percentage": effort_impact
    },
    "operational_constraints": {
      "planning_score": planning_score(0-100),
      "assessment": "evaluation_comment",
      "identified_constraints": ["identified_constraints"],
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
    "feasibility_risks": ["feasibility_risks"],
    "mitigation_strategies": ["risk_mitigation_strategies"],
    "recommendations": ["constraint_handling_recommendations"]
  }
}
"""
        super().__init__("ConstraintsAgent", system_prompt)
    
    def evaluate_constraints(self, project_requirements: str, 
                           deliverables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Evaluate constraints and external integration requirements"""
        
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

Please evaluate the above project requirements from the perspective of "Boundaries (boundary and constraint conditions)" in terms of constraints and external integration requirements.

Items to evaluate:
1. Are technical constraints clearly identified?
2. Are external system integration specifications specific?
3. Are legal regulations and compliance requirements comprehensively covered?
4. Are infrastructure constraints appropriately defined?
5. Are resource constraints (budget, personnel, schedule) realistic?
6. Are operational constraints included in the plan?

Also, please evaluate the impact of each constraint on estimation effort and generate constraint-related questions necessary for improving estimation accuracy.
"""
        
        result = self.execute_with_ai(user_input)
        
        # Response validation
        required_keys = ["constraints_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("Invalid format for constraint evaluation results")
        
        return result
    
    def analyze_integration_complexity(self, integration_requirements: str, 
                                     target_systems: List[str] = None) -> Dict[str, Any]:
        """Analyze complexity of external integrations"""
        
        systems_context = ""
        if target_systems:
            systems_context = f"\n[TARGET SYSTEMS]\n" + "\n".join([f"- {sys}" for sys in target_systems])
        
        user_input = f"""
[INTEGRATION REQUIREMENTS]
{integration_requirements}
{systems_context}

Please analyze the above external integration requirements and evaluate in detail the impact on implementation effort.
Please analyze particularly from the following perspectives:

1. API integration complexity and data format conversion
2. Implementation effort for authentication and authorization methods
3. Data synchronization and consistency requirements
4. Error handling and retry mechanisms
5. Scope of integration testing and system integration testing
6. Operational monitoring and failure response mechanisms
"""
        
        result = self.execute_with_ai(user_input)
        
        # Response validation
        required_keys = ["constraints_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("Invalid format for integration complexity analysis results")
        
        return result