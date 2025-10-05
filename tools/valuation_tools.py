from langchain.tools import tool
import yfinance as yf
from typing import Optional
import pandas as pd


@tool
def calculate_dcf(
    cash_flows: list[float],
    discount_rate: float,
    terminal_growth_rate: float = 0.02
) -> dict:
    """
    Calculate the intrinsic value of a company using the Discounted Cash Flow (DCF) model.

    Args:
        cash_flows: list of projected free cash flows (e.g., 5 years)
        discount_rate: required rate of return (as decimal, e.g., 0.1 for 10%)
        terminal_growth_rate: perpetual growth rate after projection period (default 2%)

    Returns:
        dict with present_value_per_share and intermediate steps
    """
    if not cash_flows or discount_rate <= terminal_growth_rate:
        return {"error": "Invalid inputs — check cash flows or rates."}

    pv_sum = 0
    for i, cf in enumerate(cash_flows, start=1):
        pv_sum += cf / ((1 + discount_rate) ** i)

    terminal_value = cash_flows[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
    terminal_pv = terminal_value / ((1 + discount_rate) ** len(cash_flows))

    total_value = pv_sum + terminal_pv
    return {
        "present_value": round(total_value, 2),
        "terminal_value": round(terminal_value, 2),
        "explanation": f"Discounted {len(cash_flows)} years of cash flow at {discount_rate*100:.1f}% with terminal growth {terminal_growth_rate*100:.1f}%."
    }


@tool
def calculate_ddm(
    dividend_next_year: float,
    growth_rate: float,
    discount_rate: float
) -> dict:
    """
    Calculate stock value using the Dividend Discount Model (DDM).

    Args:
        dividend_next_year: expected dividend for next year
        growth_rate: expected annual dividend growth rate (decimal)
        discount_rate: required rate of return (decimal)

    Returns:
        dict with estimated intrinsic value
    """
    if discount_rate <= growth_rate:
        return {"error": "Discount rate must be greater than growth rate."}

    intrinsic_value = dividend_next_year / (discount_rate - growth_rate)
    return {
        "intrinsic_value": round(intrinsic_value, 2),
        "explanation": f"Calculated using dividend {dividend_next_year}, growth {growth_rate*100:.1f}%, discount {discount_rate*100:.1f}%."
    }

@tool
def calculate_comparable_valuation(
    company_metric: float,
    peer_avg_multiple: float) -> dict:
    """
    Estimate valuation based on comparable company multiples.

    Args:
        company_metric: the company's own metric (e.g., earnings per share)
        peer_avg_multiple: average multiple from peer group (e.g., P/E ratio)

    Returns:
        dict with estimated value and context
    """
    estimated_value = company_metric * peer_avg_multiple
    return {
        "estimated_value": round(estimated_value, 2),
        "explanation": f"Used peer average multiple of {peer_avg_multiple}x on company metric {company_metric}."
    }



