import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import io
import datetime
from resume_parser import extract_text_from_pdf, extract_skills
from jd_parser import extract_jd_skills
from matcher import match_score
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import plotly.io as pio

st.title("📃 SkillSync")

# Upload Resume
resume_file = st.file_uploader("Upload your Resume (PDF)", type=['pdf'])

# Let user choose JD input method
jd_mode = st.radio("Choose Job Description input method:", ["Paste JD Text", "Upload JD PDF"])

jd_text_input = ""

if jd_mode == "Paste JD Text":
    jd_text_input = st.text_area("Paste Job Description Here")
elif jd_mode == "Upload JD PDF":
    jd_pdf = st.file_uploader("Upload JD (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text_input = extract_text_from_pdf(jd_pdf)

st.caption("ℹ️ Paste or upload a complete JD with 5+ skills for best accuracy.")

# Main Logic
if resume_file and jd_text_input:
    resume_text = extract_text_from_pdf(resume_file)
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_jd_skills(jd_text_input)

    if len(jd_skills) < 3:
        st.warning("⚠️ Not enough skills found in the Job Description to calculate an accurate match. Please provide a more detailed JD.")
    else:
        score, matched = match_score(resume_skills, jd_skills)
        st.success(f"✅ Resume matches {score}% of the JD.")

        # Create Match Score Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Match Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
            }
        ))
        st.plotly_chart(fig)

        missing = set(jd_skills) - set(matched)
        st.markdown(f"**Matched Skills:** {', '.join(matched) if matched else 'None'}")
        st.markdown(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")

        # ✅ Save gauge to image buffer (PNG)
        img_bytes = fig.to_image(format="png")
        img_buffer = io.BytesIO(img_bytes)

        # ✅ Generate PDF Report with Image
        def create_pdf(score, matched, missing, gauge_img):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Resume to JD Match Report")

            c.setFont("Helvetica", 10)
            c.drawString(50, height - 70, f"Generated on: {datetime.date.today().strftime('%B %d, %Y')}")

            # Insert gauge image
            c.drawImage(ImageReader(gauge_img), 370, height - 230, width=160, height=160)

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 110, f"Match Score: {score}%")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, height - 150, "Matched Skills:")
            c.setFont("Helvetica", 11)
            for i, skill in enumerate(matched):
                c.drawString(70, height - 170 - (i * 15), f"- {skill}")

            y_offset = height - 170 - (len(matched) * 15) - 30
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_offset, "Missing Skills:")
            c.setFont("Helvetica", 11)
            for j, skill in enumerate(missing):
                c.drawString(70, y_offset - 20 - (j * 15), f"- {skill}")

            c.showPage()
            c.save()
            buffer.seek(0)
            return buffer

        pdf_buffer = create_pdf(score, matched, missing, img_buffer)
        st.download_button("📥 Download Match Report (PDF)", data=pdf_buffer, file_name="match_report.pdf", mime="application/pdf")
