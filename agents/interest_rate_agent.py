from agents import Agent, function_tool

try:
    import yfinance as yf
except ImportError:
    raise ImportError("yfinance is required. Please install it via pip.")

@function_tool(strict_mode=True)
def get_interest_rate(wrapper=None, config=None):
    """
    Fetch the latest interest rate (^TNX) from Yahoo Finance.
    Returns a dict with rate, date, and source.
    """
    ticker = "^TNX"
    data = yf.Ticker(ticker)
    hist = data.history(period="5d")
    if not hist.empty:
        latest_rate = hist['Close'][-1]
        latest_date = str(hist.index[-1].date())
        return {
            'rate': float(latest_rate),
            'date': latest_date,
            'source': 'Yahoo Finance (^TNX)'
        }
    else:
        return {
            'error': 'No data found for interest rate ticker (^TNX) on Yahoo Finance.'
        }

interest_rate_agent = Agent(
    name="InterestRateAgent",
    instructions="Fetch the current interest rate using yfinance.",
    tools=[get_interest_rate],
    model="gpt-3.5-turbo",
    output_type=dict
)
