def build_analysis_prompt(
    resume_text,
    job_description
):

    return f"""
You are an expert technical recruiter.

Analyze the resume and compare it with the job description.

Return:

1. Candidate Strengths
2. Missing Skills
3. Resume Match Score (0-100)
4. Improvement Suggestions

Resume:

{resume_text}

Job Description:

{job_description}
"""

def build_questions_prompt(
    resume_text,
    job_description
):

    return f"""
Generate exactly 10 interview questions.

Return ONLY valid JSON.

Format:

{{
    "questions": [
        "question1",
        "question2",
        "question3"
    ]
}}

Resume:
{resume_text}

Job Description:
{job_description}
"""

def build_scorecard_prompt(
    questions,
    answers
):

    return f"""
You are a senior technical interviewer.

Evaluate the interview.

Provide:

1. Overall Score (0-100)

2. Technical Knowledge Score

3. Communication Score

4. Problem Solving Score

5. Strengths

6. Weaknesses

7. Improvement Plan

8. Hiring Recommendation

Questions:

{questions}

Answers:

{answers}
"""