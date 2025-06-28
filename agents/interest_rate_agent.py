from agents import Agent, function_tool

try:
    import yfinance as yf
except ImportError:
    raise ImportError("yfinance is required. Please install it via pip.")

@function_tool(strict_mode=True)
def get_uk_interest_rate(wrapper=None, config=None):
    """
    Fetch the latest UK interest rate (SONIA) from Yahoo Finance.
    Returns a dict with rate, date, and source.
    """
    ticker = "^SONIA"
    data = yf.Ticker(ticker)
    hist = data.history(period="5d")
    if not hist.empty:
        latest_rate = hist['Close'][-1]
        latest_date = str(hist.index[-1].date())
        return {
            'rate': float(latest_rate),
            'date': latest_date,
            'source': 'Yahoo Finance (^SONIA)'
        }
    else:
        return {
            'error': 'No data found for UK interest rate ticker (^SONIA) on Yahoo Finance.'
        }

interest_rate_agent = Agent(
    name="UKInterestRateAgent",
    instructions="Fetch the current UK interest rate using yfinance.",
    tools=[get_uk_interest_rate],
    model="gpt-4o-mini",
    output_type=dict
)
