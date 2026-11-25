# CareerLens — AI Career Intelligence & Job Matching Platform

An AI-powered resume analysis and job matching platform that helps users understand their resume quality, identify relevant skills, and discover job opportunities that align with their profiles.

🌐 **Live Demo:** [CareerLens – Try the Application](https://ai-career-job-matching-platform.onrender.com/)

💻 **GitHub Repository:** [AI-Career-Job-Matching-Platform](https://github.com/lohitakshajoshi28/AI-Career-Job-Matching-Platform)

---

## 🚀 Overview

CareerLens is a web-based career intelligence platform designed to simplify the job search process.

Users can upload their resumes in PDF format or paste resume text to receive an ATS-style analysis and discover relevant job opportunities.

The application combines Natural Language Processing (NLP) techniques, TF-IDF vectorization, cosine similarity, and rule-based scoring to analyze resumes and rank matching job descriptions.

## ✨ Key Features

### 📄 Resume Analysis
- Upload resumes in PDF format.
- Paste resume text directly into the application.
- Extract and analyze resume content.
- Identify technical skills and relevant keywords.

### 📊 ATS Score Analysis
- Generate an overall ATS-style resume score.
- Evaluate resume formatting and structure.
- Analyze keyword relevance.
- Assess content quality and professional impact.
- Highlight resume strengths and areas for improvement.

### 🎯 Intelligent Job Matching
- Compare resume content against available job descriptions.
- Calculate similarity scores using TF-IDF and cosine similarity.
- Rank job opportunities based on relevance.
- Help users identify opportunities aligned with their skills.

### 💡 Career Insights
- Identify relevant skills from resumes.
- Understand resume strengths and weaknesses.
- Discover areas where resume content can be improved.
- Get a clearer picture of job suitability.

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| NLP | TF-IDF Vectorization |
| Matching Algorithm | Cosine Similarity |
| Resume Processing | PDF text extraction |
| Job Dataset | CSV |
| Deployment | Render |
| Version Control | Git, GitHub |

## 🧠 How the Matching System Works

CareerLens uses a combination of text processing, similarity calculations, and rule-based analysis.

**1. Resume Input**

Users upload a PDF resume or paste their resume text into the application.

**2. Text Extraction and Processing**

The application extracts resume content and prepares the text for analysis.

**3. ATS Score Calculation**

The system evaluates three major areas:

- Format Score – Structure and layout.
- Keyword Score – Relevant industry and technical terms.
- Content Score – Content quality and professional relevance.

**4. TF-IDF Vectorization**

TF-IDF (Term Frequency–Inverse Document Frequency) converts resume text and job descriptions into numerical representations based on the importance of words.

**5. Cosine Similarity**

Cosine similarity measures the similarity between the resume and available job descriptions.

**6. Job Ranking**

The system ranks job opportunities according to their calculated similarity scores and displays the most relevant matches.

## 🏗️ Project Structure

```text
AI-Career-Job-Matching-Platform/
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── app.py
├── matcher.py
├── sample_jobs.csv
├── requirements.txt
├── .python-version
├── .gitignore
└── README.md
```

### Main Files

- `app.py` – Flask application and backend API.
- `matcher.py` – Resume matching and ATS scoring logic.
- `sample_jobs.csv` – Sample job descriptions used for matching.
- `templates/index.html` – Main application interface.
- `static/style.css` – Frontend styling.
- `static/script.js` – Frontend interactions and API communication.
- `requirements.txt` – Python dependencies.

## ⚙️ Installation and Setup

Follow these steps to run CareerLens locally.

### Prerequisites

- Python installed on your system.
- Git installed on your system.
- Visual Studio Code (recommended).

### Step 1: Clone the Repository

```bash
git clone https://github.com/lohitakshajoshi28/AI-Career-Job-Matching-Platform.git
```

### Step 2: Navigate to the Project Directory

```bash
cd AI-Career-Job-Matching-Platform
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open the Application

Open your browser and visit:

```text
http://localhost:5000
```

The application should now be running locally.

## 🌐 Live Deployment

The project is deployed using Render.

**Try CareerLens here:**

https://ai-career-job-matching-platform.onrender.com/

## 🔮 Future Enhancements

- Integrate real-time job listing APIs.
- Introduce semantic matching using sentence embeddings.
- Add user accounts and resume analysis history.
- Improve resume recommendations with generative AI.
- Expand the job dataset across multiple industries.
- Add personalized career development recommendations.

## 👨‍💻 Author

**Lohitaksha Joshi**

GitHub: [@lohitakshajoshi28](https://github.com/lohitakshajoshi28)

---

⭐ If you find this project interesting, consider giving the repository a star!

**CareerLens — Understand Your Resume. Discover Your Opportunities.**
