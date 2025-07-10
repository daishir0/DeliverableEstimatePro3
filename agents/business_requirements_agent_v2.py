"""
業務・機能要件エージェント - 修正要求対応版
"""

from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import BusinessEvaluationResult


class BusinessRequirementsAgentV2(PydanticAIAgent):
    """業務・機能要件エージェント - 修正要求反映強化版"""
    
    def __init__(self):
        system_prompt = """
あなたは経験豊富なビジネス要件分析スペシャリストです。
システム開発プロジェクトの業務・機能要件を「What（何を作るか）」と「Why（なぜ作るか）」の視点で評価するのが主な役割です。

【重要】修正要求がある場合は、前回評価結果を参考にしつつ、ユーザーの修正要求を必ず反映した新しい評価を行ってください。

【責務】
1. 業務要件の明確性評価
2. 機能要件の完全性評価
3. ビジネス価値の妥当性評価
4. 見積精度向上のための業務面質問生成
5. 修正要求による要件変更の影響評価

【評価観点】
- 業務目的の明確性（目標・KPI設定）
- 機能要件の具体性（機能仕様の詳細度）
- ユーザーストーリーの完全性（ユーザー視点の網羅性）
- ビジネス価値の定量化（ROI・効果測定）
- ステークホルダーの特定（関係者・承認フロー）
- 業務フローの明確性（現状業務・新業務の整理）

【修正要求への対応】
- ユーザーからの修正要求は必ず評価に反映する
- 前回評価との変更点を明確にする
- 修正による業務面への影響を評価する
- 新たに発生するリスクや推奨事項を特定する

【評価基準】
- 高評価 (Score: 80-100): 明確で具体的、ビジネス価値が定量化されている
- 中評価 (Score: 50-79): 基本的な内容は含まれているが、詳細化が必要
- 低評価 (Score: 0-49): 不明確で抽象的、具体化が必要

結果は指定されたPydanticモデル形式で返してください。
修正要求がある場合は、必ず評価スコアや内容を更新してください。
"""
        super().__init__("BusinessRequirementsAgentV2", system_prompt)
    
    def evaluate_business_requirements(self, project_requirements: str,
                                      deliverables: List[Dict[str, Any]] = None,
                                      previous_evaluation: Dict[str, Any] = None,
                                      user_feedback: str = "") -> Dict[str, Any]:
        """業務・機能要件の評価（修正要求対応）"""
        
        # deliverables が None または空の場合のエラーハンドリング
        if deliverables is None:
            deliverables = []
            
        deliverables_context = ""
        if deliverables:
            deliverables_context = "\n【成果物リスト】\n" + "\n".join([
                f"- {d.get('name', '')}: {d.get('description', '')}"
                for d in deliverables
            ])
        
        # 前回評価の文脈を追加
        previous_context = ""
        if previous_evaluation:
            # 辞書型の場合は文字列に変換
            if isinstance(previous_evaluation, dict):
                import json
                previous_context = f"\n【前回評価結果】\n{json.dumps(previous_evaluation, ensure_ascii=False, indent=2)}"
            else:
                previous_context = f"\n【前回評価結果】\n{previous_evaluation}"
        
        # 修正要求の文脈を追加
        feedback_context = ""
        if user_feedback:
            feedback_context = f"\n【ユーザー修正要求】\n{user_feedback}\n⚠️ この修正要求を必ず反映して評価を更新してください。"
        
        user_input = f"""
【プロジェクト要件】
{project_requirements}
{deliverables_context}
{previous_context}
{feedback_context}

上記のプロジェクト要件を、業務・機能要件の観点から「What（何を作るか）」と「Why（なぜ作るか）」の視点で評価してください。

評価すべき項目：
1. 業務目的は明確に定義されているか？
2. 機能要件は具体的で実装可能な形で記述されているか？
3. ユーザーストーリーは網羅的に定義されているか？
4. ビジネス価値は定量的に測定可能か？
5. ステークホルダーは明確に特定されているか？
6. 業務フローは現状・新業務ともに整理されているか？

【重要】修正要求がある場合は：
- 修正要求による業務・機能要件への影響を評価
- 前回評価からの変更点を明確化
- 新たなリスクや推奨事項を特定
- 評価スコアを適切に更新

また、見積もり精度向上のために必要な業務面での質問を生成してください。
"""
        
        # Pydantic構造化出力を使用
        additional_context = {
            "previous_evaluation": previous_evaluation if previous_evaluation is not None else {},
            "user_feedback": user_feedback,
            "has_modification_request": bool(user_feedback)
        }
        
        try:
            result = self.execute_with_pydantic(user_input, BusinessEvaluationResult, additional_context)
            
            # resultがNoneの場合のエラーハンドリング
            if result is None:
                return self._create_error_response("Pydantic実行結果がNoneです")
            
            # 成功時の結果をラップ
            if result.get("success"):
                # business_evaluationキーでラップ
                business_evaluation = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
                
                return {
                    "success": True,
                    "business_evaluation": business_evaluation,
                    "_agent_metadata": result.get("_agent_metadata", {})
                }
            
            return result
        except Exception as e:
            import traceback
            error_msg = f"業務要件評価中にエラーが発生しました: {str(e)}\n{traceback.format_exc()}"
            print(f"[{self.agent_name}] エラー: {error_msg}")
            return self._create_error_response(error_msg)
    
    def generate_clarification_questions(self, current_requirements: str,
                                        focus_areas: List[str] = None,
                                        user_feedback: str = "") -> Dict[str, Any]:
        """業務要件明確化のための質問生成（修正要求対応）"""
        
        # focus_areas が None の場合のエラーハンドリング
        if focus_areas is None:
            focus_areas = []
            
        focus_context = ""
        if focus_areas:
            focus_context = f"\n【重点確認エリア】\n" + "\n".join([f"- {area}" for area in focus_areas])
        
        feedback_context = ""
        if user_feedback:
            feedback_context = f"\n【ユーザー修正要求】\n{user_feedback}\n⚠️ この修正要求に関連する質問を重点的に生成してください。"
        
        user_input = f"""
【現在の要件】
{current_requirements}
{focus_context}
{feedback_context}

上記の要件に対して、業務・機能面での明確化を進めるための質問を生成してください。
特に見積もり精度に直接影響する要素について重点的に質問を作成してください。

修正要求がある場合は、その要求に関連する追加質問も含めてください。
"""
        
        additional_context = {
            "user_feedback": user_feedback,
            "focus_areas": focus_areas if focus_areas is not None else []
        }
        
        try:
            result = self.execute_with_pydantic(user_input, BusinessEvaluationResult, additional_context)
            
            # resultがNoneの場合のエラーハンドリング
            if result is None:
                return self._create_error_response("Pydantic実行結果がNoneです")
            
            # 成功時の結果をラップ
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
            error_msg = f"質問生成中にエラーが発生しました: {str(e)}\n{traceback.format_exc()}"
            print(f"[{self.agent_name}] エラー: {error_msg}")
            return self._create_error_response(error_msg)