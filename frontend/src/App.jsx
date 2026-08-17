import { useState } from 'react'
import JobInfoForm from './components/JobInfoForm.jsx'
import JDDisplay from './components/JDDisplay.jsx'
import ErrorBanner from './components/ErrorBanner.jsx'
import { generateJD, modifyJD } from './services/jdApi.js'

export default function App() {
  const [jobDescription, setJobDescription] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isModifying, setIsModifying] = useState(false)
  const [error, setError] = useState('')

  async function handleGenerate(formData) {
    setError('')
    setIsGenerating(true)
    try {
      const jd = await generateJD(formData)
      setJobDescription(jd)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsGenerating(false)
    }
  }

  async function handleModify(customPrompt) {
    setError('')
    setIsModifying(true)
    try {
      const updatedJd = await modifyJD({ currentJd: jobDescription, customPrompt })
      setJobDescription(updatedJd)
    } catch (err) {
      // Preserve the current JD on failure — don't overwrite it
      setError(err.message)
    } finally {
      setIsModifying(false)
    }
  }

  return (
    <div className="app">
      <ErrorBanner message={error} />
      <JobInfoForm onGenerate={handleGenerate} isGenerating={isGenerating} />
      {jobDescription !== null && (
        <JDDisplay
          jobDescription={jobDescription}
          onEdit={setJobDescription}
          onModify={handleModify}
          isModifying={isModifying}
        />
      )}
    </div>
  )
}
