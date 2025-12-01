import React, { useState } from 'react';
import { Ghost, Play, Terminal } from 'lucide-react';

const StartScreen = ({ onStart }) => {
    const [playerName, setPlayerName] = useState('User');
    const [isHovered, setIsHovered] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        onStart(playerName);
    };

    return (
        <div className="h-screen w-full flex flex-col items-center justify-center bg-[url('/bg-grid.svg')] bg-cover relative overflow-hidden">
            {/* Background Overlay for Noir Atmosphere */}
            <div className="absolute inset-0 bg-gradient-to-b from-black/20 via-black/50 to-black/90 pointer-events-none"></div>

            <div className="z-10 flex flex-col items-center gap-8 max-w-md w-full p-8">
                {/* Logo / Title */}
                <div className="flex flex-col items-center gap-4 animate-fade-in-down">
                    <div className="relative">
                        <div className="absolute inset-0 bg-cyan-500/20 blur-xl rounded-full animate-pulse"></div>
                        <Ghost size={80} className="text-cyan-400 relative z-10 drop-shadow-[0_0_15px_rgba(0,243,255,0.5)]" />
                    </div>
                    <h1 className="text-5xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600 drop-shadow-[0_0_10px_rgba(0,243,255,0.3)]">
                        PHANTOM LOG
                    </h1>
                    <p className="text-gray-400 tracking-widest text-sm uppercase border-b border-gray-800 pb-2">
                        Silicon Noir Mystery Agent
                    </p>
                </div>

                {/* Start Form */}
                <form onSubmit={handleSubmit} className="w-full flex flex-col gap-6 glass-panel p-8 border-cyan-500/20 shadow-[0_0_30px_rgba(0,0,0,0.5)]">
                    <div className="flex flex-col gap-2">
                        <label className="text-xs text-cyan-500/80 font-mono uppercase tracking-wider flex items-center gap-2">
                            <Terminal size={16} /> Agent Identity
                        </label>
                        <input
                            type="text"
                            value={playerName}
                            onChange={(e) => setPlayerName(e.target.value)}
                            className="bg-black/50 border border-gray-700 text-gray-200 px-4 py-3 rounded-sm focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all font-mono text-center tracking-wider"
                            placeholder="Enter Codename..."
                        />
                    </div>

                    <button
                        type="submit"
                        onMouseEnter={() => setIsHovered(true)}
                        onMouseLeave={() => setIsHovered(false)}
                        className="group relative bg-cyan-900/20 border border-cyan-500/50 text-cyan-400 py-4 px-6 rounded-sm font-bold tracking-widest uppercase transition-all hover:bg-cyan-500 hover:text-black hover:shadow-[0_0_20px_rgba(0,243,255,0.4)] flex items-center justify-center gap-3 overflow-hidden"
                    >
                        <span className="relative z-10">Initialize Protocol</span>
                        <Play size={18} className={`relative z-10 transition-transform ${isHovered ? 'translate-x-1' : ''}`} />

                        {/* Button Glitch Effect Overlay */}
                        <div className="absolute inset-0 bg-cyan-400/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                    </button>
                </form>

                {/* Footer Status */}
                <div className="text-xs text-gray-600 font-mono flex gap-4">
                    <span className="flex items-center gap-1">
                        <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                        SYSTEM ONLINE
                    </span>
                    <span>v1.0.4</span>
                </div>
            </div>
        </div>
    );
};

export default StartScreen;
