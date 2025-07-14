"""
Simple Workflow Orchestrator - 4-Agent Integration
Lightweight version without LangGraph
"""

import asyncio
import os
import traceback
from typing import Dict, Any, List

from config.i18n_config import t

from agents.estimation_agent_v2 import EstimationAgentV2
from agents.business_requirements_agent_v2 import BusinessRequirementsAgentV2
from agents.quality_requirements_agent import QualityRequirementsAgent
from agents.constraints_agent import ConstraintsAgent
from state_manager import (
    EstimationState, create_initial_state, log_agent_execution,
    update_evaluation_result, is_evaluation_complete, get_evaluation_summary,
    save_iteration_to_history
)

# Load debug mode settings
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def debug_log(message):
    """Function to output debug logs"""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")


class SimpleWorkflowOrchestrator:
    """Simple 4-agent workflow orchestrator"""
    
    def __init__(self):
        self.estimation_agent = EstimationAgentV2()
        self.business_agent = BusinessRequirementsAgentV2()
        self.quality_agent = QualityRequirementsAgent()
        self.constraints_agent = ConstraintsAgent()
    
    def execute_workflow(self, excel_input: str, 
                        system_requirements: str, 
                        deliverables: List[Dict[str, Any]]) -> EstimationState:
        """Execute workflow"""
        print(f"🚀 {t('workflow.orchestrator.title')}")
        
        # Create initial state
        state = create_initial_state(excel_input, system_requirements, deliverables)
        
        try:
            # Step 1: Execute parallel evaluation
            state = self._execute_parallel_evaluation(state)
            
            # Step 2: Generate estimation
            state = self._execute_estimation_generation(state)
            
            # Step 3: User interaction loop
            state = self._execute_user_interaction_loop(state)
            
            print(f"🎯 {t('workflow.orchestrator.completed')}")
            return state
            
        except Exception as e:
            error_msg = f"❌ {t('errors.system.workflow_error', error=str(e))}"
            print(error_msg)
            state["errors"] = state.get("errors", []) + [error_msg]
            return state
    
    def _execute_parallel_evaluation(self, state: EstimationState) -> EstimationState:
        """Execute parallel evaluation - actual parallel execution version"""
        print(f"🔄 {t('workflow.orchestrator.parallel_evaluation_start')}")
        
        try:
            import concurrent.futures
            import time
            
            # Function definitions for parallel execution
            def run_business_evaluation():
                start_time = time.time()
                print(f"  📋 {t('workflow.agents.business.start')}")
                
                try:
                    # Debug log
                    if DEBUG_MODE:
                        debug_log(f"Before business agent execution: state keys = {list(state.keys())}")
                        debug_log(f"system_requirements = {state['system_requirements'][:50]}...")
                        debug_log(f"deliverables_memory type = {type(state['deliverables_memory'])}")
                        debug_log(f"deliverables_memory length = {len(state['deliverables_memory']) if state['deliverables_memory'] else 0}")
                        
                        previous_eval = state.get("previous_evaluation_results", {})
                        debug_log(f"previous_evaluation_results type = {type(previous_eval)}")
                        debug_log(f"previous_evaluation_results keys = {list(previous_eval.keys()) if isinstance(previous_eval, dict) else 'Not a dict'}")
                        
                        business_eval = previous_eval.get("business_evaluation") if isinstance(previous_eval, dict) else None
                        debug_log(f"business_evaluation type = {type(business_eval)}")
                    
                    # Handle modification requests: pass previous evaluation results and user feedback
                    previous_eval = state.get("previous_evaluation_results", {})
                    if previous_eval is None:
                        previous_eval = {}
                    
                    business_eval = previous_eval.get("business_evaluation") if isinstance(previous_eval, dict) else None
                    user_feedback = state.get("user_feedback", "")
                    
                    # Debug log
                    if DEBUG_MODE:
                        debug_log(f"Just before business agent execution: previous_eval = {type(business_eval)}")
                    
                    result = self.business_agent.evaluate_business_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"],
                        previous_evaluation=business_eval,
                        user_feedback=user_feedback
                    )
                    
                    end_time = time.time()
                    print(f"  📋 {t('workflow.agents.business.complete')} ({end_time - start_time:.2f}seconds)")
                    return ("business", result)
                except Exception as e:
                    if DEBUG_MODE:
                        debug_log(f"Business agent execution error: {str(e)}")
                        debug_log(f"Error details: {traceback.format_exc()}")
                    raise e
            
            def run_quality_evaluation():
                start_time = time.time()
                print(f"  🎯 {t('workflow.agents.quality.start')}")
                result = self.quality_agent.evaluate_quality_requirements(
                    state["system_requirements"],
                    state["deliverables_memory"]
                )
                end_time = time.time()
                print(f"  🎯 {t('workflow.agents.quality.complete')} ({end_time - start_time:.2f}seconds)")
                return ("quality", result)
            
            def run_constraints_evaluation():
                start_time = time.time()
                print(f"  🔒 {t('workflow.agents.constraints.start')}")
                result = self.constraints_agent.evaluate_constraints(
                    state["system_requirements"],
                    state["deliverables_memory"]
                )
                end_time = time.time()
                print(f"  🔒 {t('workflow.agents.constraints.complete')} ({end_time - start_time:.2f}seconds)")
                return ("constraints", result)
            
            # True parallel execution
            print(f"⚡ {t('workflow.performance.parallel_execution_start')}")
            parallel_start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Execute 3 tasks in parallel
                futures = [
                    executor.submit(run_business_evaluation),
                    executor.submit(run_quality_evaluation),
                    executor.submit(run_constraints_evaluation)
                ]
                
                # Collect results
                results = {}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        agent_type, result = future.result()
                        results[agent_type] = result
                        if DEBUG_MODE:
                            debug_log(f"Agent {agent_type} completed: result keys = {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                    except Exception as e:
                        error_msg = f"❌ Agent execution error: {str(e)}"
                        print(error_msg)
                        if DEBUG_MODE:
                            debug_log(f"Error details: {traceback.format_exc()}")
                            # Identify which agent had the error
                            for i, f in enumerate(futures):
                                if f == future:
                                    agent_types = ["business", "quality", "constraints"]
                                    if i < len(agent_types):
                                        debug_log(f"Agent with error: {agent_types[i]}")
            
            parallel_end_time = time.time()
            print(f"⚡ {t('workflow.display.execution_messages.parallel_completed', time=f'{parallel_end_time - parallel_start_time:.2f}')}")
            
            # Reflect results in state
            updated_state = state.copy()
            
            if "business" in results:
                updated_state = log_agent_execution(updated_state, "BusinessRequirementsAgent", results["business"])
                if results["business"].get("success"):
                    updated_state = update_evaluation_result(updated_state, "BusinessRequirementsAgent", results["business"])
            
            if "quality" in results:
                updated_state = log_agent_execution(updated_state, "QualityRequirementsAgent", results["quality"])
                if results["quality"].get("success"):
                    updated_state = update_evaluation_result(updated_state, "QualityRequirementsAgent", results["quality"])
            
            if "constraints" in results:
                updated_state = log_agent_execution(updated_state, "ConstraintsAgent", results["constraints"])
                if results["constraints"].get("success"):
                    updated_state = update_evaluation_result(updated_state, "ConstraintsAgent", results["constraints"])
            
            updated_state["iteration_count"] = state["iteration_count"] + 1
            updated_state["current_step"] = "parallel_evaluation_complete"
            
            print(f"✅ {t('workflow.display.execution_messages.evaluation_completed')}")
            return updated_state
            
        except Exception as e:
            print(f"❌ Parallel evaluation system error: {str(e)}")
            # Fallback: alternative parallel execution method
            print("🔄 Fallback: Switching to ThreadPoolExecutor parallel execution")
            return self._execute_fallback_parallel_evaluation(state)
    
    def _execute_fallback_parallel_evaluation(self, state: EstimationState) -> EstimationState:
        """Fallback parallel evaluation execution (using ThreadPoolExecutor)"""
        try:
            import concurrent.futures
            import time
            
            print("🔄 Starting fallback parallel execution...")
            parallel_start_time = time.time()
            
            # Function definitions for parallel execution (enhanced error handling version)
            def safe_run_business_evaluation():
                try:
                    start_time = time.time()
                    print(f"  📋 {t('workflow.agents.business.start')}")
                    result = self.business_agent.evaluate_business_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  📋 {t('workflow.agents.business.complete')} ({end_time - start_time:.2f}seconds)")
                    return ("business", result)
                except Exception as e:
                    print(f"  📋 Business & Functional Requirements Evaluation - Error: {str(e)}")
                    return ("business", {"success": False, "error": str(e)})
            
            def safe_run_quality_evaluation():
                try:
                    start_time = time.time()
                    print(f"  🎯 {t('workflow.agents.quality.start')}")
                    result = self.quality_agent.evaluate_quality_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  🎯 {t('workflow.agents.quality.complete')} ({end_time - start_time:.2f}seconds)")
                    return ("quality", result)
                except Exception as e:
                    print(f"  🎯 Quality & Non-Functional Requirements Evaluation - Error: {str(e)}")
                    return ("quality", {"success": False, "error": str(e)})
            
            def safe_run_constraints_evaluation():
                try:
                    start_time = time.time()
                    print(f"  🔒 {t('workflow.agents.constraints.start')}")
                    result = self.constraints_agent.evaluate_constraints(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  🔒 {t('workflow.agents.constraints.complete')} ({end_time - start_time:.2f}seconds)")
                    return ("constraints", result)
                except Exception as e:
                    print(f"  🔒 Constraints & External Integration Requirements Evaluation - Error: {str(e)}")
                    return ("constraints", {"success": False, "error": str(e)})
            
            # Parallel execution with ThreadPoolExecutor
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                print("⚡ Running 3 agents in parallel with ThreadPoolExecutor...")
                
                # Execute 3 tasks in parallel
                futures = {
                    executor.submit(safe_run_business_evaluation): "business",
                    executor.submit(safe_run_quality_evaluation): "quality", 
                    executor.submit(safe_run_constraints_evaluation): "constraints"
                }
                
                # Collect results
                results = {}
                completed_count = 0
                
                for future in concurrent.futures.as_completed(futures):
                    completed_count += 1
                    agent_type_expected = futures[future]
                    try:
                        agent_type, result = future.result(timeout=120)  # 2-minute timeout
                        results[agent_type] = result
                        print(f"✅ {agent_type} agent completed ({completed_count}/3)")
                    except concurrent.futures.TimeoutError:
                        print(f"⏰ {agent_type_expected} agent - Timeout")
                        results[agent_type_expected] = {"success": False, "error": "Timeout"}
                    except Exception as e:
                        print(f"❌ {agent_type_expected} agent - Execution error: {str(e)}")
                        results[agent_type_expected] = {"success": False, "error": str(e)}
            
            parallel_end_time = time.time()
            print(f"⚡ {t('workflow.display.execution_messages.parallel_completed', time=f'{parallel_end_time - parallel_start_time:.2f}')}")
            
            # Reflect results in state
            updated_state = state.copy()
            
            for agent_type, result in results.items():
                if agent_type == "business":
                    updated_state = log_agent_execution(updated_state, "BusinessRequirementsAgent", result)
                    if result.get("success"):
                        updated_state = update_evaluation_result(updated_state, "BusinessRequirementsAgent", result)
                elif agent_type == "quality":
                    updated_state = log_agent_execution(updated_state, "QualityRequirementsAgent", result)
                    if result.get("success"):
                        updated_state = update_evaluation_result(updated_state, "QualityRequirementsAgent", result)
                elif agent_type == "constraints":
                    updated_state = log_agent_execution(updated_state, "ConstraintsAgent", result)
                    if result.get("success"):
                        updated_state = update_evaluation_result(updated_state, "ConstraintsAgent", result)
            
            updated_state["iteration_count"] = state["iteration_count"] + 1
            updated_state["current_step"] = "parallel_evaluation_complete"
            
            # Check success status
            success_count = sum(1 for result in results.values() if result.get("success"))
            print(f"📊 Evaluation success rate: {success_count}/3 agents")
            
            print(f"✅ {t('workflow.display.execution_messages.evaluation_completed')}")
            return updated_state
            
        except Exception as e:
            print(f"❌ Overall parallel evaluation system error: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"Parallel evaluation system error: {str(e)}"]
            return state
    
    def _execute_estimation_generation(self, state: EstimationState) -> EstimationState:
        """Execute estimation generation"""
        print(f"💰 {t('workflow.estimation.generation_start')}")
        
        if not is_evaluation_complete(state):
            error_msg = "Parallel evaluation not completed"
            state["errors"] = state.get("errors", []) + [error_msg]
            return state
        
        # Integrate evaluation results
        evaluation_feedback = {
            "business_evaluation": state.get("business_evaluation"),
            "quality_evaluation": state.get("quality_evaluation"),
            "constraints_evaluation": state.get("constraints_evaluation")
        }
        
        try:
            print(f"  🧮 {t('workflow.estimation.calculating')}")
            result = self.estimation_agent.generate_estimate(
                state["deliverables_memory"],
                state["system_requirements"],
                evaluation_feedback
            )
            
            state = log_agent_execution(state, "EstimationAgent", result)
            if result.get("success"):
                state = update_evaluation_result(state, "EstimationAgent", result)
            
            state["current_step"] = "estimation_complete"
            print(f"✅ {t('workflow.estimation.generation_complete')}")
            return state
            
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Estimation generation error: {str(e)}"]
            return state
    
    def _execute_user_interaction_loop(self, state: EstimationState) -> EstimationState:
        """Execute user interaction loop"""
        print(f"👥 {t('workflow.user_interaction.title')}")
        
        max_iterations = 3
        iteration = 0
        
        while iteration < max_iterations:
            # Display current results
            self._display_current_results(state)
            
            # Wait for user input
            user_response = input(f"\n{t('workflow.user_interaction.approval_prompt')}").strip().lower()
            
            if user_response in ['y', 'yes', 'approve']:
                state["user_approved"] = True
                state["current_step"] = "approved"
                print(f"✅ {t('workflow.user_interaction.approved')}")
                break
            elif user_response in ['n', 'no', 'reject']:
                state["user_approved"] = False
                feedback = input(t('workflow.user_interaction.feedback_prompt'))
                state["user_feedback"] = feedback
                state["current_step"] = "needs_refinement"
            else:
                state["user_approved"] = False
                state["user_feedback"] = user_response
                state["current_step"] = "needs_refinement"
            
            # Execute improvement
            if not state.get("user_approved"):
                state = self._execute_refinement(state)
                iteration += 1
            
        if not state.get("user_approved"):
            print(f"⚠️ {t('workflow.user_interaction.max_iterations')}")
        
        return state
    
    def _execute_refinement(self, state: EstimationState) -> EstimationState:
        """Execute refinement (enhanced modification request version)"""
        print(f"🔄 {t('workflow.refinement.title')}")
        
        try:
            # Save current state to history
            state = save_iteration_to_history(state, state.get("user_feedback", ""))
            
            # Get current and previous estimates
            current_estimate = state.get("estimation_result", {})
            previous_estimate = None
            
            # Get previous estimate from history
            history = state.get("iteration_history", [])
            if len(history) >= 2:
                previous_estimate = history[-2].get("estimation_result")
            
            feedback = state.get("user_feedback", "")
            
            # Integrate evaluation results (latest version reflecting modification requests)
            evaluation_feedback = {
                "business_evaluation": state.get("business_evaluation"),
                "quality_evaluation": state.get("quality_evaluation"),
                "constraints_evaluation": state.get("constraints_evaluation")
            }
            
            print("  🧮 Recalculating estimate reflecting modification requests...")
            result = self.estimation_agent.refine_estimate(
                current_estimate,
                feedback,
                evaluation_feedback,
                previous_estimate
            )
            
            state = log_agent_execution(state, "EstimationAgent_Refinement", result)
            if result.get("success"):
                state = update_evaluation_result(state, "EstimationAgent", result)
            
            state["iteration_count"] = state["iteration_count"] + 1
            state["current_step"] = "refinement_complete"
            
            # Verify changes from modification requests
            self._verify_modification_applied(state, feedback)
            
            print(f"✅ {t('workflow.refinement.completed')}")
            return state
            
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"Refinement execution error: {str(e)}"]
            return state
    
    def _verify_modification_applied(self, state: EstimationState, feedback: str):
        """Verify if modification requests were applied"""
        if not feedback:
            return
        
        current_est = state.get("estimation_result", {})
        if not current_est.get("success"):
            return
        
        est_result = current_est.get("estimation_result", {})
        tech_assumptions = est_result.get("technical_assumptions", {})
        
        # Simple validation (example: response time requirements)
        if "response" in feedback.lower() and "5seconds" in feedback:
            if "response" not in str(tech_assumptions).lower() and "performance" not in str(tech_assumptions).lower():
                print("⚠️ Warning: Response time requirements may not be reflected in technical assumptions")
        
        # Library/platform requirements validation
        if "library" in feedback.lower() or "platform" in feedback.lower():
            dev_stack = tech_assumptions.get("development_stack", "")
            if len(dev_stack.split(",")) <= 2:  # Few specific libraries
                print("⚠️ Warning: Library/platform requirements may not be sufficiently specified")
    
    def _display_current_results(self, state: EstimationState):
        """Display current results - detailed version"""
        print("\n" + "="*80)
        print(f"📋 {t('workflow.display.detailed_report_title')}")
        print("="*80)
        
        # 1. Evaluation summary
        summary = get_evaluation_summary(state)
        print(f"📊 {t('workflow.display.evaluation_status')}")
        print(f"  {t('workflow.display.business_requirements')}: {'✅' if summary['business_complete'] else '❌'}")
        print(f"  {t('workflow.display.quality_requirements')}: {'✅' if summary['quality_complete'] else '❌'}")
        print(f"  {t('workflow.display.constraints_requirements')}: {'✅' if summary['constraints_complete'] else '❌'}")
        print(f"  {t('workflow.display.estimation_generation')}: {'✅' if summary['estimation_complete'] else '❌'}")
        
        # 2. Detailed evaluation results for each agent
        self._display_agent_evaluations(state)
        
        # 3. Estimation results
        if state.get("estimation_result") and state["estimation_result"].get("success"):
            est_result = state["estimation_result"]["estimation_result"]
            print(f"\n💰 {t('workflow.display.estimation_result')}")
            print(f"  {t('workflow.display.total_effort', days=est_result['financial_summary']['total_effort_days'])}")
            print(f"  {t('workflow.display.total_amount', amount=est_result['financial_summary']['total_jpy'])}")
            print(f"  {t('workflow.display.confidence', confidence=est_result['overall_confidence'])}")
            
            # 4. Detailed breakdown by all deliverables (no omissions)
            self._display_all_deliverable_estimates(est_result)
            
            # 5. Major risks and recommendations
            self._display_risks_and_recommendations(est_result, state)
        
        # 6. Errors and warnings
        if state.get("errors"):
            print(f"\n❌ Number of errors: {len(state['errors'])}")
            for error in state["errors"][-3:]:  # Show only the latest 3
                print(f"  - {error}")
        
        if state.get("warnings"):
            print(f"⚠️ Number of warnings: {len(state['warnings'])}")
    
    def _display_agent_evaluations(self, state: EstimationState):
        """Display detailed evaluation results for each agent"""
        print(f"\n🤖 {t('workflow.display.agent_evaluation_details')}")
        print("-" * 60)
        
        # Business & functional requirements agent evaluation
        if state.get("business_evaluation"):
            business_eval = state["business_evaluation"]
            if business_eval.get("success"):
                print(f"📋 {t('workflow.display.business_agent_evaluation')}")
                if isinstance(business_eval, dict) and "overall_score" in business_eval:
                    print(f"  Overall Score: {business_eval.get('overall_score', 'N/A')}/100")
                    print(f"  Business Purpose Clarity: {business_eval.get('business_purpose', {}).get('clarity_score', 'N/A')}/100")
                    print(f"  Functional Requirements Completeness: {business_eval.get('functional_requirements', {}).get('completeness_score', 'N/A')}/100")
                    print(f"  Major Risks: {', '.join(business_eval.get('risk_factors', [])[:3])}")
                else:
                    print(f"  {t('workflow.display.evaluation_data')}: {str(business_eval)[:200]}...")
            else:
                print(f"📋 Business & Functional Requirements Agent: Error - {business_eval.get('error', 'Unknown')}")
        
        # Quality & non-functional requirements agent evaluation
        if state.get("quality_evaluation"):
            quality_eval = state["quality_evaluation"]
            if quality_eval.get("success"):
                print(f"\n🎯 {t('workflow.display.quality_agent_evaluation')}")
                if isinstance(quality_eval, dict) and "overall_score" in quality_eval:
                    print(f"  Overall Score: {quality_eval.get('overall_score', 'N/A')}/100")
                    print(f"  Performance Requirements: {quality_eval.get('performance_requirements', {}).get('definition_score', 'N/A')}/100")
                    print(f"  Security Requirements: {quality_eval.get('security_requirements', {}).get('completeness_score', 'N/A')}/100")
                    print(f"  Effort Impact: +{quality_eval.get('total_effort_impact', 'N/A')}%")
                else:
                    print(f"  {t('workflow.display.evaluation_data')}: {str(quality_eval)[:200]}...")
            else:
                print(f"🎯 Quality & Non-Functional Requirements Agent: Error - {quality_eval.get('error', 'Unknown')}")
        
        # Constraints & external integration requirements agent evaluation
        if state.get("constraints_evaluation"):
            constraints_eval = state["constraints_evaluation"]
            if constraints_eval.get("success"):
                print(f"\n🔒 {t('workflow.display.constraints_agent_evaluation')}")
                if isinstance(constraints_eval, dict) and "overall_score" in constraints_eval:
                    print(f"  Overall Score: {constraints_eval.get('overall_score', 'N/A')}/100")
                    print(f"  Technical Constraints Clarity: {constraints_eval.get('technical_constraints', {}).get('clarity_score', 'N/A')}/100")
                    print(f"  External Integration Specifications: {constraints_eval.get('external_integrations', {}).get('specification_score', 'N/A')}/100")
                    print(f"  Feasibility Risks: {', '.join(constraints_eval.get('feasibility_risks', [])[:3])}")
                else:
                    print(f"  {t('workflow.display.evaluation_data')}: {str(constraints_eval)[:200]}...")
            else:
                print(f"🔒 Constraints & External Integration Requirements Agent: Error - {constraints_eval.get('error', 'Unknown')}")
    
    def _display_all_deliverable_estimates(self, est_result: Dict[str, Any]):
        """Display estimates for all deliverables (no omissions)"""
        print(f"\n📋 {t('workflow.display.deliverable_estimates_detail')}")
        print("-" * 80)
        print(f"{t('workflow.display.table_headers.no'):<4} {t('workflow.display.table_headers.deliverable_name'):<25} {t('workflow.display.table_headers.base_effort'):<8} {t('workflow.display.table_headers.final_effort'):<8} {t('workflow.display.table_headers.amount'):<12} {t('workflow.display.table_headers.confidence'):<6}")
        print("-" * 80)
        
        deliverable_estimates = est_result.get('deliverable_estimates', [])
        for i, item in enumerate(deliverable_estimates, 1):
            name = item.get('name', 'N/A')[:23]  # Character limit
            base_effort = item.get('base_effort_days', 0)
            final_effort = item.get('final_effort_days', 0)
            cost = item.get('cost_jpy', 0)
            confidence = item.get('confidence_score', 0)
            
            print(f"{i:<4} {name:<25} {base_effort:<8.1f} {final_effort:<8.1f} ¥{cost:<11,} {confidence:<6.2f}")
        
        print("-" * 80)
        financial_summary = est_result.get('financial_summary', {})
        print(f"{t('workflow.display.table_headers.total'):<4} {'':<25} {'':<8} {financial_summary.get('total_effort_days', 0):<8.1f} ¥{financial_summary.get('total_jpy', 0):<11,}")
    
    def _display_risks_and_recommendations(self, est_result: Dict[str, Any], state: EstimationState = None):
        """Display major risks and recommendations"""
        print(f"\n⚠️ {t('workflow.display.main_risks')}")
        key_risks = est_result.get('key_risks', [])
        for i, risk in enumerate(key_risks, 1):
            print(f"  {i}. {risk}")
        
        print(f"\n💡 {t('workflow.display.recommendations')}")
        recommendations = est_result.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        print(f"\n🔧 {t('workflow.display.technical_assumptions')}")
        tech_assumptions = est_result.get('technical_assumptions', {})
        print(f"  {t('workflow.display.engineer_level', level=tech_assumptions.get('engineer_level', 'N/A'))}")
        print(f"  {t('workflow.display.daily_rate', rate=tech_assumptions.get('daily_rate_jpy', 'N/A'))}")
        print(f"  {t('workflow.display.development_stack', stack=tech_assumptions.get('development_stack', 'N/A'))}")
        print(f"  {t('workflow.display.team_size', size=tech_assumptions.get('team_size', 'N/A'))}")
        print(f"  {t('workflow.display.project_duration', duration=tech_assumptions.get('project_duration_months', 'N/A'))}")
        
        # Add history display (only when state is available)
        if state is not None:
            self._display_iteration_history(state)
    
    def _display_iteration_history(self, state: EstimationState):
        """Display iteration history"""
        history = state.get("iteration_history", [])
        
        if len(history) <= 1:
            return  # Don't display if history is minimal
        
        print(f"\n📊 Estimation Assumptions History:")
        print("-" * 80)
        
        for i, entry in enumerate(history, 1):
            iteration_num = entry.get("iteration_number", i)
            feedback = entry.get("user_feedback", "")
            tech_assumptions = entry.get("technical_assumptions", {})
            changes = entry.get("changes_summary", [])
            
            print(f"\n【Estimation Iteration {iteration_num}】")
            if feedback:
                print(f"  User Request: {feedback}")

            if tech_assumptions:
                print(f"  Technical Assumptions:")
                print(f"    - Development Stack: {tech_assumptions.get('development_stack', 'N/A')}")
                print(f"    - Daily Rate: ¥{tech_assumptions.get('daily_rate_jpy', 'N/A'):,}")

                # Display special requirements like performance requirements
                special_requirements = []
                dev_stack = tech_assumptions.get('development_stack', '')
                if 'Redis' in dev_stack or 'cache' in dev_stack.lower():
                    special_requirements.append("Cache Implementation")
                if 'Nginx' in dev_stack or 'CDN' in dev_stack:
                    special_requirements.append("CDN & Load Balancer")
                if 'response' in str(tech_assumptions).lower() or 'performance' in str(tech_assumptions).lower():
                    special_requirements.append("Performance Optimization")

                if special_requirements:
                    print(f"    - Special Requirements: {', '.join(special_requirements)}")

            if changes:
                print(f"  Changes: {', '.join(changes)}")
        
        # Total change summary
        if len(history) >= 2:
            first_est = history[0].get("estimation_result", {}).get("estimation_result", {}).get("financial_summary", {})
            last_est = history[-1].get("estimation_result", {}).get("estimation_result", {}).get("financial_summary", {})
            
            if first_est and last_est:
                first_total = first_est.get("total_effort_days", 0)
                last_total = last_est.get("total_effort_days", 0)
                first_cost = first_est.get("total_jpy", 0)
                last_cost = last_est.get("total_jpy", 0)
                
                print(f"\n📈 Cumulative Changes from Modification Requests:")
                print(f"  Effort Change: {first_total:.1f} person-days → {last_total:.1f} person-days ({last_total-first_total:+.1f} person-days)")
                print(f"  Cost Change: ¥{first_cost:,} → ¥{last_cost:,} (¥{last_cost-first_cost:+,})")
                
                if first_total > 0:
                    effort_change_pct = ((last_total - first_total) / first_total) * 100
                    print(f"  Change Rate: {effort_change_pct:+.1f}%")