import React from 'react';
import { Sun, Moon, Search, Play, FolderOpen } from 'lucide-react';

const RightPanel = ({ phase, survivorCount, onNextTurn }) => {
  return (
    <div className="h-full flex flex-col border-l border-noir-700 bg-noir-800/30 p-5 space-y-6">
      
      {/* Game Info Box */}
      <div className="space-y-4">
        <h2 className="flex items-center gap-2 text-neon-cyan font-bold font-mono text-sm uppercase tracking-widest">
          <FolderOpen className="w-4 h-4" /> Game Info
        </h2>
        
        <div className="bg-noir-900 border border-noir-700 rounded-lg p-4 space-y-3 shadow-inner">
           <div className="flex justify-between items-center text-sm">
              <span className="text-gray-400">생존자</span>
              <span className="text-white font-mono">{survivorCount} / 5</span>
           </div>
           <div className="flex justify-between items-center text-sm">
              <span className="text-gray-400">발견된 단서</span>
              <span className="text-neon-cyan font-mono">2 개</span>
           </div>
        </div>
      </div>

      {/* Phase Indicator */}
      <div className="bg-gradient-to-b from-noir-800 to-noir-900 border border-noir-700 rounded-xl p-6 text-center shadow-lg relative overflow-hidden group">
         <div className="absolute inset-0 bg-neon-cyan/5 group-hover:bg-neon-cyan/10 transition-colors" />
         
         <div className="relative z-10 flex flex-col items-center gap-2">
            {(phase && phase.includes('Day')) || phase === 'discussion' ? (
                <Sun className="w-10 h-10 text-yellow-500 animate-pulse" />
            ) : (
                <Moon className="w-10 h-10 text-purple-400 animate-pulse" />
            )}
            <h3 className="font-bold text-lg text-white mt-1 capitalize">{phase}</h3>
            <p className="text-xs text-gray-500">AI와 대화하며 범인을 찾아보세요</p>
         </div>
      </div>

      {/* Control Actions (Next Turn) */}
      <div className="space-y-3">
         <button 
            onClick={onNextTurn}
            className="w-full py-4 bg-gradient-to-r from-neon-pink to-pink-600 rounded-lg text-white font-bold shadow-lg shadow-neon-pink/20 hover:shadow-neon-pink/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2 cursor-pointer"
         >
            <Play className="w-4 h-4 fill-current" />
            다음 턴으로 (Next)
         </button>
         
         <button className="w-full py-3 bg-noir-800 border border-noir-600 rounded-lg text-gray-300 hover:text-white hover:border-gray-400 transition-colors flex items-center justify-center gap-2 text-sm cursor-pointer">
            <Search className="w-4 h-4" />
            단서 정밀 분석
         </button>
      </div>
    </div>
  );
};

export default RightPanel;