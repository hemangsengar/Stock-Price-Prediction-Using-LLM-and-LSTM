import React from 'react';
import { AlertCircle, ShieldCheck } from 'lucide-react';

const ComparisonBlock = () => (
    <section className="comparison-section">
        <div className="comparison-grid">
            <div className="comp-item legacy">
                <h4><AlertCircle /> Traditional Analysis</h4>
                <ul className="comp-list">
                    <li>Human bias in headline interpretation</li>
                    <li>Lagging indicators (SMA/EMA) only</li>
                    <li>Manual peer-to-sector valuation</li>
                    <li>Slow reaction to black-swan news</li>
                </ul>
            </div>
            <div className="comp-divider"></div>
            <div className="comp-item neural">
                <h4><ShieldCheck /> StockPulse Neural AI</h4>
                <ul className="comp-list">
                    <li>Zero-bias LLM sentiment quantification</li>
                    <li>Deep-learning LSTM trend forecasting</li>
                    <li>Automated multi-peer relative valuation</li>
                    <li>Instant 60-day sequence processing</li>
                </ul>
            </div>
        </div>
    </section>
);

export default ComparisonBlock;
