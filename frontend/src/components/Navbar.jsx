import React, { useState, useEffect } from 'react';
import { Github, Linkedin, FileText, Menu, X, Zap, ExternalLink } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Navbar = () => {
    const [scrolled, setScrolled] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    useEffect(() => {
        const onScroll = () => setScrolled(window.scrollY > 50);
        window.addEventListener('scroll', onScroll);
        return () => window.removeEventListener('scroll', onScroll);
    }, []);

    const links = [
        { label: 'About', href: '#about' },
        { label: 'Try Demo', href: '#terminal' },
        { label: 'GitHub', href: 'https://github.com/hemangsengar/Stock-Price-Prediction-Using-LLM-and-LSTM', external: true, icon: Github },
    ];

    return (
        <nav style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            zIndex: 1000,
            padding: scrolled ? '1rem 2rem' : '1.5rem 2rem',
            background: scrolled ? 'rgba(2, 6, 23, 0.95)' : 'transparent',
            backdropFilter: scrolled ? 'blur(20px)' : 'none',
            borderBottom: scrolled ? '1px solid var(--glass-border)' : 'none',
            transition: 'all 0.3s ease'
        }}>
            <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                {/* Logo & Brand */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
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
                    <div>
                        <div style={{ fontWeight: 800, fontSize: '1.25rem', letterSpacing: '-0.02em' }}>StockPulse AI</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', letterSpacing: '1px' }}>LSTM + LLM RESEARCH</div>
                    </div>
                </div>

                {/* Desktop Links */}
                <div className="nav-links-desktop" style={{ display: 'flex', alignItems: 'center', gap: '2.5rem' }}>
                    {links.map((link, idx) => (
                        <a
                            key={idx}
                            href={link.href}
                            target={link.external ? '_blank' : undefined}
                            rel={link.external ? 'noopener noreferrer' : undefined}
                            style={{
                                color: 'var(--text-secondary)',
                                textDecoration: 'none',
                                fontSize: '0.9rem',
                                fontWeight: 500,
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                                transition: 'color 0.2s'
                            }}
                            onMouseOver={(e) => e.target.style.color = 'white'}
                            onMouseOut={(e) => e.target.style.color = 'var(--text-secondary)'}
                        >
                            {link.icon && <link.icon size={16} />}
                            {link.label}
                            {link.external && <ExternalLink size={12} />}
                        </a>
                    ))}
                    <a
                        href="#terminal"
                        style={{
                            background: 'var(--accent-blue)',
                            color: '#020617',
                            padding: '0.6rem 1.5rem',
                            borderRadius: '10px',
                            fontWeight: 700,
                            fontSize: '0.85rem',
                            textDecoration: 'none',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '8px'
                        }}
                    >
                        Launch Terminal
                    </a>
                </div>

                {/* Mobile Menu Toggle */}
                <button
                    className="mobile-menu-btn"
                    onClick={() => setMobileOpen(!mobileOpen)}
                    style={{
                        display: 'none',
                        background: 'transparent',
                        border: 'none',
                        color: 'white',
                        cursor: 'pointer'
                    }}
                >
                    {mobileOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        style={{
                            position: 'absolute',
                            top: '100%',
                            left: 0,
                            right: 0,
                            background: 'rgba(2, 6, 23, 0.98)',
                            padding: '2rem',
                            borderBottom: '1px solid var(--glass-border)'
                        }}
                    >
                        {links.map((link, idx) => (
                            <a
                                key={idx}
                                href={link.href}
                                target={link.external ? '_blank' : undefined}
                                onClick={() => setMobileOpen(false)}
                                style={{
                                    display: 'block',
                                    color: 'var(--text-secondary)',
                                    textDecoration: 'none',
                                    padding: '1rem 0',
                                    borderBottom: '1px solid var(--glass-border)'
                                }}
                            >
                                {link.label}
                            </a>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
};

export default Navbar;
