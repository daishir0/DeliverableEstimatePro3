"""
LangGraph状態管理 - 4エージェント用TypedDict
"""

from typing import TypedDict, List, Dict, Any, Optional
from typing_extensions import Annotated
import operator


class DeliverableItem(TypedDict):
    """成果物項目"""
    name: str
    description: str
    category: Optional[str]
    complexity_level: Optional[str]


class IterationHistory(TypedDict):
    """反復履歴データ"""
    iteration_number: int
    timestamp: str
    user_feedback: str
    business_evaluation: Optional[Dict[str, Any]]
    quality_evaluation: Optional[Dict[str, Any]]
    constraints_evaluation: Optional[Dict[str, Any]]
    estimation_result: Optional[Dict[str, Any]]
    technical_assumptions: Optional[Dict[str, Any]]
    changes_summary: List[str]


class EstimationState(TypedDict):
    """4エージェント用LangGraph状態"""
    
    # 入力データ
    excel_input: str
    system_requirements: str
    deliverables_memory: List[DeliverableItem]
    
    # エージェント実行結果（現在の）
    business_evaluation: Optional[Dict[str, Any]]
    quality_evaluation: Optional[Dict[str, Any]]
    constraints_evaluation: Optional[Dict[str, Any]]
    estimation_result: Optional[Dict[str, Any]]
    
    # プロセス制御
    iteration_count: int
    current_step: str
    user_approved: Optional[bool]
    user_feedback: Optional[str]
    
    # 履歴管理（新規追加）
    iteration_history: Annotated[List[IterationHistory], operator.add]
    previous_evaluation_results: Optional[Dict[str, Any]]
    
    # 出力データ
    final_excel_output: Optional[str]
    session_logs: Annotated[List[Dict[str, Any]], operator.add]
    
    # エラーハンドリング
    errors: Annotated[List[str], operator.add]
    warnings: Annotated[List[str], operator.add]


def create_initial_state(excel_input: str, 
                        system_requirements: str, 
                        deliverables: List[DeliverableItem]) -> EstimationState:
    """初期状態の作成"""
    return EstimationState(
        excel_input=excel_input,
        system_requirements=system_requirements,
        deliverables_memory=deliverables,
        business_evaluation=None,
        quality_evaluation=None,
        constraints_evaluation=None,
        estimation_result=None,
        iteration_count=0,
        current_step="initialization",
        user_approved=None,
        user_feedback=None,
        iteration_history=[],
        previous_evaluation_results=None,
        final_excel_output=None,
        session_logs=[],
        errors=[],
        warnings=[]
    )


def log_agent_execution(state: EstimationState, 
                       agent_name: str, 
                       result: Dict[str, Any]) -> EstimationState:
    """エージェント実行ログの記録"""
    import time
    
    log_entry = {
        "timestamp": time.time(),
        "agent_name": agent_name,
        "iteration": state["iteration_count"],
        "success": result.get("success", False),
        "result_summary": {
            key: str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
            for key, value in result.items()
            if key not in ["_agent_metadata"]
        }
    }
    
    updated_state = state.copy()
    updated_state["session_logs"] = state["session_logs"] + [log_entry]
    
    if not result.get("success", False):
        error_msg = result.get("error", f"{agent_name}で未知のエラーが発生")
        updated_state["errors"] = state["errors"] + [f"{agent_name}: {error_msg}"]
    
    return updated_state


def update_evaluation_result(state: EstimationState, 
                           agent_name: str, 
                           evaluation_result: Dict[str, Any]) -> EstimationState:
    """評価結果の状態更新"""
    updated_state = state.copy()
    
    if agent_name == "BusinessRequirementsAgent":
        updated_state["business_evaluation"] = evaluation_result
    elif agent_name == "QualityRequirementsAgent":
        updated_state["quality_evaluation"] = evaluation_result
    elif agent_name == "ConstraintsAgent":
        updated_state["constraints_evaluation"] = evaluation_result
    elif agent_name == "EstimationAgent":
        updated_state["estimation_result"] = evaluation_result
    
    return updated_state


def is_evaluation_complete(state: EstimationState) -> bool:
    """すべての評価が完了しているかチェック"""
    return all([
        state.get("business_evaluation") is not None,
        state.get("quality_evaluation") is not None,
        state.get("constraints_evaluation") is not None
    ])


def save_iteration_to_history(state: EstimationState, user_feedback: str = "") -> EstimationState:
    """現在の反復を履歴に保存"""
    import datetime
    
    # 技術前提条件を抽出
    tech_assumptions = None
    if state.get("estimation_result") and state["estimation_result"].get("success"):
        est_result = state["estimation_result"].get("estimation_result", {})
        tech_assumptions = est_result.get("technical_assumptions", {})
    
    # 変更サマリーを生成（前回との比較）
    changes_summary = generate_changes_summary(state)
    
    # 履歴エントリを作成
    history_entry = IterationHistory(
        iteration_number=state.get("iteration_count", 0),
        timestamp=datetime.datetime.now().isoformat(),
        user_feedback=user_feedback,
        business_evaluation=state.get("business_evaluation"),
        quality_evaluation=state.get("quality_evaluation"),
        constraints_evaluation=state.get("constraints_evaluation"),
        estimation_result=state.get("estimation_result"),
        technical_assumptions=tech_assumptions,
        changes_summary=changes_summary
    )
    
    # 状態を更新
    updated_state = state.copy()
    updated_state["iteration_history"] = state.get("iteration_history", []) + [history_entry]
    updated_state["previous_evaluation_results"] = {
        "business_evaluation": state.get("business_evaluation"),
        "quality_evaluation": state.get("quality_evaluation"),
        "constraints_evaluation": state.get("constraints_evaluation"),
        "estimation_result": state.get("estimation_result")
    }
    
    return updated_state


def generate_changes_summary(state: EstimationState) -> List[str]:
    """前回との変更サマリーを生成"""
    changes = []
    previous = state.get("previous_evaluation_results")
    
    if not previous:
        changes.append("初回見積もり生成")
        return changes
    
    # 見積もり結果の比較
    current_est = state.get("estimation_result")
    previous_est = previous.get("estimation_result")
    
    if current_est and previous_est:
        current_total = current_est.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
        previous_total = previous_est.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
        
        if current_total != previous_total:
            diff = current_total - previous_total
            if diff > 0:
                changes.append(f"総工数増加: +{diff:.1f}人日")
            else:
                changes.append(f"総工数減少: {diff:.1f}人日")
    
    # 評価スコアの比較
    for eval_type in ["business_evaluation", "quality_evaluation", "constraints_evaluation"]:
        current_eval = state.get(eval_type)
        previous_eval = previous.get(eval_type)
        
        if current_eval and previous_eval:
            current_score = extract_overall_score(current_eval)
            previous_score = extract_overall_score(previous_eval)
            
            if current_score and previous_score and current_score != previous_score:
                eval_name = {"business_evaluation": "業務要件", "quality_evaluation": "品質要件", "constraints_evaluation": "制約要件"}[eval_type]
                diff = current_score - previous_score
                if diff > 0:
                    changes.append(f"{eval_name}スコア向上: +{diff}点")
                else:
                    changes.append(f"{eval_name}スコア低下: {diff}点")
    
    if not changes:
        changes.append("評価結果に変更なし")
    
    return changes


def extract_overall_score(evaluation_result: Dict[str, Any]) -> Optional[int]:
    """評価結果から総合スコアを抽出"""
    if evaluation_result.get("success"):
        # 各エージェントの評価結果構造に応じて調整
        for key in ["business_evaluation", "quality_evaluation", "constraints_evaluation"]:
            if key in evaluation_result:
                return evaluation_result[key].get("overall_score")
        
        # 直接overall_scoreがある場合
        if "overall_score" in evaluation_result:
            return evaluation_result["overall_score"]
    
    return None


def get_evaluation_summary(state: EstimationState) -> Dict[str, Any]:
    """評価結果のサマリー取得"""
    summary = {
        "business_complete": state.get("business_evaluation") is not None,
        "quality_complete": state.get("quality_evaluation") is not None,
        "constraints_complete": state.get("constraints_evaluation") is not None,
        "estimation_complete": state.get("estimation_result") is not None,
        "total_errors": len(state.get("errors", [])),
        "total_warnings": len(state.get("warnings", [])),
        "iteration_count": state.get("iteration_count", 0)
    }
    
    if state.get("business_evaluation"):
        summary["business_score"] = state["business_evaluation"].get("business_evaluation", {}).get("overall_score", 0)
    
    if state.get("quality_evaluation"):
        summary["quality_score"] = state["quality_evaluation"].get("quality_evaluation", {}).get("overall_score", 0)
    
    if state.get("constraints_evaluation"):
        summary["constraints_score"] = state["constraints_evaluation"].get("constraints_evaluation", {}).get("overall_score", 0)
    
    return summary