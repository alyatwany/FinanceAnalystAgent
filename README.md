🧠 FinanceAnalystAgent

FinanceAnalystAgent is an AI-powered multi-agent system for financial data collection, extraction, and valuation.
It combines specialized agents and tools to analyze filings, stock data, and market sentiment — producing structured insights and valuation outputs (e.g., DCFs).

🏗️ System Overview
                      ┌──────────────────────────┐
                      │  Financial Analyst Agent │  <-- main orchestrator (has tools + can call other agents)
                      └────────────┬─────────────┘
                                   │
             ┌─────────────────────┴─────────────────────┐
             │                                           │
┌──────────────────────────┐                 ┌──────────────────────────┐
│  Data Collector Agent    │  <-- full agent │   Extractor LLM/Agent   │
│  (chooses tools to fetch │                 │  (parses raw text →     │
│   and aggregate raw data)│                 │   Pydantic schemas)     │
└────────────┬─────────────┘                 └──────────────────────────┘
             │
     (tools the collector can choose from)
             │
   ┌─────────┴─────────┐
   │ get_sec_filings            │ (scrape/SEC API)
   │ get_complete_stock_info    │ (yfinance wrapper)
   │ get_financial_ratios       │
   │ get_news_headlines/sentiment│
   │ get_macro_data / rates      │
   └─────────────────────────────┘

⚙️ Agents and Tools
Financial Analyst Agent (Main)

Orchestrates all analysis

Uses:

DataCollectorAgent

Extractor LLM

calculate_dcf, calculate_ddm, compare_valuation, etc.

Data Collector Agent

Full agent with its own reasoning loop and tools:

get_sec_filings

get_complete_stock_info

get_financial_ratios

get_news_headlines/sentiment

get_macro_data

Extractor LLM Agent

Parses unstructured text → structured pydantic data

Used for filings, reports, and sentiment extraction

🧩 Example Flow

Analyst agent requests company valuation.

Data Collector fetches SEC filings + market data.

Extractor converts filings into structured JSON fields.

Analyst computes DCF/DDM valuations and summarizes results.

🚀 Quick Start
git clone https://github.com/alyatwany/FinanceAnalystAgent.git
cd FinanceAnalystAgent
pip install -r requirements.txt
echo "OPENAI_API_KEY=sk-..." > .env
python main.py

📂 Key Folders

agents/ — Analyst, Collector, Extractor logic

tools/ — valuation, data fetchers

schemas/ — Pydantic models

main.py — entry point

📈 Roadmap

Add Sentiment Agent

Add Report Generator (PDF/HTML)

Batch multi-ticker analysis

Caching + concurrency support
