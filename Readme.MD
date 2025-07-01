# 🧠 Loan Application Processing System using OpenAI Agent SDK

This project implements a modular, intelligent agent pipeline to automate loan application decision-making. Built with OpenAI's Agent SDK and powered by deterministic tools, it evaluates compliance (SLA), detects fraud, validates audit trails, explains decisions, and dispatches final reports using MCP-integrated channels (e.g., Slack, Zapier). A Streamlit UI enables CSV-based batch processing and summary review.

The decision logic is fully configurable via a JSON matrix, allowing you to tune how SLA, fraud, and affordability results determine the final recommendation.
---

## ❗ Problem Statement

There is a backlog of loan applications that are currently manually checked, and this is slowing down the loan approval process.

## 💡 Proposed Solution

To create an agent workflow that will process loan applications agentically and autonomously.
---

## 📋 Setup & Run Instructions

### ✅ Quick Start

```bash
git clone <your-repo-url>
cd loan_decision_pipeline
cp .env.example .env  # Add your keys here
pip install -r requirements.txt
```

### ▶️ CLI Usage
```bash
python eval_runner.py     # Runs full pipeline on all records in CSV
python main_runner.py     # Tests single application (optionally sends to MCP)
```

### 🖥 Run the Streamlit UI
```bash
streamlit run ui/streamlit_app.py
```
Then open your browser to: http://localhost:8501

Upload `loan_applications_large.csv` or similar to process and view summaries.

---

## ✅ Use Case

Monitor the journey from loan application submission to approval/rejection. The system:
- Detects SLA violations
- Flags fraud risk
- Validates step-wise process compliance
- Explains decisions
- Sends summaries to relevant stakeholders

---

## 📋 User Stories

### 1. **Loan Officer – SLA Monitoring**
> "As a loan officer, I want to be notified if any loan processing step exceeds the SLA limit so I can take action."

### 2. **Risk Analyst – Fraud Pattern Detection**
> "As a risk analyst, I want to know if the application matches known fraud signals to intervene early."

### 3. **Compliance Manager – Audit Trail Check**
> "As a compliance officer, I need to ensure that loan steps follow a valid, sequential flow."

### 4. **Business Lead – Summary & Insights**
> "As a business lead, I want to receive clear summaries of loan processing outputs and their explanations."

---

## 🌟 Test Criteria

| Metric         | Description                                                   |
|----------------|---------------------------------------------------------------|
| **Completeness** | Each user story has functional logic mapped in code          |
| **Validity**     | Output reflects realistic data, behavior, and edge cases     |
| **Coverage**     | Handles delays, no-fraud, fraud, sequence errors, etc.       |

---

## ⚙️ Technical Requirements

### ✅ Technologies Used
- **OpenAI Agent SDK**: For building deterministic function-calling agents
- **Function Tools**: Logic-bound utilities called by agents
- **Multichannel Plugin (MCP)**: Sends final output via external systems (Zapier, Slack, etc.)
- **Streamlit**: For interactive UI to upload, process, and view summaries
- **Python 3.10+**, `aiohttp`, `pandas`, `dotenv`, `streamlit`

---

## 🧹 How It Works – End-to-End Flow

1. **Input**: Loan applications (from CSV/json)
2. **Context Prep**: Convert record into `LoanApplicationJourney` dataclass
3. **Tool Execution via Orchestration**:
   - `check_sla()` → SLA compliance
   - `check_fraud()` → fraud signal check
   - `check_audit_trail()` → event sequencing validation
   - `explain_decision()` → justification summary
   - `synthesize_summary()` → final report format
4. **Orchestration is managed by `orchestrate_application()`** in `orchestrator_pipeline.py`
5. **UI** is implemented in Streamlit (`streamlit_app.py`) and prints summaries
6. **ReportAgent** optionally sends the result via MCP

---

## 🛡️ Agent Architecture Diagram
```
+---------------------------+
|   LoanApplicationJourney  |
+---------------------------+
              |
              v
+-------------------------------+
| orchestrate_application()     |
+-------------------------------+
 |     |        |       |     |
 v     v        v       v     v
SLA  Fraud   Audit   Explain  
Check Check  Trail   Reason   
 |     |        |       |     
 +-----+--------+-------+-----+
              |
              v
     +------------------------+
     |  synthesize_summary()  |
     +------------------------+
              |
              v
     +------------------------+
     |    ReportAgent (MCP)   |
     +------------------------+
```

> 🧠 Agent Orchestration can be extended to include GPT-driven routing and external MCP hooks for affordability, fraud, and credit scoring.

---

## 📄 Example Output

📩 **Loan Decision Summary**
- Application ID: APP-0042
- SLA Result: SLA violations in: KYC, FinalApproval
- Fraud Result: ⚠️ Fraud flag triggered
- Recommendation: Recommend manual review due to delays and risk.
- Explanation: Application shows SLA violations and matches fraud patterns.
- Timestamp: 2025-06-27T11:04:00

---

## 🧠 Why OpenAI Agent SDK?

This project uses deterministic agents built on OpenAI's Agent SDK:
- **Function Tools**: Logic tools exposed via decorators to agents
- **Context Objects**: Rich data models (e.g. `LoanApplicationJourney`) for structured reasoning
- **Orchestration**: Deterministic execution handled via an explicit orchestration function (`orchestrate_application()`), improving clarity and modularity over `Runner.run()` abstraction.

This ensures **predictability**, **auditability**, and easy integration with external systems (via MCP).

---

## 👥 Responsibilities (Group 5)

| Team Member       | Responsibility                                 |
|-------------------|------------------------------------------------|
| Steven Kok        | System architecture, orchestrator, report/MCP  |
| [Teammate A]      | Function tool dev, audit & fraud logic         |
| [Teammate B]      | Report formatting, evaluation loop             |

---

## 📁 File-by-File Breakdown

### `data_model.py`
Defines:
- `LoanApplicationJourney`: per-record context
- `TrendAnalysisResult`: report object passed to MCP

### `tools/`
- `check_sla.py`: SLA violations
- `check_fraud.py`: fraud rule
- `check_audit_trail.py`: step-sequence validation
- `explain_decision.py`: narrative summary
- `synthesize_summary.py`: final message builder

### `agents/`
- `sla_agent.py`, `fraud_agent.py`: single-purpose tool agents
- `recommendation_agent.py`: LLM-only fallback
- `orchestrator_agent.py`: older agent-based implementation (replaced by functional orchestration)
- `report_agent.py`: dispatches final report via MCP

### `orchestrator_pipeline.py`
Core logic for orchestrating all tools into a final decision summary.
Used by both the CLI and main runner.

### `main_runner.py`
Single-record runner with optional MCP integration.
Used for testing/debugging individual loan journeys.

### `eval_runner.py`
Batch evaluation from CSV using `orchestrate_application()`.
Prints summaries directly to console (no MCP).

### `ui/streamlit_app.py`
Streamlit app with upload form, processes CSV, renders all results sequentially.

### `.env.example`
Your keys: `OPENAI_API_KEY`, `MCP_SERVER_URL_SSE`

### `requirements.txt`
```txt
openai
pandas
python-dotenv
aiohttp
pydantic
streamlit
```

---

## ▶️ Getting Started

```bash
git clone <your-repo-url>
cd loan_decision_pipeline
cp .env.example .env  # Add your keys here
pip install -r requirements.txt
python eval_runner.py
```

To launch the Streamlit UI:
```bash
streamlit run ui/streamlit_app.py
```

---

## ✅ Status
- [x] Steps 1–6 of BRIDGE AI Framework implemented and tested with synthetic data
- [x] Step 7: Streamlit UI for batch processing and display
- [ ] Step 8: Begin MCP-integrated Agent Extension (LLM + External Service Hooks)

## 🚧 TODO: Post-MVP Enhancements

- [ ] 🔗 **Re-enable MCP / Zapier Integration**
  - File: `agents/report_agent.py`
  - Un-comment the `MCPServerSse` block
  - Restore `mcp_servers=[mcp_server]` in the `report_agent` definition
  - Make sure `.env` contains a working `MCP_SERVER_URL_SSE` pointing to your webhook

- [ ] 💬 Add WhatsApp or Email delivery via Zapier

- [ ] ⚠️ Add Affordability and Risk-Based Decisioning
  - Implement tools for affordability score, credit risk evaluation
  - Enhance `explain_decision()` to incorporate those features
  - Enable richer business rules for automated approvals or escalation

- [ ] 🎨 UI Enhancements
  - Downloadable report exports (CSV, Markdown)
  - Collapsible sections or visual indicators (e.g., color-coded cards)
  - MCP status logging or alert dashboard

- [ ] 🧠 Final Decision Recommendation
  - Add `final_decision` to `TrendAnalysisResult`
  - Evaluate tool output (SLA, fraud, affordability) against matrix
  - Store matrix in config.json and use `get_recommendation_matrix()`
  - Append decision to summaries (CLI, UI)

- [ ] 🤖 GPT-Augmented Agent
  - Use OpenAI's Agent SDK to dynamically route tool calls based on input
  - Integrate `Agent.run()` flow for GPT-based prompting

- [ ] 🔗 Advanced MCP Integrations
  - Build an MCP server that can call external credit bureau APIs (e.g., UK provider)
  - Allow toggling between deterministic rules vs. MCP lookup
  - Route this logic through a `recommendation_agent.py` that can use either:
    - Local `check_affordability()` tool
    - External data via MCP
  - Expose configuration via `.env` or UI toggle

---

## 📐 Architecture Refactor Roadmap

To evolve this project into a scalable, production-grade, multi-agent orchestration platform, the following architecture and design enhancements are proposed:

### 🔁 Multi-Agent Extensibility

- Design a centralized `agent_registry.py` to define:
  - Agent name (e.g., "secured_lending", "mortgage_lending")
  - Associated orchestration logic (e.g., `orchestrate_secured()`)
  - Routing type: `"deterministic"`, `"mcp"`, or `"gpt"`-driven
- Allow new agents to be added by appending a single entry to the registry

### 🌐 MCP Service Expansion

- Create MCP Server variants per agent type:
  - `SecuredLoanMCP`, `MortgageLoanMCP`, etc.
- Each agent can optionally use:
  - Deterministic tool
  - External data (credit bureau, valuation APIs) via MCP
- Support toggle per environment via `.env` or config flag

### 🏷️ Lending Type Enrichment

- Refactor input data model (`LoanApplicationJourney`) to include:
  - `loan_type`: one of `["overdraft", "personal_loan", "credit_card", "car_loan", "mortgage"]`
- Update `orchestrator_pipeline` to route logic by loan type

### 🔌 Tool-as-API Pattern

- Refactor tools to be exposed as lightweight REST APIs
- Agents call tools via HTTP (use `aiohttp` client)
- Benefits:
  - Improves isolation and debugging
  - Enables microservice deployment
  - Allows horizontal scaling

### 📡 Orchestration State Exposure

- Provide orchestration logs/status via API endpoint
- Track tool calls, inputs, outputs, and decisions
- Allow front end to poll/report orchestration journey

### ☁️ Scalable Infrastructure Design

- Define container strategy (Docker)
  - One container per agent
  - One container per tool
- Optional: use Kubernetes for orchestration
- Optional: use Redis/pubsub for async tool messaging

### 🧑‍💼 Multi-User Experience

- Define user roles:
  - Loan applicant: submits one record
  - Loan processor: sees queue of loans to evaluate
- Split UI into:
  - Application portal (submission)
  - Underwriter dashboard (streamlit or Flask)
- Use session state to manage user role and views

---

## 🧱 New Backlog (Architecture Phase)

| ID | Task | Type |
|----|------|------|
| A1 | Create `agent_registry.py` with routing config | 🧠 Agent Infra |
| A2 | Refactor `orchestrator_pipeline.py` to use agent registry | 🔁 Orchestration |
| A3 | Add `loan_type` field to `LoanApplicationJourney` | 📦 Data Model |
| A4 | Refactor all tools to be REST services (`aiohttp` or Flask) | 🛠 Tool API |
| A5 | Create `orchestration_state.py` to track execution events | 🔍 Observability |
| A6 | Build MCP server variations per agent type | 🌐 MCP Infra |
| A7 | Add toggle in `.env` for MCP vs Local tool | ⚙️ Config |
| A8 | Add basic Streamlit user role management | 👥 UI |
| A9 | Create separate views for applicant vs processor | 🖼 UI |
| A10 | Dockerize each tool and agent | ☁️ Infra |
| A11 | Define MVP Kubernetes spec (optional) | ☁️ Infra |

---