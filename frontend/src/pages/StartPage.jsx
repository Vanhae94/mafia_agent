import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Fingerprint, ScanEye } from 'lucide-react';
import { motion } from 'framer-motion';

const StartPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-noir-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-noir-800 via-noir-900 to-black pointer-events-none" />
      <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px)', backgroundSize: '40px 40px' }}></div>

      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="z-10 text-center space-y-8 p-10 border border-noir-700 bg-noir-800/50 backdrop-blur-md rounded-2xl shadow-2xl max-w-lg w-full"
      >
        <div className="flex justify-center mb-4">
          <ScanEye className="w-16 h-16 text-neon-cyan animate-pulse" />
        </div>
        
        <div>
          <h1 className="text-5xl font-bold tracking-tighter text-white mb-2 font-mono">
            PHANTOM <span className="text-neon-cyan">LOG</span>
          </h1>
          <p className="text-gray-400 text-sm tracking-widest uppercase">Multi-Agent Deduction System</p>
        </div>

        <div className="space-y-4 text-left bg-black/40 p-4 rounded border border-noir-700 font-mono text-xs text-gray-400">
          <p>> SYSTEM: Initializing...</p>
          <p>> TARGET: 5 Suspects Detected.</p>
          <p>> MISSION: Find the <span className="text-neon-pink">PHANTOM</span> before nightfall.</p>
        </div>

        <button onClick={() => navigate('/game')} className="w-full group relative px-8 py-4 bg-transparent overflow-hidden rounded-lg border border-neon-cyan text-neon-cyan hover:bg-neon-cyan hover:text-black transition-all duration-300 shadow-[0_0_15px_rgba(6,182,212,0.3)] hover:shadow-glow-cyan cursor-pointer">
          <span className="relative z-10 flex items-center justify-center gap-2 font-bold tracking-wider">
            <Fingerprint className="w-5 h-5" /> START INVESTIGATION
          </span>
        </button>
      </motion.div>
    </div>
  );
};
export default StartPage;