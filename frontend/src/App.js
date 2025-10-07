import React from 'react';
import GovernanceOverview from './components/GovernanceOverview';
import RiskAssessment from './components/RiskAssessment';
import PolicyCompliance from './components/PolicyCompliance';
import BiasAnalysis from './components/BiasAnalysis';
import AuditReporting from './components/AuditReporting';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Enterprise AI Audit Platform</h1>
      </header>
      <main>
        <GovernanceOverview />
        <RiskAssessment />
        <PolicyCompliance />
        <BiasAnalysis />
        <AuditReporting />
      </main>
    </div>
  );
}

export default App;
