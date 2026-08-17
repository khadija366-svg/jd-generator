import { useState } from 'react'

export default function JobInfoForm({ onGenerate, isGenerating }) {
  const [jobTitle, setJobTitle] = useState('')
  const [experienceRequired, setExperienceRequired] = useState('')
  const [requiredSkillsText, setRequiredSkillsText] = useState('')
  const [employmentType, setEmploymentType] = useState('')

  function handleSubmit(e) {
    e.preventDefault()
    // "Python, FastAPI, PostgreSQL, REST APIs" -> ["Python", "FastAPI", "PostgreSQL", "REST APIs"]
    const requiredSkills = requiredSkillsText
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0)

    onGenerate({ jobTitle, experienceRequired, requiredSkills, employmentType })
  }

  return (
    <form className="card" onSubmit={handleSubmit}>
      <h1>AI Job Description Generator</h1>

      <label className="field">
        <span>Job Title</span>
        <input
          type="text"
          placeholder="Backend Developer"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          required
        />
      </label>

      <label className="field">
        <span>Experience Required</span>
        <input
          type="text"
          placeholder="2-3 years"
          value={experienceRequired}
          onChange={(e) => setExperienceRequired(e.target.value)}
          required
        />
      </label>

      <label className="field">
        <span>Required Skills</span>
        <input
          type="text"
          placeholder="Python, FastAPI, PostgreSQL, REST APIs"
          value={requiredSkillsText}
          onChange={(e) => setRequiredSkillsText(e.target.value)}
          required
        />
        <small>Comma-separated</small>
      </label>

      <label className="field">
        <span>Employment Type</span>
        <input
          type="text"
          placeholder="Full-time"
          value={employmentType}
          onChange={(e) => setEmploymentType(e.target.value)}
          required
        />
      </label>

      <button type="submit" disabled={isGenerating}>
        {isGenerating ? 'Generating...' : 'Generate JD'}
      </button>
    </form>
  )
}
