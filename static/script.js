const toggleBtns = document.querySelectorAll(".toggle-btn");
const resumeText = document.getElementById("resumeText");
const fileDropZone = document.getElementById("fileDropZone");
const resumeFile = document.getElementById("resumeFile");
const analyzeBtn = document.getElementById("analyzeBtn");
const errorMsg = document.getElementById("errorMsg");
const resultsSection = document.getElementById("results");

let mode = "text";

toggleBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    toggleBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    mode = btn.dataset.mode;
    if (mode === "text") {
      resumeText.style.display = "block";
      fileDropZone.style.display = "none";
    } else {
      resumeText.style.display = "none";
      fileDropZone.style.display = "block";
    }
  });
});

const tabBtns = document.querySelectorAll(".tab-btn");
tabBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    tabBtns.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    document.querySelectorAll(".tab-panel").forEach(p => p.style.display = "none");
    document.getElementById("tab-" + btn.dataset.tab).style.display = "block";
  });
});

analyzeBtn.addEventListener("click", async () => {
  errorMsg.textContent = "";
  const formData = new FormData();

  if (mode === "text") {
    if (resumeText.value.trim().length < 20) {
      errorMsg.textContent = "Please paste a bit more resume content first.";
      return;
    }
    formData.append("resume_text", resumeText.value);
  } else {
    if (!resumeFile.files.length) {
      errorMsg.textContent = "Please choose a PDF file first.";
      return;
    }
    formData.append("resume_file", resumeFile.files[0]);
  }

  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "Analyzing...";

  try {
    const res = await fetch("/api/analyze", { method: "POST", body: formData });
    const data = await res.json();

    if (!res.ok) {
      errorMsg.textContent = data.error || "Something went wrong.";
      return;
    }

    renderResults(data);
    resultsSection.style.display = "block";
    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
  } catch (e) {
    errorMsg.textContent = "Could not reach the server. Is the Flask app running?";
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze my resume";
  }
});

function renderResults(data) {
  const ats = data.ats;

  document.getElementById("ratingBadge").textContent = ats.rating;
  document.getElementById("ratingDesc").textContent =
    `Overall, your resume is a ${ats.rating.toLowerCase()} start. Follow the suggestions below to improve your score.`;

  document.getElementById("formatScore").textContent = ats.format_score;
  document.getElementById("keywordScore").textContent = ats.keyword_score;
  document.getElementById("contentScore").textContent = ats.content_score;

  // Gauge: circumference = 2 * pi * r(70) = 439.8
  const circumference = 439.8;
  const offset = circumference - (ats.overall_score / 100) * circumference;
  const gaugeFill = document.getElementById("gaugeFill");
  gaugeFill.style.strokeDasharray = circumference;
  setTimeout(() => { gaugeFill.style.strokeDashoffset = offset; }, 100);
  document.getElementById("gaugeNumber").textContent = ats.overall_score;

  animateBar("barKeywords", "barKeywordsPct", ats.keyword_score);
  animateBar("barFormat", "barFormatPct", ats.format_score);
  animateBar("barContent", "barContentPct", ats.content_score);

  const strengthsList = document.getElementById("strengthsList");
  strengthsList.innerHTML = "";
  ats.strengths.forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    strengthsList.appendChild(li);
  });

  const improvementsList = document.getElementById("improvementsList");
  improvementsList.innerHTML = "";
  ats.improvements.forEach(s => {
    const li = document.createElement("li");
    li.textContent = s;
    improvementsList.appendChild(li);
  });

  const skillsDetected = document.getElementById("skillsDetected");
  skillsDetected.innerHTML = "";
  data.skills_detected.forEach(s => {
    const span = document.createElement("span");
    span.className = "skill-pill";
    span.textContent = titleCase(s);
    skillsDetected.appendChild(span);
  });

  const jobMatches = document.getElementById("jobMatches");
  jobMatches.innerHTML = "";
  data.matches.forEach(job => {
    const card = document.createElement("div");
    card.className = "job-card";
    card.innerHTML = `
      <div class="job-top">
        <div>
          <p class="job-title">${job.title} — ${job.company}</p>
          <p class="job-company">📍 ${job.location}</p>
        </div>
        <div class="match-pct">
          <div class="match-pct-num">${job.match_score}%</div>
          <div class="match-pct-label">Match</div>
        </div>
      </div>
      <p class="job-desc">${job.description}</p>
      <div class="job-skills-grid">
        <div class="job-skills-col">
          <label>✓ Matched skills</label>
          ${job.matched_skills.map(s => `<span class="tag">${titleCase(s)}</span>`).join("") || "—"}
        </div>
        <div class="job-skills-col">
          <label>📌 Skills to learn</label>
          ${job.missing_skills.map(s => `<span class="tag">${titleCase(s)}</span>`).join("") || "None"}
        </div>
      </div>
    `;
    jobMatches.appendChild(card);
  });
}

function animateBar(barId, pctId, value) {
  const bar = document.getElementById(barId);
  const pct = document.getElementById(pctId);
  setTimeout(() => { bar.style.width = value + "%"; }, 100);
  pct.textContent = value + "%";
}

function titleCase(s) {
  return s.replace(/\w\S*/g, t => t.charAt(0).toUpperCase() + t.substr(1));
}
