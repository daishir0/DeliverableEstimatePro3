"""
PydanticOutputParser対応ベースAIエージェント
"""

import os
from typing import Dict, Any, Optional, Type
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError
import time


class PydanticAIAgent:
    """PydanticOutputParser対応ベースクラス"""
    
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        
        # APIキーの存在確認
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "dummy_key_for_testing":
            print(f"⚠️ 警告: OpenAI APIキーが設定されていません。{self.agent_name}はダミーデータを返します。")
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
        """Pydantic構造化出力での実行（エラーハンドリング強化版）"""
        
        # APIキーが無い場合はダミーデータを返す
        if self.llm is None:
            return self._create_dummy_response(pydantic_model)
        
        # 入力の安全性チェック
        if not user_input or not isinstance(user_input, str):
            return self._create_error_response("無効な入力データです")
        
        # PydanticOutputParserの設定
        try:
            parser = PydanticOutputParser(pydantic_object=pydantic_model)
        except Exception as e:
            return self._create_error_response(f"パーサー作成エラー: {str(e)}")
        
        # コンテキスト情報を追加
        context_str = ""
        if additional_context:
            try:
                import json
                context_str = f"\n\n【追加コンテキスト】\n{json.dumps(additional_context, ensure_ascii=False, indent=2)}"
            except Exception as e:
                print(f"[{self.agent_name}] コンテキスト処理警告: {str(e)}")
                context_str = f"\n\n【追加コンテキスト】\n{str(additional_context)}"
        
        # プロンプトテンプレート作成
        try:
            prompt = ChatPromptTemplate.from_template(
                self.system_prompt + "\n\n{user_input}{context_str}\n\n{format_instructions}"
            ).partial(format_instructions=parser.get_format_instructions())
            
            # チェーン作成
            chain = prompt | self.llm | parser
        except Exception as e:
            return self._create_error_response(f"プロンプト・チェーン作成エラー: {str(e)}")
        
        # リトライ実行（指数バックオフ付き）
        for attempt in range(self.max_retries):
            try:
                print(f"[{self.agent_name}] 実行試行 {attempt + 1}/{self.max_retries}")
                
                result = chain.invoke({
                    "user_input": user_input,
                    "context_str": context_str
                })
                
                # Pydanticモデルを辞書に変換
                if isinstance(result, BaseModel):
                    result_dict = result.dict()
                    result_dict["success"] = True
                    result_dict["_agent_metadata"] = {
                        "agent_name": self.agent_name,
                        "attempt_number": attempt + 1,
                        "model_used": self.model,
                        "execution_time": time.time()
                    }
                    print(f"[{self.agent_name}] ✅ 実行成功")
                    return result_dict
                else:
                    # 辞書形式の場合
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
                print(f"[{self.agent_name}] バリデーションエラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_dummy_response(pydantic_model, f"バリデーションエラー: {str(e)}")
                time.sleep(2 ** attempt)  # 指数バックオフ
                
            except Exception as e:
                print(f"[{self.agent_name}] 実行エラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_dummy_response(pydantic_model, f"実行エラー: {str(e)}")
                time.sleep(2 ** attempt)  # 指数バックオフ
        
        return self._create_dummy_response(pydantic_model, "最大リトライ回数に達しました")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """エラーレスポンスの標準フォーマット"""
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
        """ダミーレスポンスの作成（エラー時やAPIキー無し時）"""
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
                # 汎用ダミー
                return {
                    "success": True,
                    "dummy_data": True,
                    "overall_score": 75,
                    "note": f"APIキーが無いため{self.agent_name}のダミーデータです",
                    "error_note": error_message,
                    "_agent_metadata": {
                        "agent_name": self.agent_name,
                        "status": "dummy",
                        "execution_time": time.time()
                    }
                }
        except Exception as e:
            print(f"[{self.agent_name}] ダミー作成エラー: {str(e)}")
            return self._create_error_response(f"ダミー作成エラー: {str(e)}")
    
    def _create_dummy_business_evaluation(self) -> Dict[str, Any]:
        """業務要件評価のダミーデータ"""
        return {
            "success": True,
            "overall_score": 75,
            "business_purpose": {
                "clarity_score": 70,
                "assessment": "ダミーデータ: 業務目的は基本的に明確",
                "missing_elements": ["詳細なKPI設定"]
            },
            "functional_requirements": {
                "completeness_score": 80,
                "assessment": "ダミーデータ: 機能要件は概ね網羅",
                "missing_elements": ["画面遷移の詳細"]
            },
            "user_stories": {
                "coverage_score": 65,
                "assessment": "ダミーデータ: ユーザーストーリーは部分的",
                "missing_elements": ["エラーケースの考慮"]
            },
            "business_value": {
                "quantification_score": 60,
                "assessment": "ダミーデータ: ビジネス価値の定量化が不足",
                "missing_elements": ["ROI計算"]
            },
            "stakeholders": {
                "identification_score": 70,
                "assessment": "ダミーデータ: 主要ステークホルダーは特定済み",
                "missing_elements": ["承認フロー"]
            },
            "business_flow": {
                "clarity_score": 75,
                "assessment": "ダミーデータ: 業務フローは基本的に整理済み",
                "missing_elements": ["例外処理フロー"]
            },
            "improvement_questions": [
                {
                    "category": "業務目的",
                    "question": "具体的なKPI目標値は？",
                    "purpose": "定量評価のため",
                    "impact_on_estimation": "工数の精度向上"
                }
            ],
            "risk_factors": ["要件変更リスク", "ステークホルダー調整コスト"],
            "recommendations": ["KPI設定の明確化", "ユーザーストーリーの詳細化"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_quality_evaluation(self) -> Dict[str, Any]:
        """品質要件評価のダミーデータ"""
        return {
            "success": True,
            "overall_score": 70,
            "performance_requirements": {
                "definition_score": 65,
                "assessment": "ダミーデータ: パフォーマンス要件は部分的に定義",
                "missing_elements": ["具体的なレスポンス時間"],
                "effort_impact_percentage": 15.0
            },
            "security_requirements": {
                "completeness_score": 75,
                "assessment": "ダミーデータ: セキュリティ要件は基本レベル",
                "missing_elements": ["脆弱性対策詳細"],
                "effort_impact_percentage": 20.0
            },
            "availability_reliability": {
                "specification_score": 60,
                "assessment": "ダミーデータ: 可用性要件が不明確",
                "missing_elements": ["稼働率目標"],
                "effort_impact_percentage": 10.0
            },
            "scalability_maintainability": {
                "consideration_score": 70,
                "assessment": "ダミーデータ: 拡張性は考慮済み",
                "missing_elements": ["メンテナンス計画"],
                "effort_impact_percentage": 12.0
            },
            "usability": {
                "requirement_score": 65,
                "assessment": "ダミーデータ: ユーザビリティは基本考慮",
                "missing_elements": ["アクセシビリティ要件"],
                "effort_impact_percentage": 8.0
            },
            "operational_monitoring": {
                "planning_score": 55,
                "assessment": "ダミーデータ: 運用監視計画が不足",
                "missing_elements": ["監視項目の詳細"],
                "effort_impact_percentage": 15.0
            },
            "improvement_questions": [
                {
                    "category": "パフォーマンス",
                    "question": "想定するレスポンス時間は？",
                    "purpose": "パフォーマンス設計のため",
                    "impact_on_estimation": "最適化工数の算出"
                }
            ],
            "total_effort_impact": 25.0,
            "risk_factors": ["パフォーマンス不足リスク", "運用監視不備"],
            "recommendations": ["パフォーマンス要件の明確化", "監視計画の策定"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_constraints_evaluation(self) -> Dict[str, Any]:
        """制約要件評価のダミーデータ"""
        return {
            "success": True,
            "overall_score": 65,
            "technical_constraints": {
                "clarity_score": 60,
                "assessment": "ダミーデータ: 技術制約は部分的に明確",
                "identified_constraints": ["React/Node.js使用"],
                "missing_elements": ["ライブラリ制限"],
                "effort_impact_percentage": 10.0
            },
            "external_integrations": {
                "specification_score": 55,
                "assessment": "ダミーデータ: 外部連携仕様が不十分",
                "identified_constraints": ["決済システム連携"],
                "missing_elements": ["API仕様詳細"],
                "effort_impact_percentage": 20.0
            },
            "compliance_regulations": {
                "coverage_score": 70,
                "assessment": "ダミーデータ: 基本的な法規制は考慮",
                "identified_constraints": ["個人情報保護法"],
                "missing_elements": ["業界固有規制"],
                "effort_impact_percentage": 15.0
            },
            "infrastructure_constraints": {
                "definition_score": 65,
                "assessment": "ダミーデータ: インフラ制約は概ね明確",
                "identified_constraints": ["クラウド利用"],
                "missing_elements": ["具体的なサービス制限"],
                "effort_impact_percentage": 8.0
            },
            "resource_constraints": {
                "realism_score": 75,
                "assessment": "ダミーデータ: リソース制約は現実的",
                "identified_constraints": ["予算制限", "スケジュール制限"],
                "missing_elements": ["人員スキル制約"],
                "effort_impact_percentage": 12.0
            },
            "operational_constraints": {
                "planning_score": 60,
                "assessment": "ダミーデータ: 運用制約は部分的に計画",
                "identified_constraints": ["運用時間制限"],
                "missing_elements": ["サポート体制"],
                "effort_impact_percentage": 10.0
            },
            "improvement_questions": [
                {
                    "category": "技術制約",
                    "question": "使用禁止ライブラリはありますか？",
                    "purpose": "技術選定のため",
                    "impact_on_estimation": "実装方式の決定"
                }
            ],
            "total_effort_impact": 18.0,
            "feasibility_risks": ["外部連携不具合", "法規制変更"],
            "mitigation_strategies": ["早期API検証", "法務確認"],
            "recommendations": ["外部連携仕様の詳細化", "制約条件の明文化"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy",
                "execution_time": time.time()
            }
        }
    
    def _create_dummy_estimation_result(self) -> Dict[str, Any]:
        """見積もり結果のダミーデータ"""
        return {
            "success": True,
            "deliverable_estimates": [
                {
                    "name": "要件定義書",
                    "description": "システム要件定義",
                    "base_effort_days": 5.0,
                    "complexity_multiplier": 1.2,
                    "risk_multiplier": 1.1,
                    "final_effort_days": 6.6,
                    "cost_jpy": 330000,
                    "confidence_score": 0.8,
                    "rationale": "ダミーデータ: 標準的な要件定義工数"
                },
                {
                    "name": "システム設計書",
                    "description": "技術設計書",
                    "base_effort_days": 8.0,
                    "complexity_multiplier": 1.3,
                    "risk_multiplier": 1.2,
                    "final_effort_days": 12.5,
                    "cost_jpy": 625000,
                    "confidence_score": 0.75,
                    "rationale": "ダミーデータ: アーキテクチャ設計工数"
                }
            ],
            "financial_summary": {
                "total_effort_days": 245.0,
                "subtotal_jpy": 12250000,
                "tax_jpy": 1225000,
                "total_jpy": 13475000
            },
            "technical_assumptions": {
                "engineer_level": "Python使用可能な平均的エンジニア",
                "daily_rate_jpy": 50000,
                "development_stack": "React, Express.js, PostgreSQL",
                "team_size": 4,
                "project_duration_months": 6
            },
            "overall_confidence": 0.78,
            "key_risks": ["技術的複雑性", "外部連携リスク", "スケジュール制約"],
            "recommendations": ["プロトタイプ作成", "早期技術検証", "リスク管理計画"],
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "status": "dummy", 
                "execution_time": time.time()
            }
        }