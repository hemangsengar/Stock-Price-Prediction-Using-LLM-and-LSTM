import React from 'react';
import { Github, Linkedin, Mail, Heart, Zap } from 'lucide-react';

const ProfessionalFooter = () => (
    <footer className="professional-footer">
        <div className="container">
            <div style={{
                display: 'grid',
                gridTemplateColumns: '2fr 1fr',
                gap: '4rem',
                alignItems: 'start'
            }}>
                {/* Left: Project Info */}
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '1.5rem' }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            background: 'linear-gradient(135deg, var(--accent-blue), var(--accent-cyan))',
                            borderRadius: '12px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                        }}>
                            <Zap size={20} color="#020617" />
                        </div>
                        <div className="footer-logo">StockPulse AI</div>
                    </div>
                    <p style={{ color: 'var(--text-secondary)', maxWidth: '400px', lineHeight: 1.7, marginBottom: '2rem' }}>
                        A technical demonstration of combining Deep Learning (LSTM) with Large Language Models (Claude 3)
                        for intelligent stock market analysis. Built as a portfolio project to showcase full-stack AI engineering skills.
                    </p>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                        <a
                            href="https://github.com/hemangsengar/"
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                                width: '44px',
                                height: '44px',
                                background: 'rgba(255,255,255,0.05)',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--text-secondary)',
                                transition: 'all 0.2s'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.background = 'var(--accent-blue)';
                                e.currentTarget.style.color = '#020617';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                                e.currentTarget.style.color = 'var(--text-secondary)';
                            }}
                        >
                            <Github size={20} />
                        </a>
                        <a
                            href="https://linkedin.com/in/hemangsinghsengar"
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{
                                width: '44px',
                                height: '44px',
                                background: 'rgba(255,255,255,0.05)',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--text-secondary)',
                                transition: 'all 0.2s'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.background = 'var(--accent-blue)';
                                e.currentTarget.style.color = '#020617';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                                e.currentTarget.style.color = 'var(--text-secondary)';
                            }}
                        >
                            <Linkedin size={20} />
                        </a>
                        <a
                            href="mailto:hemang.sengar@gmail.com"
                            style={{
                                width: '44px',
                                height: '44px',
                                background: 'rgba(255,255,255,0.05)',
                                borderRadius: '12px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: 'var(--text-secondary)',
                                transition: 'all 0.2s'
                            }}
                            onMouseOver={(e) => {
                                e.currentTarget.style.background = 'var(--accent-blue)';
                                e.currentTarget.style.color = '#020617';
                            }}
                            onMouseOut={(e) => {
                                e.currentTarget.style.background = 'rgba(255,255,255,0.05)';
                                e.currentTarget.style.color = 'var(--text-secondary)';
                            }}
                        >
                            <Mail size={20} />
                        </a>
                    </div>
                </div>

                {/* Right: Tech Stack Summary */}
                <div>
                    <h4 style={{
                        color: 'var(--accent-blue)',
                        fontSize: '0.85rem',
                        textTransform: 'uppercase',
                        letterSpacing: '1px',
                        marginBottom: '1.5rem'
                    }}>
                        Built With
                    </h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                        {['Python', 'FastAPI', 'TensorFlow', 'React', 'Claude 3 API', 'SQLite', 'Framer Motion'].map((tech) => (
                            <span key={tech} style={{
                                padding: '0.4rem 0.8rem',
                                background: 'rgba(255,255,255,0.03)',
                                border: '1px solid var(--glass-border)',
                                borderRadius: '6px',
                                fontSize: '0.8rem',
                                color: 'var(--text-secondary)'
                            }}>
                                {tech}
                            </span>
                        ))}
                    </div>
                </div>
            </div>

            {/* Bottom Bar */}
            <div style={{
                borderTop: '1px solid var(--glass-border)',
                marginTop: '4rem',
                paddingTop: '2rem',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                color: 'var(--text-secondary)',
                fontSize: '0.85rem',
                flexWrap: 'wrap',
                gap: '1rem'
            }}>
                <p style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    Made with <Heart size={14} color="var(--accent-rose)" /> for learning & demonstration
                </p>
                <p>© 2025 StockPulse AI • Open Source Project</p>
            </div>
        </div>
    </footer>
);

export default ProfessionalFooter;
