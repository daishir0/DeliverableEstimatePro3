"""
制約・外部連携要件エージェント - Boundaries評価
"""

from typing import Dict, Any, List
from .base_ai_agent import BaseAIAgent


class ConstraintsAgent(BaseAIAgent):
    """制約・外部連携要件エージェント - Boundaries視点での評価"""
    
    def __init__(self):
        system_prompt = """
あなたは経験豊富なシステム制約・連携分析スペシャリストです。
システム開発プロジェクトの制約・外部連携要件を「Boundaries（境界・制約条件）」の視点で評価するのが主な役割です。

【責務】
1. 技術制約の特定・評価
2. 外部システム連携要件の分析
3. 法規制・コンプライアンス要件の確認
4. リソース・スケジュール制約の評価

【評価観点】
- 技術制約（使用技術・プラットフォーム・ライブラリ制限）
- 外部システム連携（API・データベース・認証システム・決済系）
- 法規制・コンプライアンス（個人情報保護・業界規制・標準規格）
- インフラ制約（クラウド・オンプレミス・ネットワーク・セキュリティ）
- リソース制約（予算・人員・スケジュール・環境）
- 運用制約（サポート体制・メンテナンス窓口・SLA）

【評価基準】
- 高評価 (Score: 80-100): 制約が明確で実現可能性が検証されている
- 中評価 (Score: 50-79): 主要な制約は特定されているが、詳細確認が必要
- 低評価 (Score: 0-49): 制約が不明確で実現リスクが高い

【制約の工数影響度】
- 外部API連携: +15-30%の工数増
- レガシーシステム連携: +25-50%の工数増
- 高度セキュリティ要件: +20-40%の工数増
- 特殊コンプライアンス対応: +30-60%の工数増
- 複雑なインフラ要件: +20-35%の工数増
- 厳格なスケジュール制約: +10-25%の工数増

【質問生成の観点】
- 連携する外部システムの詳細仕様
- 使用必須・禁止技術の明確化
- 法規制・コンプライアンス要件の具体化
- インフラ・環境制約の詳細
- 予算・スケジュール・人員制約
- 運用・サポート体制の要件

必ず以下のJSON形式で回答してください：
{
  "success": true,
  "constraints_evaluation": {
    "overall_score": 総合評価点数(0-100),
    "technical_constraints": {
      "clarity_score": 明確性スコア(0-100),
      "assessment": "評価コメント",
      "identified_constraints": ["特定された制約"],
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "external_integrations": {
      "specification_score": 仕様スコア(0-100),
      "assessment": "評価コメント",
      "identified_integrations": ["特定された連携"],
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "compliance_regulations": {
      "coverage_score": 網羅性スコア(0-100),
      "assessment": "評価コメント",
      "identified_requirements": ["特定された要件"],
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "infrastructure_constraints": {
      "definition_score": 定義スコア(0-100),
      "assessment": "評価コメント",
      "identified_constraints": ["特定された制約"],
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "resource_constraints": {
      "realism_score": 現実性スコア(0-100),
      "assessment": "評価コメント",
      "identified_constraints": ["特定された制約"],
      "missing_elements": ["不足している要素"],
      "effort_impact_percentage": 工数影響度
    },
    "operational_constraints": {
      "planning_score": 計画スコア(0-100),
      "assessment": "評価コメント",
      "identified_constraints": ["特定された制約"],
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
    "feasibility_risks": ["実現可能性リスク"],
    "mitigation_strategies": ["リスク緩和策"],
    "recommendations": ["制約対応推奨事項"]
  }
}
"""
        super().__init__("ConstraintsAgent", system_prompt)
    
    def evaluate_constraints(self, project_requirements: str, 
                           deliverables: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """制約・外部連携要件の評価"""
        
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

上記のプロジェクト要件を、制約・外部連携要件の観点から「Boundaries（境界・制約条件）」の視点で評価してください。

評価すべき項目：
1. 技術制約は明確に特定されているか？
2. 外部システム連携の仕様は具体的か？
3. 法規制・コンプライアンス要件は網羅されているか？
4. インフラ制約は適切に定義されているか？
5. リソース制約（予算・人員・スケジュール）は現実的か？
6. 運用制約は計画に含まれているか？

また、各制約が見積もり工数に与える影響度を評価し、見積もり精度向上のために必要な制約面での質問を生成してください。
"""
        
        result = self.execute_with_ai(user_input)
        
        # レスポンス検証
        required_keys = ["constraints_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("制約評価結果の形式が不正です")
        
        return result
    
    def analyze_integration_complexity(self, integration_requirements: str, 
                                     target_systems: List[str] = None) -> Dict[str, Any]:
        """外部連携の複雑度分析"""
        
        systems_context = ""
        if target_systems:
            systems_context = f"\n【対象システム】\n" + "\n".join([f"- {sys}" for sys in target_systems])
        
        user_input = f"""
【連携要件】
{integration_requirements}
{systems_context}

上記の外部連携要件を分析し、実装工数への影響度を詳細に評価してください。
特に以下の観点で分析してください：

1. API連携の複雑度とデータ形式変換
2. 認証・認可方式の実装工数
3. データ同期・整合性確保の要件
4. エラーハンドリング・リトライ機構
5. 連携テスト・結合テストの範囲
6. 運用監視・障害対応の仕組み
"""
        
        result = self.execute_with_ai(user_input)
        
        # レスポンス検証
        required_keys = ["constraints_evaluation"]
        if not self.validate_response(result, required_keys):
            return self._create_error_response("連携複雑度分析結果の形式が不正です")
        
        return result