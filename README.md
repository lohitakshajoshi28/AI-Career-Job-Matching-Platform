# CareerLens — AI Career Intelligence & Job Matching Platform (v2)

A polished, SaaS-style version of the platform with:
- Custom HTML/CSS/JS frontend (no more default Streamlit look)
- A real Flask backend + JSON API
- **ATS Score Analysis** — a rule-based resume checker (overall score,
  format/keyword/content breakdown, circular score gauge, strengths &
  improvements) inspired by real ATS tools
- **Job Matches** — TF-IDF + cosine similarity ranking against sample jobs

## Project structure
```
career-matcher-v2/
├── app.py              # Flask backend + API
├── matcher.py          # Matching + ATS scoring logic ("the AI")
├── sample_jobs.csv     # Sample job postings
├── requirements.txt
├── templates/
│   └── index.html      # Page structure
└── static/
    ├── style.css        # Design system (colors, type, layout)
    └── script.js         # Frontend logic (fetch, render, animate)
```

## How to run it

### Step 1 — Install dependencies
```
pip install -r requirements.txt
```

### Step 2 — Start the server
```
python app.py
```

### Step 3 — Open it
Go to **http://localhost:5000** in your browser.

### Step 4 — Try it
Paste a resume (or upload a PDF), click "Analyze my resume," and switch
between the **ATS Score Analysis** and **Job Matches** tabs.

## How to put it online for free
1. Push this folder to a new GitHub repository.
2. Deploy for free on [Render](https://render.com) or [Railway](https://railway.app):
   - New Web Service → connect your repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `python app.py`
3. You'll get a public URL to share.

## How the scoring actually works (for interview talking points)

**Job matching** — TF-IDF turns your resume and each job description into
weighted word vectors; cosine similarity measures how close those vectors
are. This is a standard information-retrieval technique.

**ATS score** — a transparent, rule-based checker (not a black box):
- *Format score*: checks for email/phone, bullet points, standard section
  headers, and reasonable length
- *Keyword score*: counts how many recognized technical skills appear
- *Content score*: checks for action verbs and quantified achievements
  (numbers, %, etc.)

Being able to explain exactly *why* a score is what it is (rather than
"the AI said so") is a strength when you present this project — it shows
you understand what you built.

## Where to go next
- Swap the CSV for a real jobs dataset or live jobs API
- Replace TF-IDF with sentence embeddings for meaning-based matching
- Add resume upload history with a small database (SQLite is enough to start)
- Add an LLM-powered rewrite suggestion feature using the Claude API
