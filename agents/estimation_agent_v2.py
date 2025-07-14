"""
Estimation Agent - PydanticOutputParser Compatible Version
"""

from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import EstimationResult


class EstimationAgentV2(PydanticAIAgent):
    """Estimation Agent - Pydantic Structured Output Compatible"""
    
    def __init__(self):
        system_prompt = """
You are an experienced system development estimation specialist.
Your primary role is to generate accurate estimates from deliverable lists and requirement information.

[RESPONSIBILITIES]
1. Calculate effort estimates for deliverables
2. Calculate costs (daily rate × effort)
3. Clarify technical prerequisites
4. Evaluate estimation reliability

[EFFORT ESTIMATION STANDARDS]
- Requirements Definition: 2-8 person-days (adjusted by complexity)
- System Design: 4-12 person-days (adjusted by architecture complexity)
- Frontend Development: 8-25 person-days (adjusted by number of screens and features)
- Backend Development: 10-30 person-days (adjusted by number of APIs and business logic complexity)
- Database Design & Implementation: 5-18 person-days (adjusted by number of tables and relationships)
- Test Implementation: 5-15 person-days (adjusted by test scope)
- Security Implementation: 3-15 person-days (adjusted by security level)
- Deployment & Operations Setup: 2-10 person-days (adjusted by infrastructure complexity)

[COMPLEXITY ADJUSTMENT FACTORS]
- Low: 1.0x
- Medium: 1.3x
- High: 1.8x

[RISK ADJUSTMENT FACTORS]
- New technology/unfamiliar domain: +30%
- External system dependencies: +20%
- Performance requirements: +25%
- Advanced security: +30%
- Multiple payment integrations: +25%
- Large-scale data: +20%

[DEFAULT TECHNICAL PREREQUISITES]
- Engineer level: Average engineer capable of using Python
- Development environment: Standard development environment
- Daily rate: 50,000 JPY (configurable)

Please perform the following calculations for each deliverable:
1. Calculate base effort
2. Adjust for complexity
3. Adjust for risks
4. Calculate final effort and cost
5. Evaluate reliability

Please return results in the specified Pydantic model format.
"""
        super().__init__("EstimationAgentV2", system_prompt)
    
    def generate_estimate(self, deliverables: List[Dict[str, Any]], 
                         project_requirements: str, 
                         evaluation_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main method for estimate generation"""
        
        # Convert deliverables list to string
        deliverables_str = "\n".join([
            f"- {d.get('name', '')}: {d.get('description', '')}" 
            for d in deliverables
        ])
        
        user_input = f"""
[DELIVERABLES LIST]
{deliverables_str}

[PROJECT REQUIREMENTS]
{project_requirements}

[EVALUATION FEEDBACK]
Business & Functional Requirements Evaluation: {evaluation_feedback.get('business_evaluation', 'Not evaluated') if evaluation_feedback else 'Not evaluated'}
Quality & Non-functional Requirements Evaluation: {evaluation_feedback.get('quality_evaluation', 'Not evaluated') if evaluation_feedback else 'Not evaluated'}
Constraints & External Integration Evaluation: {evaluation_feedback.get('constraints_evaluation', 'Not evaluated') if evaluation_feedback else 'Not evaluated'}

Based on the above information, please execute effort estimation and cost calculation for each deliverable.
Please adjust effort considering the content of evaluation feedback.
"""
        
        # Use Pydantic structured output
        result = self.execute_with_pydantic(user_input, EstimationResult, evaluation_feedback)
        
        # Wrap results on success
        if result.get("success"):
            # Exclude _agent_metadata and wrap with estimation_result key
            estimation_result = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
            
            return {
                "success": True,
                "estimation_result": estimation_result,
                "_agent_metadata": result.get("_agent_metadata", {})
            }
        
        return result
    
    def refine_estimate(self, current_estimate: Dict[str, Any], 
                       feedback: str, 
                       evaluation_updates: Dict[str, Any] = None,
                       previous_estimate: Dict[str, Any] = None) -> Dict[str, Any]:
        """Improve estimates based on feedback (enhanced for modification requests)"""
        
        # Comparison context with previous estimate
        comparison_context = ""
        if previous_estimate:
            prev_total = previous_estimate.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
            curr_total = current_estimate.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
            comparison_context = f"""
[COMPARISON WITH PREVIOUS ESTIMATE]
Previous total effort: {prev_total} person-days
Current total effort: {curr_total} person-days
Difference: {curr_total - prev_total:+.1f} person-days
"""
        
        user_input = f"""
[CURRENT ESTIMATE]
{current_estimate}
{comparison_context}

[USER MODIFICATION REQUEST]
{feedback}

[UPDATED EVALUATION RESULTS]
{evaluation_updates if evaluation_updates else 'No updates'}

⚠️[IMPORTANT] Please be sure to recalculate the estimate reflecting the user's modification request.

Specific changes due to modification request:
1. Add/change technical requirements pointed out in feedback
2. Concretize performance requirements and library constraints
3. Accurately calculate the impact on effort and cost
4. Update technical prerequisites (libraries, performance requirements, etc.)
5. Identify new risk factors

[Example: When 5-second response time requirement is added]
- Add performance optimization effort
- Add cache/CDN implementation effort
- Add database optimization effort
- Add library selection (Redis, Nginx, etc.) to technical prerequisites

The estimate results must be changed from the previous version. Same results are not acceptable.
"""
        
        # Include modification request analysis information in additional context
        additional_context = {
            "user_feedback": feedback,
            "previous_estimate": previous_estimate,
            "evaluation_updates": evaluation_updates,
            "requires_recalculation": True
        }
        
        # Use Pydantic structured output
        result = self.execute_with_pydantic(user_input, EstimationResult, additional_context)
        
        # Wrap results on success
        if result.get("success"):
            estimation_result = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
            
            return {
                "success": True,
                "estimation_result": estimation_result,
                "_agent_metadata": result.get("_agent_metadata", {})
            }
        
        return result