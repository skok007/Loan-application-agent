from agents import Agent

recommendation_agent = Agent(
    name="RecommendationAgent",
    instructions=(
        "You are a loan decision assistant. Based on SLA compliance and fraud risk results, "
        "write a concise recommendation:\n"
        "- If there are SLA violations, suggest process review.\n"
        "- If fraud is flagged, advise escalation.\n"
        "- Otherwise, recommend approval consideration.\n"
        "Use a professional tone."
    ),
    model="gpt-4o-mini",
    output_type=str
)