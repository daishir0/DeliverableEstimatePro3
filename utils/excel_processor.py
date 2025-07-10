"""
Excel処理ユーティリティ
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class ExcelProcessor:
    """Excel入出力処理"""
    
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls']
    
    def read_deliverables_from_excel(self, file_path: str) -> Dict[str, Any]:
        """ExcelファイルからDeliverable情報を読み込み"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": f"ファイルが見つかりません: {file_path}"}
            
            # 拡張子チェック
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_extensions:
                return {"success": False, "error": f"サポートされていないファイル形式: {file_ext}"}
            
            # Excel読み込み
            df = pd.read_excel(file_path)
            
            # データバリデーション
            if df.empty:
                return {"success": False, "error": "Excelファイルが空です"}
            
            # A列(Name)、B列(Description)の存在確認
            if len(df.columns) < 2:
                return {"success": False, "error": "A列(Name)、B列(Description)が必要です"}
            
            # Deliverable情報の抽出
            deliverables = []
            for idx, row in df.iterrows():
                name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
                description = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                
                if name and description:  # 空行をスキップ
                    deliverables.append({
                        "name": name,
                        "description": description,
                        "category": self._infer_category(name, description),
                        "complexity_level": "medium"  # デフォルト
                    })
            
            if not deliverables:
                return {"success": False, "error": "有効な成果物データが見つかりません"}
            
            return {
                "success": True,
                "deliverables": deliverables,
                "total_count": len(deliverables),
                "source_file": file_path
            }
            
        except Exception as e:
            return {"success": False, "error": f"Excel読み込みエラー: {str(e)}"}
    
    def write_estimation_to_excel(self, estimation_result: Dict[str, Any], 
                                 original_file_path: str,
                                 output_dir: str = "./output") -> Dict[str, Any]:
        """見積もり結果をExcelに出力"""
        try:
            # 出力ディレクトリ作成
            os.makedirs(output_dir, exist_ok=True)
            
            # タイムスタンプ付きファイル名生成
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(output_dir, f"estimate_{timestamp}.xlsx")
            
            # 元データ読み込み
            original_df = pd.read_excel(original_file_path)
            
            # 見積もりデータ統合
            output_data = self._merge_estimation_data(original_df, estimation_result)
            
            # Excel出力
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                output_data["main"].to_excel(writer, sheet_name='見積書', index=False)
                
                if "assumptions" in output_data:
                    output_data["assumptions"].to_excel(writer, sheet_name='前提条件', index=False)
                
                if "summary" in output_data:
                    output_data["summary"].to_excel(writer, sheet_name='サマリー', index=False)
            
            return {
                "success": True,
                "output_file": output_file,
                "file_name": f"estimate_{timestamp}.xlsx",
                "total_amount": self._extract_total_amount(estimation_result)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Excel出力エラー: {str(e)}"}
    
    def _infer_category(self, name: str, description: str) -> str:
        """成果物のカテゴリを推定"""
        text = f"{name} {description}".lower()
        
        if any(keyword in text for keyword in ["要件", "仕様", "定義"]):
            return "documentation"
        elif any(keyword in text for keyword in ["フロントエンド", "画面", "ui", "ux"]):
            return "frontend_development"
        elif any(keyword in text for keyword in ["バックエンド", "api", "サーバー"]):
            return "backend_development"
        elif any(keyword in text for keyword in ["データベース", "db", "テーブル"]):
            return "database"
        elif any(keyword in text for keyword in ["テスト", "試験"]):
            return "testing"
        elif any(keyword in text for keyword in ["セキュリティ", "暗号化", "認証"]):
            return "security"
        elif any(keyword in text for keyword in ["デプロイ", "運用", "インフラ"]):
            return "deployment"
        else:
            return "other"
    
    def _merge_estimation_data(self, original_df: pd.DataFrame, 
                              estimation_result: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """見積もりデータと元データの統合"""
        try:
            # メインシート作成
            main_data = original_df.copy()
            
            # 見積もり情報を追加
            if estimation_result.get("success") and "estimation_result" in estimation_result:
                est_data = estimation_result["estimation_result"]
                deliverable_estimates = est_data.get("deliverable_estimates", [])
                
                # 工数・金額列を追加
                main_data["予想工数(人日)"] = ""
                main_data["金額(円)"] = ""
                main_data["信頼度"] = ""
                
                # 見積もりデータをマッピング
                for est in deliverable_estimates:
                    name = est.get("name", "")
                    # 名前でマッチング
                    matching_rows = main_data[main_data.iloc[:, 0].str.contains(name, na=False)]
                    if not matching_rows.empty:
                        idx = matching_rows.index[0]
                        main_data.at[idx, "予想工数(人日)"] = est.get("final_effort_days", 0)
                        main_data.at[idx, "金額(円)"] = est.get("cost_jpy", 0)
                        main_data.at[idx, "信頼度"] = est.get("confidence_score", 0)
                
                # サマリー行追加
                financial_summary = est_data.get("financial_summary", {})
                summary_row = {
                    main_data.columns[0]: "【合計】",
                    main_data.columns[1]: "総合計",
                    "予想工数(人日)": financial_summary.get("total_effort_days", 0),
                    "金額(円)": financial_summary.get("total_jpy", 0),
                    "信頼度": est_data.get("overall_confidence", 0)
                }
                main_data = pd.concat([main_data, pd.DataFrame([summary_row])], ignore_index=True)
            
            # 前提条件シート作成
            assumptions_data = self._create_assumptions_sheet(estimation_result)
            
            # サマリーシート作成
            summary_data = self._create_summary_sheet(estimation_result)
            
            return {
                "main": main_data,
                "assumptions": assumptions_data,
                "summary": summary_data
            }
            
        except Exception as e:
            # エラー時は元データのみ返す
            return {"main": original_df}
    
    def _create_assumptions_sheet(self, estimation_result: Dict[str, Any]) -> pd.DataFrame:
        """前提条件シート作成"""
        assumptions = []
        
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            tech_assumptions = estimation_result["estimation_result"].get("technical_assumptions", {})
            
            for key, value in tech_assumptions.items():
                assumptions.append({
                    "項目": key,
                    "前提条件": str(value)
                })
        
        return pd.DataFrame(assumptions)
    
    def _create_summary_sheet(self, estimation_result: Dict[str, Any]) -> pd.DataFrame:
        """サマリーシート作成"""
        summary = []
        
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            est_data = estimation_result["estimation_result"]
            financial_summary = est_data.get("financial_summary", {})
            
            summary = [
                {"項目": "総工数", "値": f"{financial_summary.get('total_effort_days', 0)}人日"},
                {"項目": "小計", "値": f"¥{financial_summary.get('subtotal_jpy', 0):,}"},
                {"項目": "消費税", "値": f"¥{financial_summary.get('tax_jpy', 0):,}"},
                {"項目": "総額", "値": f"¥{financial_summary.get('total_jpy', 0):,}"},
                {"項目": "全体信頼度", "値": f"{est_data.get('overall_confidence', 0)}"}
            ]
        
        return pd.DataFrame(summary)
    
    def _extract_total_amount(self, estimation_result: Dict[str, Any]) -> int:
        """総額の抽出"""
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            financial_summary = estimation_result["estimation_result"].get("financial_summary", {})
            return financial_summary.get("total_jpy", 0)
        return 0