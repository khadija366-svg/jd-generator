import { useState } from 'react'

export default function JDDisplay({ jobDescription, onEdit, onModify, isModifying }) {
  const [customPrompt, setCustomPrompt] = useState('')
  const [copied, setCopied] = useState(false)

  function handleCopy() {
    navigator.clipboard.writeText(jobDescription).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    })
  }

  function handleModify() {
    if (!customPrompt.trim()) return
    onModify(customPrompt)
  }

  return (
    <div className="card">
      <div className="jd-header">
        <h2>Generated Job Description</h2>
        <button type="button" className="secondary" onClick={handleCopy}>
          {copied ? 'Copied!' : 'Copy JD'}
        </button>
      </div>

      <textarea
        className="jd-textarea"
        value={jobDescription}
        onChange={(e) => onEdit(e.target.value)}
        rows={16}
      />

      <label className="field">
        <span>Custom Prompt</span>
        <textarea
          placeholder="Make this JD more concise and emphasize Python and FastAPI experience."
          value={customPrompt}
          onChange={(e) => setCustomPrompt(e.target.value)}
          rows={3}
        />
      </label>

      <button type="button" onClick={handleModify} disabled={isModifying || !customPrompt.trim()}>
        {isModifying ? 'Modifying...' : 'Modify JD'}
      </button>
    </div>
  )
}
