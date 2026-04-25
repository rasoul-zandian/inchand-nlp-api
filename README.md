# 🧠 Product Review Summarization API (Persian NLP)

An intelligent API for analyzing and summarizing product reviews using NLP and LLMs.

---

## 🚀 Features

- Smart comment analysis (Persian language)
- LLM-powered summarization (OpenAI)
- Automatic pros & cons extraction
- Sentiment overview generation
- Cache system with hash validation
- Cost optimization (minimum comment threshold)
- Fallback mechanism for LLM failures

---

## 🏗 Architecture

- FastAPI (Backend)
- Service-based architecture
- File-based caching (JSON)
- Hash-based invalidation
- Modular design

---

## 📡 API Endpoints

### Health Check
GET /api/v1/health

### Get Summary
GET /api/v1/summary/{product_id}

### Summary Status
GET /api/v1/summary/{product_id}/status

### Force Refresh
POST /api/v1/refresh/{product_id}

---

## 🧠 How it works

1. Fetch product comments
2. Generate hash signature
3. Check cache validity
4. If valid → return cached summary
5. If not → generate new summary using LLM

---

## ⚙️ Setup

```bash
git clone ...
cd project
pip install -r requirements.txt