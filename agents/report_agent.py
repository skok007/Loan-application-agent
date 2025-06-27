from agents import Agent, ModelSettings
from tools.synthesize_summary import synthesize_summary
# from agents.mcp import MCPServerSse
import os
from utils.load_env import setup_environment

setup_environment()

# TODO: Re-enable this once Zapier webhook is ready
# mcp_url = os.environ.get("MCP_SERVER_URL_SSE")
# mcp_server = MCPServerSse(name="LoanReportMCP", params={"url": mcp_url})

report_agent = Agent(
    name="ReportAgent",
    instructions="Use the summary tool to produce the final loan report. Do NOT send it externally.",
    model="gpt-4-0613",
    tools=[synthesize_summary],
    # mcp_servers=[mcp_server],  # <-- Temporarily disabled for local testing
    model_settings=ModelSettings(tool_choice="required"),
    output_type=str
)