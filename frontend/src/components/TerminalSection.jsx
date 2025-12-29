import React from 'react';
import { Terminal as TerminalIcon, Search, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

const TerminalSection = ({ query, setQuery, onSearch, loading }) => {
    const caseStudies = [
        { name: "Reliance Industries", ticker: "RELIANCE.NS", desc: "High-cap volatility & neural momentum." },
        { name: "TCS", ticker: "TCS.NS", desc: "Blue-chip stability & relative valuation." }
    ];

    return (
        <section id="terminal" style={{ margin: '6rem 0' }}>
            <div className="section-header">
                <div className="badge-label">READY TO DEPLOY</div>
                <h2>Launch the <span>Terminal</span></h2>
                <p>Analyze a specific ticker or test a live case study with pre-computed sequences.</p>
            </div>

            <div className="case-study-grid">
                {caseStudies.map((item, idx) => (
                    <motion.div
                        key={idx}
                        whileHover={{ y: -8, borderColor: 'var(--accent-blue)' }}
                        className="case-btn"
                        onClick={() => onSearch(item.ticker)}
                    >
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <div>
                                <h4>{item.name}</h4>
                                <p>{item.desc}</p>
                            </div>
                            <div style={{ padding: '8px', background: 'rgba(56, 189, 248, 0.1)', borderRadius: '8px', color: 'var(--accent-blue)' }}>
                                <Zap size={16} />
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                className="search-container-v3"
            >
                <form onSubmit={(e) => { e.preventDefault(); onSearch(); }} className="command-bar">
                    <div className="command-icon">
                        <TerminalIcon size={20} />
                    </div>
                    <input
                        type="text"
                        placeholder="Search NSE Ticker (e.g. INFOSYS, RELIANCE, WIPRO)..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? (
                            <span className="analysis-pulse">ANALYZING...</span>
                        ) : (
                            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                RUN NEURAL SCAN <Search size={18} />
                            </span>
                        )}
                    </button>
                </form>
                <p style={{ marginTop: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                    Powered by Claude 3 Opus & LSTM Hidden Layers
                </p>
            </motion.div>
        </section>
    );
};

export default TerminalSection;
