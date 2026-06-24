import streamlit as st
import json

from resume_parser import extract_resume_text

from prompts import (
    build_analysis_prompt,
    build_questions_prompt,
    build_scorecard_prompt
)

from llm import ask_llm
from report_generator import (
    generate_pdf_report
)

st.set_page_config(
    page_title="Interview Pilot AI",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "job_description" not in st.session_state:
    st.session_state.job_description = None

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "scorecard" not in st.session_state:
    st.session_state.scorecard = None

st.title("AI Interview Pilot")

st.markdown(
    """
Upload your resume, paste a job description,
and take an AI-generated interview.
"""
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)


if st.button("Generate Report"):

    if uploaded_file and job_description:

        with st.spinner("Analyzing Resume..."):

            resume_text = extract_resume_text(
                uploaded_file
            )

            st.session_state.resume_text = (resume_text)
            st.session_state.job_description = (job_description)

            analysis_prompt = build_analysis_prompt(
                resume_text,
                job_description
            )

            analysis = ask_llm(
                analysis_prompt
            )

            st.session_state.analysis = analysis

            st.rerun()

if st.session_state.analysis:

    st.subheader("Resume Analysis")

    st.markdown(st.session_state.analysis)

    if st.button("Generate Interview"):

        with st.spinner(
            "Generating Interview Questions..."
        ):

            question_prompt = build_questions_prompt(
                st.session_state.resume_text,
                st.session_state.job_description
            )

            questions_json = ask_llm(
                question_prompt
            )

            try:

                questions_json = (
                    questions_json
                    .replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

                questions = json.loads(
                    questions_json
                )["questions"]

                st.session_state.questions = questions

                st.session_state.current_question = 0

                st.session_state.answers = []

                st.session_state.interview_started = True

                st.session_state.scorecard = None

                st.success(
                    "Interview Ready!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Question Generation Failed: {e}"
                )


if (
    st.session_state.interview_started
    and
    st.session_state.current_question
    < len(st.session_state.questions)
):

    idx = st.session_state.current_question

    total = len(
        st.session_state.questions
    )

    st.progress(
        (idx + 1) / total
    )

    st.subheader(
        f"Question {idx + 1} / {total}"
    )

    st.write(
        st.session_state.questions[idx]
    )

    answer = st.text_area(
        "Your Answer",
        key=f"answer_{idx}"
    )

    if st.button(
        "Next Question"
    ):

        st.session_state.answers.append(
            {
                "question":
                st.session_state.questions[idx],

                "answer":
                answer
            }
        )

        st.session_state.current_question += 1

        st.rerun()

if (
    st.session_state.interview_started
    and
    st.session_state.current_question
    >= len(st.session_state.questions)
    and
    st.session_state.scorecard is None
):

    with st.spinner(
        "Evaluating Interview..."
    ):

        evaluation_prompt = (
            build_scorecard_prompt(
                st.session_state.questions,
                st.session_state.answers
            )
        )

        scorecard = ask_llm(
            evaluation_prompt
        )

        st.session_state.scorecard = (
            scorecard
        )

        st.rerun()


if st.session_state.scorecard:

    st.success(
        "Interview Complete "
    )

    st.subheader(
        "Final Scorecard"
    )

    pdf_file = generate_pdf_report(
        st.session_state.analysis,
        st.session_state.scorecard
    )

    st.markdown(
        st.session_state.scorecard
    )

    st.download_button(
        label="📄 Download PDF Report",

        data=pdf_file,

        file_name="Interview_Report.pdf",

        mime="application/pdf"
    )

    if st.button(
        "Start New Interview"
    ):

        st.session_state.questions = []

        st.session_state.current_question = 0

        st.session_state.answers = []

        st.session_state.interview_started = False

        st.session_state.scorecard = None

        st.rerun()

st.markdown("---")

st.caption(
    "Built with Streamlit, Groq and Python"
)