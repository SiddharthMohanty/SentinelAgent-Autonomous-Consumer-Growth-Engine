# 🛡️ SentinelAgent: Autonomous Churn Engine

An event-driven, multi-agent AI system built to autonomously detect, evaluate, and mitigate B2B SaaS customer churn in real-time. 

Built with **LangGraph**, **LangChain**, and **Streamlit**, SentinelAgent shifts churn management from a reactive, offline batch process to a proactive, stateful AI orchestration pipeline.

## 📖 The Problem
Traditional churn mitigation relies on delayed analytics and rigid rule engines. When a high-value enterprise client encounters a critical outage, waiting for human support to triage the ticket results in lost revenue. However, granting an LLM unsupervised autonomy to issue financial concessions is a massive business risk.

## 💡 The Solution
SentinelAgent leverages a **Stateful Multi-Agent Architecture** to combine the semantic reasoning of an LLM with the deterministic safety of hardcoded business rules. It evaluates unstructured support tickets, cross-references them with hard CRM data (LTV, SLA Tier), and executes retention strategies. For high-stakes actions, it pauses execution via a **Human-in-the-Loop (HITL)** checkpointer, ensuring zero financial risk without dropping conversational context.

---

## ✨ Key Features
* **Multi-Agent Orchestration:** Specialized nodes for data ingestion, semantic reasoning, and business logic execution.
* **Deterministic Structured Outputs:** Utilizes Pydantic schemas to force strict, machine-readable JSON outputs from the LLM.
* **Human-in-the-Loop (HITL) Checkpointing:** LangGraph's `MemorySaver` safely freezes execution state for high-value accounts, awaiting human authorization before resuming.
* **Fail-Fast Conditional Routing:** Low-risk events are routed directly to termination, bypassing expensive compute and logic nodes.
* **Interactive UI:** A real-time Streamlit dashboard that streams LangGraph state transitions and visualizes the architectural node map.

---

## 🧠 System Architecture

The core logic executes through a cyclic, stateful graph:

1. **The Profiler Node:** Retrieves the Customer 360 profile (LTV, Tier, History) via a simulated DB tool.
2. **The Assessor Node (LLM):** Ingests the unstructured trigger event and CRM data to evaluate `Churn Risk` (Low/Medium/High) and generate a reasoning trace.
3. **The Proposer Node (Rules Engine):** Applies deterministic business logic. If LTV > $10,000 and Risk is High, it drafts a high-value retention package and flags `requires_approval = True`.
4. **The Executor Gate:** The graph pauses. If human approval is granted, the graph thread is rehydrated and completed.

---

## 📂 Project Structure

```text
sentinel-agent/
│
├── app.py                 # Streamlit frontend & UI logic
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API Keys)
│
├── data/
│   └── customers.json     # Mock structured CRM/Healthcare Data Fabric
│
└── core/                  # LangGraph Backend Orchestration
    ├── __init__.py
    ├── state.py           # Defines the central Pydantic/TypedDict state
    ├── workflow.py        # Graph compilation and routing edges
    │
    ├── nodes/             # Isolated Agent Logic
    │   ├── profiler.py    # Data ingestion
    │   ├── assessor.py    # LLM reasoning
    │   └── executor.py    # Deterministic strategy rules
    │
    └── tools/
        └── db_tools.py    # Tool definition for JSON database access

```


## Tech Stack

* Orchestration: LangGraph, LangChain
* LLM Provider: OpenAI (gpt-4o-mini)
* Frontend: Streamlit
* Data Validation: Pydantic