# Development Guide for DeliverableEstimatePro v3

## Overview

This guide provides comprehensive information for developers who want to contribute to, extend, or customize the DeliverableEstimatePro v3 system. It covers development environment setup, code architecture, testing procedures, and contribution guidelines.

## 🚀 Development Environment Setup

### Prerequisites
- **Python 3.8+** (3.9+ recommended for optimal performance)
- **Git** for version control
- **IDE** (VS Code, PyCharm, or similar with Python support)
- **OpenAI API Key** with sufficient credits for development testing

### Development Installation

#### 1. Repository Setup
```bash
# Clone the repository
git clone https://github.com/daishir0/DeliverableEstimatePro3.git
cd DeliverableEstimatePro3

# Create development branch
git checkout -b feature/your-feature-name
```

#### 2. Virtual Environment Setup
```bash
# Using venv (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using conda (alternative)
conda create -n depe_dev python=3.9
conda activate depe_dev
```

#### 3. Development Dependencies
```bash
# Install all dependencies including development tools
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Install in development mode
pip install -e .
```

#### 4. Environment Configuration
```bash
# Copy and configure environment file
cp .env_example .env

# Configure for development
cat > .env << EOF
OPENAI_API_KEY=your_development_api_key
MODEL=gpt-4o-mini
DAILY_RATE=500
CURRENCY=USD
TAX_RATE=0.10
LANGUAGE=en
DEBUG_MODE=true
MAX_ITERATIONS=3
TIMEOUT_SECONDS=120
EOF
```

#### 5. Development Tools Setup
```bash
# Install additional development tools
pip install black flake8 mypy pytest pytest-cov

# Set up pre-commit hooks (if available)
pre-commit install
```

### IDE Configuration

#### VS Code Settings (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        ".pytest_cache": true
    }
}
```

#### PyCharm Configuration
1. Set Python interpreter to your virtual environment
2. Enable Pydantic plugin for better model support
3. Configure code formatter to use Black
4. Set up pytest as the default test runner

## 🏗️ Code Architecture Understanding

### Project Structure
```
DeliverableEstimatePro3/
├── agents/                     # AI Agent implementations
│   ├── __init__.py
│   ├── base_ai_agent.py       # Base agent class
│   ├── pydantic_agent_base.py # Pydantic-based agent base
│   ├── business_requirements_agent_v2.py
│   ├── quality_requirements_agent.py
│   ├── constraints_agent.py
│   ├── estimation_agent_v2.py
│   └── pydantic_models.py     # Data model definitions
├── config/                     # Configuration management
│   └── i18n_config.py
├── input/                      # Input Excel files
├── locales/                    # Internationalization files
│   ├── en/
│   └── ja/
├── output/                     # Generated estimation results
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── currency_utils.py
│   ├── excel_processor.py
│   └── i18n_utils.py
├── tests/                      # Test suite (to be created)
├── main.py                     # Application entry point
├── workflow_orchestrator_simple.py  # Main orchestration logic
├── state_manager.py           # State management
├── requirements.txt
├── .env_example
└── README.md
```

### Key Design Patterns

#### 1. Agent Pattern
Each agent follows a consistent pattern:
```python
class ExampleAgent(PydanticAIAgent):
    """Agent documentation with purpose and capabilities"""
    
    def __init__(self):
        system_prompt = """Detailed agent prompt"""
        super().__init__("AgentName", system_prompt)
    
    def primary_method(self, input_data: str) -> Dict[str, Any]:
        """Main evaluation method with type hints"""
        # Input processing
        # Agent execution  
        # Error handling
        # Result formatting
        return result
```

#### 2. Pydantic Models
All data structures use Pydantic for validation:
```python
class ExampleResult(BaseModel):
    """Data model with comprehensive validation"""
    score: int = Field(ge=0, le=100, description="Score between 0-100")
    assessment: str = Field(min_length=1, description="Assessment text")
    recommendations: List[str] = Field(default_factory=list)
    
    @validator('score')
    def validate_score_range(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Score must be between 0 and 100')
        return v
```

#### 3. Error Handling Pattern
Consistent error handling across all components:
```python
def example_method(self) -> Dict[str, Any]:
    try:
        result = self._execute_core_logic()
        return {"success": True, **result}
    except ValidationError as e:
        return self._create_validation_error_response(e)
    except Exception as e:
        return self._create_error_response(str(e))
```

## 🧪 Testing Framework

### Test Structure
```
tests/
├── __init__.py
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests
│   ├── test_agents/
│   │   ├── test_business_agent.py
│   │   ├── test_quality_agent.py
│   │   ├── test_constraints_agent.py
│   │   └── test_estimation_agent.py
│   ├── test_utils/
│   │   ├── test_currency_utils.py
│   │   └── test_excel_processor.py
│   └── test_orchestrator.py
├── integration/                # Integration tests
│   ├── test_agent_integration.py
│   └── test_workflow_integration.py
├── fixtures/                   # Test data
│   ├── sample_input.xlsx
│   ├── sample_requirements.txt
│   └── expected_outputs/
└── performance/                # Performance tests
    └── test_parallel_execution.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=utils --cov-report=html

# Run specific test categories
pytest tests/unit/            # Unit tests only
pytest tests/integration/     # Integration tests only
pytest tests/performance/     # Performance tests only

# Run tests for specific module
pytest tests/unit/test_agents/test_business_agent.py

# Run tests in verbose mode
pytest -v

# Run tests with debugging
pytest -s --pdb
```

### Writing Tests

#### Unit Test Example
```python
import pytest
from unittest.mock import Mock, patch
from agents.business_requirements_agent_v2 import BusinessRequirementsAgentV2

class TestBusinessRequirementsAgent:
    
    @pytest.fixture
    def agent(self):
        return BusinessRequirementsAgentV2()
    
    @pytest.fixture
    def sample_requirements(self):
        return "Build an e-commerce platform with user authentication"
    
    def test_agent_initialization(self, agent):
        """Test agent proper initialization"""
        assert agent.agent_name == "BusinessRequirementsAgentV2"
        assert agent.system_prompt is not None
    
    @patch('agents.pydantic_agent_base.PydanticAIAgent.execute_with_pydantic')
    def test_evaluate_business_requirements_success(
        self, mock_execute, agent, sample_requirements
    ):
        """Test successful business requirements evaluation"""
        # Arrange
        mock_execute.return_value = {
            "success": True,
            "overall_score": 75,
            "business_purpose": {"definition_score": 80}
        }
        
        # Act
        result = agent.evaluate_business_requirements(sample_requirements)
        
        # Assert
        assert result["success"] is True
        assert "business_evaluation" in result
        assert result["business_evaluation"]["overall_score"] == 75
    
    def test_evaluate_business_requirements_validation_error(
        self, agent, sample_requirements
    ):
        """Test handling of validation errors"""
        # Test error handling scenarios
        pass
```

#### Integration Test Example
```python
import pytest
from workflow_orchestrator_simple import SimpleWorkflowOrchestrator

class TestWorkflowIntegration:
    
    @pytest.fixture
    def orchestrator(self):
        return SimpleWorkflowOrchestrator()
    
    @pytest.fixture
    def sample_deliverables(self):
        return [
            {"name": "Frontend Development", "description": "React-based UI"},
            {"name": "Backend Development", "description": "Node.js API"}
        ]
    
    def test_full_estimation_workflow(
        self, orchestrator, sample_deliverables
    ):
        """Test complete estimation workflow"""
        # Arrange
        requirements = "E-commerce platform with 1000 concurrent users"
        
        # Act
        result = orchestrator.execute_estimation(
            deliverables=sample_deliverables,
            system_requirements=requirements
        )
        
        # Assert
        assert result["success"] is True
        assert "estimation_result" in result
        assert len(result["estimation_result"]["deliverable_estimates"]) >= 2
```

### Test Fixtures and Mock Data
```python
# conftest.py
import pytest
import pandas as pd

@pytest.fixture
def sample_excel_data():
    """Sample Excel data for testing"""
    return pd.DataFrame({
        'Deliverable Name': [
            'Requirements Definition',
            'Frontend Development',
            'Backend Development'
        ],
        'Description': [
            'Project requirements document',
            'React-based user interface',
            'Node.js REST API'
        ]
    })

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "choices": [{
            "message": {
                "content": '{"success": true, "overall_score": 75}'
            }
        }]
    }
```

## 🔧 Development Workflows

### Adding a New Agent

#### 1. Create Agent Class
```python
# agents/new_agent.py
from typing import Dict, Any, List
from .pydantic_agent_base import PydanticAIAgent
from .pydantic_models import NewAgentResult

class NewSpecializedAgent(PydanticAIAgent):
    """
    New agent for specialized domain analysis
    
    Purpose: Describe the agent's specific role and capabilities
    """
    
    def __init__(self):
        system_prompt = """
        Your specialized agent system prompt here.
        Define the agent's role, responsibilities, and evaluation criteria.
        """
        super().__init__("NewSpecializedAgent", system_prompt)
    
    def evaluate_domain(self, input_data: str) -> Dict[str, Any]:
        """Main evaluation method"""
        try:
            result = self.execute_with_pydantic(input_data, NewAgentResult)
            
            if result.get("success"):
                return {
                    "success": True,
                    "new_evaluation": {k: v for k, v in result.items() 
                                     if k not in ["success", "_agent_metadata"]},
                    "_agent_metadata": result.get("_agent_metadata", {})
                }
            return result
            
        except Exception as e:
            return self._create_error_response(str(e))
```

#### 2. Define Pydantic Model
```python
# agents/pydantic_models.py
class NewAgentResult(BaseModel):
    """Data model for new agent results"""
    overall_score: int = Field(ge=0, le=100)
    domain_analysis: Dict[str, Any]
    recommendations: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "overall_score": 75,
                "domain_analysis": {"aspect_score": 80},
                "recommendations": ["Specific recommendation"]
            }
        }
```

#### 3. Update Orchestrator
```python
# workflow_orchestrator_simple.py
def _execute_parallel_evaluation(self, state: EstimationState) -> EstimationState:
    """Execute parallel evaluation with new agent"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # Updated worker count
        futures = [
            executor.submit(self._run_business_evaluation, state),
            executor.submit(self._run_quality_evaluation, state),
            executor.submit(self._run_constraints_evaluation, state),
            executor.submit(self._run_new_agent_evaluation, state)  # Add new agent
        ]
        
        for future in concurrent.futures.as_completed(futures, timeout=120):
            result = future.result()
            state.update(result)
    
    return state

def _run_new_agent_evaluation(self, state: EstimationState) -> EstimationState:
    """Execute new agent evaluation"""
    from agents.new_agent import NewSpecializedAgent
    
    agent = NewSpecializedAgent()
    result = agent.evaluate_domain(state.system_requirements)
    
    if result.get("success"):
        state.new_evaluation = result.get("new_evaluation")
    
    return state
```

#### 4. Write Tests
```python
# tests/unit/test_agents/test_new_agent.py
import pytest
from agents.new_agent import NewSpecializedAgent

class TestNewSpecializedAgent:
    
    @pytest.fixture
    def agent(self):
        return NewSpecializedAgent()
    
    def test_agent_initialization(self, agent):
        assert agent.agent_name == "NewSpecializedAgent"
    
    def test_evaluate_domain_success(self, agent):
        # Test implementation
        pass
```

### Extending Existing Agents

#### 1. Adding New Evaluation Dimensions
```python
# agents/business_requirements_agent_v2.py
def evaluate_business_requirements(self, project_requirements: str, ...):
    """Enhanced evaluation with new dimension"""
    
    # Add new evaluation context
    new_dimension_context = f"""
    [NEW EVALUATION DIMENSION]
    Please also evaluate: [specific new criteria]
    """
    
    enhanced_user_input = user_input + new_dimension_context
    
    # Execute with updated input
    result = self.execute_with_pydantic(enhanced_user_input, BusinessEvaluationResult)
    return result
```

#### 2. Updating Pydantic Models
```python
# agents/pydantic_models.py
class BusinessEvaluationResult(BaseModel):
    """Updated model with new fields"""
    overall_score: int = Field(ge=0, le=100)
    business_purpose: BusinessEvaluationDetail
    functional_requirements: BusinessEvaluationDetail
    new_dimension: BusinessEvaluationDetail  # New field
    
    # Migration method for backward compatibility
    @root_validator(pre=True)
    def handle_legacy_format(cls, values):
        if "new_dimension" not in values:
            values["new_dimension"] = {
                "definition_score": 50,
                "assessment": "Not evaluated in legacy format",
                "missing_elements": [],
                "recommendations": []
            }
        return values
```

### Customizing System Behavior

#### 1. Currency Support Extension
```python
# utils/currency_utils.py
class CurrencyFormatter:
    CURRENCY_SYMBOLS = {
        'USD': '$',
        'JPY': '¥',
        'EUR': '€',
        'GBP': '£',
        'CAD': 'C$',     # New currency
        'AUD': 'A$'      # New currency
    }
    
    def format_amount(self, amount: float, currency: str = None) -> str:
        """Enhanced formatting with new currencies"""
        currency = currency or self.currency
        symbol = self.CURRENCY_SYMBOLS.get(currency, currency)
        
        # Add new formatting rules
        if currency in ['CAD', 'AUD']:
            return f"{symbol}{amount:,.2f}"
        elif currency == 'JPY':
            return f"{symbol}{amount:,.0f}"
        else:
            return f"{symbol}{amount:,.2f}"
```

#### 2. Localization Addition
```bash
# Add new language support
mkdir -p locales/es
cp locales/en/* locales/es/

# Translate files
# locales/es/app.json
{
  "application": {
    "name": "DeliverableEstimatePro v3",
    "welcome": "¡Bienvenido al sistema de estimación!"
  }
}
```

## 🐛 Debugging and Troubleshooting

### Debug Mode Configuration
```bash
# Enable comprehensive debugging
DEBUG_MODE=true
TIMEOUT_SECONDS=300  # Increased timeout for debugging
```

### Logging Configuration
```python
# Add to main.py or orchestrator
import logging

logging.basicConfig(
    level=logging.DEBUG if os.getenv('DEBUG_MODE') == 'true' else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Common Debugging Techniques

#### 1. Agent Execution Debugging
```python
def debug_agent_execution(self, agent_name: str, input_data: str):
    """Debug specific agent execution"""
    logger.debug(f"Executing agent: {agent_name}")
    logger.debug(f"Input data: {input_data[:200]}...")  # First 200 chars
    
    start_time = time.time()
    result = agent.execute(input_data)
    execution_time = time.time() - start_time
    
    logger.debug(f"Agent {agent_name} completed in {execution_time:.2f}s")
    logger.debug(f"Result success: {result.get('success', False)}")
    
    return result
```

#### 2. Pydantic Validation Debugging
```python
def debug_pydantic_validation(self, data: Dict, model_class: Type[BaseModel]):
    """Debug Pydantic model validation"""
    try:
        validated_data = model_class(**data)
        logger.debug(f"Validation successful for {model_class.__name__}")
        return validated_data
    except ValidationError as e:
        logger.error(f"Validation failed for {model_class.__name__}: {e}")
        for error in e.errors():
            logger.error(f"  Field: {error['loc']}, Error: {error['msg']}")
        raise
```

#### 3. API Communication Debugging
```python
def debug_api_call(self, prompt: str, model: str):
    """Debug OpenAI API calls"""
    logger.debug(f"API Call - Model: {model}")
    logger.debug(f"API Call - Prompt length: {len(prompt)} characters")
    logger.debug(f"API Call - Prompt preview: {prompt[:100]}...")
    
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        logger.debug(f"API Response - Tokens used: {response.usage.total_tokens}")
        return response
    except Exception as e:
        logger.error(f"API Call failed: {str(e)}")
        raise
```

### Performance Profiling
```python
import cProfile
import pstats

def profile_estimation(deliverables, requirements):
    """Profile estimation performance"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Execute estimation
    result = orchestrator.execute_estimation(deliverables, requirements)
    
    profiler.disable()
    
    # Analyze results
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions
    
    return result
```

## 📋 Code Quality Standards

### Code Formatting
```bash
# Format code with Black
black --line-length 100 agents/ utils/ tests/

# Check code style with flake8
flake8 agents/ utils/ tests/ --max-line-length=100

# Type checking with mypy
mypy agents/ utils/ --ignore-missing-imports
```

### Documentation Standards
```python
def example_function(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Example function with comprehensive documentation.
    
    This function demonstrates the documentation standards for the project.
    All public functions and classes should have docstrings following this format.
    
    Args:
        param1 (str): The first parameter description
        param2 (int, optional): The second parameter with default value. Defaults to 10.
    
    Returns:
        Dict[str, Any]: Dictionary containing the results with keys:
            - success (bool): Whether the operation was successful
            - data (Any): The actual result data
            - metadata (Dict): Additional operation metadata
    
    Raises:
        ValueError: If param1 is empty or None
        TypeError: If param2 is not an integer
    
    Example:
        >>> result = example_function("test", 20)
        >>> print(result["success"])
        True
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    
    return {
        "success": True,
        "data": f"Processed {param1} with {param2}",
        "metadata": {"execution_time": 0.1}
    }
```

### Git Workflow
```bash
# Feature development workflow
git checkout main
git pull origin main
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new estimation dimension

- Add new evaluation criteria for technical complexity
- Update agent prompts and response models
- Add comprehensive tests for new functionality"

# Push and create pull request
git push origin feature/new-feature
```

### Commit Message Standards
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Scopes**: agents, utils, orchestrator, tests, docs

**Examples**:
```
feat(agents): add support for risk assessment scoring

fix(orchestrator): resolve parallel execution timeout issue

docs(readme): update installation instructions for Windows

test(agents): add integration tests for business agent
```

## 🤝 Contributing Guidelines

### Pull Request Process
1. **Fork and Branch**: Create feature branch from main
2. **Development**: Implement changes following coding standards
3. **Testing**: Add comprehensive tests for new functionality
4. **Documentation**: Update relevant documentation
5. **Quality Check**: Ensure all code quality checks pass
6. **Pull Request**: Create PR with detailed description

### Pull Request Template
```markdown
## Description
Brief description of the changes and their purpose.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated  
- [ ] Manual testing completed
- [ ] All tests pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Code is commented where necessary
- [ ] Documentation updated
- [ ] No breaking changes without version bump
```

### Code Review Guidelines
**For Reviewers**:
- Check functionality and logic correctness
- Verify test coverage and quality
- Ensure documentation is updated
- Validate performance implications
- Check for security considerations

**For Contributors**:
- Respond to feedback promptively
- Make requested changes thoughtfully
- Update tests when modifying logic
- Keep changes focused and atomic

## 🚀 Deployment and Release

### Local Development Deployment
```bash
# Run in development mode
python main.py input/test_project.xlsx

# Run with debug logging
DEBUG_MODE=true python main.py input/test_project.xlsx
```

### Production Deployment Preparation
```bash
# Install production dependencies only
pip install --no-dev -r requirements.txt

# Set production environment
DEBUG_MODE=false
TIMEOUT_SECONDS=120

# Run comprehensive tests
pytest tests/ --cov=agents --cov=utils

# Build distribution package
python setup.py sdist bdist_wheel
```

### Release Process
1. **Version Bump**: Update version in setup.py
2. **Changelog**: Update CHANGELOG.md with new features and fixes
3. **Tag Release**: Create git tag with version number
4. **Build Package**: Generate distribution packages
5. **Documentation**: Update documentation for new features

This development guide provides a comprehensive foundation for contributing to and extending the DeliverableEstimatePro v3 system. Follow these guidelines to maintain code quality, ensure compatibility, and facilitate collaboration.