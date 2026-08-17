from app.services.openai_service import generate_completion

GENERATE_SYSTEM_PROMPT = """You are a professional HR/recruitment assistant. \
Given a job title, required experience, required skills, and employment type, \
write a complete, professional, realistic Job Description.

Structure the JD with these sections where relevant:
- Job Title
- Job Overview / Summary
- Responsibilities
- Required Qualifications
- Required Skills
- Experience Requirements
- Employment Type

Rules:
- Use ONLY the information provided by the user.
- Do NOT invent a company name, salary, location, benefits, working hours, \
or technologies/skills that were not supplied.
- Return ONLY the job description text. No explanation, no preamble, no notes."""

MODIFY_SYSTEM_PROMPT = """You are a professional HR/recruitment assistant editing an \
existing Job Description according to a custom instruction from the user.

Rules:
- Preserve the original factual information (title, experience, skills, employment type) \
unless the instruction explicitly asks to change it.
- Follow the user's custom instruction closely.
- Do NOT add salary, location, benefits, company information, or new requirements \
that were not already present or explicitly requested.
- Keep the JD professional, well-structured, and internally consistent.
- Return ONLY the revised job description text. No explanation, no preamble, no notes."""


def generate_jd(job_title: str, experience_required: str, required_skills: list[str], employment_type: str) -> str:
    user_content = (
        f"Job Title: {job_title}\n"
        f"Experience Required: {experience_required}\n"
        f"Required Skills: {', '.join(required_skills)}\n"
        f"Employment Type: {employment_type}"
    )
    return generate_completion(GENERATE_SYSTEM_PROMPT, user_content)


def modify_jd(current_jd: str, custom_prompt: str) -> str:
    user_content = (
        f"Current Job Description:\n{current_jd}\n\n"
        f"Custom Instruction:\n{custom_prompt}"
    )
    return generate_completion(MODIFY_SYSTEM_PROMPT, user_content)
