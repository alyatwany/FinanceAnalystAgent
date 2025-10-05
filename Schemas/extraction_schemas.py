from pydantic import BaseModel, Field
from typing import List,Optional


Schemas= ['get_sec_filings','get_news_sentiment']


class get_sec_filings(BaseModel):
    """Extracted financial data from SEC filing (10-K / 10-Q)."""

    revenue: Optional[str] = Field(None, description="Total revenue for the period")
    gross_profit: Optional[str] = Field(None, description="Gross profit for the period")
    operating_income: Optional[str] = Field(None, description="Operating income or EBIT")
    net_income: Optional[str] = Field(None, description="Net income for the period")
    eps_basic: Optional[str] = Field(None, description="Earnings per share, basic")
    eps_diluted: Optional[str] = Field(None, description="Earnings per share, diluted")

    total_assets: Optional[str] = Field(None, description="Total assets at end of period")
    total_liabilities: Optional[str] = Field(None, description="Total liabilities at end of period")
    total_equity: Optional[str] = Field(None, description="Total stockholders' equity")
    current_assets: Optional[str] = Field(None, description="Total current assets")
    current_liabilities: Optional[str] = Field(None, description="Total current liabilities")
    cash_and_equivalents: Optional[str] = Field(None, description="Cash and cash equivalents at end of period")
    long_term_debt: Optional[str] = Field(None, description="Total long-term debt")

    operating_cash_flow: Optional[str] = Field(None, description="Net cash provided by operating activities")
    investing_cash_flow: Optional[str] = Field(None, description="Net cash used in investing activities")
    financing_cash_flow: Optional[str] = Field(None, description="Net cash used in financing activities")
    capital_expenditures: Optional[str] = Field(None, description="Payments for property, plant, and equipment")
    free_cash_flow: Optional[str] = Field(None, description="Operating cash flow minus capital expenditures")

    roe: Optional[str] = Field(None, description="Return on equity")
    roa: Optional[str] = Field(None, description="Return on assets")
    debt_to_equity: Optional[str] = Field(None, description="Debt-to-equity ratio")
    current_ratio: Optional[str] = Field(None, description="Current ratio")
    pe_ratio: Optional[str] = Field(None, description="Price-to-earnings ratio")
    pb_ratio: Optional[str] = Field(None, description="Price-to-book ratio")

    risk_factors: Optional[List[str]] = Field(None, description="Key risk factors mentioned in the filing")
    mda_highlights: Optional[List[str]] = Field(None, description="Key points from Management Discussion & Analysis section")
    business_overview: Optional[str] = Field(None, description="Summary of the business section")
    outlook_summary: Optional[str] = Field(None, description="Forward-looking statements or company outlook")
    
    filing_date: Optional[str] = Field(None, description="Date of the filing")
    form_type: Optional[str] = Field(None, description="Filing type (10-K, 10-Q, etc.)")
    company_name: Optional[str] = Field(None, description="Name of the company")
    ticker: Optional[str] = Field(None, description="Stock ticker symbol")


class NewsSentimentSchema(BaseModel):
    """Structured sentiment data extracted from financial news articles"""
    
    headline: Optional[str] = Field(None, description="Title of the news article")
    source: Optional[str] = Field(None, description="Name of the news outlet or publisher")
    date: Optional[str] = Field(None, description="Publication date of the article")
    sentiment_score: Optional[float] = Field(None, description="Overall sentiment score, ranging from -1 (negative) to +1 (positive)")
    sentiment_label: Optional[str] = Field(None, description="Categorical sentiment label such as 'positive', 'neutral', or 'negative'")
    related_tickers: Optional[List[str]] = Field(None, description="List of stock tickers mentioned in the article")
    impact_estimation: Optional[str] = Field(None, description="Estimated qualitative impact on company or market (e.g., 'high', 'medium', 'low')")
    summary: Optional[str] = Field(None, description="Brief summary of the article content")
    key_entities: Optional[List[str]] = Field(None, description="People, companies, or organizations mentioned in the article")
    topics: Optional[List[str]] = Field(None, description="Key topics or themes discussed (e.g., 'earnings', 'merger', 'lawsuit')")

