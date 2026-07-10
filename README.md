# Smart Stadium & Tournament Operations Engine 🏟️⚡

A high-performance, production-ready asynchronous triage and operational parsing engine designed to segment unstructured match-day stadium logs and automatically execute tactical dispatch routing under heavy traffic conditions.

## 🏗️ Core Architecture & Engineering Trade-offs

### 1. High-Speed Regex Segmentation Layer (Day 2)
* **Design Choice:** Utilizes deterministic regular expressions (`re`) and `pdfplumber` for initial data stream slicing instead of hitting an LLM immediately.
* **Trade-off/Benefit:** Achieves a **$0.00 compute cost** for initial processing and drops latency to sub-millisecond speeds, protecting the system from heavy token usage and rate limits during massive crowd surges.

### 2. Logarithmic Severity Scoring Matrix Engine (Day 3)
* **Design Choice:** Implements a mathematically bounded scoring engine ($10.00$ to $100.00$) driven by explicit keyword weights and a logarithmic saturation curve:
  $$\text{Score} = \text{Base} + (\beta_1 \cdot \ln(x_{\text{critical}} + 1)) + (\beta_2 \cdot \ln(x_{\text{moderate}} + 1))$$
* **Trade-off/Benefit:** Prevents malicious actors from faking emergencies via "keyword stuffing" (e.g., repeating the word "fire" 100 times), providing stable threat assessments to commanders.

### 3. Serverless AI Operational Reasoner with High-Availability Failover (Day 4)
* **Design Choice:** Integrates Meta's Llama-3-8B-Instruct via Hugging Face's serverless inference API alongside an integrated code-driven structural fallback layer.
* **Trade-off/Benefit:** If network conditions degrade or API limits are reached, the system instantly slips into an automated backup mode, guaranteeing a structured, clean operational directive packet without throwing a 500 server crash code.

---

## 🛠️ Technical Stack & Dependencies
* **Core Language:** Python 3.11+
* **Framework:** FastAPI (Asynchronous ASGI Server Engine)
* **Environment & Package Manager:** `uv` (Fast, isolated environment orchestration)
* **Extraction & AI:** `pdfplumber`, `requests`, `python-dotenv`

---

## 🚀 Local Installation & Quickstart Guide

### 1. Initialize and Setup Runtime Environments
Ensure you have `uv` or standard Python installed. Run these setup chains:
```bash
# Spin up environment and load tools
uv venv
.\venv\Scripts\Activate.ps1
uv pip install -r requirements.txt