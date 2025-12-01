import React from 'react';
import { User, Skull } from 'lucide-react';

const CharacterStatus = ({ character }) => {
  const isDead = character.status === 'dead';
  const isSuspicious = character.suspicion >= 50;

  return (
    <div className={`relative p-4 rounded border transition-all duration-300 ${isDead ? 'border-gray-800 bg-gray-900/50 opacity-60 grayscale' : isSuspicious ? 'border-neon-pink/50 bg-neon-pink/5 shadow-[inset_0_0_20px_rgba(244,63,94,0.1)]' : 'border-noir-700 bg-noir-800 hover:border-neon-cyan/50'}`}>
      <div className="flex justify-between items-start mb-2">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-full ${isDead ? 'bg-gray-800' : 'bg-noir-900'}`}>
            {isDead ? <Skull className="w-5 h-5 text-gray-500" /> : <User className="w-5 h-5 text-gray-300" />}
          </div>
          <div>
            <h3 className="font-bold text-sm">{character.name}</h3>
            <span className="text-xs text-gray-500 block">{character.job}</span>
          </div>
        </div>
        {character.isTalking && (
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-cyan opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-neon-cyan"></span>
          </span>
        )}
      </div>
      <div className="mt-3">
        <div className="flex justify-between text-[10px] font-mono mb-1 text-gray-400">
          <span>SUSPICION LEVEL</span>
          <span className={isSuspicious ? 'text-neon-pink' : 'text-neon-cyan'}>{character.suspicion}%</span>
        </div>
        <div className="w-full bg-noir-900 rounded-full h-1.5 overflow-hidden">
          <div className={`h-full transition-all duration-500 ${isSuspicious ? 'bg-neon-pink' : 'bg-neon-cyan'}`} style={{ width: `${character.suspicion}%` }} />
        </div>
      </div>
      {isDead && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-[1px] rounded">
          <span className="text-red-600 font-black border-2 border-red-600 px-2 py-1 rotate-[-15deg] text-lg">DECEASED</span>
        </div>
      )}
    </div>
  );
};
export default CharacterStatus;