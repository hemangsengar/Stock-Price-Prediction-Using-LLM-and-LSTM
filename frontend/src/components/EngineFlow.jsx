import React from 'react';
import { Database, Zap, BrainCircuit, Target, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const EngineFlow = () => {
    const steps = [
        { icon: Database, name: "Market Data", desc: "Real-time Yahoo Finance OHLCV ingest" },
        { icon: Zap, name: "LSTM Layer", desc: "60-day temporal feature extraction" },
        { icon: BrainCircuit, name: "Claude 3", desc: "Linguistic sentiment quantification" },
        { icon: Target, name: "Alpha Score", desc: "Unified quantitative recommendation" }
    ];

    return (
        <section style={{ margin: '8rem 0' }}>
            <div className="section-header">
                <div className="badge-label">NEURAL PIPELINE</div>
                <h2>The Pulse <span>Architecture</span></h2>
                <p>How we transform raw noise into high-conviction financial signals.</p>
            </div>

            <div className="engine-flow-container">
                {steps.map((step, idx) => (
                    <React.Fragment key={idx}>
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: idx * 0.2 }}
                            className="flow-node"
                        >
                            <div className="flow-icon-box">
                                <step.icon size={32} />
                            </div>
                            <h4 style={{ marginBottom: '0.5rem', fontWeight: 700 }}>{step.name}</h4>
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', maxWidth: '160px', margin: '0 auto' }}>
                                {step.desc}
                            </p>
                        </motion.div>
                        {idx < steps.length - 1 && (
                            <div className="flow-line"></div>
                        )}
                    </React.Fragment>
                ))}
            </div>
        </section>
    );
};

export default EngineFlow;
