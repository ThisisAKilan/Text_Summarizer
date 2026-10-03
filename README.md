# 🧠 Smart Study Notes Generator

A lightweight Python application leveraging pre-trained Generative AI models via the **Hugging Face `transformers`** pipeline to take paragraph inputs, generate concise study summaries and key bullet points, and calculate word reduction metrics in real-time.

---

## 📌 Features

- **Pre-trained Generative AI Model**: Uses `sshleifer/distilbart-cnn-12-6` abstractive summarization model via Hugging Face pipeline.
- **Word Reduction Metrics**: Calculates original word count, summary word count, and text reduction percentage.
- **Key Points Extraction**: Extracts key study bullet points automatically.
- **CLI & Web Interface**: Run via an interactive command-line interface or launch a modern glassmorphism web app UI.
- **Automated Test Suite**: Includes `test_notes_generator.py` to evaluate performance across 3 distinct domain paragraphs.
- **Deployment-Ready**: Prepared with `Dockerfile`, `Procfile`, and `render.yaml` for instant cloud deployment.

---

## 🚀 Local Usage

### 1. Installation
Ensure Python 3.8+ is installed. Install required packages:
```bash
pip install -r requirements.txt
```

### 2. Run CLI Application
```bash
python app.py
```
From the interactive menu:
- Input custom study paragraphs.
- Test sample paragraphs.
- Process all test samples and view reduction percentages.

### 3. Run Automated Tests
```bash
python test_notes_generator.py
```
This executes 3 test cases, records metrics, and saves results to `test_results.json`.

### 4. Launch Web App UI Locally
```bash
python web_server.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## ☁️ Deployment Instructions

### 1. Deploying to Render
1. Connect your GitHub repository `https://github.com/ThisisAKilan/Text_Summarizer.git` to [Render](https://render.com).
2. Click **New +** -> **Web Service**.
3. Select this repository.
4. Render will automatically detect `render.yaml` or use the following build settings:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python web_server.py`

### 2. Deploying to Hugging Face Spaces
1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Select **Docker** or **Streamlit/Gradio** SDK.
3. Push this repository's `Dockerfile` and python files to your Space.

### 3. Deploying using Docker Container
```bash
docker build -t smart-study-notes .
docker run -p 5000:5000 smart-study-notes
```

---

## 📊 Sample Test Results

| Test Paragraph | Domain | Original Words | Summary Words | Reduction % |
|---|---|:---:|:---:|:---:|
| **Paragraph 1** | Healthcare & AI | 109 | 52 | **52.29%** |
| **Paragraph 2** | Renewable Energy | 100 | 35 | **65.00%** |
| **Paragraph 3** | Social Media & Psychology | 87 | 32 | **63.22%** |

---

## 📝 Observations on Quality

- **Relevance**: The model retains essential core arguments and primary domain entities (e.g., MRI scans, photovoltaic solar costs, digital wellness).
- **Coherence**: Summaries maintain fluent grammar, logical structure, and zero sentence fragmentation.
- **Conciseness**: Consistently achieves over **50-65% text compression** while maintaining clear context for study note taking.
