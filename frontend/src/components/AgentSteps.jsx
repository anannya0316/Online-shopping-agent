const ACTION_META = {
  search_amazon:     { label: 'Searched Amazon', icon: '🛒' },
  search_aggregator: { label: 'Searched the web', icon: '🌐' },
}

export default function AgentSteps({ steps }) {
  return (
    <div className="steps-card">
      <p className="steps-title">Agent Reasoning</p>
      <div className="steps-list">
        {steps.map((s, i) => {
          const { label, icon } = ACTION_META[s.action] ?? { label: s.action, icon: '🤖' }
          return (
            <div key={i} className="step">
              <div className="step-icon">{icon}</div>
              <div className="step-content">
                <span className="step-label">{label}</span>
                <span className="step-found">{s.found} products found</span>
              </div>
            </div>
          )
        })}
        <div className="step">
          <div className="step-icon">✅</div>
          <div className="step-content">
            <span className="step-label">Selected best match</span>
          </div>
        </div>
      </div>
    </div>
  )
}
