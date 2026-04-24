import { useState } from 'react'
import SearchBar from './components/SearchBar'
import ProductCard from './components/ProductCard'
import AgentSteps from './components/AgentSteps'
import './App.css'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [steps, setSteps] = useState([])
  const [error, setError] = useState(null)

  const handleSearch = async (query, budget) => {
    setLoading(true)
    setResult(null)
    setSteps([])
    setError(null)

    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, budget }),
      })
      const data = await res.json()

      if (!res.ok) {
        setError(data.error || 'Something went wrong')
      } else {
        setSteps(data.steps)
        setResult(data.product)
      }
    } catch {
      setError('Could not connect to the server. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-badge">AI-Powered</div>
        <h1 className="title">Online Shopping Agent</h1>
        <p className="subtitle">
          Finds the best product across Amazon &amp; the web using autonomous LLM reasoning
        </p>
      </header>

      <main className="main">
        <SearchBar onSearch={handleSearch} loading={loading} />

        {loading && (
          <div className="loading-state">
            <div className="spinner" />
            <p>Agent is thinking and searching&hellip;</p>
          </div>
        )}

        {!loading && steps.length > 0 && <AgentSteps steps={steps} />}

        {!loading && error && <div className="error-card">{error}</div>}

        {!loading && result && <ProductCard product={result} />}
      </main>
    </div>
  )
}
