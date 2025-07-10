"""
Pydanticモデル定義 - 構造化出力用
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class DeliverableEstimate(BaseModel):
    """成果物見積もり"""
    name: str = Field(description="成果物名")
    description: str = Field(description="成果物説明")
    base_effort_days: float = Field(description="基礎工数（人日）")
    complexity_multiplier: float = Field(description="複雑度係数")
    risk_multiplier: float = Field(description="リスク係数")
    final_effort_days: float = Field(description="最終工数（人日）")
    cost_jpy: int = Field(description="金額（円）")
    confidence_score: float = Field(description="信頼度（0-1）")
    rationale: str = Field(description="見積根拠")


class FinancialSummary(BaseModel):
    """財務サマリー"""
    total_effort_days: float = Field(description="総工数（人日）")
    subtotal_jpy: int = Field(description="小計（円）")
    tax_jpy: int = Field(description="消費税（円）")
    total_jpy: int = Field(description="総額（円）")


class TechnicalAssumptions(BaseModel):
    """技術前提条件"""
    engineer_level: str = Field(description="エンジニアレベル")
    daily_rate_jpy: int = Field(description="人日単価（円）")
    development_stack: str = Field(description="想定技術スタック")
    team_size: int = Field(description="想定チームサイズ")
    project_duration_months: int = Field(description="想定期間（月）")


class EstimationResult(BaseModel):
    """見積もり結果"""
    deliverable_estimates: List[DeliverableEstimate] = Field(description="成果物別見積もりリスト")
    financial_summary: FinancialSummary = Field(description="財務サマリー")
    technical_assumptions: TechnicalAssumptions = Field(description="技術前提条件")
    overall_confidence: float = Field(description="全体信頼度（0-1）")
    key_risks: List[str] = Field(description="主要リスク要因")
    recommendations: List[str] = Field(description="推奨事項")


class BusinessEvaluationDetail(BaseModel):
    """業務評価詳細"""
    clarity_score: int = Field(description="明確性スコア（0-100）")
    assessment: str = Field(description="評価コメント")
    missing_elements: List[str] = Field(description="不足している要素")


class ImprovementQuestion(BaseModel):
    """改善のための質問"""
    category: str = Field(description="質問カテゴリ")
    question: str = Field(description="具体的な質問")
    purpose: str = Field(description="質問の目的")
    impact_on_estimation: str = Field(description="見積もりへの影響")


class BusinessEvaluationResult(BaseModel):
    """業務・機能要件評価結果"""
    overall_score: int = Field(description="総合評価点数（0-100）")
    business_purpose: BusinessEvaluationDetail = Field(description="業務目的の評価")
    functional_requirements: BusinessEvaluationDetail = Field(description="機能要件の評価")
    user_stories: BusinessEvaluationDetail = Field(description="ユーザーストーリーの評価")
    business_value: BusinessEvaluationDetail = Field(description="ビジネス価値の評価")
    stakeholders: BusinessEvaluationDetail = Field(description="ステークホルダーの評価")
    business_flow: BusinessEvaluationDetail = Field(description="業務フローの評価")
    improvement_questions: List[ImprovementQuestion] = Field(description="改善のための質問リスト")
    risk_factors: List[str] = Field(description="業務面のリスク要因")
    recommendations: List[str] = Field(description="改善推奨事項")


class QualityEvaluationDetail(BaseModel):
    """品質評価詳細"""
    definition_score: int = Field(description="定義スコア（0-100）")
    assessment: str = Field(description="評価コメント")
    missing_elements: List[str] = Field(description="不足している要素")
    effort_impact_percentage: float = Field(description="工数影響度（%）")


class QualityEvaluationResult(BaseModel):
    """品質・非機能要件評価結果"""
    overall_score: int = Field(description="総合評価点数（0-100）")
    performance_requirements: QualityEvaluationDetail = Field(description="パフォーマンス要件の評価")
    security_requirements: QualityEvaluationDetail = Field(description="セキュリティ要件の評価")
    availability_reliability: QualityEvaluationDetail = Field(description="可用性・信頼性の評価")
    scalability_maintainability: QualityEvaluationDetail = Field(description="拡張性・保守性の評価")
    usability: QualityEvaluationDetail = Field(description="ユーザビリティの評価")
    operational_monitoring: QualityEvaluationDetail = Field(description="運用監視の評価")
    improvement_questions: List[ImprovementQuestion] = Field(description="改善のための質問リスト")
    total_effort_impact: float = Field(description="総工数影響度（%）")
    risk_factors: List[str] = Field(description="品質面のリスク要因")
    recommendations: List[str] = Field(description="品質向上推奨事項")


class ConstraintsEvaluationDetail(BaseModel):
    """制約評価詳細"""
    clarity_score: int = Field(description="明確性スコア（0-100）")
    assessment: str = Field(description="評価コメント")
    identified_constraints: List[str] = Field(description="特定された制約")
    missing_elements: List[str] = Field(description="不足している要素")
    effort_impact_percentage: float = Field(description="工数影響度（%）")


class ConstraintsEvaluationResult(BaseModel):
    """制約・外部連携要件評価結果"""
    overall_score: int = Field(description="総合評価点数（0-100）")
    technical_constraints: ConstraintsEvaluationDetail = Field(description="技術制約の評価")
    external_integrations: ConstraintsEvaluationDetail = Field(description="外部連携の評価")
    compliance_regulations: ConstraintsEvaluationDetail = Field(description="法規制・コンプライアンスの評価")
    infrastructure_constraints: ConstraintsEvaluationDetail = Field(description="インフラ制約の評価")
    resource_constraints: ConstraintsEvaluationDetail = Field(description="リソース制約の評価")
    operational_constraints: ConstraintsEvaluationDetail = Field(description="運用制約の評価")
    improvement_questions: List[ImprovementQuestion] = Field(description="改善のための質問リスト")
    total_effort_impact: float = Field(description="総工数影響度（%）")
    feasibility_risks: List[str] = Field(description="実現可能性リスク")
    mitigation_strategies: List[str] = Field(description="リスク緩和策")
    recommendations: List[str] = Field(description="制約対応推奨事項")