import React from 'react';
import { motion } from 'framer-motion';
import { Zap, Clock, Database, BarChart3 } from 'lucide-react';

const StatsBanner = () => {
    const stats = [
        { icon: BarChart3, value: "60/40", label: "Quant-Sentiment Fusion" },
        { icon: Clock, value: "<3s", label: "Analysis Speed" },
        { icon: Database, value: "5+", label: "Data Sources" },
        { icon: Zap, value: "85%", label: "Cache Hit Rate" }
    ];

    return (
        <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '2rem',
            padding: '3rem',
            background: 'rgba(255, 255, 255, 0.02)',
            borderRadius: '24px',
            border: '1px solid var(--glass-border)',
            margin: '4rem 0'
        }}>
            {stats.map((stat, idx) => (
                <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: idx * 0.1 }}
                    style={{ textAlign: 'center' }}
                >
                    <stat.icon size={24} style={{ color: 'var(--accent-blue)', marginBottom: '1rem' }} />
                    <div style={{ fontSize: '2.5rem', fontWeight: 800, color: 'white', marginBottom: '0.5rem' }}>
                        {stat.value}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                        {stat.label}
                    </div>
                </motion.div>
            ))}
        </div>
    );
};

export default StatsBanner;
