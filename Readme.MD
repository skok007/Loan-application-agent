# 🧠 Loan Application Processing System using OpenAI Agent SDK

This project implements a modular, intelligent agent pipeline to automate loan application decision-making. Built with OpenAI's Agent SDK and powered by deterministic tools, it evaluates compliance (SLA), detects fraud, validates audit trails, explains decisions, and dispatches final reports using MCP-integrated channels (e.g., Slack, Zapier). A Streamlit UI enables CSV-based batch processing and summary review.

The decision logic is fully configurable via a JSON matrix, allowing you to tune how SLA, fraud, and affordability results determine the final recommendation.

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
- [ ] Re-enable and test Zapier MCP webhook in report_agent.py

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