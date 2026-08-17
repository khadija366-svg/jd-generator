from pydantic import BaseModel, field_validator


class GenerateJDRequest(BaseModel):
    job_title: str
    experience_required: str
    required_skills: list[str]
    employment_type: str

    @field_validator("job_title", "experience_required", "employment_type")
    @classmethod
    def not_empty_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("This field cannot be empty.")
        return v.strip()

    @field_validator("required_skills")
    @classmethod
    def not_empty_list(cls, v: list[str]) -> list[str]:
        cleaned = [s.strip() for s in v if s and s.strip()]
        if not cleaned:
            raise ValueError("Required skills cannot be empty.")
        return cleaned


class ModifyJDRequest(BaseModel):
    current_jd: str
    custom_prompt: str

    @field_validator("current_jd", "custom_prompt")
    @classmethod
    def not_empty_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("This field cannot be empty.")
        return v.strip()


class JDResponse(BaseModel):
    success: bool
    job_description: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
