"""
State Manager for DeliverableEstimatePro v3
Manages workflow state, agent results, and iteration history
"""

from typing import Dict, Any, List
import json
from datetime import datetime

# Type definition for estimation state
EstimationState = Dict[str, Any]

def create_initial_state(excel_input: str, system_requirements: str, deliverables: List[Dict[str, Any]]) -> EstimationState:
    """Create initial workflow state"""
    return {
        "excel_input": excel_input,
        "system_requirements": system_requirements,
        "deliverables_memory": deliverables,
        "current_step": "initialized",
        "iteration_count": 0,
        "session_logs": [],
        "errors": [],
        "warnings": [],
        "user_approved": False,
        "user_feedback": "",
        "iteration_history": [],
        
        # Agent evaluation results
        "business_evaluation": None,
        "quality_evaluation": None,
        "constraints_evaluation": None,
        "estimation_result": None,
        
        # Previous evaluation results (for refinement)
        "previous_evaluation_results": {}
    }

def log_agent_execution(state: EstimationState, agent_name: str, result: Dict[str, Any]) -> EstimationState:
    """Log agent execution results to session logs"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "success": result.get("success", False),
        "execution_time": result.get("_agent_metadata", {}).get("execution_time", 0),
        "attempt_number": result.get("_agent_metadata", {}).get("attempt_number", 1)
    }
    
    if not result.get("success"):
        log_entry["error"] = result.get("error", "Unknown error")
        # Add to errors list
        state["errors"] = state.get("errors", []) + [f"{agent_name}: {result.get('error', 'Unknown error')}"]
    
    state["session_logs"] = state.get("session_logs", []) + [log_entry]
    return state

def update_evaluation_result(state: EstimationState, agent_name: str, result: Dict[str, Any]) -> EstimationState:
    """Update evaluation results in state based on agent type"""
    if not result.get("success"):
        return state
    
    if agent_name == "BusinessRequirementsAgent":
        state["business_evaluation"] = result
    elif agent_name == "QualityRequirementsAgent":
        state["quality_evaluation"] = result
    elif agent_name == "ConstraintsAgent":
        state["constraints_evaluation"] = result
    elif agent_name == "EstimationAgent":
        state["estimation_result"] = result
    
    return state

def is_evaluation_complete(state: EstimationState) -> bool:
    """Check if all required evaluations are complete"""
    required_evaluations = ["business_evaluation", "quality_evaluation", "constraints_evaluation"]
    
    for eval_key in required_evaluations:
        if not state.get(eval_key) or not state[eval_key].get("success"):
            return False
    
    return True

def get_evaluation_summary(state: EstimationState) -> Dict[str, bool]:
    """Get summary of evaluation completion status"""
    return {
        "business_complete": bool(state.get("business_evaluation", {}).get("success")),
        "quality_complete": bool(state.get("quality_evaluation", {}).get("success")),
        "constraints_complete": bool(state.get("constraints_evaluation", {}).get("success")),
        "estimation_complete": bool(state.get("estimation_result", {}).get("success"))
    }

def save_iteration_to_history(state: EstimationState, user_feedback: str = "") -> EstimationState:
    """Save current iteration results to history for future reference"""
    iteration_entry = {
        "iteration_number": state.get("iteration_count", 0) + 1,
        "timestamp": datetime.now().isoformat(),
        "user_feedback": user_feedback,
        "business_evaluation": state.get("business_evaluation"),
        "quality_evaluation": state.get("quality_evaluation"),
        "constraints_evaluation": state.get("constraints_evaluation"),
        "estimation_result": state.get("estimation_result"),
        "session_logs": state.get("session_logs", []).copy(),
        "errors": state.get("errors", []).copy(),
        "warnings": state.get("warnings", []).copy()
    }
    
    # Add technical assumptions if available
    if state.get("estimation_result", {}).get("success"):
        est_result = state["estimation_result"].get("estimation_result", {})
        iteration_entry["technical_assumptions"] = est_result.get("technical_assumptions", {})
        
        # Extract summary of changes
        changes_summary = []
        if user_feedback:
            if "response" in user_feedback.lower() or "performance" in user_feedback.lower():
                changes_summary.append("Performance requirements updated")
            if "library" in user_feedback.lower() or "platform" in user_feedback.lower():
                changes_summary.append("Technology stack updated")
            if "security" in user_feedback.lower():
                changes_summary.append("Security requirements updated")
        
        iteration_entry["changes_summary"] = changes_summary
    
    state["iteration_history"] = state.get("iteration_history", []) + [iteration_entry]
    
    # Update previous evaluation results for next iteration
    state["previous_evaluation_results"] = {
        "business_evaluation": state.get("business_evaluation"),
        "quality_evaluation": state.get("quality_evaluation"),
        "constraints_evaluation": state.get("constraints_evaluation")
    }
    
    return state

def add_warning(state: EstimationState, warning_message: str) -> EstimationState:
    """Add warning message to state"""
    state["warnings"] = state.get("warnings", []) + [warning_message]
    return state

def add_error(state: EstimationState, error_message: str) -> EstimationState:
    """Add error message to state"""
    state["errors"] = state.get("errors", []) + [error_message]
    return state

def reset_user_feedback(state: EstimationState) -> EstimationState:
    """Reset user feedback after processing"""
    state["user_feedback"] = ""
    state["user_approved"] = False
    return state

def get_current_iteration_summary(state: EstimationState) -> Dict[str, Any]:
    """Get summary of current iteration for display"""
    return {
        "iteration_count": state.get("iteration_count", 0),
        "current_step": state.get("current_step", "unknown"),
        "evaluations_complete": is_evaluation_complete(state),
        "total_errors": len(state.get("errors", [])),
        "total_warnings": len(state.get("warnings", [])),
        "user_approved": state.get("user_approved", False),
        "has_estimation_result": bool(state.get("estimation_result", {}).get("success"))
    }

def export_state_to_json(state: EstimationState, output_path: str) -> bool:
    """Export current state to JSON file for debugging/analysis"""
    try:
        # Create a clean copy without circular references
        export_data = {
            "metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "iteration_count": state.get("iteration_count", 0),
                "current_step": state.get("current_step", "unknown")
            },
            "inputs": {
                "excel_input": state.get("excel_input"),
                "system_requirements": state.get("system_requirements"),
                "deliverables_count": len(state.get("deliverables_memory", []))
            },
            "evaluation_results": {
                "business_evaluation": state.get("business_evaluation"),
                "quality_evaluation": state.get("quality_evaluation"),
                "constraints_evaluation": state.get("constraints_evaluation"),
                "estimation_result": state.get("estimation_result")
            },
            "session_info": {
                "session_logs": state.get("session_logs", []),
                "errors": state.get("errors", []),
                "warnings": state.get("warnings", []),
                "user_approved": state.get("user_approved", False),
                "user_feedback": state.get("user_feedback", "")
            },
            "iteration_history": state.get("iteration_history", [])
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error exporting state to JSON: {e}")
        return False