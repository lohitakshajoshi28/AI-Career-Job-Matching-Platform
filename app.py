
from flask import Flask, request, jsonify, render_template
import pandas as pd

from matcher import (
    extract_text_from_pdf,
    extract_skills,
    rank_jobs,
    skill_gap,
    analyze_ats
)

app = Flask(__name__)

jobs_df = pd.read_csv("sample_jobs.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    resume_text = ""

    if "resume_file" in request.files and request.files["resume_file"].filename:
        f = request.files["resume_file"]
        resume_text = extract_text_from_pdf(f)
    else:
        resume_text = request.form.get("resume_text", "")

    if not resume_text or len(resume_text.strip()) < 20:
        return jsonify({
            "error": "Please provide a resume with more content."
        }), 400

    resume_skills = extract_skills(resume_text)

    top_matches = rank_jobs(
        resume_text,
        jobs_df,
        top_n=5
    )

    matches = []

    for _, job in top_matches.iterrows():
        matched, missing = skill_gap(
            resume_skills,
            job["required_skills"]
        )

        matches.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "description": job["description"],
            "match_score": job["match_score"],
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
        })

    ats = analyze_ats(resume_text)

    return jsonify({
        "skills_detected": sorted(resume_skills),
        "matches": matches,
        "ats": ats,
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        use_reloader=False
    )