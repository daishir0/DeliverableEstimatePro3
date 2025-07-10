"""
ベースAIエージェント - 全エージェントの共通基盤
"""

import json
import time
from typing import Dict, Any, Optional
from openai import OpenAI
import os


class BaseAIAgent:
    """全エージェントの基底クラス"""
    
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("MODEL", "gpt-4o-mini")
        self.max_retries = 3
        self.retry_delay = 1
    
    def execute_with_ai(self, user_input: str, additional_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """AI実行のメインメソッド（リトライ機能付き）"""
        
        # コンテキスト情報を追加
        context_str = ""
        if additional_context:
            context_str = f"\n\n【追加コンテキスト】\n{json.dumps(additional_context, ensure_ascii=False, indent=2)}"
        
        full_user_input = f"{user_input}{context_str}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": full_user_input}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                    max_tokens=2000
                )
                
                content = response.choices[0].message.content
                result = json.loads(content)
                
                # メタデータを追加
                result["_agent_metadata"] = {
                    "agent_name": self.agent_name,
                    "execution_time": time.time(),
                    "attempt_number": attempt + 1,
                    "model_used": self.model
                }
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"[{self.agent_name}] JSON解析エラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_error_response(f"JSON解析失敗: {str(e)}")
                time.sleep(self.retry_delay)
                
            except Exception as e:
                print(f"[{self.agent_name}] API実行エラー (試行 {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return self._create_error_response(f"API実行失敗: {str(e)}")
                time.sleep(self.retry_delay)
        
        return self._create_error_response("最大リトライ回数に達しました")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """エラーレスポンスの標準フォーマット"""
        return {
            "success": False,
            "error": error_message,
            "agent_name": self.agent_name,
            "_agent_metadata": {
                "agent_name": self.agent_name,
                "execution_time": time.time(),
                "status": "error"
            }
        }
    
    def validate_response(self, response: Dict[str, Any], required_keys: list) -> bool:
        """レスポンスの必須キー検証"""
        if not response.get("success", False):
            return False
        
        for key in required_keys:
            if key not in response:
                print(f"[{self.agent_name}] 必須キー '{key}' が見つかりません")
                return False
        
        return True