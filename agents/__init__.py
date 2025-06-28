from typing import TypeVar, Generic, Callable, Any, List, Optional
from dataclasses import dataclass
from functools import wraps
import asyncio
from openai import AsyncOpenAI
import os

# Type variable for context
T = TypeVar('T')

@dataclass
class ModelSettings:
    tool_choice: str = "auto"
    temperature: float = 0.0
    max_tokens: Optional[int] = None

class RunContextWrapper(Generic[T]):
    def __init__(self, context: T):
        self.context = context

def function_tool(strict_mode: bool = True):
    """Decorator to mark a function as a tool"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapped(*args, **kwargs):
            # For direct function calls, just execute the function normally
            return func(*args, **kwargs)
        wrapped._is_tool = True
        wrapped._strict_mode = strict_mode
        wrapped._original_func = func  # Store the original function
        return wrapped
    return decorator

class Agent(Generic[T]):
    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4-0613",
        tools: List[Callable] = None,
        model_settings: ModelSettings = None,
        output_type: type = str,
        mcp_servers: List = None
    ):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools or []
        self.model_settings = model_settings or ModelSettings()
        self.output_type = output_type
        self.mcp_servers = mcp_servers or []
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def run(self, input: str, context: T = None) -> Any:
        """
        Run the agent using the first available tool and return the result.
        This simulates the behavior of a deterministic function-calling agent.
        The result includes a fixed application structure.
        """
        wrapper = RunContextWrapper(context) if context else None

        # Execute the first tool in the agent's tool list
        if self.tools:
            tool = self.tools[0]
            if getattr(tool, '_is_tool', False):
                try:
                    tool_result = tool(wrapper) if wrapper else tool()
                except Exception as e:
                    tool_result = f"[Error while running tool: {e}]"
            else:
                tool_result = "[Tool is not properly decorated with @function_tool]"
        else:
            tool_result = f"[Agent {self.name} has no tools configured]"

        # Build the required structure
        result = {
            "application_id": "APP-LOCAL-001",
            "submitted_time": "2025-06-01T09:00:00",
            "reviewed_time": "2025-06-01T09:30:00",
            "approved_time": "2025-06-01T10:00:00",
            "rejected_time": None,
            "processing_steps": {"KYC": 72, "CreditCheck": 28, "FinalApproval": 35},
            "flagged_for_fraud": False,
            "monthly_income": 5000,
            "monthly_costs": 2000,
            "requested_amount": 25000,
            "monthly_debt": 400,
            "tool_result": tool_result
        }

        # Return a compatible mock object with .final_output
        return type('Response', (), {'final_output': result})()