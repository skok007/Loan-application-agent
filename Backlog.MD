📝 Backlog: Loan Application Agent System

This backlog captures enhancements and improvements to evolve the agent system from a workflow validator to a fully-featured, decisioning-capable tool.

⸻

🔧 Functional Enhancements

1. Affordability Assessment Tool
	•	Add fields: monthly_income, requested_amount, monthly_debt
	•	Create check_affordability.py as a tool
	•	Add logic to compute affordability ratio
	•	Load decisioning thresholds from config file (e.g. JSON)
	•	Display results in the UI and reports

2. Credit Risk Tool (Next)
	•	Simulate or ingest risk scores (e.g., A/B/C)
	•	Map scores to decision logic
	•	Add check_credit_risk.py as a function tool

3. Enhanced Explanation Agent
	•	Update explain_decision.py to include:
	•	Affordability rationale
	•	Credit risk tier logic
	•	SLA and fraud cross-analysis

4. Loan Decision Engine (Consolidated Recommendation)
	•	Add recommendation_engine.py that:
	•	Consumes all tool outputs
	•	Applies business rules
	•	Returns: Approve / Review / Reject

⸻

🖥️ UI Enhancements

5. Export Functionality in Streamlit
	•	Add button to export all summaries as:
	•	CSV
	•	Markdown
	•	JSON

6. Dynamic Filtering UI
	•	Allow filtering by:
	•	Fraud flagged
	•	SLA violation
	•	Recommendation type

7. Summary Dashboard View
	•	Add header stats:
	•	% Approved / Rejected
	•	SLA pass rate
	•	Avg income / requested amount

⸻

🔁 Workflow + Architecture

8. Agent Registry / Dispatcher
	•	Create a registry or factory for tools
	•	Dynamically route orchestration logic
	•	Easier to plug/unplug tools

9. Test Suite
	•	Unit tests for tools
	•	Golden test records with known outcomes

⸻

🔗 Integrations & Deployment

10. MCP (Zapier) Re-enable
	•	Restore report_agent.py with active webhook
	•	Confirm .env works
	•	Use Zapier for Slack or email delivery

11. Streamlit Deployment
	•	Push to Streamlit Cloud or Hugging Face Spaces
	•	Add logo and simple landing intro

⸻

💡 Exploration Ideas
	•	Ingest real credit bureau mock data
	•	Include optional document parsing (ID, income proof)
	•	Use LLM for justification generation instead of rule-based only