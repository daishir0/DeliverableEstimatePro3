"""
Excel Processing Utility
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from datetime import datetime


class ExcelProcessor:
    """Excel input/output processing"""
    
    def __init__(self):
        self.supported_extensions = ['.xlsx', '.xls']
    
    def read_deliverables_from_excel(self, file_path: str) -> Dict[str, Any]:
        """Read deliverable information from Excel file"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File not found: {file_path}"}
            
            # Extension check
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.supported_extensions:
                return {"success": False, "error": f"Unsupported file format: {file_ext}"}
            
            # Excel reading
            df = pd.read_excel(file_path)
            
            # Data validation
            if df.empty:
                return {"success": False, "error": "Excel file is empty"}
            
            # Check existence of column A (Name) and column B (Description)
            if len(df.columns) < 2:
                return {"success": False, "error": "Column A (Name) and Column B (Description) are required"}
            
            # Extract deliverable information
            deliverables = []
            for idx, row in df.iterrows():
                name = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
                description = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                
                if name and description:  # Skip empty rows
                    deliverables.append({
                        "name": name,
                        "description": description,
                        "category": self._infer_category(name, description),
                        "complexity_level": "medium"  # Default
                    })
            
            if not deliverables:
                return {"success": False, "error": "No valid deliverable data found"}
            
            return {
                "success": True,
                "deliverables": deliverables,
                "total_count": len(deliverables),
                "source_file": file_path
            }
            
        except Exception as e:
            return {"success": False, "error": f"Excel reading error: {str(e)}"}
    
    def write_estimation_to_excel(self, estimation_result: Dict[str, Any], 
                                 original_file_path: str,
                                 output_dir: str = "./output") -> Dict[str, Any]:
        """Output estimation results to Excel"""
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(output_dir, f"estimate_{timestamp}.xlsx")
            
            # Load original data
            original_df = pd.read_excel(original_file_path)
            
            # Integrate estimation data
            output_data = self._merge_estimation_data(original_df, estimation_result)
            
            # Excel output
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                output_data["main"].to_excel(writer, sheet_name='Estimate', index=False)
                
                if "assumptions" in output_data:
                    output_data["assumptions"].to_excel(writer, sheet_name='Assumptions', index=False)
                
                if "summary" in output_data:
                    output_data["summary"].to_excel(writer, sheet_name='Summary', index=False)
            
            return {
                "success": True,
                "output_file": output_file,
                "file_name": f"estimate_{timestamp}.xlsx",
                "total_amount": self._extract_total_amount(estimation_result)
            }
            
        except Exception as e:
            return {"success": False, "error": f"Excel output error: {str(e)}"}
    
    def _infer_category(self, name: str, description: str) -> str:
        """Infer deliverable category"""
        text = f"{name} {description}".lower()
        
        # Check for documentation keywords (English first, then Japanese for compatibility)
        if any(keyword in text for keyword in ["requirements", "specification", "definition", "要件", "仕様", "定義"]):
            return "documentation"
        elif any(keyword in text for keyword in ["frontend", "screen", "ui", "ux", "フロントエンド", "画面"]):
            return "frontend_development"
        elif any(keyword in text for keyword in ["backend", "api", "server", "バックエンド", "サーバー"]):
            return "backend_development"
        elif any(keyword in text for keyword in ["database", "db", "table", "データベース", "テーブル"]):
            return "database"
        elif any(keyword in text for keyword in ["test", "testing", "テスト", "試験"]):
            return "testing"
        elif any(keyword in text for keyword in ["security", "encryption", "authentication", "セキュリティ", "暗号化", "認証"]):
            return "security"
        elif any(keyword in text for keyword in ["deploy", "deployment", "operation", "infrastructure", "デプロイ", "運用", "インフラ"]):
            return "deployment"
        else:
            return "other"
    
    def _merge_estimation_data(self, original_df: pd.DataFrame, 
                              estimation_result: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
        """Integrate estimation data with original data"""
        try:
            # Create main sheet
            main_data = original_df.copy()
            
            # Add estimation information
            if estimation_result.get("success") and "estimation_result" in estimation_result:
                est_data = estimation_result["estimation_result"]
                deliverable_estimates = est_data.get("deliverable_estimates", [])
                
                # Add effort and cost columns
                main_data["Estimated Effort (Person-days)"] = ""
                main_data["Cost (JPY)"] = ""
                main_data["Confidence"] = ""
                
                # Map estimation data
                for est in deliverable_estimates:
                    name = est.get("name", "")
                    # Match by name
                    matching_rows = main_data[main_data.iloc[:, 0].str.contains(name, na=False)]
                    if not matching_rows.empty:
                        idx = matching_rows.index[0]
                        main_data.at[idx, "Estimated Effort (Person-days)"] = est.get("final_effort_days", 0)
                        main_data.at[idx, "Cost (JPY)"] = est.get("cost_jpy", 0)
                        main_data.at[idx, "Confidence"] = est.get("confidence_score", 0)
                
                # Add summary row
                financial_summary = est_data.get("financial_summary", {})
                summary_row = {
                    main_data.columns[0]: "【Total】",
                    main_data.columns[1]: "Grand Total",
                    "Estimated Effort (Person-days)": financial_summary.get("total_effort_days", 0),
                    "Cost (JPY)": financial_summary.get("total_jpy", 0),
                    "Confidence": est_data.get("overall_confidence", 0)
                }
                main_data = pd.concat([main_data, pd.DataFrame([summary_row])], ignore_index=True)
            
            # Create assumptions sheet
            assumptions_data = self._create_assumptions_sheet(estimation_result)
            
            # Create summary sheet
            summary_data = self._create_summary_sheet(estimation_result)
            
            return {
                "main": main_data,
                "assumptions": assumptions_data,
                "summary": summary_data
            }
            
        except Exception as e:
            # Return only original data on error
            return {"main": original_df}
    
    def _create_assumptions_sheet(self, estimation_result: Dict[str, Any]) -> pd.DataFrame:
        """Create assumptions sheet"""
        assumptions = []
        
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            tech_assumptions = estimation_result["estimation_result"].get("technical_assumptions", {})
            
            for key, value in tech_assumptions.items():
                assumptions.append({
                    "Item": key,
                    "Assumption": str(value)
                })
        
        return pd.DataFrame(assumptions)
    
    def _create_summary_sheet(self, estimation_result: Dict[str, Any]) -> pd.DataFrame:
        """Create summary sheet"""
        summary = []
        
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            est_data = estimation_result["estimation_result"]
            financial_summary = est_data.get("financial_summary", {})
            
            summary = [
                {"Item": "Total Effort", "Value": f"{financial_summary.get('total_effort_days', 0)} person-days"},
                {"Item": "Subtotal", "Value": f"¥{financial_summary.get('subtotal_jpy', 0):,}"},
                {"Item": "Tax", "Value": f"¥{financial_summary.get('tax_jpy', 0):,}"},
                {"Item": "Total Amount", "Value": f"¥{financial_summary.get('total_jpy', 0):,}"},
                {"Item": "Overall Confidence", "Value": f"{est_data.get('overall_confidence', 0)}"}
            ]
        
        return pd.DataFrame(summary)
    
    def _extract_total_amount(self, estimation_result: Dict[str, Any]) -> int:
        """Extract total amount"""
        if estimation_result.get("success") and "estimation_result" in estimation_result:
            financial_summary = estimation_result["estimation_result"].get("financial_summary", {})
            return financial_summary.get("total_jpy", 0)
        return 0