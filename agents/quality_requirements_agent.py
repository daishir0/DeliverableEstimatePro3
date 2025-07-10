"""
品質・非機能要件エージェント - How well評価
"""

from typing import Dict, Any, List
from .base_ai_agent import BaseAIAgent


class QualityRequirementsAgent(BaseAIAgent):
    """品質・非機能要件エージェント - How well視点での評価"""
    
    def __init__(self):
        system_prompt = """
あなたは経験豊富な品質・非機能要件分析スペシャリストです。
システム開発プロジェクトの品質・非機能要件を「How well（どの程度の品質で作るか）」の視点で評価するのが主な役割です。

【責務】
1. 性能要件の妥当性評価
2. セキュリティ要件の完全性評価
3. 可用性・拡張性の評価
4. 運用性・保守性の評価

【評価観点】
- パフォーマンス要件（レスポンス時間・スループット・同時接続数）
- セキュリティレベル（認証・認可・暗号化・脆弱性対策）
- 可用性・信頼性（稼働率・障害復旧時間・データバックアップ）
- 拡張性・保守性（将来拡張・メンテナンス容易性）
- ユーザビリティ（操作性・アクセシビリティ・多言語対応）
- 運用監視（ログ・監視・アラート）

【評価基準】
- 高評価 (Score: 80-100): 具体的で測定可能な品質基準が設定されている
- 中評価 (Score: 50-79): 基本的な品質要件は含まれているが、詳細化が必要
- 低評価 (Score: 0-49): 品質要件が不明確で具体化が必要

【品質要件の工数影響度】
- パフォーマンス最適化: +20-40%の工数増
- 高度セキュリティ実装: +30-50%の工数増
- 高可用性設計: +25-45%の工数増
- 国際化対応: +15-30%の工数増
- アクセシビリティ対応: +10-25%の工数増

【質問生成の観点】
- 想定する同時アクセス数・ピーク時負荷
- レスポンス時間・処理性能の要件
- セキュリティレベル・コンプライアンス要件
- 可用性・稼働率の目標値
- 将来の拡張予定・成長見込み
- 運用体制・監視要件

必ず以下のJSON形式で回答してください：
{
  "success": true,
  "quality_evaluation": {
    "overall_score": 総合評価点数(0-100),
    "performance_requirements": {
      "definition_score": 定義スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "security_requirements": {
      "completeness_score": 完全性スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "availability_reliability": {
      "specification_score": 仕様スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "scalability_maintainability": {
      "consideration_score": 考慮スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "usability": {
      "requirement_score": 要件スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "operational_monitoring": {
      "planning_score": 計画スコア(0-100),
      "assessment": "評価コメント",
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "improvement_questions": [
      {
        "category": "質問カテゴリ",
        "question": "具体的な質問",
        "purpose": "質問の目的",
        "impact_on_estimation": "見積もりへの影響"
      }
    ],
    "total_effort_impact": 総工数影響度,
    "risk_factors": ["品質面のリスク要因"],
    "recommendations": ["品質向上推奨事項"]
  }
}
"""
        super().__init__("QualityRequirementsAgent", system_prompt)
    
    def evaluate_quality_requirements(self, project_requirements: str, 
                                    deliverables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """品質・非機能要件の評価"""
        
        deliverables_context = ""
        if deliverables:
            deliverables_context = "\n【成果物リスト】\n" + "\n".join([
                f"- {d.get('name', '')}: {d.get('description', '')}" 
                for d in deliverables
            ])
        
        user_input = f"""
【プロジェクト要件】
{project_requirements}
{deliverables_context}

上記のプロジェクト要件を、品質・非機能要件の観点から「How well（どの程度の品質で作るか）」の視点で評価してください。

評価すべき項目：
1. パフォーマンス要件は具体的に定義されているか？
2. セキュリティ要件は必要十分に設定されているか？
3. 可用性・信頼性の目標は明確か？
4. 拡張性・保守性は考慮されているか？
5. ユーザビリティ要件は適切に設定されているか？
6. 運用監視の計画は含まれているか？

また、各品質要件が見積もり工数に与える影響度を評価し、見積もり精度向上のために必要な品質面での質問を生成してください。
"""
        
        result = self.execute_with_ai(user_input)
        
        # レスポンス検証
        required_keys = ["quality_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("品質要件評価結果の形式が不正です")
        
        return result
    
    def analyze_performance_impact(self, performance_requirements: str, 
                                 current_architecture: str = None) -> Dict[str, Any]:
        """パフォーマンス要件の工数影響分析"""
        
        architecture_context = ""
        if current_architecture:
            architecture_context = f"\n【想定アーキテクチャ】\n{current_architecture}"
        
        user_input = f"""
【パフォーマンス要件】
{performance_requirements}
{architecture_context}

上記のパフォーマンス要件を分析し、実装工数への影響度を詳細に評価してください。
特に以下の観点で分析してください：

1. データベース最適化の必要性
2. キャッシュ戦略の実装要否
3. 負荷分散・スケーリング設計
4. パフォーマンステストの範囲
5. 監視・計測システムの構築
"""
        
        result = self.execute_with_ai(user_input)
        
        # レスポンス検証
        required_keys = ["quality_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("パフォーマンス影響分析結果の形式が不正です")
        
        return result