import React from 'react';
import { Shield, Cpu, CloudLightning, Activity, BarChart3, Lock } from 'lucide-react';
import { motion } from 'framer-motion';

const FeatureGrid = () => {
    const features = [
        {
            icon: Cpu,
            title: "LSTM Forecasting",
            desc: "Deep Neural Networks trained on 60-day historical technical windows for trend prediction."
        },
        {
            icon: CloudLightning,
            title: "LLM Sentiment",
            desc: "Instant linguistic analysis of complex financial news through Claude 3 Opus integration."
        },
        {
            icon: Activity,
            title: "Unified Alpha Score",
            desc: "A proprietary 0-100 metric fusing quantitative momentum with qualitative news sentiment."
        },
        {
            icon: Lock,
            title: "Persistent Caching",
            desc: "SQLite-backed caching layer reduces API latency by 85% for high-frequency ticker lookups."
        },
        {
            icon: Shield,
            title: "Signal Filtering",
            desc: "Automatic noise reduction through multi-period technical verification models."
        },
        {
            icon: BarChart3,
            title: "Sector Pulse",
            desc: "Automated relative valuation against industry peers to identify outlier performance."
        }
    ];

    return (
        <section style={{ margin: '8rem 0' }}>
            <div className="section-header">
                <div className="badge-label">ENGINEERING EXCELLENCE</div>
                <h2>Built for the <span>Next Generation</span></h2>
                <p>Advanced features designed to provide retail investors with enterprise-grade intelligence.</p>
            </div>

            <div className="feature-grid">
                {features.map((f, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, scale: 0.9 }}
                        whileInView={{ opacity: 1, scale: 1 }}
                        viewport={{ once: true }}
                        transition={{ delay: idx * 0.1 }}
                        className="feature-card"
                    >
                        <div className="icon"><f.icon size={32} /></div>
                        <h3>{f.title}</h3>
                        <p>{f.desc}</p>
                    </motion.div>
                ))}
            </div>
        </section>
    );
};

export default FeatureGrid;
