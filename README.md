# 🧠 FinanceAnalystAgent

> An AI-powered multi-agent system for comprehensive financial data collection, extraction, and valuation analysis.

**FinanceAnalystAgent** combines specialized AI agents and financial tools to analyze SEC filings, stock data, and market sentiment — producing structured insights and sophisticated valuation outputs including DCF models.

---

## 🎯 Features

- **Multi-Agent Architecture** - Specialized agents working together for complex financial analysis
- **Automated Data Collection** - Fetch SEC filings, market data, and financial ratios
- **Intelligent Extraction** - Convert unstructured filings into structured data using LLM parsing
- **Valuation Models** - Built-in DCF, DDM, and comparative valuation calculators
- **Market Sentiment Analysis** - News headline aggregation and sentiment scoring

---

## 🏗️ System Architecture

```
                      ┌──────────────────────────┐
                      │  Financial Analyst Agent │
                      │   (Main Orchestrator)    │
                      └────────────┬─────────────┘
                                   │
             ┌─────────────────────┴─────────────────────┐
             │                                           │
┌──────────────────────────┐                 ┌──────────────────────────┐
│  Data Collector Agent    │                 │   Extractor LLM Agent   │
│  • Tool selection        │                 │   • Raw text parsing    │
│  • Data aggregation      │                 │   • Pydantic schemas    │
│  • Multi-source fetch    │                 │   • Structure validation│
└────────────┬─────────────┘                 └──────────────────────────┘
             │
   ┌─────────┴──────────────────────────┐
   │  Available Tools:                  │
   │  • get_sec_filings                 │
   │  • get_complete_stock_info         │
   │  • get_financial_ratios            │
   │  • get_news_headlines              │
   │  • get_sentiment_analysis          │
   │  • get_macro_data                  │
   │  • get_interest_rates              │
   └────────────────────────────────────┘
```

---

## ⚙️ Agents & Components

### 🎯 Financial Analyst Agent (Main)
The primary orchestrator that coordinates all analysis tasks.

**Capabilities:**
- Orchestrates multi-agent workflows
- Performs valuation calculations (DCF, DDM)
- Generates comparative analysis
- Synthesizes final investment insights

**Tools Available:**
- `calculate_dcf` - Discounted Cash Flow valuation
- `calculate_ddm` - Dividend Discount Model
- `compare_valuation` - Comparative metrics analysis

### 📊 Data Collector Agent
An autonomous agent with reasoning capabilities for intelligent data gathering.

**Tools:**
- `get_sec_filings` - Scrapes SEC EDGAR filings (10-K, 10-Q, 8-K)
- `get_complete_stock_info` - Real-time market data via yfinance
- `get_financial_ratios` - Calculates key financial metrics
- `get_news_headlines` - Aggregates recent news
- `get_sentiment_analysis` - Analyzes market sentiment
- `get_macro_data` - Fetches macroeconomic indicators

### 🔍 Extractor LLM Agent
Specialized in converting unstructured text into structured data.

**Features:**
- Parses SEC filings and financial reports
- Extracts key financial metrics
- Validates data against Pydantic schemas
- Structures sentiment and qualitative data

---

## 🔄 Example Workflow

```
1. User Request
   └─> "Analyze AAPL and provide valuation"
   
2. Analyst Agent (orchestrates)
   ├─> Calls Data Collector Agent
   │   ├─> Fetches SEC 10-K filing
   │   ├─> Gets current stock data
   │   └─> Retrieves financial ratios
   │
   ├─> Calls Extractor Agent
   │   ├─> Parses filing to JSON
   │   └─> Extracts revenue, cash flow, debt
   │
   └─> Performs Analysis
       ├─> Calculates DCF valuation
       ├─> Calculates DDM valuation
       └─> Generates investment summary
       
3. Output
   └─> Structured valuation report with recommendations
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/alyatwany/FinanceAnalystAgent.git
cd FinanceAnalystAgent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env

# Run the system
python main.py
```

### Basic Usage

```python
from agents import FinancialAnalystAgent

# Initialize the agent
analyst = FinancialAnalystAgent()

# Analyze a company
result = analyst.analyze("AAPL", analysis_type="full_valuation")

# View results
print(result.valuation_summary)
```

---

## 📂 Project Structure

```
FinanceAnalystAgent/
├── agents/
│   ├── analyst.py          # Main orchestrator agent
│   ├── collector.py        # Data collection agent
│   └─
