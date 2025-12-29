import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Zap, Layers, BrainCircuit } from 'lucide-react';

const techStack = {
    "FastAPI": {
        desc: "High-performance asynchronous backend for parallelizing data fetches and model inference.",
        code: `app = FastAPI()\n\n@app.post("/analyze")\nasync def analyze(ticker: str):\n    # Parallel fetch + inference\n    results = await engine.run(ticker)\n    return results`
    },
    "LSTM": {
        desc: "Recurrent Neural Network optimized for time-series forecasting across 60-day historical technical windows.",
        code: `model = Sequential([\n    LSTM(50, return_sequences=True),\n    Dropout(0.2),\n    LSTM(50),\n    Dense(1, activation='linear')\n])`
    },
    "Claude 3": {
        desc: "LLM Orchestration for qualitative news synthesis and high-precision ticker resolution.",
        code: `async def synthesize(news):\n    response = await claude.messages.create(\n        model="claude-3-opus",\n        prompt=f"Quantify impact of: {news}"\n    )`
    }
};

const TechDeepDive = () => {
    const [activeTech, setActiveTech] = useState("FastAPI");

    return (
        <section style={{ margin: '6rem 0' }}>
            <div className="section-header">
                <div className="badge-label">THE ARCHITECTURE</div>
                <h2>Engineered for Raw Speed</h2>
                <p>A high-information stack designed for low-latency financial intelligence.</p>
            </div>

            <div className="tech-chips">
                {Object.keys(techStack).map(key => (
                    <div
                        key={key}
                        className={`tech-chip ${activeTech === key ? 'active' : ''}`}
                        onClick={() => setActiveTech(key)}
                    >
                        {key === 'FastAPI' && <Zap size={16} />}
                        {key === 'LSTM' && <Layers size={16} />}
                        {key === 'Claude 3' && <BrainCircuit size={16} />}
                        {key}
                    </div>
                ))}
            </div>

            <AnimatePresence mode="wait">
                <motion.div
                    key={activeTech}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                >
                    <p style={{ textAlign: 'center', marginBottom: '2rem', color: 'var(--text-secondary)', maxWidth: '600px', margin: '0 auto 2rem' }}>
                        {techStack[activeTech].desc}
                    </p>
                    <div className="code-window">
                        <div style={{ display: 'flex', gap: '6px', marginBottom: '1rem' }}>
                            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ff5f56' }}></div>
                            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#ffbd2e' }}></div>
                            <div style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#27c93f' }}></div>
                        </div>
                        <pre style={{ margin: 0, color: '#94a3b8' }}>
                            <code>{techStack[activeTech].code}</code>
                        </pre>
                    </div>
                </motion.div>
            </AnimatePresence>
        </section>
    );
};

export default TechDeepDive;
