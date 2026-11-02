/**
 * Multiple Disease Prediction System — Frontend Application
 *
 * Handles:
 *  - Fetching available diseases from the API
 *  - Rendering disease cards dynamically
 *  - Opening prediction forms with correct fields per disease
 *  - Form submission, validation, and result display
 *  - Scroll animations and mobile nav
 */

"use strict";

// ──────────── API Base ────────────
const API_BASE = window.location.origin;

// ──────────── Form Field Definitions ────────────
// Field order matches the exact feature order each model was trained on.

const DISEASE_FORMS = {
    diabetes: {
        title: "🩸 Diabetes Prediction",
        endpoint: "/api/predict/diabetes",
        fields: [
            { name: "Pregnancies",              label: "Pregnancies",                  type: "number", placeholder: "e.g. 5",    step: "1",     hint: "Number of times pregnant" },
            { name: "Glucose",                  label: "Glucose",                      type: "number", placeholder: "e.g. 166",  step: "any",   hint: "Plasma glucose (mg/dL)" },
            { name: "BloodPressure",            label: "Blood Pressure",               type: "number", placeholder: "e.g. 72",   step: "any",   hint: "Diastolic BP (mm Hg)" },
            { name: "SkinThickness",            label: "Skin Thickness",               type: "number", placeholder: "e.g. 19",   step: "any",   hint: "Triceps fold (mm)" },
            { name: "Insulin",                  label: "Insulin",                      type: "number", placeholder: "e.g. 175",  step: "any",   hint: "2-Hr serum insulin (mu U/ml)" },
            { name: "BMI",                      label: "BMI",                          type: "number", placeholder: "e.g. 25.8", step: "any",   hint: "Body mass index (kg/m²)" },
            { name: "DiabetesPedigreeFunction", label: "Diabetes Pedigree Function",   type: "number", placeholder: "e.g. 0.587",step: "any",   hint: "Pedigree function score" },
            { name: "Age",                      label: "Age",                          type: "number", placeholder: "e.g. 51",   step: "1",     hint: "Age in years" },
        ],
    },

    heart: {
        title: "❤️ Heart Disease Prediction",
        endpoint: "/api/predict/heart",
        fields: [
            { name: "age",      label: "Age",                   type: "number", placeholder: "e.g. 62",   step: "1",   hint: "Age in years" },
            { name: "sex",      label: "Sex",                   type: "select", options: [{v:1,l:"Male"},{v:0,l:"Female"}], hint: "Biological sex" },
            { name: "cp",       label: "Chest Pain Type",       type: "select", options: [{v:0,l:"0 — Typical Angina"},{v:1,l:"1 — Atypical Angina"},{v:2,l:"2 — Non-anginal"},{v:3,l:"3 — Asymptomatic"}], hint: "Type of chest pain" },
            { name: "trestbps", label: "Resting Blood Pressure",type: "number", placeholder: "e.g. 140",  step: "any", hint: "mm Hg on admission" },
            { name: "chol",     label: "Cholesterol",           type: "number", placeholder: "e.g. 268",  step: "any", hint: "Serum cholesterol (mg/dl)" },
            { name: "fbs",      label: "Fasting Blood Sugar > 120",type: "select",options:[{v:1,l:"True (> 120 mg/dl)"},{v:0,l:"False"}], hint: "FBS > 120 mg/dl" },
            { name: "restecg",  label: "Resting ECG",           type: "select", options: [{v:0,l:"0 — Normal"},{v:1,l:"1 — ST-T Abnormality"},{v:2,l:"2 — LV Hypertrophy"}], hint: "ECG result" },
            { name: "thalach",  label: "Max Heart Rate",        type: "number", placeholder: "e.g. 160",  step: "any", hint: "Maximum heart rate achieved" },
            { name: "exang",    label: "Exercise Induced Angina",type: "select",options:[{v:1,l:"Yes"},{v:0,l:"No"}], hint: "Angina during exercise" },
            { name: "oldpeak",  label: "ST Depression (Oldpeak)",type: "number",placeholder: "e.g. 3.6",  step: "any", hint: "ST depression vs. rest" },
            { name: "slope",    label: "Slope of Peak ST",      type: "select", options: [{v:0,l:"0 — Upsloping"},{v:1,l:"1 — Flat"},{v:2,l:"2 — Downsloping"}], hint: "Peak exercise ST slope" },
            { name: "ca",       label: "Major Vessels (ca)",    type: "select", options: [{v:0,l:"0"},{v:1,l:"1"},{v:2,l:"2"},{v:3,l:"3"},{v:4,l:"4"}], hint: "Vessels colored by fluoroscopy" },
            { name: "thal",     label: "Thalassemia",           type: "select", options: [{v:0,l:"0 — Normal"},{v:1,l:"1 — Fixed Defect"},{v:2,l:"2 — Reversible Defect"},{v:3,l:"3 — Other"}], hint: "Thalassemia type" },
        ],
    },

    parkinsons: {
        title: "🧠 Parkinson's Disease Prediction",
        endpoint: "/api/predict/parkinsons",
        fields: [
            { name: "fo",             label: "MDVP:Fo(Hz)",         type: "number", placeholder: "e.g. 119.992",  step: "any", hint: "Avg vocal fundamental freq" },
            { name: "fhi",            label: "MDVP:Fhi(Hz)",        type: "number", placeholder: "e.g. 157.302",  step: "any", hint: "Max vocal fundamental freq" },
            { name: "flo",            label: "MDVP:Flo(Hz)",        type: "number", placeholder: "e.g. 74.997",   step: "any", hint: "Min vocal fundamental freq" },
            { name: "jitter_percent", label: "MDVP:Jitter(%)",      type: "number", placeholder: "e.g. 0.00784",  step: "any", hint: "Jitter percentage" },
            { name: "jitter_abs",     label: "MDVP:Jitter(Abs)",    type: "number", placeholder: "e.g. 0.00007",  step: "any", hint: "Absolute jitter (μs)" },
            { name: "rap",            label: "MDVP:RAP",            type: "number", placeholder: "e.g. 0.00370",  step: "any", hint: "Relative amplitude perturbation" },
            { name: "ppq",            label: "MDVP:PPQ",            type: "number", placeholder: "e.g. 0.00554",  step: "any", hint: "5-pt period perturbation quotient" },
            { name: "ddp",            label: "Jitter:DDP",          type: "number", placeholder: "e.g. 0.01109",  step: "any", hint: "Avg abs diff of jitter cycles" },
            { name: "shimmer",        label: "MDVP:Shimmer",        type: "number", placeholder: "e.g. 0.04374",  step: "any", hint: "Local shimmer" },
            { name: "shimmer_db",     label: "MDVP:Shimmer(dB)",    type: "number", placeholder: "e.g. 0.426",    step: "any", hint: "Shimmer in dB" },
            { name: "apq3",           label: "Shimmer:APQ3",        type: "number", placeholder: "e.g. 0.02182",  step: "any", hint: "3-pt amplitude perturbation" },
            { name: "apq5",           label: "Shimmer:APQ5",        type: "number", placeholder: "e.g. 0.03130",  step: "any", hint: "5-pt amplitude perturbation" },
            { name: "apq",            label: "MDVP:APQ",            type: "number", placeholder: "e.g. 0.02971",  step: "any", hint: "Amplitude perturbation quotient" },
            { name: "dda",            label: "Shimmer:DDA",         type: "number", placeholder: "e.g. 0.06545",  step: "any", hint: "Avg abs diff of shimmer" },
            { name: "nhr",            label: "NHR",                 type: "number", placeholder: "e.g. 0.02211",  step: "any", hint: "Noise-to-harmonics ratio" },
            { name: "hnr",            label: "HNR",                 type: "number", placeholder: "e.g. 21.033",   step: "any", hint: "Harmonics-to-noise ratio" },
            { name: "rpde",           label: "RPDE",                type: "number", placeholder: "e.g. 0.414783", step: "any", hint: "Recurrence period density entropy" },
            { name: "dfa",            label: "DFA",                 type: "number", placeholder: "e.g. 0.815285", step: "any", hint: "Detrended fluctuation analysis" },
            { name: "spread1",        label: "Spread1",             type: "number", placeholder: "e.g. -4.813031",step: "any", hint: "Nonlinear freq variation" },
            { name: "spread2",        label: "Spread2",             type: "number", placeholder: "e.g. 0.266482", step: "any", hint: "Nonlinear freq variation" },
            { name: "d2",             label: "D2",                  type: "number", placeholder: "e.g. 2.301442", step: "any", hint: "Correlation dimension" },
            { name: "ppe",            label: "PPE",                 type: "number", placeholder: "e.g. 0.284654", step: "any", hint: "Pitch period entropy" },
        ],
    },
};

// ──────────── DOM Elements ────────────
const diseasesGrid      = document.getElementById("diseases-grid");
const overlay           = document.getElementById("prediction-overlay");
const panelTitle        = document.getElementById("panel-title");
const panelClose        = document.getElementById("panel-close");
const formFields        = document.getElementById("form-fields");
const predictionForm    = document.getElementById("prediction-form");
const btnSubmit         = document.getElementById("btn-submit");
const btnReset          = document.getElementById("btn-reset");
const resultContainer   = document.getElementById("result-container");
const resultCard        = document.getElementById("result-card");
const resultIcon        = document.getElementById("result-icon");
const resultTitle       = document.getElementById("result-title");
const resultMessage     = document.getElementById("result-message");
const resultProbability = document.getElementById("result-probability");
const mobileMenuBtn     = document.getElementById("mobile-menu-btn");
const navLinks          = document.getElementById("nav-links");

let currentDisease = null;

// ──────────── Fetch & Render Disease Cards ────────────
async function loadDiseases() {
    try {
        const res = await fetch(`${API_BASE}/api/diseases`);
        if (!res.ok) throw new Error("Failed to fetch diseases");
        const diseases = await res.json();
        renderDiseaseCards(diseases);
    } catch (err) {
        console.error("Error loading diseases:", err);
        diseasesGrid.innerHTML = `
            <div style="grid-column:1/-1;text-align:center;padding:3rem;color:var(--text-muted);">
                ⚠️ Unable to connect to the API. Ensure the server is running.
            </div>`;
    }
}

function renderDiseaseCards(diseases) {
    if (!diseases || diseases.length === 0) {
        diseasesGrid.innerHTML = `
            <div style="grid-column:1/-1;text-align:center;padding:3rem;color:var(--text-muted);">
                No models available.
            </div>`;
        return;
    }

    diseasesGrid.innerHTML = diseases.map((d, i) => `
        <div class="disease-card animate-on-scroll" data-disease="${d.id}" style="animation-delay:${i * 0.1}s" onclick="openPrediction('${d.id}')">
            <div class="card-icon">${d.icon}</div>
            <h3 class="card-title">${d.name}</h3>
            <p class="card-desc">${d.description}</p>
            <div class="card-meta">
                <span class="meta-item">📊 ${d.features_count} Features</span>
                <span class="meta-item">🎯 ${d.accuracy} Accuracy</span>
                <span class="meta-item">🤖 ${d.model_type.split("(")[0].trim()}</span>
            </div>
            <div class="card-action">Start Prediction →</div>
        </div>
    `).join("");

    // Trigger scroll animations for newly added cards
    observeAnimations();
}

// ──────────── Open Prediction Form ────────────
function openPrediction(diseaseId) {
    const formDef = DISEASE_FORMS[diseaseId];
    if (!formDef) return;

    currentDisease = diseaseId;
    panelTitle.innerHTML = formDef.title;

    // Build form fields
    formFields.innerHTML = formDef.fields.map(f => {
        if (f.type === "select") {
            const opts = f.options.map(o => `<option value="${o.v}">${o.l}</option>`).join("");
            return `
                <div class="form-group">
                    <label class="form-label" for="field-${f.name}">
                        ${f.label}
                        <span class="label-hint">${f.hint}</span>
                    </label>
                    <select class="form-input form-select" id="field-${f.name}" name="${f.name}" required>
                        ${opts}
                    </select>
                </div>`;
        }
        return `
            <div class="form-group">
                <label class="form-label" for="field-${f.name}">
                    ${f.label}
                    <span class="label-hint">${f.hint}</span>
                </label>
                <input class="form-input"
                       id="field-${f.name}"
                       name="${f.name}"
                       type="${f.type}"
                       placeholder="${f.placeholder}"
                       step="${f.step || 'any'}"
                       required>
            </div>`;
    }).join("");

    // Reset state
    resultContainer.classList.remove("show");
    btnSubmit.classList.remove("loading");

    // Show overlay
    overlay.classList.add("active");
    document.body.style.overflow = "hidden";

    // Focus first input
    setTimeout(() => {
        const first = formFields.querySelector("input, select");
        if (first) first.focus();
    }, 300);
}

// ──────────── Close Modal ────────────
function closePrediction() {
    overlay.classList.remove("active");
    document.body.style.overflow = "";
    currentDisease = null;
}

panelClose.addEventListener("click", closePrediction);
overlay.addEventListener("click", (e) => {
    if (e.target === overlay) closePrediction();
});
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && overlay.classList.contains("active")) closePrediction();
});

// ──────────── Form Submission ────────────
predictionForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentDisease) return;

    const formDef = DISEASE_FORMS[currentDisease];
    const formData = new FormData(predictionForm);
    const payload = {};

    // Convert to proper numeric types
    for (const field of formDef.fields) {
        const raw = formData.get(field.name);
        if (raw === null || raw === "") {
            alert(`Please fill in: ${field.label}`);
            return;
        }
        const val = Number(raw);
        if (isNaN(val)) {
            alert(`Invalid number for: ${field.label}`);
            return;
        }
        // Use integer for int fields
        if (field.step === "1" || field.type === "select") {
            payload[field.name] = Math.round(val);
        } else {
            payload[field.name] = val;
        }
    }

    // Show loading
    btnSubmit.classList.add("loading");
    resultContainer.classList.remove("show");

    try {
        const res = await fetch(`${API_BASE}${formDef.endpoint}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: "Unknown error" }));
            throw new Error(err.detail || JSON.stringify(err));
        }

        const data = await res.json();
        displayResult(data);
    } catch (err) {
        console.error("Prediction error:", err);
        resultCard.className = "result-card positive";
        resultIcon.textContent = "❌";
        resultTitle.textContent = "Prediction Failed";
        resultMessage.textContent = err.message || "Something went wrong. Please try again.";
        resultProbability.style.display = "none";
        resultContainer.classList.add("show");
    } finally {
        btnSubmit.classList.remove("loading");
    }
});

// ──────────── Display Result ────────────
function displayResult(data) {
    const isPositive = data.prediction === 1;

    resultCard.className = `result-card ${isPositive ? "positive" : "negative"}`;
    resultIcon.textContent = isPositive ? "⚠️" : "✅";
    resultTitle.textContent = data.result;
    resultMessage.textContent = data.message;

    if (data.probability !== null && data.probability !== undefined) {
        resultProbability.style.display = "inline-flex";
        resultProbability.textContent = `📊 Confidence: ${(data.probability * 100).toFixed(1)}% probability of positive`;
    } else {
        resultProbability.style.display = "none";
    }

    resultContainer.classList.add("show");

    // Scroll result into view inside the modal
    resultContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ──────────── Reset Form ────────────
btnReset.addEventListener("click", () => {
    predictionForm.reset();
    resultContainer.classList.remove("show");
});

// ──────────── Mobile Nav ────────────
mobileMenuBtn.addEventListener("click", () => {
    navLinks.classList.toggle("open");
});

// Close mobile nav on link click
navLinks.addEventListener("click", (e) => {
    if (e.target.tagName === "A") {
        navLinks.classList.remove("open");
    }
});

// ──────────── Smooth Scroll for Nav ────────────
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener("click", (e) => {
        const target = document.querySelector(link.getAttribute("href"));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: "smooth" });

            // Update active state
            document.querySelectorAll(".navbar-links a").forEach(l => l.classList.remove("active"));
            link.classList.add("active");
        }
    });
});

// ──────────── Scroll Animations (IntersectionObserver) ────────────
function observeAnimations() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    document.querySelectorAll(".animate-on-scroll").forEach(el => {
        observer.observe(el);
    });
}

// ──────────── Active nav on scroll ────────────
window.addEventListener("scroll", () => {
    const sections = ["home", "diseases", "how-it-works", "tech-stack"];
    let current = "";
    for (const id of sections) {
        const el = document.getElementById(id);
        if (el && el.getBoundingClientRect().top <= 150) {
            current = id;
        }
    }
    document.querySelectorAll(".navbar-links a").forEach(a => {
        a.classList.toggle("active", a.getAttribute("href") === `#${current}`);
    });
});

// ──────────── Init ────────────
document.addEventListener("DOMContentLoaded", () => {
    loadDiseases();
    observeAnimations();
});
