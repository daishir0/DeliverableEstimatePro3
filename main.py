"""
DeliverableEstimatePro3 - メインアプリケーション
4エージェント生成AI構成
"""

import os
import sys
import traceback
from typing import List, Dict, Any
from dotenv import load_dotenv

from workflow_orchestrator_simple import SimpleWorkflowOrchestrator
from utils.excel_processor import ExcelProcessor
from config.i18n_config import t, setup_i18n
from state_manager import EstimationState

# デバッグモードの設定を読み込み
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

def debug_log(message):
    """デバッグログを出力する関数"""
    if DEBUG_MODE:
        print(f"[DEBUG] {message}")


class DeliverableEstimatePro3:
    """メインアプリケーションクラス"""
    
    def __init__(self):
        # 環境変数読み込み（既にmain()で実行済み）
        # load_dotenv()
        
        # 必須環境変数チェック
        required_env = ["OPENAI_API_KEY"]
        missing_env = [var for var in required_env if not os.getenv(var)]
        if missing_env:
            raise ValueError(t("app.config.required_env_missing", vars=missing_env))
        
        # コンポーネント初期化
        self.workflow_orchestrator = SimpleWorkflowOrchestrator()
        self.excel_processor = ExcelProcessor()
        
        # 設定値
        self.daily_rate = float(os.getenv("DAILY_RATE", "50000"))
        self.tax_rate = float(os.getenv("TAX_RATE", "0.10"))
        self.output_dir = os.getenv("OUTPUT_DIR", "./output")
        
        # デバッグモード設定
        self.debug_mode = DEBUG_MODE
        if self.debug_mode:
            debug_log(t("app.main.debug_mode"))
            api_key_status = t("app.config.api_key_set") if os.getenv('OPENAI_API_KEY') else t("app.config.api_key_not_set")
            debug_log(t("app.config.api_key_status", status=api_key_status))
            debug_log(f"DAILY_RATE: {self.daily_rate}")
            debug_log(f"TAX_RATE: {self.tax_rate}")
            debug_log(f"OUTPUT_DIR: {self.output_dir}")
    
    def run(self):
        """メインアプリケーション実行"""
        print(f"🚀 {t('app.main.title')}")
        print("="*60)
        
        try:
            # 1. 入力収集
            excel_file, requirements = self._collect_inputs()
            
            # 2. Excel解析
            deliverables = self._process_excel_input(excel_file)
            if not deliverables:
                return
            
            # 3. ワークフロー実行
            final_state = self._execute_estimation_workflow(excel_file, requirements, deliverables)
            
            # 4. 結果出力
            self._output_results(final_state, excel_file)
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️ {t('errors.system.user_interrupt')}")
        except Exception as e:
            error_msg = f"\n❌ {t('errors.system.unexpected', error=str(e))}"
            print(error_msg)
            if self.debug_mode:
                debug_log(f"エラー詳細: {traceback.format_exc()}")
    
    def _collect_inputs(self) -> tuple:
        """入力情報の収集"""
        print(f"\n📝 {t('app.input.title')}")
        print("-" * 30)
        
        # コマンドライン引数からExcelファイルパスを取得
        excel_file = None
        if len(sys.argv) > 1:
            excel_file = sys.argv[1]
            print(t("app.input.excel_file_from_arg", file=excel_file))
        else:
            excel_file = input(t("app.input.excel_file_prompt")).strip()
            if not excel_file:
                excel_file = "./input/sample_input.xlsx"  # デフォルト
                print(t("app.input.default_file_used", file=excel_file))
        
        # システム要件
        print(f"\n{t('app.input.system_requirements_prompt')}")
        requirements_lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            requirements_lines.append(line)
        
        requirements = "\n".join(requirements_lines)
        if not requirements.strip():
            requirements = t("app.defaults.requirements")
            print(t("app.input.default_requirements_used", requirements=requirements))
        
        return excel_file, requirements
    
    def _process_excel_input(self, excel_file: str) -> List[Dict[str, Any]]:
        """Excel入力の処理"""
        print(f"\n📊 {t('app.excel.analyzing')}")
        
        result = self.excel_processor.read_deliverables_from_excel(excel_file)
        
        if not result.get("success"):
            print(t("app.excel.error", error=result.get('error')))
            return None
        
        deliverables = result["deliverables"]
        print(t("app.excel.success", count=len(deliverables)))
        
        # 成果物一覧表示
        print(f"\n📋 {t('app.excel.deliverables_list')}")
        for i, item in enumerate(deliverables, 1):
            print(t("app.excel.deliverable_item", index=i, name=item['name'], description=item['description']))
        
        return deliverables
    
    def _execute_estimation_workflow(self, excel_file: str, requirements: str, 
                                   deliverables: List[Dict[str, Any]]) -> EstimationState:
        """見積もりワークフローの実行"""
        print(f"\n🤖 {t('workflow.orchestrator.title')}")
        print("-" * 40)
        
        final_state = self.workflow_orchestrator.execute_workflow(
            excel_file, requirements, deliverables
        )
        
        return final_state
    
    def _output_results(self, final_state: EstimationState, original_excel: str):
        """結果出力"""
        print(f"\n📤 {t('app.output.title')}")
        
        if not final_state.get("user_approved"):
            print(f"⚠️ {t('app.output.not_approved')}")
            return
        
        estimation_result = final_state.get("estimation_result")
        if not estimation_result or not estimation_result.get("success"):
            print(f"❌ {t('app.output.invalid_result')}")
            return
        
        # Excel出力
        output_result = self.excel_processor.write_estimation_to_excel(
            estimation_result, original_excel, self.output_dir
        )
        
        if output_result.get("success"):
            print(t("app.output.excel_success", file=output_result['output_file']))
            print(t("app.output.total_amount", amount=f"{output_result['total_amount']:,}"))
        else:
            print(t("app.output.excel_error", error=output_result.get('error')))
        
        # セッションログ出力
        self._output_session_logs(final_state)
    
    def _output_session_logs(self, final_state: EstimationState):
        """セッションログの出力"""
        try:
            import json
            from datetime import datetime
            
            log_file = os.path.join(self.output_dir, "session_log.json")
            
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "session_summary": {
                    "iteration_count": final_state.get("iteration_count", 0),
                    "final_step": final_state.get("current_step", "unknown"),
                    "user_approved": final_state.get("user_approved", False),
                    "total_errors": len(final_state.get("errors", [])),
                    "total_warnings": len(final_state.get("warnings", []))
                },
                "session_logs": final_state.get("session_logs", []),
                "errors": final_state.get("errors", []),
                "warnings": final_state.get("warnings", [])
            }
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            print(t("app.output.session_log", file=log_file))
            
        except Exception as e:
            print(t("app.output.log_error", error=str(e)))


def main():
    """メイン関数"""
    try:
        # 環境変数を最初に読み込む
        load_dotenv()
        
        # .envの言語設定を反映してi18nを初期化
        setup_i18n()
        
        app = DeliverableEstimatePro3()
        app.run()
    except Exception as e:
        print(t("errors.system.app_init", error=str(e)))
        sys.exit(1)


if __name__ == "__main__":
    main()