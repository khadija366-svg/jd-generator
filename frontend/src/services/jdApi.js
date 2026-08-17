const API_BASE = 'http://localhost:8000/api/jd'

async function handleResponse(response) {
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const message = data?.detail || 'Something went wrong. Please try again.'
    throw new Error(message)
  }
  return data
}

export async function generateJD({ jobTitle, experienceRequired, requiredSkills, employmentType }) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      job_title: jobTitle,
      experience_required: experienceRequired,
      required_skills: requiredSkills,
      employment_type: employmentType,
    }),
  })
  const data = await handleResponse(response)
  return data.job_description
}

export async function modifyJD({ currentJd, customPrompt }) {
  const response = await fetch(`${API_BASE}/modify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      current_jd: currentJd,
      custom_prompt: customPrompt,
    }),
  })
  const data = await handleResponse(response)
  return data.job_description
}
