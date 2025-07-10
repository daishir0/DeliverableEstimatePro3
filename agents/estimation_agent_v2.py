"""
見積もりエージェント - PydanticOutputParser対応版
"""

from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import EstimationResult


class EstimationAgentV2(PydanticAIAgent):
    """見積もりエージェント - Pydantic構造化出力対応"""
    
    def __init__(self):
        system_prompt = """
あなたは経験豊富なシステム開発見積もりスペシャリストです。
成果物リストと要件情報から正確な見積もりを生成するのが主な役割です。

【責務】
1. 成果物の工数見積もり計算
2. 金額計算（人日単価×工数）
3. 技術前提条件の明確化
4. 見積もりの信頼度評価

【工数見積もり基準】
- 要件定義書: 2-8人日（複雑度により調整）
- システム設計書: 4-12人日（アーキテクチャ複雑度により調整）
- フロントエンド開発: 8-25人日（画面数・機能により調整）
- バックエンド開発: 10-30人日（API数・ビジネスロジック複雑度により調整）
- データベース設計・実装: 5-18人日（テーブル数・関連性により調整）
- テスト実装: 5-15人日（テスト範囲により調整）
- セキュリティ実装: 3-15人日（セキュリティレベルにより調整）
- デプロイ・運用設定: 2-10人日（インフラ複雑度により調整）

【複雑度調整係数】
- Low: 1.0倍
- Medium: 1.3倍  
- High: 1.8倍

【リスク調整係数】
- 新技術・未経験領域: +30%
- 外部システム依存: +20%
- パフォーマンス要件: +25%
- 高度セキュリティ: +30%
- 複数決済連携: +25%
- 大規模データ: +20%

【技術前提条件のデフォルト】
- エンジニアレベル: Python使用可能な平均的エンジニア
- 開発環境: 標準的な開発環境
- 人日単価: 50,000円（設定により変更可能）

各成果物について以下の計算を行ってください：
1. 基礎工数の算出
2. 複雑度による調整
3. リスクによる調整
4. 最終工数と金額の計算
5. 信頼度の評価

結果は指定されたPydanticモデル形式で返してください。
"""
        super().__init__("EstimationAgentV2", system_prompt)
    
    def generate_estimate(self, deliverables: List[Dict[str, Any]], 
                         project_requirements: str, 
                         evaluation_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        """見積もり生成のメインメソッド"""
        
        # 成果物リストを文字列に変換
        deliverables_str = "\n".join([
            f"- {d.get('name', '')}: {d.get('description', '')}" 
            for d in deliverables
        ])
        
        user_input = f"""
【成果物リスト】
{deliverables_str}

【プロジェクト要件】
{project_requirements}

【評価フィードバック】
業務・機能要件評価: {evaluation_feedback.get('business_evaluation', '未評価') if evaluation_feedback else '未評価'}
品質・非機能要件評価: {evaluation_feedback.get('quality_evaluation', '未評価') if evaluation_feedback else '未評価'}
制約・外部連携評価: {evaluation_feedback.get('constraints_evaluation', '未評価') if evaluation_feedback else '未評価'}

上記の情報を基に、各成果物の工数見積もりと金額計算を実行してください。
評価フィードバックの内容も考慮して、工数調整を行ってください。
"""
        
        # Pydantic構造化出力を使用
        result = self.execute_with_pydantic(user_input, EstimationResult, evaluation_feedback)
        
        # 成功時の結果をラップ
        if result.get("success"):
            # _agent_metadataを除外してestimation_resultキーでラップ
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
        """フィードバックに基づく見積もり改善（修正要求強化版）"""
        
        # 前回見積もりとの比較コンテキスト
        comparison_context = ""
        if previous_estimate:
            prev_total = previous_estimate.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
            curr_total = current_estimate.get("estimation_result", {}).get("financial_summary", {}).get("total_effort_days", 0)
            comparison_context = f"""
【前回見積もりとの比較】
前回総工数: {prev_total}人日
現在総工数: {curr_total}人日
差分: {curr_total - prev_total:+.1f}人日
"""
        
        user_input = f"""
【現在の見積もり】
{current_estimate}
{comparison_context}

【ユーザー修正要求】
{feedback}

【更新された評価結果】
{evaluation_updates if evaluation_updates else '更新なし'}

⚠️【重要】ユーザーの修正要求を必ず反映して見積もりを再計算してください。

修正要求による具体的な変更内容：
1. フィードバックで指摘された技術要件の追加・変更
2. パフォーマンス要件やライブラリ制約の具体化
3. それらによる工数・金額への影響を正確に計算
4. 技術前提条件の更新（ライブラリ、パフォーマンス要件等）
5. 新たなリスク要因の特定

【例：レスポンス時間5秒要件が追加された場合】
- パフォーマンス最適化工数を追加
- キャッシュ・CDN実装工数を追加  
- データベース最適化工数を追加
- ライブラリ選定（Redis、Nginx等）を技術前提条件に追加

見積もり結果は必ず前回から変更してください。同じ結果は受け付けません。
"""
        
        # 修正要求の解析情報を追加コンテキストに含める
        additional_context = {
            "user_feedback": feedback,
            "previous_estimate": previous_estimate,
            "evaluation_updates": evaluation_updates,
            "requires_recalculation": True
        }
        
        # Pydantic構造化出力を使用
        result = self.execute_with_pydantic(user_input, EstimationResult, additional_context)
        
        # 成功時の結果をラップ
        if result.get("success"):
            estimation_result = {k: v for k, v in result.items() if k not in ["success", "_agent_metadata"]}
            
            return {
                "success": True,
                "estimation_result": estimation_result,
                "_agent_metadata": result.get("_agent_metadata", {})
            }
        
        return result