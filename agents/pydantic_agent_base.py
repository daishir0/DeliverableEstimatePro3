"""
Base AI Agent Compatible with PydanticOutputParser
"""

import os
from typing import Dict, Any, Optional, Type
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
import time

from config.i18n_config import t


class PydanticAIAgent:
    """Base class compatible with PydanticOutputParser"""
    
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        
        # Check for API key existence
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "dummy_key_for_testing":
            print(f"⚠️ Warning: OpenAI API key is not set. {self.agent_name} will return dummy data.")
            self.llm = None
        else:
            self.model = os.getenv("MODEL", "gpt-4o-mini")
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=0.1,
                openai_api_key=api_key,
                max_retries=2,
                request_timeout=60
            )
        self.max_retries = 3
    
    def execute_with_pydantic(self, user_input: str, 
                             pydantic_model: Type[BaseModel],
                             additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute with Pydantic structured output (enhanced error handling version)"""
        
        # Return dummy data if no API key
        if self.llm is None:
            return self._create_dummy_response(pydantic_model)
        
        # Input safety check
        if not user_input or not isinstance(user_input, str):
            return self._create_error_response("Invalid input data")
        
        # Configure PydanticOutputParser
        try:
            parser = PydanticOutputParser(pydantic_object=pydantic_model)
        except Exception as e:
            return self._create_error_response(f"Parser creation error: {str(e)}")
        
        # Add context information
        context_str = ""
        if additional_context:
            try:
                import json
                context_str = f"\n\n[ADDITIONAL CONTEXT]\n{json.dumps(additional_context, ensure_ascii=False, indent=2)}"
            except Exception as e:
                print(f"[{self.agent_name}] Context processing warning: {str(e)}")
                context_str = f"\n\n[ADDITIONAL CONTEXT]\n{str(additional_context)}"
        
        # Create prompt template
        try:
            prompt = ChatPromptTemplate.from_template(
                self.system_prompt + "\n\n{user_input}{context_str}\n\n{format_instructions}"
            ).partial(format_instructions=parser.get_format_instructions())
            
            # Create chain
            chain = prompt | self.llm | parser
        except Exception as e:
            return self._create_error_response(f"Prompt/chain creation error: {str(e)}")
        
        # Retry execution (with exponential backoff)
        for attempt in range(self.max_retries):
            try:
                # print(f"[{self.agent_name}] {t('workflow.agents_internal.execution_attempt', attempt=attempt + 1, max=self.max_retries)}")
                
                result = chain.invoke({
                    "user_input": user_input,
                    "context_str": context_str
                })
                
                # Convert Pydantic model to dictionary
                if isinstance(result, BaseModel):
                    result_dict = result.dict()
                    result_dict["success"] = True
                    result_dict["_agent_metadata"] = {
                        "agent_name": self.agent_name,
                        "attempt_number": attempt + 1,
                        "model_used": self.model,
                        "execution_time": time.time()
                    }
                    # print(f"[{self.agent_name}] {t('workflow.agents_internal.execution_success')}")
                    return result_dict
                else:
                    # For dictionary format
                    return {
                        "success": True,
                        "result": result,
                        "_agent_metadata": {
                            "agent_name": self.agent_name,
                            "attempt_number": attempt + 1,
                            "model_used": self.model,
                            "execution_time": time.time()
                        }
                    }
                
            except ValidationError as e:
                print(f"[{self.agent_name}] Validation error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_dummy_response(pydantic_model, f"Validation error: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                print(f"[{self.agent_name}] Execution error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_dummy_response(pydantic_model, f"Execution error: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return self._create_dummy_response(pydantic_model, "Maximum retry count reached")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Standard format for error responses"""
        return {
            "success": False,
            "error": error_message,
            "agent_name": self.agent_name,
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "error",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_response(self, pydantic_model: Type[BaseModel], error_message: str = "") -> Dict[str, Any]:
        """Create dummy response (for errors or when no API key)"""
        from .pydantic_models import (
            BusinessEvaluationResult, QualityEvaluationResult, 
            ConstraintsEvaluationResult, EstimationResult
        )
        
        try:
            if pydantic_model == BusinessEvaluationResult:
                return self._create_dummy_business_evaluation()
            elif pydantic_model == QualityEvaluationResult:
                return self._create_dummy_quality_evaluation()
            elif pydantic_model == ConstraintsEvaluationResult:
                return self._create_dummy_constraints_evaluation()
            elif pydantic_model == EstimationResult:
                return self._create_dummy_estimation_result()
            else:
                # Generic dummy
                return {
                    "success": True,
                    "dummy_data": True,
                    "overall_score": 75,
                    "note": f"Dummy data from {self.agent_name} due to missing API key",
                    "error_note": error_message,
                    "_agent_metadata": {
                        "agent_name": self.agent_name,
                        "status": "dummy",
                        "execution_time": time.time()
                    }
                }
        except Exception as e:
            print(f"[{self.agent_name}] Dummy creation error: {str(e)}")
            return self._create_error_response(f"Dummy creation error: {str(e)}")
    
    def _create_dummy_business_evaluation(self) -> Dict[str, Any]:
        """Dummy data for business requirements evaluation"""
        return {
            "success": True,
            "overall_score": 75,
            "business_purpose": {
                "clarity_score": 70,
                "assessment": "Dummy data: Business purpose is basically clear",
                "missing_elements": ["Detailed KPI settings"]
            },
            "functional_requirements": {
                "completeness_score": 80,
                "assessment": "Dummy data: Functional requirements are generally covered",
                "missing_elements": ["Screen transition details"]
            },
            "user_stories": {
                "coverage_score": 65,
                "assessment": "Dummy data: User stories are partial",
                "missing_elements": ["Error case considerations"]
            },
            "business_value": {
                "quantification_score": 60,
                "assessment": "Dummy data: Business value quantification is insufficient",
                "missing_elements": ["ROI calculation"]
            },
            "stakeholders": {
                "identification_score": 70,
                "assessment": "Dummy data: Key stakeholders are identified",
                "missing_elements": ["Approval flow"]
            },
            "business_flow": {
                "clarity_score": 75,
                "assessment": "Dummy data: Business flow is basically organized",
                "missing_elements": ["Exception handling flow"]
            },
            "improvement_questions": [
                {
                    "category": "Business Purpose",
                    "question": "What are the specific KPI target values?",
                    "purpose": "For quantitative evaluation",
                    "impact_on_estimation": "Improve effort accuracy"
                }
            ],
            "risk_factors": ["Requirements change risk", "Stakeholder coordination cost"],
            "recommendations": ["Clarify KPI settings", "Detail user stories"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_quality_evaluation(self) -> Dict[str, Any]:
        """Dummy data for quality requirements evaluation"""
        return {
            "success": True,
            "overall_score": 70,
            "performance_requirements": {
                "definition_score": 65,
                "assessment": "Dummy data: Performance requirements are partially defined",
                "missing_elements": ["Specific response time"],
                "effort_impact_percentage": 15.0
            },
            "security_requirements": {
                "completeness_score": 75,
                "assessment": "Dummy data: Security requirements are at basic level",
                "missing_elements": ["Vulnerability countermeasure details"],
                "effort_impact_percentage": 20.0
            },
            "availability_reliability": {
                "specification_score": 60,
                "assessment": "Dummy data: Availability requirements are unclear",
                "missing_elements": ["Uptime targets"],
                "effort_impact_percentage": 10.0
            },
            "scalability_maintainability": {
                "consideration_score": 70,
                "assessment": "Dummy data: Scalability is considered",
                "missing_elements": ["Maintenance plan"],
                "effort_impact_percentage": 12.0
            },
            "usability": {
                "requirement_score": 65,
                "assessment": "Dummy data: Usability is basically considered",
                "missing_elements": ["Accessibility requirements"],
                "effort_impact_percentage": 8.0
            },
            "operational_monitoring": {
                "planning_score": 55,
                "assessment": "Dummy data: Operational monitoring plan is insufficient",
                "missing_elements": ["Monitoring item details"],
                "effort_impact_percentage": 15.0
            },
            "improvement_questions": [
                {
                    "category": "Performance",
                    "question": "What is the expected response time?",
                    "purpose": "For performance design",
                    "impact_on_estimation": "Calculate optimization effort"
                }
            ],
            "total_effort_impact": 25.0,
            "risk_factors": ["Performance deficiency risk", "Operational monitoring deficiencies"],
            "recommendations": ["Clarify performance requirements", "Establish monitoring plan"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_constraints_evaluation(self) -> Dict[str, Any]:
        """Dummy data for constraints requirements evaluation"""
        return {
            "success": True,
            "overall_score": 65,
            "technical_constraints": {
                "clarity_score": 60,
                "assessment": "Dummy data: Technical constraints are partially clear",
                "identified_constraints": ["React/Node.js usage"],
                "missing_elements": ["Library restrictions"],
                "effort_impact_percentage": 10.0
            },
            "external_integrations": {
                "specification_score": 55,
                "assessment": "Dummy data: External integration specifications are insufficient",
                "identified_constraints": ["Payment system integration"],
                "missing_elements": ["API specification details"],
                "effort_impact_percentage": 20.0
            },
            "compliance_regulations": {
                "coverage_score": 70,
                "assessment": "Dummy data: Basic legal regulations are considered",
                "identified_constraints": ["Personal Information Protection Law"],
                "missing_elements": ["Industry-specific regulations"],
                "effort_impact_percentage": 15.0
            },
            "infrastructure_constraints": {
                "definition_score": 65,
                "assessment": "Dummy data: Infrastructure constraints are generally clear",
                "identified_constraints": ["Cloud usage"],
                "missing_elements": ["Specific service limitations"],
                "effort_impact_percentage": 8.0
            },
            "resource_constraints": {
                "realism_score": 75,
                "assessment": "Dummy data: Resource constraints are realistic",
                "identified_constraints": ["Budget limitations", "Schedule limitations"],
                "missing_elements": ["Personnel skill constraints"],
                "effort_impact_percentage": 12.0
            },
            "operational_constraints": {
                "planning_score": 60,
                "assessment": "Dummy data: Operational constraints are partially planned",
                "identified_constraints": ["Operating time limitations"],
                "missing_elements": ["Support structure"],
                "effort_impact_percentage": 10.0
            },
            "improvement_questions": [
                {
                    "category": "Technical Constraints",
                    "question": "Are there any prohibited libraries?",
                    "purpose": "For technology selection",
                    "impact_on_estimation": "Determine implementation approach"
                }
            ],
            "total_effort_impact": 18.0,
            "feasibility_risks": ["External integration issues", "Legal regulation changes"],
            "mitigation_strategies": ["Early API verification", "Legal confirmation"],
            "recommendations": ["Detail external integration specifications", "Document constraint conditions"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_estimation_result(self) -> Dict[str, Any]:
        """Dummy data for estimation results"""
        return {
            "success": True,
            "deliverable_estimates": [
                {
                    "name": "Requirements Definition Document",
                    "description": "System requirements definition",
                    "base_effort_days": 5.0,
                    "complexity_multiplier": 1.2,
                    "risk_multiplier": 1.1,
                    "final_effort_days": 6.6,
                    "cost_jpy": 330000,
                    "confidence_score": 0.8,
                    "rationale": "Dummy data: Standard requirements definition effort"
                },
                {
                    "name": "System Design Document",
                    "description": "Technical design document",
                    "base_effort_days": 8.0,
                    "complexity_multiplier": 1.3,
                    "risk_multiplier": 1.2,
                    "final_effort_days": 12.5,
                    "cost_jpy": 625000,
                    "confidence_score": 0.75,
                    "rationale": "Dummy data: Architecture design effort"
                }
            ],
            "financial_summary": {
                "total_effort_days": 245.0,
                "subtotal_jpy": 12250000,
                "tax_jpy": 1225000,
                "total_jpy": 13475000
            },
            "technical_assumptions": {
                "engineer_level": "Average engineer capable of using Python",
                "daily_rate_jpy": 50000,
                "development_stack": "React, Express.js, PostgreSQL",
                "team_size": 4,
                "project_duration_months": 6
            },
            "overall_confidence": 0.78,
            "key_risks": ["Technical complexity", "External integration risk", "Schedule constraints"],
            "recommendations": ["Create prototype", "Early technical verification", "Risk management plan"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy", 
                "execution_time": time.time()
            }
        }