"""
Core AI logic for the Career Intelligence platform.

Two capabilities live here:
1. Job matching — TF-IDF + cosine similarity between a resume and job postings
2. ATS scoring — rule-based analysis of how "parseable" and keyword-rich a
   resume is, similar in spirit to real Applicant Tracking System checkers

Both are genuine, explainable techniques (no black-box claims) — good
talking points for a portfolio.
"""

import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "react native",
    "node.js", "express", "django", "flask", "flutter", "sql", "mysql",
    "postgresql", "mongodb", "firebase", "aws", "azure", "gcp", "docker",
    "kubernetes", "ci/cd", "jenkins", "git", "linux", "bash", "rest api",
    "graphql", "html", "css", "figma", "ui design", "ux research",
    "prototyping", "excel", "power bi", "tableau", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "machine learning", "nlp",
    "spacy", "embeddings", "data analysis", "data cleaning", "etl",
    "airflow", "bigquery", "redshift", "statistics", "a/b testing",
    "selenium", "manual testing", "jira", "networking", "cloudwatch",
]

SECTION_HEADERS = ["experience", "education", "skills", "summary", "projects",
                    "certifications", "objective", "work history"]

ACTION_VERBS = ["led", "built", "developed", "managed", "improved", "increased",
                "designed", "created", "implemented", "optimized", "launched",
                "reduced", "automated", "delivered", "architected", "mentored",
                "analyzed", "streamlined", "achieved", "drove"]


def extract_text_from_pdf(file_obj) -> str:
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def extract_skills(text: str) -> set:
    text_lower = text.lower()
    found = set()
    for skill in KNOWN_SKILLS:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def rank_jobs(resume_text: str, jobs_df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    documents = [resume_text] + jobs_df["description"].tolist()
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    scores = cosine_similarity(resume_vector, job_vectors).flatten()

    results = jobs_df.copy()
    results["match_score"] = (scores * 100).round(1)
    results = results.sort_values("match_score", ascending=False)
    return results.head(top_n)


def skill_gap(resume_skills: set, job_required_skills: str) -> tuple:
    required = {s.strip().lower() for s in job_required_skills.split(",")}
    matched = required & resume_skills
    missing = required - resume_skills
    return matched, missing


def analyze_ats(text: str) -> dict:
    """
    Rule-based ATS-style resume analysis. Returns format/keyword/content
    sub-scores, an overall score, and lists of strengths & improvements.
    """
    text_lower = text.lower()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    word_count = len(text.split())

    strengths, improvements = [], []

    # --- Format score ---
    format_points = 0
    has_email = bool(re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text))
    has_phone = bool(re.search(r"(\+?\d[\d\-\s]{8,}\d)", text))
    bullet_lines = sum(1 for l in lines if re.match(r"^[\-\u2022\*]", l))
    headers_found = [h for h in SECTION_HEADERS if h in text_lower]

    if has_email:
        format_points += 20; strengths.append("Email address is clearly present")
    else:
        improvements.append("Add a clear email address near the top")

    if has_phone:
        format_points += 15; strengths.append("Phone number detected")
    else:
        improvements.append("Add a phone number for recruiter contact")

    if bullet_lines >= 3:
        format_points += 25; strengths.append("Clean, readable format using bullet points")
    else:
        improvements.append("Use bullet points to list achievements — easier for ATS and humans to scan")

    if len(headers_found) >= 3:
        format_points += 25; strengths.append(f"Standard section headers found ({', '.join(headers_found[:3])})")
    else:
        improvements.append("Add clear section headers like 'Experience', 'Education', 'Skills'")

    if 150 <= word_count <= 900:
        format_points += 15
    else:
        improvements.append("Resume length looks off — aim for roughly 300–700 words")

    format_score = min(100, format_points)

    # --- Keyword score ---
    resume_skills = extract_skills(text)
    keyword_score = min(100, round((len(resume_skills) / 10) * 100))
    if len(resume_skills) >= 6:
        strengths.append(f"Strong technical keyword coverage ({len(resume_skills)} recognized skills)")
    else:
        improvements.append("Add more industry-specific keywords and technical terms")

    # --- Content quality score ---
    content_points = 0
    action_verb_hits = sum(1 for v in ACTION_VERBS if re.search(rf"\b{v}\b", text_lower))
    quantified_hits = len(re.findall(r"\b\d+%|\b\d+\+|\$\d+|\b\d{2,}\b", text))

    if action_verb_hits >= 5:
        content_points += 40; strengths.append("Uses strong action verbs (e.g. built, led, improved)")
    else:
        improvements.append("Start bullet points with strong action verbs (led, built, improved, launched)")

    if quantified_hits >= 3:
        content_points += 40; strengths.append("Includes quantified, measurable achievements")
    else:
        improvements.append("Quantify achievements with numbers or percentages (e.g. 'improved speed by 30%')")

    if word_count >= 150:
        content_points += 20

    content_score = min(100, content_points)

    overall_score = round(format_score * 0.3 + keyword_score * 0.4 + content_score * 0.3)

    if overall_score >= 85:
        rating = "Excellent"
    elif overall_score >= 70:
        rating = "Good"
    elif overall_score >= 50:
        rating = "Fair"
    else:
        rating = "Needs Work"

    return {
        "overall_score": overall_score,
        "rating": rating,
        "format_score": format_score,
        "keyword_score": keyword_score,
        "content_score": content_score,
        "strengths": strengths,
        "improvements": improvements,
        "skills_found": sorted(resume_skills),
    }
