import React from 'react';
import { Terminal, Sparkles, ChevronDown } from 'lucide-react';
import { motion } from 'framer-motion';

const Hero = ({ onLaunch }) => (
  <section className="hero-v3">
    <motion.div 
      initial={{ opacity: 0, y: 30 }} 
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
    >
      <div className="badge-label">
        <Sparkles size={14} style={{ marginRight: '8px' }} />
        V3.0 Neural Update
      </div>
      <h1>
        Trading is Noise.<br/>
        <span style={{ color: 'var(--accent-blue)' }}>Predict the Signal.</span>
      </h1>
      <p className="hero-sub">
        Retail investors lose because they react to headlines. StockPulse AI wins by quantifying them. 
        We fuse deep temporal LSTM forecasting with real-time Claude 3 news synthesis to generate 
        one unified <strong style={{ color: 'var(--accent-cyan)' }}>Alpha Score</strong>.
      </p>
      <div style={{ display: 'flex', gap: '1.5rem', justifyContent: 'center', flexWrap: 'wrap' }}>
        <motion.button 
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.98 }}
          onClick={onLaunch}
          style={{ 
            background: 'var(--accent-blue)', 
            color: '#020617', 
            border: 'none', 
            padding: '1.25rem 3rem', 
            borderRadius: '16px', 
            fontWeight: 800, 
            fontSize: '1.1rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '12px'
          }}
        >
          Launch Terminal <Terminal size={20} />
        </motion.button>
        <motion.button 
          whileHover={{ scale: 1.05 }}
          onClick={() => document.querySelector('.comparison-section')?.scrollIntoView({ behavior: 'smooth' })}
          style={{ 
            background: 'transparent', 
            color: 'var(--text-secondary)', 
            border: '1px solid var(--glass-border)', 
            padding: '1.25rem 2.5rem', 
            borderRadius: '16px', 
            fontWeight: 600, 
            fontSize: '1rem',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}
        >
          Learn More <ChevronDown size={18} />
        </motion.button>
      </div>
    </motion.div>
    
    {/* Scroll indicator */}
    <motion.div 
      animate={{ y: [0, 10, 0] }}
      transition={{ repeat: Infinity, duration: 2 }}
      style={{ 
        position: 'absolute', 
        bottom: '2rem', 
        left: '50%', 
        transform: 'translateX(-50%)',
        color: 'var(--text-secondary)',
        opacity: 0.5
      }}
    >
      <ChevronDown size={24} />
    </motion.div>
  </section>
);

export default Hero;
