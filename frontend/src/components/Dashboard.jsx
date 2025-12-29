import React from 'react';
import {
    Database,
    TrendingUp,
    TrendingDown,
    Activity,
    Newspaper,
    Users,
    Target,
    Zap,
    ArrowUpRight,
    ArrowDownRight
} from 'lucide-react';
import { motion } from 'framer-motion';

const Dashboard = ({ data }) => {
    const isPositive = data.lstm_trend.toLowerCase().includes('bullish');
    const isNeutral = data.lstm_trend.toLowerCase().includes('sideways');

    return (
        <div className="dashboard-v3">
            {/* 💎 Header: The Core Asset */}
            <div className="result-panel" style={{ gridColumn: 'span 12' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                    <div>
                        <div className="ticker-title">{data.ticker} / NSE</div>
                        <h1 style={{ fontSize: '3rem', fontWeight: 800, margin: '0.5rem 0' }}>{data.company_name}</h1>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <div className="price-v3">₹{data.latest_price.toLocaleString()}</div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', justifyContent: 'flex-end', fontSize: '1.2rem', fontWeight: 600 }}>
                            {isPositive ? <ArrowUpRight color="var(--accent-emerald)" /> : <ArrowDownRight color="var(--accent-rose)" />}
                            <span className={isPositive ? "up" : "down"}>{data.lstm_trend} Indicator</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* 🎯 Neural Intelligence Dial */}
            <div className="result-panel" style={{ gridColumn: 'span 5', textAlign: 'center' }}>
                <div className="stat-label" style={{ marginBottom: '2rem' }}>Neural Alpha Score</div>
                <div className="alpha-gauge-v3">
                    <svg viewBox="0 0 100 100" style={{ transform: 'rotate(-90deg)', filter: 'drop-shadow(0 0 8px var(--accent-blue))' }}>
                        <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="6" />
                        <motion.circle
                            cx="50" cy="50" r="45"
                            fill="none"
                            stroke="var(--accent-blue)"
                            strokeWidth="6"
                            strokeDasharray="283"
                            initial={{ strokeDashoffset: 283 }}
                            animate={{ strokeDashoffset: 283 - (283 * (data.unified_alpha_score / 100)) }}
                            transition={{ duration: 1.5, ease: "easeOut" }}
                        />
                    </svg>
                    <div className="alpha-main-val">
                        <h2>{Math.round(data.unified_alpha_score)}</h2>
                        <p style={{ opacity: 0.5, fontSize: '0.8rem', textTransform: 'uppercase' }}>Weight: 60/40</p>
                    </div>
                </div>
                <div style={{ marginTop: '2.5rem' }}>
                    <div className={`recommendation-badge ${data.recommendation.toLowerCase()}`}>
                        <Target size={18} /> {data.recommendation}
                    </div>
                </div>
            </div>

            {/* 📊 Technical Performance Matrix */}
            <div className="result-panel" style={{ gridColumn: 'span 7' }}>
                <div className="stat-label" style={{ marginBottom: '2rem' }}>Technical Momentum Indicators</div>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                    <div className="stat-box">
                        <div className="stat-label">Relative Strength (RSI)</div>
                        <div className="stat-value">{data.indicators.rsi.toFixed(2)}</div>
                        <div className="momentum-meter">
                            <div className="meter-fill" style={{ width: `${data.indicators.rsi}%`, background: data.indicators.rsi > 70 ? 'var(--accent-rose)' : data.indicators.rsi < 30 ? 'var(--accent-emerald)' : 'var(--accent-blue)' }}></div>
                        </div>
                    </div>
                    <div className="stat-box">
                        <div className="stat-label">Moving Average (SMA 50)</div>
                        <div className="stat-value">₹{data.indicators.sma50.toFixed(0)}</div>
                        <div style={{ fontSize: '0.8rem', marginTop: '8px', color: data.latest_price > data.indicators.sma50 ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                            {data.latest_price > data.indicators.sma50 ? '● Trading Above SMA' : '● Trading Below SMA'}
                        </div>
                    </div>
                    <div className="stat-box">
                        <div className="stat-label">Trend Momentum (MACD)</div>
                        <div className="stat-value">{data.indicators.macd.toFixed(2)}</div>
                    </div>
                    <div className="stat-box">
                        <div className="stat-label">Short-term EMA (20)</div>
                        <div className="stat-value">₹{data.indicators.ema20.toFixed(0)}</div>
                    </div>
                </div>
            </div>

            {/* 🧠 Executive AI Logic */}
            <div className="result-panel" style={{ gridColumn: 'span 12' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '2rem' }}>
                    <div style={{ padding: '8px', background: 'rgba(56, 189, 248, 0.1)', borderRadius: '12px', color: 'var(--accent-blue)' }}>
                        <Database size={20} />
                    </div>
                    <div className="stat-label" style={{ margin: 0 }}>Executive Intelligence Synthesis</div>
                </div>
                <p className="insight-card">{data.claude_summary}</p>
            </div>

            {/* 📰 Sentiment Feed & Sector Comparison */}
            <div style={{ gridColumn: 'span 8' }} className="result-panel">
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '2rem' }}>
                    <Newspaper size={20} className="text-blue-400" />
                    <div className="stat-label" style={{ margin: 0 }}>Neural Sentiment Feed</div>
                </div>
                <div className="news-list" style={{ maxHeight: '400px', overflowY: 'auto', paddingRight: '1rem' }}>
                    {data.key_headlines.map((item, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: idx * 0.1 }}
                            className="headline-card"
                        >
                            <a href={item.link} target="_blank" rel="noopener noreferrer" style={{ color: 'white', textDecoration: 'none', fontWeight: 600, display: 'block', marginBottom: '8px', fontSize: '1.05rem' }}>
                                {item.title}
                            </a>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>Yahoo Finance • Real-time</span>
                                {item.sentiment_impact && (
                                    <span style={{ fontSize: '0.8rem', padding: '4px 10px', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', color: 'var(--accent-blue)' }}>
                                        Impact: {item.sentiment_impact}
                                    </span>
                                )}
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            <div style={{ gridColumn: 'span 4' }} className="result-panel">
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '2rem' }}>
                    <Users size={20} className="text-blue-400" />
                    <div className="stat-label" style={{ margin: 0 }}>Sector Pulse</div>
                </div>
                <div className="peer-list">
                    {data.peers.map((peer, idx) => (
                        <div key={idx} className="peer-row">
                            <span style={{ fontWeight: 700, fontSize: '1.1rem' }}>{peer.ticker}</span>
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ fontSize: '0.8rem', opacity: 0.5 }}>Daily Change</div>
                                <span className={peer.change_pct >= 0 ? "up" : "down"} style={{ fontWeight: 800 }}>
                                    {peer.change_pct >= 0 ? "+" : ""}{peer.change_pct.toFixed(2)}%
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
                <div style={{ marginTop: '2.5rem', background: 'rgba(56, 189, 248, 0.05)', padding: '1rem', borderRadius: '12px', fontSize: '0.8rem', color: 'var(--text-secondary)', textAlign: 'center' }}>
                    Relative Strength Index shows current position against {data.peers.length} major industry rivals.
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
