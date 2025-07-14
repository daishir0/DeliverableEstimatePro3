"""
Business & Functional Requirements Agent - Enhanced for Modification Requests
"""

from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import BusinessEvaluationResult


class BusinessRequirementsAgentV2(PydanticAIAgent):
    """Business & Functional Requirements Agent - Enhanced for Modification Request Handling"""
    
    def __init__(self):
        system_prompt = """
You are an experienced business requirements analysis specialist.
Your primary role is to evaluate business and functional requirements for system development projects from the perspectives of "What (what to build)" and "Why (why to build it)".

[IMPORTANT] When there are modification requests, please conduct a new evaluation that reflects the user's modification requests while referring to previous evaluation results.

[RESPONSIBILITIES]
1. Evaluate clarity of business requirements
2. Evaluate completeness of functional requirements
3. Evaluate validity of business value
4. Generate business-focused questions to improve estimation accuracy
5. Evaluate impact of requirement changes due to modification requests

[EVALUATION PERSPECTIVES]
- Clarity of business objectives (goal and KPI setting)
- Specificity of functional requirements (level of detail in functional specifications)
- Completeness of user stories (comprehensiveness from user perspective)
- Quantification of business value (ROI and effect measurement)
- Stakeholder identification (stakeholders and approval flow)
- Clarity of business flow (organization of current and new business processes)

[HANDLING MODIFICATION REQUESTS]
- Always reflect user modification requests in the evaluation
- Clearly identify changes from previous evaluation
- Evaluate business impact of modifications
- Identify newly emerging risks and recommendations

[EVALUATION CRITERIA]
- High rating (Score: 80-100): Clear and specific, business value is quantified
- Medium rating (Score: 50-79): Basic content is included but requires detailed elaboration
- Low rating (Score: 0-49): Unclear and abstract, requires concretization

Please return results in the specified Pydantic model format.
When there are modification requests, be sure to update evaluation scores and content.
"""
        super().__init__("BusinessRequirementsAgentV2", system_prompt)
    
    def evaluate_business_requirements(self, project_requirements: str,
                                      deliverables: List[Dict[str, Any]] = None,
                                      previous_evaluation: Dict[str, Any] = None,
                                      user_feedback: str = "") -> Dict[str, Any]:
        """Evaluate business and functional requirements (with modification request support)"""
        
        # Error handling when deliverables is None or empty
        if deliverables is None:
            deliverables = []
            
        deliverables_context = ""
        if deliverables:
            deliverables_context = "\n[DELIVERABLES LIST]\n" + "\n".join([
                f"- {d.get('name', '')}: {d.get('description', '')}"
                for d in deliverables
            ])
        
        # Add context from previous evaluation
        previous_context = ""
        if previous_evaluation:
            # Convert to string if it's a dictionary
            if isinstance(previous_evaluation, dict):
                import json
                previous_context = f"\n[PREVIOUS EVALUATION RESULTS]\n{json.dumps(previous_evaluation, ensure_ascii=False, indent=2)}"
            else:
                previous_context = f"\n[PREVIOUS EVALUATION RESULTS]\n{previous_evaluation}"
        
        # Add context for modification requests
        feedback_context = ""
        if user_feedback:
            feedback_context = f"\n[USER MODIFICATION REQUEST]\n{user_feedback}\n⚠️ Please be sure to update the evaluation reflecting this modification request."
        
        user_input = f"""
[PROJECT REQUIREMENTS]
{project_requirements}
{deliverables_context}
{previous_context}
{feedback_context}

Please evaluate the above project requirements from the perspectives of "What (what to build)" and "Why (why to build it)" in terms of business and functional requirements.

Items to evaluate:
1. Are business objectives clearly defined?
2. Are functional requirements described in specific and implementable terms?
3. Are user stories comprehensively defined?
4. Is business value quantitatively measurable?
5. Are stakeholders clearly identified?
6. Are business flows organized for both current and new business processes?

[IMPORTANT] When there are modification requests:
- Evaluate the impact of modification requests on business and functional requirements
- Clarify changes from previous evaluation
- Identify new risks and recommendations
- Update evaluation scores appropriately

Also, please generate business-focused questions necessary for improving estimation accuracy.
"""
        
        # Use Pydantic structured output
        additional_context = {
            "previous_evaluation": previous_evaluation if previous_evaluation is not None else {},
            "user_feedback": user_feedback,
            "has_modification_request": bool(user_feedback)
        }
        
        try:
            result = self.execute_with_pydantic(user_input, BusinessEvaluationResult, additional_context)
            
            # Error handling when result is None
            if result is None:
                return self._create_error_response("Pydantic execution result is None")
            
            # Wrap successful results
            if result.get("success"):
                # Wrap with business_evaluation key
                business_evaluation = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
                
                return {
                    "success": True,
                    "business_evaluation": business_evaluation,
                    "_agent_metadata": result.get("_agent_metadata", {})
                }
            
            return result
        except Exception as e:
            import traceback
            error_msg = f"An error occurred during business requirements evaluation: {str(e)}\n{traceback.format_exc()}"
            print(f"[{self.agent_name}] Error: {error_msg}")
            return self._create_error_response(error_msg)
    
    def generate_clarification_questions(self, current_requirements: str,
                                        focus_areas: List[str] = None,
                                        user_feedback: str = "") -> Dict[str, Any]:
        """Generate clarification questions for business requirements (with modification request support)"""
        
        # Error handling when focus_areas is None
        if focus_areas is None:
            focus_areas = []
            
        focus_context = ""
        if focus_areas:
            focus_context = f"\n[FOCUS AREAS]\n" + "\n".join([f"- {area}" for area in focus_areas])
        
        feedback_context = ""
        if user_feedback:
            feedback_context = f"\n[USER MODIFICATION REQUEST]\n{user_feedback}\n⚠️ Please focus on generating questions related to this modification request."
        
        user_input = f"""
[CURRENT REQUIREMENTS]
{current_requirements}
{focus_context}
{feedback_context}

Please generate questions to clarify business and functional aspects for the above requirements.
Focus particularly on creating questions about elements that directly impact estimation accuracy.

If there are modification requests, please include additional questions related to those requests.
"""
        
        additional_context = {
            "user_feedback": user_feedback,
            "focus_areas": focus_areas if focus_areas is not None else []
        }
        
        try:
            result = self.execute_with_pydantic(user_input, BusinessEvaluationResult, additional_context)
            
            # Error handling when result is None
            if result is None:
                return self._create_error_response("Pydantic execution result is None")
            
            # Wrap successful results
            if result.get("success"):
                business_evaluation = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
                
                return {
                    "success": True,
                    "business_evaluation": business_evaluation,
                    "_agent_metadata": result.get("_agent_metadata", {})
                }
            
            return result
        except Exception as e:
            import traceback
            error_msg = f"An error occurred during question generation: {str(e)}\n{traceback.format_exc()}"
            print(f"[{self.agent_name}] Error: {error_msg}")
            return self._create_error_response(error_msg)