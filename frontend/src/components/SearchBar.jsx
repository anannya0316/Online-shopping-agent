import { useState } from 'react'

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [budget, setBudget] = useState(500)
  const [noBudget, setNoBudget] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!query.trim()) return
    onSearch(query.trim(), noBudget ? null : budget)
  }

  return (
    <form className="search-card" onSubmit={handleSubmit}>
      <div className="field">
        <label>What are you looking for?</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='e.g. "iPhone 14", "noise-cancelling headphones"'
          disabled={loading}
        />
      </div>

      <div className="field">
        <div className="budget-label">
          <label>Budget</label>
          {!noBudget && <span className="budget-value">${budget}</span>}
        </div>
        <input
          type="range"
          className="slider"
          min="50"
          max="2000"
          step="50"
          value={budget}
          onChange={(e) => setBudget(Number(e.target.value))}
          disabled={loading || noBudget}
        />
        <label className="no-budget-label">
          <input
            type="checkbox"
            checked={noBudget}
            onChange={(e) => setNoBudget(e.target.checked)}
            disabled={loading}
          />
          No budget limit
        </label>
      </div>

      <button type="submit" className="search-btn" disabled={loading || !query.trim()}>
        {loading ? 'Searching…' : 'Find Best Product'}
      </button>
    </form>
  )
}
