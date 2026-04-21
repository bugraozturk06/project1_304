import streamlit as st
import google.generativeai as genai

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="METU-IE Summer Practice Assistant",
    page_icon="🎓",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem; font-weight: 700;
    color: #1a1a2e; margin-bottom: 0;
}
.sub-title { color: #6b7280; font-size: 0.95rem; margin-top: 4px; margin-bottom: 24px; }
.badge {
    display: inline-block; background: #e0f2fe; color: #0369a1;
    padding: 2px 10px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600; margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── Knowledge base ────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = """
You are a helpful assistant for METU Industrial Engineering (IE) Summer Practice (Staj) procedures.
Answer questions ONLY based on the information below. If a question is outside this scope, politely
say so and direct the user to sp-ie.metu.edu.tr or the SP Committee email: ie-staj@metu.edu.tr

=== GENERAL INFORMATION ===
- Summer internships must be done by PHYSICALLY attending the workplace (remote not allowed).
- IE 300: First summer practice (manufacturing-oriented).
- IE 400: Second summer practice. Project-based internships are allowed for IE 400.
  * Project-based internship must be at least 6 weeks (30 workdays).
  * Requires a proposal submitted to SP Committee BEFORE internship begins.
- Public institutions (kamu kurumları) use a centralized system: kariyerkapisi.cbiko.gov.tr
- Erasmus internships: minimum 3 months, maximum 12 months. A short Erasmus SP (3 months) counts as only ONE of IE300/IE400.
- Foreign students are NOT allowed to do voluntary internships in Turkey (work permit required).

=== SGK INSURANCE ===
- Insurance applications are via METU OpenCourseWare (OCW): ocw.metu.edu.tr
- All 1st–4th year students are auto-registered to "IE300/400 Summer Internship" on OCW.
- Ideal time to apply: 2–3 weeks BEFORE internship starts.
- Applications processed every Monday morning for internships beginning within 2 weeks.
- Leave at least 1 full week safety margin between application and SP start.
- Do NOT apply too early (e.g., 2 months before) — Rektörlük won't process early applications.
- SGK document available on e-devlet (turkiye.gov.tr) about 2–3 workdays before SP start.
  Steps: Login → search "işe giriş" → "4A İşe Giriş Çıkış Bildirgesi" → click "Belge oluştur"
- Emergency (no Monday before start): Fill the Excel form and email ie-staj@metu.edu.tr with subject:
  "SGK basvurusu: Name Surname dd.mm.2025"

=== HOW TO APPLY FOR SGK (STEP BY STEP) ===
1. Login to ocw.metu.edu.tr with student account.
2. Find "IE300/400 Summer Internship" under "My courses".
3. Click "SGK Insurance Application" questionnaire; fill identity + company info; click Submit.
4. Upload "Declaration Form for students with/without family health insurance" (found on sp-ie.metu.edu.tr/en/forms).
5. Done. No confirmation email is sent — this is normal.

=== MISTAKES / CANCELLATIONS ===
- Made a mistake and application NOT yet sent to Rektörlük: Fill a new questionnaire; latest version overrides older.
- Made a mistake and application ALREADY sent: Email ie-staj@metu.edu.tr
- Internship cancelled: Email ie-staj@metu.edu.tr

=== VOLUNTARY INTERNSHIPS ===
- Optional, not required by the department.
- SGK insurance provided for up to 1 month per company.
- Send second application only AFTER first SGK document is issued.
- Leave at least 1 blank day between two SPs.

=== PAID SUMMER PRACTICES ===
(Only for private companies in Turkey where payment was received)
After finishing SP and receiving all payments:
1. Login to ocw.metu.edu.tr
2. Fill "Paid SP form questionnaire" under IE300/400 course.
3. Download, print, sign the Paid Summer Practice Form; upload scanned PDF to OCW.
4. Upload bank receipt (PDF) showing payment received.

=== STEPS TO FOLLOW ===
BEFORE:
1. Read the SP Manual (sp-ie.metu.edu.tr/en/forms).
2. Find a company (department list, personal contacts, previous SP databases).
3. Some companies need an SP Application Letter (template on sp-ie.metu.edu.tr/en/forms).
4. Some companies need an SP Protocol/Sözleşme — leave to Undergraduate Secretary (IE 129), pick up in 1 week.
5. Apply for SGK insurance on time via OCW.

DURING:
- Take notes regularly; prepare draft report while at the company.
- Get "SP Evaluation Form" and "Employer Survey" filled and signed by supervisor.
  Supervisor can email signed PDFs to sp-belge@metu.edu.tr or post in closed envelope.

AFTER:
- Register for IE 300 / IE 400 course during registration period.
- Submit SP report via ODTUClass before the announced deadline (STRICT).
- Report must be in PDF format.
- Reports are checked for plagiarism AND AI-generated content.

EVALUATION:
- Graded by assigned faculty.
- Reports needing corrections returned in last month of semester (2–3 weeks to correct).

=== PAPERWORK / DOCUMENTS ===
Required for official registration:
1. Add IE300/IE400 in course registration at semester start.
2. Submit SP report to Students Affairs Secretary (IE 128) within first 2 weeks of following term + soft copy via website.
3. Company sends filled & signed Evaluation Form + Employer Survey to IE 128 or sp-belge@metu.edu.tr
4. Fill the online questionnaire (announced separately).

SP Application Letter, Protocol Form, Declaration Form, Paid SP Form, IE300 Manual, IE400 Manufacturing Manual, IE400 Service Manual — all available at: sp-ie.metu.edu.tr/en/forms

=== FAQ ===
Q: How can I arrange an SP organization?
A: Apply personally to organizations OR wait for department-announced opportunities (limited capacity). If assigned through department, attendance at that company is MANDATORY.

Q: Which departments should I visit during SP?
A: Aim for an all-around tour. Gather observations through effective communication even if stationed at one department.

Q: What paperwork for official SP registration?
A: (1) Register IE300/400 in courses, (2) submit report to IE128 + online, (3) company sends evaluation form, (4) fill online questionnaire.

Q: Can multiple students from the same company submit the same report?
A: IE400: General company overview can be common. Questions part MUST be different. Problem definition MUST be different. Project part can be same only if complex AND at most 2 students.

Q: What is project-type IE400 SP?
A: Full-time project work for minimum 30 workdays. Requires 2-page proposal approved by company, submitted to SP Committee in the first week of SP.

Q: Can I do SP in a service organization for manufacturing-question IE400?
A: Yes — find analogies. Budget ≈ production plan, classified records ≈ inventory, timetables ≈ schedules, form flow ≈ material flow.

=== CONTACT ===
- SP Committee email: ie-staj@metu.edu.tr
- Student Affairs Secretary: Room IE 128 / IE 129
- SP documents email: sp-belge@metu.edu.tr
- Website: https://sp-ie.metu.edu.tr/en
"""

# ── Init Gemini ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=KNOWLEDGE_BASE,
    )

model = get_model()

# ── Init chat session ─────────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[]) if model else None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="badge">🎓 METU Industrial Engineering</div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">Summer Practice Assistant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ask anything about IE 300 / IE 400 Summer Practice procedures, SGK insurance, documents, and deadlines.</p>', unsafe_allow_html=True)

# ── Suggested questions ───────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("**💡 Try asking:**")
    cols = st.columns(2)
    suggestions = [
        "What are the requirements for IE 300?",
        "How do I apply for SGK insurance?",
        "What documents do I need before starting SP?",
        "When should I submit my SP report?",
    ]
    for i, s in enumerate(suggestions):
        if cols[i % 2].button(s, key=f"sug_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": s})
            st.rerun()

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about METU-IE Summer Practice..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not model:
            st.error("⚠️ GEMINI_API_KEY is not set. Please add it in Streamlit secrets.")
        else:
            with st.spinner("Thinking..."):
                response = st.session_state.chat.send_message(prompt)
                answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("📌 Official website: [sp-ie.metu.edu.tr/en](https://sp-ie.metu.edu.tr/en) | ✉️ ie-staj@metu.edu.tr")
