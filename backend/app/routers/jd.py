from fastapi import APIRouter, HTTPException

from app.schemas.jd import GenerateJDRequest, ModifyJDRequest, JDResponse
from app.services import jd_service
from app.core.exceptions import (
    LLMTimeoutError,
    LLMRateLimitError,
    LLMProviderError,
    LLMBadResponseError,
)

router = APIRouter(prefix="/api/jd", tags=["jd"])


def _handle_llm_errors(func, *args):
    try:
        return func(*args)
    except LLMTimeoutError:
        raise HTTPException(status_code=504, detail="The AI provider took too long to respond. Please try again.")
    except LLMRateLimitError:
        raise HTTPException(status_code=502, detail="The AI provider is rate-limited right now. Please try again shortly.")
    except (LLMProviderError, LLMBadResponseError):
        raise HTTPException(status_code=502, detail="The AI provider failed to generate a response. Please try again.")


@router.post("/generate", response_model=JDResponse)
def generate_jd(payload: GenerateJDRequest):
    jd_text = _handle_llm_errors(
        jd_service.generate_jd,
        payload.job_title,
        payload.experience_required,
        payload.required_skills,
        payload.employment_type,
    )
    return JDResponse(success=True, job_description=jd_text)


@router.post("/modify", response_model=JDResponse)
def modify_jd(payload: ModifyJDRequest):
    jd_text = _handle_llm_errors(jd_service.modify_jd, payload.current_jd, payload.custom_prompt)
    return JDResponse(success=True, job_description=jd_text)
