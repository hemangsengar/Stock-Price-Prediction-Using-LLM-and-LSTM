import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Activity } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import StatsBanner from './components/StatsBanner';
import AboutSection from './components/AboutSection';
import ComparisonBlock from './components/ComparisonBlock';
import TechDeepDive from './components/TechDeepDive';
import TerminalSection from './components/TerminalSection';
import Dashboard from './components/Dashboard';
import EngineFlow from './components/EngineFlow';
import FeatureGrid from './components/FeatureGrid';
import ProfessionalFooter from './components/ProfessionalFooter';

const API_BASE = "http://127.0.0.1:8080";

function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const resultsRef = useRef(null);

  const handleSearch = async (val) => {
    const ticker = val || query;
    if (!ticker) return;
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_BASE}/analyze`, { company_name: ticker });
      if (response.data.error) {
        setError(response.data.error);
        setData(null);
      } else {
        setData(response.data);
        setTimeout(() => resultsRef.current?.scrollIntoView({ behavior: 'smooth' }), 200);
      }
    } catch (err) {
      setError("Engine Offline. Ensure the backend is running on port 8080.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: 'relative', overflowX: 'hidden' }}>
      {/* 🧭 Navigation */}
      <Navbar />

      <div className="container">
        {/* 🚀 Hero V4 */}
        <Hero onLaunch={() => document.getElementById('terminal').scrollIntoView({ behavior: 'smooth' })} />

        {/* 📊 Stats Banner */}
        <StatsBanner />

        {/* 📋 About This Project (For Recruiters) */}
        <AboutSection />

        {/* ⚙️ Innovation Narrative */}
        <ComparisonBlock />

        {/* 🌊 Visual Pipeline */}
        <EngineFlow />

        {/* 💎 Premium Tech Deep Dive */}
        <TechDeepDive />

        {/* 🦾 Feature Showcase */}
        <FeatureGrid />

        {/* 🧿 Terminal & Search */}
        <TerminalSection
          query={query}
          setQuery={setQuery}
          onSearch={handleSearch}
          loading={loading}
        />

        {/* 📊 Results Engine */}
        <div ref={resultsRef}>
          <AnimatePresence>
            {loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ textAlign: 'center', padding: '6rem 0' }}>
                <Activity className="spinner" size={48} style={{ color: 'var(--accent-blue)', marginBottom: '2rem' }} />
                <h3 style={{ fontSize: '1.5rem', fontWeight: 600 }}>Synthesizing Quantitative & Qualitative Intelligence...</h3>
              </motion.div>
            )}

            {error && !loading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ textAlign: 'center', padding: '4rem', color: 'var(--accent-rose)' }}>
                <h3>{error}</h3>
              </motion.div>
            )}

            {data && !loading && (
              <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }}>
                <Dashboard data={data} />
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <ProfessionalFooter />
    </div>
  );
}

export default App;
