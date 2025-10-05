from langchain.tools import tool
import yfinance as yf

@tool
def get_complete_stock_info(ticker: str) -> dict:
    """Get comprehensive financial data for a stock including price history, dividends, 
    financials, and key metrics.
    
    Returns data needed for valuation models including:
    - Current price and historical prices
    - Dividend history and yield
    - Financial statements (income, balance sheet, cash flow)
    - Key ratios and metrics
    - Beta, market cap, and other company info
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        Dictionary with all available financial data
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get all available data
        info = stock.info
        dividends = stock.dividends
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        
        # Calculate dividend growth rate if available
        dividend_growth_rate = None
        if len(dividends) > 1:
            recent_divs = dividends.tail(5)  # Last 5 dividend payments
            if len(recent_divs) >= 2:
                oldest = recent_divs.iloc[0]
                newest = recent_divs.iloc[-1]
                years = (recent_divs.index[-1] - recent_divs.index[0]).days / 365.25
                if years > 0 and oldest > 0:
                    dividend_growth_rate = ((newest / oldest) ** (1 / years)) - 1
        
        # Package everything
        result = {
            # Price data
            "current_price": info.get("currentPrice"),
            "previous_close": info.get("previousClose"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
            
            # Dividend data
            "dividend_yield": info.get("dividendYield"),
            "dividend_rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio"),
            "dividend_history": dividends.to_dict() if not dividends.empty else {},
            "dividend_growth_rate": dividend_growth_rate,
            "ex_dividend_date": info.get("exDividendDate"),
            
            # Valuation metrics
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_book": info.get("priceToBook"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "enterprise_value": info.get("enterpriseValue"),
            "ev_to_revenue": info.get("enterpriseToRevenue"),
            "ev_to_ebitda": info.get("enterpriseToEbitda"),
            
            # Risk metrics
            "beta": info.get("beta"),
            "implied_volatility": info.get("impliedVolatility"),
            
            # Profitability metrics
            "profit_margins": info.get("profitMargins"),
            "operating_margins": info.get("operatingMargins"),
            "gross_margins": info.get("grossMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            
            # Growth metrics
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "revenue_per_share": info.get("revenuePerShare"),
            "earnings_per_share": info.get("trailingEps"),
            
            # Financial health
            "total_cash": info.get("totalCash"),
            "total_debt": info.get("totalDebt"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "free_cash_flow": info.get("freeCashflow"),
            "operating_cash_flow": info.get("operatingCashflow"),
            
            # Company info
            "market_cap": info.get("marketCap"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            
            # Analyst data
            "target_mean_price": info.get("targetMeanPrice"),
            "target_high_price": info.get("targetHighPrice"),
            "target_low_price": info.get("targetLowPrice"),
            "recommendation": info.get("recommendationKey"),
            "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
            
            # For DCF/valuation models - most recent financial data
            "total_revenue": financials.loc["Total Revenue"].iloc[0] if "Total Revenue" in financials.index else None,
            "ebitda": info.get("ebitda"),
            "net_income": financials.loc["Net Income"].iloc[0] if "Net Income" in financials.index else None,
            "total_assets": balance_sheet.loc["Total Assets"].iloc[0] if "Total Assets" in balance_sheet.index else None,
            "total_liabilities": balance_sheet.loc["Total Liabilities Net Minority Interest"].iloc[0] if "Total Liabilities Net Minority Interest" in balance_sheet.index else None,
            
            # Raw statements for detailed analysis
            "income_statement_latest": financials.iloc[:, 0].to_dict() if not financials.empty else {},
            "balance_sheet_latest": balance_sheet.iloc[:, 0].to_dict() if not balance_sheet.empty else {},
            "cashflow_latest": cashflow.iloc[:, 0].to_dict() if not cashflow.empty else {},
        }
        
        return result
        
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}
