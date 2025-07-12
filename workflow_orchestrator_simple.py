"""
シンプルなワークフローオーケストレーター - 4エージェント統合
LangGraphを使わない軽量版
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

# デバッグモードの設定を読み込み
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def debug_log(message):
    """デバッグログを出力する関数"""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")


class SimpleWorkflowOrchestrator:
    """シンプルな4エージェントワークフローオーケストレーター"""
    
    def __init__(self):
        self.estimation_agent = EstimationAgentV2()
        self.business_agent = BusinessRequirementsAgentV2()
        self.quality_agent = QualityRequirementsAgent()
        self.constraints_agent = ConstraintsAgent()
    
    def execute_workflow(self, excel_input: str, 
                        system_requirements: str, 
                        deliverables: List[Dict[str, Any]]) -> EstimationState:
        """ワークフロー実行"""
        print(f"🚀 {t('workflow.orchestrator.title')}")
        
        # 初期状態作成
        state = create_initial_state(excel_input, system_requirements, deliverables)
        
        try:
            # Step 1: 並列評価実行
            state = self._execute_parallel_evaluation(state)
            
            # Step 2: 見積もり生成
            state = self._execute_estimation_generation(state)
            
            # Step 3: ユーザー対話ループ
            state = self._execute_user_interaction_loop(state)
            
            print(f"🎯 {t('workflow.orchestrator.completed')}")
            return state
            
        except Exception as e:
            error_msg = f"❌ {t('errors.system.workflow_error', error=str(e))}"
            print(error_msg)
            state["errors"] = state.get("errors", []) + [error_msg]
            return state
    
    def _execute_parallel_evaluation(self, state: EstimationState) -> EstimationState:
        """並列評価実行 - 実際の並列実行版"""
        print(f"🔄 {t('workflow.orchestrator.parallel_evaluation_start')}")
        
        try:
            import concurrent.futures
            import time
            
            # 並列実行のための関数定義
            def run_business_evaluation():
                start_time = time.time()
                print(f"  📋 {t('workflow.agents.business.start')}")
                
                try:
                    # デバッグログ
                    if DEBUG_MODE:
                        debug_log(f"業務エージェント実行前: state keys = {list(state.keys())}")
                        debug_log(f"system_requirements = {state['system_requirements'][:50]}...")
                        debug_log(f"deliverables_memory type = {type(state['deliverables_memory'])}")
                        debug_log(f"deliverables_memory length = {len(state['deliverables_memory']) if state['deliverables_memory'] else 0}")
                        
                        previous_eval = state.get("previous_evaluation_results", {})
                        debug_log(f"previous_evaluation_results type = {type(previous_eval)}")
                        debug_log(f"previous_evaluation_results keys = {list(previous_eval.keys()) if isinstance(previous_eval, dict) else 'Not a dict'}")
                        
                        business_eval = previous_eval.get("business_evaluation") if isinstance(previous_eval, dict) else None
                        debug_log(f"business_evaluation type = {type(business_eval)}")
                    
                    # 修正要求対応：前回評価結果とユーザーフィードバックを渡す
                    previous_eval = state.get("previous_evaluation_results", {})
                    if previous_eval is None:
                        previous_eval = {}
                    
                    business_eval = previous_eval.get("business_evaluation") if isinstance(previous_eval, dict) else None
                    user_feedback = state.get("user_feedback", "")
                    
                    # デバッグログ
                    if DEBUG_MODE:
                        debug_log(f"業務エージェント実行直前: previous_eval = {type(business_eval)}")
                    
                    result = self.business_agent.evaluate_business_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"],
                        previous_evaluation=business_eval,
                        user_feedback=user_feedback
                    )
                    
                    end_time = time.time()
                    print(f"  📋 業務・機能要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                    return ("business", result)
                except Exception as e:
                    if DEBUG_MODE:
                        debug_log(f"業務エージェント実行エラー: {str(e)}")
                        debug_log(f"エラー詳細: {traceback.format_exc()}")
                    raise e
            
            def run_quality_evaluation():
                start_time = time.time()
                print("  🎯 品質・非機能要件評価 - 開始")
                result = self.quality_agent.evaluate_quality_requirements(
                    state["system_requirements"],
                    state["deliverables_memory"]
                )
                end_time = time.time()
                print(f"  🎯 品質・非機能要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                return ("quality", result)
            
            def run_constraints_evaluation():
                start_time = time.time()
                print("  🔒 制約・外部連携要件評価 - 開始")
                result = self.constraints_agent.evaluate_constraints(
                    state["system_requirements"],
                    state["deliverables_memory"]
                )
                end_time = time.time()
                print(f"  🔒 制約・外部連携要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                return ("constraints", result)
            
            # 真の並列実行
            print("⚡ 3エージェントを並列実行中...")
            parallel_start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # 3つのタスクを並列実行
                futures = [
                    executor.submit(run_business_evaluation),
                    executor.submit(run_quality_evaluation),
                    executor.submit(run_constraints_evaluation)
                ]
                
                # 結果を収集
                results = {}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        agent_type, result = future.result()
                        results[agent_type] = result
                        if DEBUG_MODE:
                            debug_log(f"エージェント {agent_type} 完了: result keys = {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                    except Exception as e:
                        error_msg = f"❌ エージェント実行エラー: {str(e)}"
                        print(error_msg)
                        if DEBUG_MODE:
                            debug_log(f"エラー詳細: {traceback.format_exc()}")
                            # どのエージェントでエラーが発生したかを特定
                            for i, f in enumerate(futures):
                                if f == future:
                                    agent_types = ["business", "quality", "constraints"]
                                    if i < len(agent_types):
                                        debug_log(f"エラーが発生したエージェント: {agent_types[i]}")
            
            parallel_end_time = time.time()
            print(f"⚡ 並列実行完了 - 総時間: {parallel_end_time - parallel_start_time:.2f}秒")
            
            # 結果を状態に反映
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
            
            print("✅ 並列評価完了")
            return updated_state
            
        except Exception as e:
            print(f"❌ 並列評価システムエラー: {str(e)}")
            # フォールバック: 別の並列実行方式
            print("🔄 フォールバック: ThreadPoolExecutor並列実行に切り替え")
            return self._execute_fallback_parallel_evaluation(state)
    
    def _execute_fallback_parallel_evaluation(self, state: EstimationState) -> EstimationState:
        """フォールバック用の並列評価実行（ThreadPoolExecutor使用）"""
        try:
            import concurrent.futures
            import time
            
            print("🔄 フォールバック並列実行開始...")
            parallel_start_time = time.time()
            
            # 並列実行用の関数定義（エラーハンドリング強化版）
            def safe_run_business_evaluation():
                try:
                    start_time = time.time()
                    print(f"  📋 {t('workflow.agents.business.start')}")
                    result = self.business_agent.evaluate_business_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  📋 業務・機能要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                    return ("business", result)
                except Exception as e:
                    print(f"  📋 業務・機能要件評価 - エラー: {str(e)}")
                    return ("business", {"success": False, "error": str(e)})
            
            def safe_run_quality_evaluation():
                try:
                    start_time = time.time()
                    print("  🎯 品質・非機能要件評価 - 開始")
                    result = self.quality_agent.evaluate_quality_requirements(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  🎯 品質・非機能要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                    return ("quality", result)
                except Exception as e:
                    print(f"  🎯 品質・非機能要件評価 - エラー: {str(e)}")
                    return ("quality", {"success": False, "error": str(e)})
            
            def safe_run_constraints_evaluation():
                try:
                    start_time = time.time()
                    print("  🔒 制約・外部連携要件評価 - 開始")
                    result = self.constraints_agent.evaluate_constraints(
                        state["system_requirements"],
                        state["deliverables_memory"]
                    )
                    end_time = time.time()
                    print(f"  🔒 制約・外部連携要件評価 - 完了 ({end_time - start_time:.2f}秒)")
                    return ("constraints", result)
                except Exception as e:
                    print(f"  🔒 制約・外部連携要件評価 - エラー: {str(e)}")
                    return ("constraints", {"success": False, "error": str(e)})
            
            # ThreadPoolExecutorで並列実行
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                print("⚡ 3エージェントをThreadPoolExecutorで並列実行中...")
                
                # 3つのタスクを並列実行
                futures = {
                    executor.submit(safe_run_business_evaluation): "business",
                    executor.submit(safe_run_quality_evaluation): "quality", 
                    executor.submit(safe_run_constraints_evaluation): "constraints"
                }
                
                # 結果を収集
                results = {}
                completed_count = 0
                
                for future in concurrent.futures.as_completed(futures):
                    completed_count += 1
                    agent_type_expected = futures[future]
                    try:
                        agent_type, result = future.result(timeout=120)  # 2分タイムアウト
                        results[agent_type] = result
                        print(f"✅ {agent_type}エージェント完了 ({completed_count}/3)")
                    except concurrent.futures.TimeoutError:
                        print(f"⏰ {agent_type_expected}エージェント - タイムアウト")
                        results[agent_type_expected] = {"success": False, "error": "タイムアウト"}
                    except Exception as e:
                        print(f"❌ {agent_type_expected}エージェント - 実行エラー: {str(e)}")
                        results[agent_type_expected] = {"success": False, "error": str(e)}
            
            parallel_end_time = time.time()
            print(f"⚡ 並列実行完了 - 総時間: {parallel_end_time - parallel_start_time:.2f}秒")
            
            # 結果を状態に反映
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
            
            # 成功状況の確認
            success_count = sum(1 for result in results.values() if result.get("success"))
            print(f"📊 評価成功率: {success_count}/3 エージェント")
            
            print("✅ 並列評価完了")
            return updated_state
            
        except Exception as e:
            print(f"❌ 並列評価システム全体エラー: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"並列評価システムエラー: {str(e)}"]
            return state
    
    def _execute_estimation_generation(self, state: EstimationState) -> EstimationState:
        """見積もり生成実行"""
        print("💰 見積もり生成開始")
        
        if not is_evaluation_complete(state):
            error_msg = "並列評価が完了していません"
            state["errors"] = state.get("errors", []) + [error_msg]
            return state
        
        # 評価結果を統合
        evaluation_feedback = {
            "business_evaluation": state.get("business_evaluation"),
            "quality_evaluation": state.get("quality_evaluation"),
            "constraints_evaluation": state.get("constraints_evaluation")
        }
        
        try:
            print("  🧮 見積もり計算中...")
            result = self.estimation_agent.generate_estimate(
                state["deliverables_memory"],
                state["system_requirements"],
                evaluation_feedback
            )
            
            state = log_agent_execution(state, "EstimationAgent", result)
            if result.get("success"):
                state = update_evaluation_result(state, "EstimationAgent", result)
            
            state["current_step"] = "estimation_complete"
            print("✅ 見積もり生成完了")
            return state
            
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"見積もり生成エラー: {str(e)}"]
            return state
    
    def _execute_user_interaction_loop(self, state: EstimationState) -> EstimationState:
        """ユーザー対話ループ実行"""
        print(f"👥 {t('workflow.user_interaction.title')}")
        
        max_iterations = 3
        iteration = 0
        
        while iteration < max_iterations:
            # 現在の結果を表示
            self._display_current_results(state)
            
            # ユーザー入力待機
            user_response = input(f"\n{t('workflow.user_interaction.approval_prompt')}").strip().lower()
            
            if user_response in ['y', 'yes', '承認']:
                state["user_approved"] = True
                state["current_step"] = "approved"
                print(f"✅ {t('workflow.user_interaction.approved')}")
                break
            elif user_response in ['n', 'no', '否認']:
                state["user_approved"] = False
                feedback = input(t('workflow.user_interaction.feedback_prompt'))
                state["user_feedback"] = feedback
                state["current_step"] = "needs_refinement"
            else:
                state["user_approved"] = False
                state["user_feedback"] = user_response
                state["current_step"] = "needs_refinement"
            
            # 改善実行
            if not state.get("user_approved"):
                state = self._execute_refinement(state)
                iteration += 1
            
        if not state.get("user_approved"):
            print(f"⚠️ {t('workflow.user_interaction.max_iterations')}")
        
        return state
    
    def _execute_refinement(self, state: EstimationState) -> EstimationState:
        """改善実行（修正要求強化版）"""
        print(f"🔄 {t('workflow.refinement.title')}")
        
        try:
            # 履歴に現在の状態を保存
            state = save_iteration_to_history(state, state.get("user_feedback", ""))
            
            # 現在の見積もりと前回の見積もりを取得
            current_estimate = state.get("estimation_result", {})
            previous_estimate = None
            
            # 履歴から前回の見積もりを取得
            history = state.get("iteration_history", [])
            if len(history) >= 2:
                previous_estimate = history[-2].get("estimation_result")
            
            feedback = state.get("user_feedback", "")
            
            # 評価結果の統合（修正要求を反映した最新版）
            evaluation_feedback = {
                "business_evaluation": state.get("business_evaluation"),
                "quality_evaluation": state.get("quality_evaluation"),
                "constraints_evaluation": state.get("constraints_evaluation")
            }
            
            print("  🧮 修正要求を反映した見積もり再計算中...")
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
            
            # 修正要求による変更を検証
            self._verify_modification_applied(state, feedback)
            
            print(f"✅ {t('workflow.refinement.completed')}")
            return state
            
        except Exception as e:
            state["errors"] = state.get("errors", []) + [f"改善実行エラー: {str(e)}"]
            return state
    
    def _verify_modification_applied(self, state: EstimationState, feedback: str):
        """修正要求が適用されたかを検証"""
        if not feedback:
            return
        
        current_est = state.get("estimation_result", {})
        if not current_est.get("success"):
            return
        
        est_result = current_est.get("estimation_result", {})
        tech_assumptions = est_result.get("technical_assumptions", {})
        
        # 簡単な検証（例：レスポンス時間要件）
        if "レスポンス" in feedback and "5秒" in feedback:
            if "レスポンス" not in str(tech_assumptions) and "パフォーマンス" not in str(tech_assumptions):
                print("⚠️ 警告: レスポンス時間要件が技術前提条件に反映されていない可能性があります")
        
        # ライブラリ・プラットフォーム要件の検証
        if "ライブラリ" in feedback or "プラットフォーム" in feedback:
            dev_stack = tech_assumptions.get("development_stack", "")
            if len(dev_stack.split(",")) <= 2:  # 具体的なライブラリが少ない
                print("⚠️ 警告: ライブラリ・プラットフォーム要件が十分に具体化されていない可能性があります")
    
    def _display_current_results(self, state: EstimationState):
        """現在の結果表示 - 詳細版"""
        print("\n" + "="*80)
        print("📋 見積もり結果詳細レポート")
        print("="*80)
        
        # 1. 評価サマリー
        summary = get_evaluation_summary(state)
        print(f"📊 評価完了状況:")
        print(f"  業務・機能要件: {'✅' if summary['business_complete'] else '❌'}")
        print(f"  品質・非機能要件: {'✅' if summary['quality_complete'] else '❌'}")
        print(f"  制約・外部連携: {'✅' if summary['constraints_complete'] else '❌'}")
        print(f"  見積もり生成: {'✅' if summary['estimation_complete'] else '❌'}")
        
        # 2. 各エージェント評価結果詳細
        self._display_agent_evaluations(state)
        
        # 3. 見積もり結果
        if state.get("estimation_result") and state["estimation_result"].get("success"):
            est_result = state["estimation_result"]["estimation_result"]
            print(f"\n💰 見積もり結果:")
            print(f"  総工数: {est_result['financial_summary']['total_effort_days']}人日")
            print(f"  総額: ¥{est_result['financial_summary']['total_jpy']:,}")
            print(f"  信頼度: {est_result['overall_confidence']}")
            
            # 4. 全成果物別詳細（省略なし）
            self._display_all_deliverable_estimates(est_result)
            
            # 5. 主要リスクと推奨事項
            self._display_risks_and_recommendations(est_result, state)
        
        # 6. エラー・警告
        if state.get("errors"):
            print(f"\n❌ エラー数: {len(state['errors'])}")
            for error in state["errors"][-3:]:  # 最新の3件のみ表示
                print(f"  - {error}")
        
        if state.get("warnings"):
            print(f"⚠️ 警告数: {len(state['warnings'])}")
    
    def _display_agent_evaluations(self, state: EstimationState):
        """各エージェントの評価結果詳細表示"""
        print(f"\n🤖 各エージェント評価結果詳細")
        print("-" * 60)
        
        # 業務・機能要件エージェント評価
        if state.get("business_evaluation"):
            business_eval = state["business_evaluation"]
            if business_eval.get("success"):
                print(f"📋 業務・機能要件エージェント評価:")
                if isinstance(business_eval, dict) and "overall_score" in business_eval:
                    print(f"  総合スコア: {business_eval.get('overall_score', 'N/A')}/100")
                    print(f"  業務目的明確性: {business_eval.get('business_purpose', {}).get('clarity_score', 'N/A')}/100")
                    print(f"  機能要件完全性: {business_eval.get('functional_requirements', {}).get('completeness_score', 'N/A')}/100")
                    print(f"  主要リスク: {', '.join(business_eval.get('risk_factors', [])[:3])}")
                else:
                    print(f"  評価データ: {str(business_eval)[:200]}...")
            else:
                print(f"📋 業務・機能要件エージェント: エラー - {business_eval.get('error', '不明')}")
        
        # 品質・非機能要件エージェント評価
        if state.get("quality_evaluation"):
            quality_eval = state["quality_evaluation"]
            if quality_eval.get("success"):
                print(f"\n🎯 品質・非機能要件エージェント評価:")
                if isinstance(quality_eval, dict) and "overall_score" in quality_eval:
                    print(f"  総合スコア: {quality_eval.get('overall_score', 'N/A')}/100")
                    print(f"  パフォーマンス要件: {quality_eval.get('performance_requirements', {}).get('definition_score', 'N/A')}/100")
                    print(f"  セキュリティ要件: {quality_eval.get('security_requirements', {}).get('completeness_score', 'N/A')}/100")
                    print(f"  工数影響度: +{quality_eval.get('total_effort_impact', 'N/A')}%")
                else:
                    print(f"  評価データ: {str(quality_eval)[:200]}...")
            else:
                print(f"🎯 品質・非機能要件エージェント: エラー - {quality_eval.get('error', '不明')}")
        
        # 制約・外部連携要件エージェント評価
        if state.get("constraints_evaluation"):
            constraints_eval = state["constraints_evaluation"]
            if constraints_eval.get("success"):
                print(f"\n🔒 制約・外部連携要件エージェント評価:")
                if isinstance(constraints_eval, dict) and "overall_score" in constraints_eval:
                    print(f"  総合スコア: {constraints_eval.get('overall_score', 'N/A')}/100")
                    print(f"  技術制約明確性: {constraints_eval.get('technical_constraints', {}).get('clarity_score', 'N/A')}/100")
                    print(f"  外部連携仕様: {constraints_eval.get('external_integrations', {}).get('specification_score', 'N/A')}/100")
                    print(f"  実現可能性リスク: {', '.join(constraints_eval.get('feasibility_risks', [])[:3])}")
                else:
                    print(f"  評価データ: {str(constraints_eval)[:200]}...")
            else:
                print(f"🔒 制約・外部連携要件エージェント: エラー - {constraints_eval.get('error', '不明')}")
    
    def _display_all_deliverable_estimates(self, est_result: Dict[str, Any]):
        """全成果物別見積もり表示（省略なし）"""
        print(f"\n📋 全成果物別見積もり詳細:")
        print("-" * 80)
        print(f"{'No.':<4} {'成果物名':<25} {'基礎工数':<8} {'最終工数':<8} {'金額':<12} {'信頼度':<6}")
        print("-" * 80)
        
        deliverable_estimates = est_result.get('deliverable_estimates', [])
        for i, item in enumerate(deliverable_estimates, 1):
            name = item.get('name', 'N/A')[:23]  # 文字数制限
            base_effort = item.get('base_effort_days', 0)
            final_effort = item.get('final_effort_days', 0)
            cost = item.get('cost_jpy', 0)
            confidence = item.get('confidence_score', 0)
            
            print(f"{i:<4} {name:<25} {base_effort:<8.1f} {final_effort:<8.1f} ¥{cost:<11,} {confidence:<6.2f}")
        
        print("-" * 80)
        financial_summary = est_result.get('financial_summary', {})
        print(f"{'合計':<4} {'':<25} {'':<8} {financial_summary.get('total_effort_days', 0):<8.1f} ¥{financial_summary.get('total_jpy', 0):<11,}")
    
    def _display_risks_and_recommendations(self, est_result: Dict[str, Any], state: EstimationState = None):
        """主要リスクと推奨事項表示"""
        print(f"\n⚠️ 主要リスク要因:")
        key_risks = est_result.get('key_risks', [])
        for i, risk in enumerate(key_risks, 1):
            print(f"  {i}. {risk}")
        
        print(f"\n💡 推奨事項:")
        recommendations = est_result.get('recommendations', [])
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        print(f"\n🔧 技術前提条件:")
        tech_assumptions = est_result.get('technical_assumptions', {})
        print(f"  エンジニアレベル: {tech_assumptions.get('engineer_level', 'N/A')}")
        print(f"  人日単価: ¥{tech_assumptions.get('daily_rate_jpy', 'N/A'):,}")
        print(f"  開発スタック: {tech_assumptions.get('development_stack', 'N/A')}")
        print(f"  チーム規模: {tech_assumptions.get('team_size', 'N/A')}人")
        print(f"  想定期間: {tech_assumptions.get('project_duration_months', 'N/A')}ヶ月")
        
        # 履歴表示を追加（stateがある場合のみ）
        if state is not None:
            self._display_iteration_history(state)
    
    def _display_iteration_history(self, state: EstimationState):
        """反復履歴の表示"""
        history = state.get("iteration_history", [])
        
        if len(history) <= 1:
            return  # 履歴が少ない場合は表示しない
        
        print(f"\n📊 見積もり前提条件履歴:")
        print("-" * 80)
        
        for i, entry in enumerate(history, 1):
            iteration_num = entry.get("iteration_number", i)
            feedback = entry.get("user_feedback", "")
            tech_assumptions = entry.get("technical_assumptions", {})
            changes = entry.get("changes_summary", [])
            
            print(f"\n【見積もり反復 {iteration_num}】")
            if feedback:
                print(f"  ユーザー要求: {feedback}")
            
            if tech_assumptions:
                print(f"  技術前提条件:")
                print(f"    - 開発スタック: {tech_assumptions.get('development_stack', 'N/A')}")
                print(f"    - 人日単価: ¥{tech_assumptions.get('daily_rate_jpy', 'N/A'):,}")
                
                # パフォーマンス要件など特別な要件があれば表示
                special_requirements = []
                dev_stack = tech_assumptions.get('development_stack', '')
                if 'Redis' in dev_stack or 'キャッシュ' in dev_stack:
                    special_requirements.append("キャッシュ実装")
                if 'Nginx' in dev_stack or 'CDN' in dev_stack:
                    special_requirements.append("CDN・ロードバランサ")
                if 'レスポンス' in str(tech_assumptions) or 'パフォーマンス' in str(tech_assumptions):
                    special_requirements.append("パフォーマンス最適化")
                
                if special_requirements:
                    print(f"    - 特別要件: {', '.join(special_requirements)}")
            
            if changes:
                print(f"  変更内容: {', '.join(changes)}")
        
        # 総変更サマリー
        if len(history) >= 2:
            first_est = history[0].get("estimation_result", {}).get("estimation_result", {}).get("financial_summary", {})
            last_est = history[-1].get("estimation_result", {}).get("estimation_result", {}).get("financial_summary", {})
            
            if first_est and last_est:
                first_total = first_est.get("total_effort_days", 0)
                last_total = last_est.get("total_effort_days", 0)
                first_cost = first_est.get("total_jpy", 0)
                last_cost = last_est.get("total_jpy", 0)
                
                print(f"\n📈 修正要求による累積変更:")
                print(f"  工数変化: {first_total:.1f}人日 → {last_total:.1f}人日 ({last_total-first_total:+.1f}人日)")
                print(f"  金額変化: ¥{first_cost:,} → ¥{last_cost:,} (¥{last_cost-first_cost:+,})")
                
                if first_total > 0:
                    effort_change_pct = ((last_total - first_total) / first_total) * 100
                    print(f"  変更率: {effort_change_pct:+.1f}%")