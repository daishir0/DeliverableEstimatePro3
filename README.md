# DeliverableEstimatePro v3

## Overview
DeliverableEstimatePro v3 is an advanced AI-powered system development estimation tool that utilizes a 4-agent architecture to provide accurate and comprehensive project estimates. The system processes Excel-based deliverable lists and system requirements to generate detailed cost and effort estimations through parallel AI agent evaluation.

### Key Features
- **4-Agent AI Architecture**: Parallel processing with specialized agents for different evaluation aspects
- **Multi-language Support**: English and Japanese interface support
- **Excel Integration**: Input/output processing with Excel files
- **Interactive Refinement**: User feedback loop for estimate refinement
- **Comprehensive Reporting**: Detailed estimation reports with risk analysis

### Agent Architecture
1. **Business Requirements Agent**: Evaluates functional and business requirements
2. **Quality Requirements Agent**: Assesses non-functional and quality requirements
3. **Constraints Agent**: Analyzes technical constraints and external integrations
4. **Estimation Agent**: Generates final cost and effort estimates based on all evaluations

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Step-by-step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/daishir0/DeliverableEstimatePro3.git
   cd DeliverableEstimatePro3
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env_example .env
   ```
   
   Edit the `.env` file and configure the following:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL=gpt-4o-mini
   DAILY_RATE=500
   CURRENCY=USD
   TAX_RATE=0.10
   LANGUAGE=en
   DEBUG_MODE=false
   ```

4. **Prepare input directory**
   ```bash
   mkdir -p input output
   ```

## Usage

### Basic Usage

1. **Prepare your deliverables Excel file**
   - Create an Excel file with deliverable names and descriptions
   - Place it in the `input/` directory

2. **Run the application**
   ```bash
   python main.py [path_to_excel_file]
   ```
   
   Or run without arguments and enter the file path interactively:
   ```bash
   python main.py
   ```

3. **Provide system requirements**
   - Enter your system requirements when prompted
   - Press Enter on an empty line to finish input

4. **Review and approve estimates**
   - The system will display detailed estimates
   - Approve with 'y' or provide feedback for refinement

### Advanced Configuration

#### Language Settings
Set `LANGUAGE=ja` in `.env` for Japanese interface.

#### Currency and Rate Configuration
```
DAILY_RATE=500        # Daily rate in your currency
CURRENCY=USD          # Currency code
TAX_RATE=0.10         # Tax rate (10%)
```

#### Debug Mode
Set `DEBUG_MODE=true` for detailed execution logs.

### Output Files
- **Excel Report**: Detailed estimation report in Excel format
- **Session Log**: JSON file with complete session history and agent interactions

## Notes

### System Requirements
- The system requires a stable internet connection for OpenAI API access
- Minimum 4GB RAM recommended for optimal performance
- Excel files should follow the expected format with deliverable names and descriptions

### Estimation Methodology
The system uses industry-standard estimation techniques with the following base estimates:
- Requirements Definition: 2-8 person-days
- System Design: 4-12 person-days
- Frontend Development: 8-25 person-days
- Backend Development: 10-30 person-days
- Database Design: 5-18 person-days
- Testing: 5-15 person-days
- Security Implementation: 3-15 person-days
- Deployment: 2-10 person-days

Complexity and risk factors are automatically applied based on AI agent analysis.

### Limitations
- Maximum 3 refinement iterations per session
- Requires OpenAI API access
- Excel file format must be compatible with openpyxl library

### Troubleshooting
- Ensure OpenAI API key is valid and has sufficient credits
- Check Excel file format compatibility
- Verify all required dependencies are installed
- Enable DEBUG_MODE for detailed error information

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# DeliverableEstimatePro v3

## 概要
DeliverableEstimatePro v3は、4エージェントアーキテクチャを活用した高度なAI駆動システム開発見積もりツールです。Excelベースの成果物リストとシステム要件を処理し、並列AIエージェント評価を通じて詳細なコストと工数見積もりを生成します。

### 主要機能
- **4エージェントAIアーキテクチャ**: 異なる評価側面に特化したエージェントによる並列処理
- **多言語サポート**: 英語と日本語のインターフェース対応
- **Excel連携**: Excelファイルでの入出力処理
- **インタラクティブ改善**: ユーザーフィードバックループによる見積もり改善
- **包括的レポート**: リスク分析を含む詳細な見積もりレポート

### エージェントアーキテクチャ
1. **ビジネス要件エージェント**: 機能要件とビジネス要件の評価
2. **品質要件エージェント**: 非機能要件と品質要件の評価
3. **制約エージェント**: 技術的制約と外部連携の分析
4. **見積もりエージェント**: 全評価に基づく最終的なコストと工数見積もりの生成

## インストール方法

### 前提条件
- Python 3.8以上
- OpenAI APIキー

### Step by stepのインストール方法

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/daishir0/DeliverableEstimatePro3.git
   cd DeliverableEstimatePro3
   ```

2. **必要なパッケージのインストール**
   ```bash
   pip install -r requirements.txt
   ```

3. **環境変数の設定**
   ```bash
   cp .env_example .env
   ```
   
   `.env`ファイルを編集して以下を設定：
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL=gpt-4o-mini
   DAILY_RATE=500
   CURRENCY=USD
   TAX_RATE=0.10
   LANGUAGE=ja
   DEBUG_MODE=false
   ```

4. **入力ディレクトリの準備**
   ```bash
   mkdir -p input output
   ```

## 使い方

### 基本的な使用方法

1. **成果物Excelファイルの準備**
   - 成果物名と説明を含むExcelファイルを作成
   - `input/`ディレクトリに配置

2. **アプリケーションの実行**
   ```bash
   python main.py [Excelファイルのパス]
   ```
   
   または引数なしで実行してファイルパスを対話的に入力：
   ```bash
   python main.py
   ```

3. **システム要件の提供**
   - プロンプトが表示されたらシステム要件を入力
   - 空行でEnterを押して入力完了

4. **見積もりの確認と承認**
   - システムが詳細な見積もりを表示
   - 'y'で承認、またはフィードバックを提供して改善

### 高度な設定

#### 言語設定
日本語インターフェースには`.env`で`LANGUAGE=ja`を設定。

#### 通貨とレート設定
```
DAILY_RATE=500        # 通貨単位での日当
CURRENCY=USD          # 通貨コード
TAX_RATE=0.10         # 税率（10%）
```

#### デバッグモード
詳細な実行ログには`DEBUG_MODE=true`を設定。

### 出力ファイル
- **Excelレポート**: Excel形式の詳細見積もりレポート
- **セッションログ**: 完全なセッション履歴とエージェント相互作用のJSONファイル

## 注意点

### システム要件
- OpenAI APIアクセスのため安定したインターネット接続が必要
- 最適なパフォーマンスには最低4GBのRAMを推奨
- Excelファイルは成果物名と説明を含む期待される形式に従う必要があります

### 見積もり手法
システムは以下のベース見積もりで業界標準の見積もり技術を使用：
- 要件定義: 2-8人日
- システム設計: 4-12人日
- フロントエンド開発: 8-25人日
- バックエンド開発: 10-30人日
- データベース設計: 5-18人日
- テスト: 5-15人日
- セキュリティ実装: 3-15人日
- デプロイメント: 2-10人日

複雑さとリスク要因はAIエージェント分析に基づいて自動的に適用されます。

### 制限事項
- セッションあたり最大3回の改善イテレーション
- OpenAI APIアクセスが必要
- Excelファイルはopenpyxlライブラリと互換性がある必要があります

### トラブルシューティング
- OpenAI APIキーが有効で十分なクレジットがあることを確認
- Excelファイル形式の互換性を確認
- 必要な依存関係がすべてインストールされていることを確認
- 詳細なエラー情報にはDEBUG_MODEを有効化

## ライセンス
このプロジェクトはMITライセンスの下でライセンスされています。詳細はLICENSEファイルを参照してください。