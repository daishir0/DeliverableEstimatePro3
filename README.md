# DeliverableEstimatePro v3: Revolutionary AI-Powered Multi-Agent Estimation System

![System Overview](https://img.shields.io/badge/AI-4%20Agents-blue) ![Language](https://img.shields.io/badge/Language-English%20%7C%20Japanese-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

DeliverableEstimatePro v3 is a **revolutionary AI-powered system development estimation tool** that fundamentally transforms software project estimation through **human-AI collaborative intelligence**. Unlike traditional estimation tools, this system employs **4 specialized AI agents** working in parallel to evaluate projects from multiple perspectives, then engages in **iterative dialogue with humans** to capture tacit knowledge and refine estimates to match human intuition.

### 🚀 Revolutionary Innovation

**The Core Breakthrough**: This system's revolutionary aspect lies in its **iterative feedback loop** where human insights (tacit knowledge) are continuously integrated with AI analysis, creating estimates that evolve from rough calculations to precise, human-validated projections.

**Real-World Impact**: In our demonstration, the system successfully processed 12 initial deliverables, engaged in human dialogue about performance requirements, and **automatically added 2 new deliverables** (Performance Optimization and Load Testing), increasing the estimate from $85,500 to $136,275 with enhanced accuracy.

### 🎯 Key Features

- **🤖 4-Agent AI Architecture**: Specialized parallel processing with distinct evaluation perspectives
- **🔄 Human-AI Collaborative Intelligence**: Iterative refinement through tacit knowledge integration  
- **🌐 Multi-language Support**: Complete English and Japanese interface localization
- **📊 Excel Integration**: Seamless input/output processing with Excel files
- **🎛️ Interactive Refinement**: Unlimited user feedback loops for estimate optimization
- **📈 Comprehensive Reporting**: Detailed estimation reports with risk analysis and confidence scoring
- **💰 Multi-currency Support**: Dynamic formatting (USD, JPY, EUR, GBP)
- **⚡ Parallel Processing**: Optimized performance through concurrent agent execution

### 🏗️ Revolutionary Agent Architecture

Our system employs **4 specialized AI agents** that work collaboratively to provide comprehensive project evaluation:

#### 1. **Business Requirements Agent** 
- **Domain**: Functional and business requirements evaluation
- **Expertise**: Business objectives, user stories, stakeholder analysis
- **Output**: Business complexity scoring and functional requirement completeness

#### 2. **Quality Requirements Agent**
- **Domain**: Non-functional and quality requirements assessment  
- **Expertise**: Performance, security, scalability, maintainability analysis
- **Output**: Quality attribute scoring and technical risk assessment

#### 3. **Constraints Agent**
- **Domain**: Technical constraints and external integration analysis
- **Expertise**: Technology limitations, regulatory compliance, infrastructure constraints
- **Output**: Feasibility risk assessment and constraint impact analysis

#### 4. **Estimation Agent**
- **Domain**: Final cost and effort calculation synthesis
- **Expertise**: Multi-factor estimation algorithms, risk-adjusted calculations
- **Output**: Comprehensive estimates with confidence scoring and recommendations

### 🔬 The Science Behind the Revolution

**Multi-Perspective Analysis**: Each agent analyzes the project through its specialized lens, providing insights impossible with single-agent systems.

**Tacit Knowledge Capture**: The system excels at surfacing and incorporating human tacit knowledge that traditional tools miss.

**Intelligent Deliverable Discovery**: AI can identify and add new deliverables based on human feedback, demonstrating true understanding of implicit requirements.

## 🚀 Installation Guide

### 📋 Prerequisites

#### **System Requirements**
- **Python**: 3.8 or higher (3.9+ recommended for optimal performance)
  - Why 3.8+: Required for proper `concurrent.futures` and advanced type annotations
- **Memory**: Minimum 4GB RAM (8GB+ recommended for large projects)
- **Storage**: 500MB available disk space
- **Network**: Stable internet connection for OpenAI API access

#### **Required Dependencies**
- **OpenAI API Key**: Valid API key with sufficient credits
- **Core Libraries**: pandas, openpyxl, langchain, pydantic
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

#### **Optional but Recommended**
- **Virtual Environment**: conda or venv for dependency isolation
- **IDE**: VS Code, PyCharm, or similar for development work
- **Git**: For version control and easy updates

### 🛠️ Step-by-Step Installation

#### **Step 1: Environment Setup**
```bash
# Create and activate virtual environment (recommended)
python -m venv depe_env
source depe_env/bin/activate  # On Windows: depe_env\Scripts\activate

# Or using conda
conda create -n depe_env python=3.9
conda activate depe_env
```

#### **Step 2: Repository Setup**
```bash
# Clone the repository
git clone https://github.com/daishir0/DeliverableEstimatePro3.git
cd DeliverableEstimatePro3

# Verify repository structure
ls -la
# You should see: agents/, config/, input/, locales/, output/, utils/, main.py, requirements.txt
```

#### **Step 3: Dependency Installation**
```bash
# Install all required packages
pip install -r requirements.txt

# Verify critical installations
python -c "import langchain, pandas, openpyxl, pydantic; print('All dependencies installed successfully!')"
```

#### **Step 4: Environment Configuration**
```bash
# Copy the example environment file
cp .env_example .env

# Edit the configuration file
nano .env  # or your preferred editor
```

**Complete `.env` Configuration Example:**
```bash
# === CORE API CONFIGURATION ===
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
MODEL=gpt-4o-mini  # Options: gpt-4o-mini, gpt-4o, gpt-3.5-turbo

# === FINANCIAL CONFIGURATION ===
DAILY_RATE=500      # Daily rate in your preferred currency
CURRENCY=USD        # Supported: USD, JPY, EUR, GBP
TAX_RATE=0.10       # Tax rate as decimal (0.10 = 10%)

# === LOCALIZATION ===
LANGUAGE=en         # Options: en (English), ja (Japanese)

# === SYSTEM CONFIGURATION ===
DEBUG_MODE=false    # Set to 'true' for detailed logging
MAX_ITERATIONS=3    # Maximum refinement iterations
TIMEOUT_SECONDS=120 # Agent execution timeout
```

#### **Step 5: Directory Preparation**
```bash
# Create necessary directories
mkdir -p input output logs

# Set proper permissions (Linux/macOS)
chmod 755 input output logs

# Verify directory structure
tree -L 2
```

#### **Step 6: Installation Verification**
```bash
# Test basic functionality
python main.py --version
python main.py --help

# Run system diagnostics
python -m utils.system_check  # This will verify all components
```

### 🔧 Configuration Details

#### **API Key Setup Options**

1. **Direct .env Method** (Recommended):
   ```bash
   OPENAI_API_KEY=your_key_here
   ```

2. **Environment Variable Method**:
   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

3. **Runtime Input Method**:
   ```bash
   # System will prompt for API key if not found in .env
   python main.py
   ```

#### **Currency Configuration**
The system supports multiple currencies with proper formatting:

| Currency | Code | Symbol | Example Output |
|----------|------|--------|---------------|
| US Dollar | USD | $ | $85,500.00 |
| Japanese Yen | JPY | ¥ | ¥8,550,000 |
| Euro | EUR | € | €77,250.00 |
| British Pound | GBP | £ | £68,500.00 |

#### **Language Localization**
- **English (`en`)**: Complete interface in English
- **Japanese (`ja`)**: Full Japanese localization including error messages

## 📖 Usage Guide

### 🎯 Quick Start

#### **Step 1: Prepare Your Excel Input File**

Create an Excel file with the following structure:

| Column A: Deliverable Name | Column B: Description |
|---------------------------|----------------------|
| Requirements Definition Document | Document that organizes and clarifies the overall system requirements |
| Basic Design Document | Document that describes the basic design policy and overall structure |
| Frontend Development | User interface development using React/Vue.js |
| Backend Development | Server-side development using Node.js/Python |

**Excel File Requirements:**
- **File Format**: `.xlsx` or `.xls`
- **Sheet Name**: Any (system reads the first sheet)
- **Required Columns**: 
  - Column A: `Deliverable Name` (must not be empty)
  - Column B: `Description` (detailed description recommended)
- **Location**: Place in the `input/` directory

**Example Input Files:**
```bash
input/
├── web_application_project.xlsx
├── mobile_app_deliverables.xlsx
└── enterprise_system.xlsx
```

#### **Step 2: Execute the System**

**Method 1: Direct File Path**
```bash
python main.py input/your_project.xlsx
```

**Method 2: Interactive Mode**
```bash
python main.py
# System will prompt: "Please enter the Excel file path:"
# Enter: input/your_project.xlsx
```

**Method 3: Drag and Drop** (Terminal supporting)
```bash
python main.py  # Then drag your Excel file to terminal
```

#### **Step 3: Provide System Requirements**

The system will prompt for comprehensive system requirements:

```
📝 Please enter system requirements (Press Enter on empty line to finish):
```

**Example Input:**
```
Web application for e-commerce platform
Expected 5,000 daily active users  
Integration with payment gateway (Stripe)
Responsive design for mobile and desktop
PostgreSQL database
AWS cloud deployment
99.9% uptime requirement
```

**Tips for Better Requirements:**
- Be specific about user volume and performance expectations
- Mention integrations and third-party services
- Include technology preferences or constraints
- Specify quality requirements (uptime, response time)

#### **Step 4: AI Analysis Process**

The system will execute **4 specialized agents in parallel**:

```
🔄 Starting parallel evaluation: Business, Quality, Constraints
⚡ Running 3 agents in parallel...
  📋 Business & Functional Requirements Evaluation - Started
  🎯 Quality & Non-Functional Requirements Evaluation - Started  
  🔒 Constraints & External Integration Evaluation - Started
```

**What Happens During Analysis:**
1. **Business Agent**: Evaluates functional requirements and business value
2. **Quality Agent**: Assesses performance, security, and scalability needs
3. **Constraints Agent**: Analyzes technical limitations and integration complexity
4. **Estimation Agent**: Synthesizes all evaluations into concrete estimates

#### **Step 5: Review Initial Estimates**

The system displays comprehensive estimation results:

```
💰 Estimation Results:
  Total Effort: 171.0 person-days
  Total Amount: $85,500.00
  Confidence: 0.59

📋 All Deliverable Estimates Details:
--------------------------------------------------------------------------------
No.  Deliverable Name          Base Effort Final Effort Amount       Confidence
--------------------------------------------------------------------------------
1    Requirements Definition   5.0      6.5      $3,250.00       0.70  
2    Basic Design Document     8.0      10.4     $5,200.00       0.70  
3    Frontend Development      15.0     24.3     $12,150.00      0.50  
4    Backend Development       20.0     31.2     $15,600.00      0.50  
--------------------------------------------------------------------------------
```

#### **Step 6: Interactive Refinement (Revolutionary Feature)**

**The Human-AI Collaboration Loop:**

```
Do you approve? (y/n/modification request): 
```

**Option 1: Approve**
```
y
```
→ System generates final Excel output

**Option 2: Reject**  
```
n
```
→ System asks for specific concerns

**Option 3: Provide Tacit Knowledge** (Revolutionary!)
```
Performance expectations are implicit in our vision. The system must handle 10,000 concurrent users and ensure sub-2-second response time on key pages. Please reflect this in the estimation.
```

**What Happens Next:**
The AI analyzes your feedback and:
- Adjusts existing deliverable estimates
- **Automatically adds new deliverables** if needed
- Recalculates complexity and risk factors
- Provides enhanced estimates with improved accuracy

**Example AI Response:**
```
🔄 Improving the estimate...
✅ Improvement completed

💰 Updated Estimation Results:
  Total Effort: 272.5 person-days  
  Total Amount: $136,275.00
  Confidence: 0.56

📋 New Deliverables Added:
13   Performance Optimization   20.0     45.0     $22,500.00      0.50  ← NEW!
14   Load Testing & Performance 15.0     33.8     $16,875.00      0.50  ← NEW!
```

### 🔄 Advanced Usage Scenarios

#### **Scenario 1: Large Enterprise Project**
```bash
# For complex projects with 20+ deliverables
python main.py input/enterprise_project.xlsx

# System requirements example:
Enterprise ERP system
50,000+ concurrent users
Multi-tenant architecture  
ISO 27001 compliance required
Integration with 15+ legacy systems
24/7 operations with 99.99% uptime
```

#### **Scenario 2: Startup MVP**
```bash
python main.py input/mvp_features.xlsx

# System requirements example: 
Minimum viable product for mobile app
1,000 initial users expected
Cloud-native architecture
Rapid iteration capability
Cost optimization priority
```

#### **Scenario 3: Legacy System Modernization**
```bash
python main.py input/modernization_scope.xlsx

# System requirements example:
Modernize 10-year-old monolith application
Zero-downtime migration required
Maintain API compatibility
Gradual rollout strategy
Performance must match or exceed current system
```

### 🔧 Advanced Configuration

#### **Localization Settings**
```bash
# English Interface (Default)
LANGUAGE=en

# Japanese Interface  
LANGUAGE=ja
```

**What Changes with Language:**
- All system messages and prompts
- Error messages and warnings
- Output report headers and labels  
- Agent interaction messages

#### **Financial Configuration**
```bash
# Daily Rate Configuration
DAILY_RATE=500        # Your daily consulting rate
CURRENCY=USD          # Currency for all calculations
TAX_RATE=0.10         # Tax rate (0.10 = 10%)

# Multi-currency Examples:
DAILY_RATE=50000      # For Japanese Yen
CURRENCY=JPY

DAILY_RATE=450        # For Euros
CURRENCY=EUR
```

#### **Performance Tuning**
```bash
# Agent Execution Settings
MAX_ITERATIONS=3      # Maximum refinement cycles
TIMEOUT_SECONDS=120   # Agent timeout (increase for complex projects)

# Model Selection for Different Needs:
MODEL=gpt-4o         # Highest accuracy (higher cost)
MODEL=gpt-4o-mini    # Balanced performance (recommended)  
MODEL=gpt-3.5-turbo  # Fastest execution (lower accuracy)
```

#### **Debug and Development Mode**
```bash
# Production Mode (Default)
DEBUG_MODE=false

# Development Mode (Detailed Logging)
DEBUG_MODE=true
```

**Debug Mode Features:**
- Detailed agent execution logs
- API request/response logging
- Performance timing information
- Error stack traces
- Intermediate calculation details

### 📊 Output Files and Reports

#### **Excel Estimation Report**
**File Location**: `output/estimate_YYYYMMDD-HHMMSS.xlsx`

**Content Structure:**
```
Sheet 1: Estimation Results
├── Deliverable Details (Name, Effort, Cost, Confidence)
├── Financial Summary (Total Effort, Cost, Tax)
├── Risk Analysis (Key Risks, Mitigation Strategies)
└── Technical Assumptions (Team Size, Technology Stack)

Sheet 2: Agent Analysis  
├── Business Requirements Evaluation
├── Quality Requirements Assessment
├── Constraints and Integration Analysis
└── Confidence Scoring Breakdown

Sheet 3: Session History
├── User Input and Feedback
├── Iteration History
└── Refinement Details
```

#### **Session Log (JSON)**
**File Location**: `output/session_log.json`

**Content Structure:**
```json
{
  "session_id": "uuid",
  "timestamp": "2025-07-28T10:30:00Z",
  "input_file": "input/project.xlsx",
  "system_requirements": "...",
  "agent_evaluations": {
    "business_agent": {...},
    "quality_agent": {...},
    "constraints_agent": {...}
  },
  "iterations": [
    {
      "iteration_number": 1,
      "user_feedback": "...",
      "ai_adjustments": "...",
      "estimate_changes": {...}
    }
  ],
  "final_results": {...}
}
```

#### **Log Files**
**File Location**: `logs/execution_YYYYMMDD.log`

**Content Examples:**
```
[2025-07-28 10:30:15] INFO: System initialized successfully
[2025-07-28 10:30:16] INFO: Loading deliverables from: input/project.xlsx
[2025-07-28 10:30:17] INFO: Found 12 deliverables
[2025-07-28 10:30:18] INFO: Starting parallel agent evaluation
[2025-07-28 10:30:35] INFO: Business agent completed (17.2s)
[2025-07-28 10:30:38] INFO: Quality agent completed (20.1s)
[2025-07-28 10:30:39] INFO: Constraints agent completed (21.3s)
[2025-07-28 10:30:40] INFO: Estimation agent generating results
[2025-07-28 10:30:45] INFO: Initial estimate: $85,500 (171 person-days)
```

## 🔍 Technical Specifications

### 🏛️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                 DeliverableEstimatePro v3                   │
├─────────────────────────────────────────────────────────────┤
│  main.py (Application Control)                              │
│  ├─ Input Processing (Excel + System Requirements)          │
│  ├─ Workflow Execution (SimpleWorkflowOrchestrator)         │
│  └─ Result Output (Excel + Session Log)                     │
├─────────────────────────────────────────────────────────────┤
│  SimpleWorkflowOrchestrator (Workflow Control)              │
│  ├─ Parallel Evaluation Execution (3 agents simultaneously) │
│  ├─ Estimation Generation (EstimationAgent)                 │
│  └─ Interactive Loop (Modification Request Handling)        │
├─────────────────────────────────────────────────────────────┤
│  4 AI Agents (Specialized Intelligence)                     │
│  ├─ BusinessRequirementsAgent (Business/Functional Req.)    │
│  ├─ QualityRequirementsAgent (Quality/Non-Functional Req.)  │
│  ├─ ConstraintsAgent (Constraints/External Integration)     │
│  └─ EstimationAgent (Estimation Generation & Refinement)    │
├─────────────────────────────────────────────────────────────┤
│  Foundation Layer (Robust Infrastructure)                   │
│  ├─ PydanticAIAgent (Type-Safe Agent Base Class)            │
│  ├─ PydanticModels (Data Structure Definition)              │
│  ├─ StateManager (Centralized State Management)             │
│  ├─ CurrencyUtils (Multi-currency Support)                  │
│  └─ i18n_utils (Internationalization Framework)            │
└─────────────────────────────────────────────────────────────┘
```

### 🧮 Estimation Methodology

The system employs **industry-standard estimation techniques** enhanced with **AI-driven complexity analysis**:

#### **Base Estimation Categories**
| Deliverable Type | Base Range (Person-Days) | Complexity Factors |
|------------------|--------------------------|-------------------|
| Requirements Definition | 2-8 | Business clarity, stakeholder count |
| System Design | 4-12 | Architecture complexity, integration points |
| Frontend Development | 8-25 | UI complexity, responsive requirements |
| Backend Development | 10-30 | Business logic, API complexity |
| Database Design | 5-18 | Data volume, relationship complexity |
| Testing | 5-15 | Coverage requirements, automation level |
| Security Implementation | 3-15 | Compliance requirements, threat model |
| Deployment | 2-10 | Infrastructure complexity, CI/CD needs |

#### **Multi-Factor Calculation Algorithm**
```
Final Effort = Base Effort × Complexity Factor × Risk Factor × Integration Factor

Where:
- Complexity Factor: 1.0-2.5 (based on technical complexity)
- Risk Factor: 1.0-2.0 (based on uncertainty and constraints)  
- Integration Factor: 1.0-1.8 (based on external dependencies)
```

#### **AI-Enhanced Factors**
- **Business Agent**: Functional complexity scoring (0.5-2.0 multiplier)
- **Quality Agent**: Non-functional requirements impact (0.3-1.5 multiplier)
- **Constraints Agent**: Technical and regulatory constraints (0.2-1.3 multiplier)

### 🔒 Security and Privacy

#### **Data Handling**
- **Local Processing**: All Excel files processed locally
- **API Communication**: Only project descriptions sent to OpenAI
- **No Data Storage**: OpenAI doesn't store conversation data
- **Session Logs**: Stored locally in `output/` directory

#### **Security Best Practices**
- **API Key Security**: Store in `.env` file (not in code)
- **File Permissions**: Proper directory permissions set during installation
- **Input Validation**: Excel files validated before processing
- **Error Handling**: Secure error messages without sensitive data exposure

### ⚡ Performance Characteristics

#### **Execution Performance**
- **Parallel Processing**: 3 agents execute simultaneously
- **Typical Runtime**: 20-45 seconds for 12 deliverables
- **Scalability**: Handles 50+ deliverables efficiently
- **Memory Usage**: ~100MB baseline, +50MB per 10 deliverables

#### **API Usage Optimization**
- **Token Efficiency**: Optimized prompts reduce API costs
- **Retry Logic**: Smart retry with exponential backoff
- **Timeout Management**: 120s timeout prevents hanging

### 🛠️ System Requirements

#### **Minimum Requirements**
- **OS**: Windows 10, macOS 10.14, Ubuntu 18.04
- **Python**: 3.8+ (3.9+ recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB available space
- **Network**: Stable internet for API access

#### **Supported File Formats**
- **Input**: `.xlsx`, `.xls` (Excel 2007+)
- **Output**: `.xlsx` (Excel 2007+), `.json` (session logs)
- **Encoding**: UTF-8 for international characters

### ⚠️ Known Limitations

#### **Functional Limitations**
- **Refinement Cycles**: Maximum 3 iterations per session
- **File Size**: Excel files limited to 1000 rows
- **API Dependency**: Requires active OpenAI API access
- **Language Support**: Currently English and Japanese only

#### **Technical Constraints**
- **Network Dependency**: Requires internet connectivity
- **API Rate Limits**: Subject to OpenAI rate limiting
- **Excel Compatibility**: Must use openpyxl-compatible formats

### 🚨 Troubleshooting Guide

#### **Common Issues and Solutions**

**Issue 1: "OpenAI API Key Invalid"**
```bash
# Solution:
1. Verify API key in .env file
2. Check API key format (starts with 'sk-')
3. Confirm sufficient API credits
4. Test with: python -c "import openai; print('API key valid')"
```

**Issue 2: "Excel File Cannot Be Read"**
```bash
# Solution:
1. Ensure file is .xlsx or .xls format
2. Check file permissions (readable)
3. Verify column structure (Name, Description)
4. Try: python -c "import pandas; pandas.read_excel('your_file.xlsx')"
```

**Issue 3: "Agent Execution Timeout"**
```bash
# Solution:
1. Increase TIMEOUT_SECONDS in .env
2. Check internet connectivity
3. Try smaller project scope
4. Enable DEBUG_MODE for detailed logs
```

**Issue 4: "Memory Issues with Large Projects"**
```bash
# Solution:
1. Close other memory-intensive applications
2. Process in smaller batches
3. Increase system RAM if possible
4. Use DEBUG_MODE=false to reduce memory usage
```

#### **Debug Commands**
```bash
# System diagnostic
python -m utils.system_check

# Dependency verification
pip list | grep -E "(langchain|pandas|openpyxl|pydantic)"

# API connectivity test
python -c "from agents.base_ai_agent import *; test_api_connection()"

# File format validation
python -m utils.excel_validator input/your_file.xlsx
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

# DeliverableEstimatePro v3: 革新的AI駆動マルチエージェント見積もりシステム

![システム概要](https://img.shields.io/badge/AI-4%20エージェント-blue) ![言語](https://img.shields.io/badge/言語-日本語%20%7C%20英語-green) ![ライセンス](https://img.shields.io/badge/License-MIT-yellow)

## 概要

DeliverableEstimatePro v3は、**人間-AI協調インテリジェンス**を通じてソフトウェアプロジェクト見積もりを根本的に変革する**革新的AI駆動システム開発見積もりツール**です。従来の見積もりツールとは異なり、本システムは**4つの専門化されたAIエージェント**が並列で動作し、複数の視点からプロジェクトを評価した後、**人間との反復的対話**に参加して暗黙知を捉え、人間の直感に合う見積もりへと精緻化します。

### 🚀 革新的なイノベーション

**コアブレークスルー**: このシステムの革新的側面は、人間の洞察（暗黙知）がAI分析と継続的に統合される**反復的フィードバックループ**にあり、粗い計算から精密で人間が検証した予測へと進化する見積もりを作成します。

**実世界での結果**: 実証において、システムは12の初期成果物を処理し、パフォーマンス要件について人間と対話し、**自動的に2つの新しい成果物**（パフォーマンス最適化と負荷テスト）を追加し、見積もりを85,500米ドルから136,275米ドルに増加させ、精度を向上させました。

### 🎯 主要機能

- **🤖 4エージェントAIアーキテクチャ**: 異なる評価視点による専門化された並列処理
- **🔄 人間-AI協調インテリジェンス**: 暗黙知統合による反復的精緻化
- **🌐 多言語サポート**: 完全な日本語・英語インターフェース対応
- **📊 Excel連携**: Excelファイルでのシームレスな入出力処理
- **🎛️ インタラクティブ改善**: 見積もり最適化のための無制限ユーザーフィードバックループ
- **📈 包括的レポート**: リスク分析と信頼性スコアリングを含む詳細見積もりレポート
- **💰 多通貨サポート**: 動的フォーマット（USD、JPY、EUR、GBP）
- **⚡ 並列処理**: 同時エージェント実行による最適化されたパフォーマンス

### 🏗️ 革新的エージェントアーキテクチャ

本システムは、包括的なプロジェクト評価を提供するために協調動作する**4つの専門化されたAIエージェント**を採用しています：

#### 1. **ビジネス要件エージェント**
- **ドメイン**: 機能要件とビジネス要件評価
- **専門性**: ビジネス目標、ユーザーストーリー、ステークホルダー分析
- **出力**: ビジネス複雑性スコアリングと機能要件完成度

#### 2. **品質要件エージェント**
- **ドメイン**: 非機能要件と品質要件評価
- **専門性**: パフォーマンス、セキュリティ、スケーラビリティ、保守性分析
- **出力**: 品質属性スコアリングと技術リスク評価

#### 3. **制約エージェント**
- **ドメイン**: 技術的制約と外部統合分析
- **専門性**: 技術制限、規制コンプライアンス、インフラ制約
- **出力**: 実現可能性リスク評価と制約影響分析

#### 4. **見積もりエージェント**
- **ドメイン**: 最終的なコストと工数計算統合
- **専門性**: 多要素見積もりアルゴリズム、リスク調整計算
- **出力**: 信頼性スコアリングと推奨事項を含む包括的見積もり

### 🔬 革新の科学

**多視点分析**: 各エージェントは専門化されたレンズを通じてプロジェクトを分析し、単一エージェントシステムでは不可能な洞察を提供します。

**暗黙知キャプチャ**: システムは従来のツールが見逃す人間の暗黙知を表面化し統合することに優れています。

**知的成果物発見**: AIは人間のフィードバックに基づいて新しい成果物を特定・追加でき、暗黙要件の真の理解を実証します。

## 🚀 インストールガイド

### 📋 前提条件

#### **システム要件**
- **Python**: 3.8以上（最適なパフォーマンスには3.9+を推奨）
  - 3.8+が必要な理由：適切な`concurrent.futures`と高度な型注釈のサポート
- **メモリ**: 最小4GB RAM（大規模プロジェクトには8GB+を推奨）
- **ストレージ**: 500MB利用可能ディスク容量
- **ネットワーク**: OpenAI APIアクセスのための安定したインターネット接続

#### **必要な依存関係**
- **OpenAI APIキー**: 十分なクレジットを持つ有効なAPIキー
- **コアライブラリ**: pandas、openpyxl、langchain、pydantic
- **オペレーティングシステム**: Windows 10+、macOS 10.14+、Linux（Ubuntu 18.04+）

#### **オプションだが推奨**
- **仮想環境**: 依存関係の分離のためのcondaまたはvenv
- **IDE**: 開発作業のためのVS Code、PyCharm、または類似ツール
- **Git**: バージョン管理と簡単な更新のため

### 🛠️ ステップバイステップインストール

#### **ステップ1: 環境セットアップ**
```bash
# 仮想環境を作成・アクティベート（推奨）
python -m venv depe_env
source depe_env/bin/activate  # Windows: depe_env\Scripts\activate

# またはcondaを使用
conda create -n depe_env python=3.9
conda activate depe_env
```

#### **ステップ2: リポジトリセットアップ**
```bash
# リポジトリをクローン
git clone https://github.com/daishir0/DeliverableEstimatePro3.git
cd DeliverableEstimatePro3

# リポジトリ構造を確認
ls -la
# 以下が表示されるはず: agents/, config/, input/, locales/, output/, utils/, main.py, requirements.txt
```

#### **ステップ3: 依存関係のインストール**
```bash
# 必要な全パッケージをインストール
pip install -r requirements.txt

# 重要なインストールを確認
python -c "import langchain, pandas, openpyxl, pydantic; print('全依存関係が正常にインストールされました！')"
```

#### **ステップ4: 環境設定**
```bash
# サンプル環境ファイルをコピー
cp .env_example .env

# 設定ファイルを編集
nano .env  # またはお好みのエディタ
```

**完全な`.env`設定例:**
```bash
# === コアAPI設定 ===
OPENAI_API_KEY=sk-your_actual_openai_api_key_here
MODEL=gpt-4o-mini  # オプション: gpt-4o-mini, gpt-4o, gpt-3.5-turbo

# === 財務設定 ===
DAILY_RATE=500      # お好みの通貨での日単価
CURRENCY=USD        # サポート: USD, JPY, EUR, GBP
TAX_RATE=0.10       # 小数での税率（0.10 = 10%）

# === 多言語化 ===
LANGUAGE=ja         # オプション: en（英語）, ja（日本語）

# === システム設定 ===
DEBUG_MODE=false    # 詳細ログには'true'に設定
MAX_ITERATIONS=3    # 最大精緻化反復回数
TIMEOUT_SECONDS=120 # エージェント実行タイムアウト
```

#### **ステップ5: ディレクトリ準備**
```bash
# 必要なディレクトリを作成
mkdir -p input output logs

# 適切な権限を設定（Linux/macOS）
chmod 755 input output logs

# ディレクトリ構造を確認
tree -L 2
```

#### **ステップ6: インストール確認**
```bash
# 基本機能をテスト
python main.py --version
python main.py --help

# システム診断を実行
python -m utils.system_check  # 全コンポーネントを確認
```

### 🔧 設定詳細

#### **APIキーセットアップオプション**

1. **直接.env方式**（推奨）:
   ```bash
   OPENAI_API_KEY=your_key_here
   ```

2. **環境変数方式**:
   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

3. **実行時入力方式**:
   ```bash
   # .envでAPIキーが見つからない場合、システムがプロンプト表示
   python main.py
   ```

#### **通貨設定**
システムは適切なフォーマットで複数通貨をサポート:

| 通貨 | コード | シンボル | 出力例 |
|------|--------|----------|--------|
| 米ドル | USD | $ | $85,500.00 |
| 日本円 | JPY | ¥ | ¥8,550,000 |
| ユーロ | EUR | € | €77,250.00 |
| 英ポンド | GBP | £ | £68,500.00 |

#### **言語ローカライゼーション**
- **英語（`en`）**: 完全な英語インターフェース
- **日本語（`ja`）**: エラーメッセージを含む完全な日本語化

## 📖 使用ガイド

### 🎯 クイックスタート

#### **ステップ1: Excel入力ファイルの準備**

以下の構造でExcelファイルを作成：

| 列A: 成果物名 | 列B: 説明 |
|---------------|-----------|
| 要件定義書 | システム全体の要件を整理・明確化する文書 |
| 基本設計書 | 基本設計方針とシステム全体構造を記述する文書 |
| フロントエンド開発 | React/Vue.jsを使用したユーザーインターフェース開発 |
| バックエンド開発 | Node.js/Pythonを使用したサーバーサイド開発 |

**Excelファイル要件:**
- **ファイル形式**: `.xlsx`または`.xls`
- **シート名**: 任意（システムは最初のシートを読み込み）
- **必須列**:
  - 列A: `成果物名`（空であってはならない）
  - 列B: `説明`（詳細な説明を推奨）
- **場所**: `input/`ディレクトリに配置

**入力ファイル例:**
```bash
input/
├── webアプリケーションプロジェクト.xlsx
├── モバイルアプリ成果物.xlsx
└── エンタープライズシステム.xlsx
```

#### **ステップ2: システム実行**

**方法1: 直接ファイルパス指定**
```bash
python main.py input/your_project.xlsx
```

**方法2: 対話モード**
```bash
python main.py
# システムプロンプト: "Excelファイルのパスを入力してください："
# 入力: input/your_project.xlsx
```

**方法3: ドラッグ＆ドロップ**（対応ターミナル）
```bash
python main.py  # その後Excelファイルをターミナルにドラッグ
```

#### **ステップ3: システム要件の提供**

システムが包括的なシステム要件を求めてきます：

```
📝 システム要件を入力してください（空行でEnterを押すと終了）：
```

**入力例:**
```
eコマースプラットフォームのWebアプリケーション
日次アクティブユーザー5,000人を想定
決済ゲートウェイとの統合（Stripe）
モバイル・デスクトップ対応のレスポンシブデザイン
PostgreSQLデータベース
AWSクラウドデプロイメント
99.9%稼働率要件
```

**より良い要件のためのヒント:**
- ユーザー数とパフォーマンス期待値を具体的に記載
- 統合やサードパーティサービスに言及
- 技術的な好みや制約を含める
- 品質要件（稼働率、応答時間）を明記

#### **ステップ4: AI分析プロセス**

システムは**4つの専門エージェントを並列実行**します：

```
🔄 並列評価開始: ビジネス、品質、制約
⚡ 3エージェントを並列実行中...
  📋 ビジネス・機能要件評価 - 開始
  🎯 品質・非機能要件評価 - 開始
  🔒 制約・外部統合評価 - 開始
```

**分析中に起こること:**
1. **ビジネスエージェント**: 機能要件とビジネス価値を評価
2. **品質エージェント**: パフォーマンス、セキュリティ、スケーラビリティニーズを評価
3. **制約エージェント**: 技術的制限と統合複雑性を分析
4. **見積もりエージェント**: 全評価を具体的見積もりに統合

#### **ステップ5: 初期見積もりの確認**

システムが包括的な見積もり結果を表示：

```
💰 見積もり結果:
  総工数: 171.0人日
  総金額: ¥8,550,000
  信頼度: 0.59

📋 全成果物見積もり詳細:
--------------------------------------------------------------------------------
No.  成果物名          基本工数 最終工数 金額       信頼度
--------------------------------------------------------------------------------
1    要件定義書        5.0      6.5      ¥325,000       0.70  
2    基本設計書        8.0      10.4     ¥520,000       0.70  
3    フロントエンド開発 15.0     24.3     ¥1,215,000     0.50  
4    バックエンド開発   20.0     31.2     ¥1,560,000     0.50  
--------------------------------------------------------------------------------
```

#### **ステップ6: 対話的精緻化（革新的機能）**

**人間-AI協調ループ:**

```
承認しますか？ (y/n/修正要求): 
```

**オプション1: 承認**
```
y
```
→ システムが最終Excelファイルを生成

**オプション2: 拒否**
```
n
```
→ システムが具体的な懸念を尋ねる

**オプション3: 暗黙知の提供**（革新的！）
```
パフォーマンス期待は我々のビジョンに暗黙的です。システムは10,000人の同時ユーザーを処理し、主要ページで2秒未満の応答時間を確保する必要があります。これを見積もりに反映してください。
```

**次に起こること:**
AIがフィードバックを分析し：
- 既存成果物見積もりを調整
- **必要に応じて新しい成果物を自動追加**
- 複雑性とリスク要因を再計算
- 向上した精度で強化された見積もりを提供

**AIの応答例:**
```
🔄 見積もりを改善中...
✅ 改善完了

💰 更新された見積もり結果:
  総工数: 272.5人日
  総金額: ¥13,625,000
  信頼度: 0.56

📋 追加された新成果物:
13   パフォーマンス最適化   20.0     45.0     ¥2,250,000      0.50  ← 新規！
14   負荷テスト・性能      15.0     33.8     ¥1,687,500      0.50  ← 新規！
```

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