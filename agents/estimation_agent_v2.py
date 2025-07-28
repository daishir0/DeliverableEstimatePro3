"""
Estimation Agent - Advanced Multi-Factor Calculation Engine

This agent serves as the synthesis and calculation engine for the multi-agent estimation system.
It integrates evaluations from BusinessRequirementsAgent, QualityRequirementsAgent, and 
ConstraintsAgent to produce comprehensive, accurate effort and cost estimates with detailed
confidence scoring and risk assessment.

Key Capabilities:
- Multi-factor effort calculation with complexity and risk adjustments
- Dynamic deliverable addition based on user feedback and implicit requirements
- Iterative refinement through human-AI collaboration loops
- Currency-aware cost calculation with tax and total computation
- Confidence scoring based on requirement clarity and risk factors
- Technical assumption documentation and recommendation generation

Estimation Methodology:
- Base effort estimation using industry-standard ranges for each deliverable type
- Complexity factor application (1.0x - 1.8x) based on technical difficulty
- Risk factor adjustment (+20% - +50%) for uncertainty and dependencies
- Quality requirement impact integration from QualityRequirementsAgent
- Constraint impact consideration from ConstraintsAgent analysis

Revolutionary Features:
- Tacit Knowledge Integration: Interprets human feedback to identify implicit requirements
- Intelligent Deliverable Discovery: Automatically adds missing deliverables (e.g., performance optimization)
- Iterative Refinement: Supports unlimited modification cycles with change tracking
- Multi-Currency Support: Dynamic currency formatting and tax calculation

Architecture Integration:
- Final synthesis agent in the 4-agent pipeline
- Receives structured input from 3 parallel evaluation agents
- Produces EstimationResult with comprehensive financial and technical details
- Supports real-time modification request processing during interactive sessions
"""

from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import EstimationResult
from utils.currency_utils import currency_formatter


class EstimationAgentV2(PydanticAIAgent):
    """
    Advanced Multi-Factor Estimation Synthesis Engine
    
    This agent represents the culmination of the 4-agent estimation system, synthesizing
    business, quality, and constraint evaluations into accurate effort and cost estimates.
    It employs sophisticated multi-factor calculation algorithms with real-time refinement
    capabilities based on human feedback and tacit knowledge integration.
    
    Core Calculation Framework:
    Final Effort = Base Effort × Complexity Factor × Risk Factor × Quality Impact × Constraint Impact
    
    Base Effort Standards (Industry-calibrated):
    - Requirements Definition: 2-8 person-days
    - System Design: 4-12 person-days  
    - Frontend Development: 8-25 person-days
    - Backend Development: 10-30 person-days
    - Database Design: 5-18 person-days
    - Testing: 5-15 person-days
    - Security Implementation: 3-15 person-days
    - Deployment: 2-10 person-days
    
    Adjustment Factors:
    - Complexity Multipliers: Low (1.0x), Medium (1.3x), High (1.8x)
    - Risk Adjustments: New technology (+30%), External dependencies (+20%), 
      Performance requirements (+25%), Advanced security (+30%)
    
    Revolutionary Capabilities:
    1. Tacit Knowledge Processing: Interprets human feedback to identify unstated requirements
    2. Dynamic Deliverable Addition: Automatically adds deliverables based on implicit needs
    3. Iterative Refinement: Processes modification requests with change impact analysis
    4. Confidence Scoring: Provides reliability assessment for each estimate component
    5. Multi-Currency Support: Handles global currency formatting and tax calculations
    
    Output Structure:
    - Detailed deliverable estimates with effort, cost, and confidence scores
    - Comprehensive financial summary with subtotals, tax, and total calculations
    - Technical assumptions and technology stack recommendations
    - Risk factors identification and mitigation strategies
    - Iteration history tracking for modification request processing
    """
    
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
- Daily rate: Will be specified in currency settings (configurable)

Please perform the following calculations for each deliverable:
1. Calculate base effort
2. Adjust for complexity
3. Adjust for risks
4. Calculate final effort and cost
5. Evaluate reliability

IMPORTANT: Financial Summary Calculation Rules:
- total_effort_days = sum of all deliverable final_effort_days
- subtotal = sum of all deliverable costs
- tax = subtotal × tax_rate (if applicable)
- total = subtotal + tax
- Ensure financial_summary.total exactly matches the sum of all deliverable costs

CRITICAL JSON FORMAT REQUIREMENT:
- In the financial_summary section, provide ONLY calculated numeric values
- DO NOT include calculation formulas or expressions like "6.5 + 10.4 + ..."
- Calculate the totals yourself and provide the final numbers only
- Example: "total_effort_days": 191.24 (not "6.5 + 10.4 + ...")

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
        
        # Use Pydantic structured output with currency information
        currency_info = currency_formatter.get_currency_info()
        
        # Add currency information to the user input
        enhanced_user_input = user_input + f"""

[CURRENCY SETTINGS]
Daily Rate: {currency_info['daily_rate']} {currency_info['currency']}
Currency: {currency_info['currency']}
"""
        
        result = self.execute_with_pydantic(enhanced_user_input, EstimationResult, evaluation_feedback)
        
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

⚠️[CRITICAL] You MUST recalculate the estimate reflecting the user's modification request.
The estimate MUST change from the previous version. Identical results are NOT acceptable.

Specific changes due to modification request:
1. Add/change technical requirements pointed out in feedback
2. Concretize performance requirements and library constraints
3. Accurately calculate the impact on effort and cost
4. Update technical prerequisites (libraries, performance requirements, etc.)
5. Identify new risk factors
6. ADD NEW DELIVERABLES if required by the modification request

[Example: When performance requirements like "10,000 concurrent users, sub-2-second response time" are added]
- ADD "Performance Optimization" deliverable (15-30 person-days)
- ADD "Load Testing & Performance Tuning" deliverable (10-20 person-days)
- INCREASE Backend Development effort (+20-50%)
- INCREASE Frontend Development effort (+15-30%)
- ADD cache/CDN implementation effort
- ADD database optimization effort
- ADD library selection (Redis, Nginx, etc.) to technical prerequisites
- UPDATE technical assumptions with performance requirements

MANDATORY: If user mentions performance requirements (concurrent users, response time), you MUST add performance-related deliverables.

IMPORTANT: Financial Summary Calculation Rules:
- total_effort_days = sum of all deliverable final_effort_days
- subtotal = sum of all deliverable costs
- tax = subtotal × tax_rate (if applicable)
- total = subtotal + tax
- Ensure financial_summary.total exactly matches the sum of all deliverable costs

CRITICAL JSON FORMAT REQUIREMENT:
- In the financial_summary section, provide ONLY calculated numeric values
- DO NOT include calculation formulas or expressions like "6.5 + 10.4 + ..."
- Calculate the totals yourself and provide the final numbers only
- Example: "total_effort_days": 191.24 (not "6.5 + 10.4 + ...")

The estimate results must be changed from the previous version. Same results are not acceptable.
"""
        
        # Include modification request analysis information in additional context
        additional_context = {
            "user_feedback": feedback,
            "previous_estimate": previous_estimate,
            "evaluation_updates": evaluation_updates,
            "requires_recalculation": True
        }
        
        # Use Pydantic structured output with currency information
        currency_info = currency_formatter.get_currency_info()
        
        # Add currency information to the user input
        enhanced_user_input = user_input + f"""

[CURRENCY SETTINGS]
Daily Rate: {currency_info['daily_rate']} {currency_info['currency']}
Currency: {currency_info['currency']}
"""
        
        result = self.execute_with_pydantic(enhanced_user_input, EstimationResult, additional_context)
        
        # Wrap results on success
        if result.get("success"):
            estimation_result = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
            
            return {
                "success": True,
                "estimation_result": estimation_result,
                "_agent_metadata": result.get("_agent_metadata", {})
            }
        
        return result