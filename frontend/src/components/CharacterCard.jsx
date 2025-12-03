import React from 'react';
import { Skull, MessageSquare, Target, Vote } from 'lucide-react';

const CharacterCard = ({ character, onAction }) => {
  const isDead = character.status === 'dead';
  const isSuspicious = character.suspicion >= 5;

  return (
    <div className={`relative flex flex-col p-3 rounded-xl border transition-all duration-300 group
      ${isDead
        ? 'bg-noir-900/50 border-noir-800 opacity-60 grayscale'
        : 'bg-noir-800/80 border-noir-700 hover:border-neon-cyan/50 hover:shadow-glow-cyan'
      }`}>

      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-lg
                ${isDead ? 'bg-gray-800 text-gray-500' : 'bg-neon-cyan text-black'}`}>
              {character.name[0]}
            </div>
            <div>
              <h3 className="font-bold text-gray-200 text-sm leading-tight">{character.name}</h3>
              <p className="text-[11px] text-neon-cyan font-mono">{character.job}</p>
            </div>
          </div>
        </div>
        {isDead && <Skull className="w-5 h-5 text-gray-600" />}
      </div>

      {/* Traits */}
      <div className="mb-3">
        <p className="text-xs text-gray-500 line-clamp-2 min-h-[1.5em]">
          "{character.personality || character.traits || '정보 없음'}"
        </p>
      </div>

      {/* Suspicion Meter */}
      <div className="mt-auto space-y-2">
        <div className="flex justify-between text-[11px] font-mono text-gray-400">
          <span className="flex items-center gap-1 text-neon-pink">
            ⚠ 의심도
          </span>
          <span>{character.suspicion}/10</span>
        </div>
        <div className="w-full bg-noir-900 rounded-full h-1.5 overflow-hidden border border-noir-700">
          <div
            className={`h-full transition-all duration-500 ${isSuspicious ? 'bg-neon-pink' : 'bg-orange-400'}`}
            style={{ width: `${character.suspicion * 10}%` }}
          />
        </div>

        {/* Action Buttons */}
        {!isDead && (
          <div className="grid grid-cols-3 gap-1 mt-3 pt-3 border-t border-noir-700/50">
            <button
              onClick={() => onAction('suspect')}
              className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-neon-pink/10 group/btn transition-colors"
            >
              <Target className="w-3 h-3 text-gray-500 group-hover/btn:text-neon-pink" />
              <span className="text-[9px] text-gray-500 group-hover/btn:text-neon-pink">의심</span>
            </button>
            <button
              onClick={() => onAction('start_one_on_one')}
              className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-neon-cyan/10 group/btn transition-colors"
            >
              <MessageSquare className="w-3 h-3 text-gray-500 group-hover/btn:text-neon-cyan" />
              <span className="text-[9px] text-gray-500 group-hover/btn:text-neon-cyan">1:1</span>
            </button>
            <button
              onClick={() => onAction('vote')}
              className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-white/10 group/btn transition-colors"
            >
              <Vote className="w-3 h-3 text-gray-500 group-hover/btn:text-white" />
              <span className="text-[9px] text-gray-500 group-hover/btn:text-white">투표</span>
            </button>
          </div>
        )}
      </div>

      {isDead && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/60 backdrop-blur-[2px] rounded-xl z-10 pointer-events-none">
          <div className="border-4 border-red-600/80 p-2 rotate-[-15deg] shadow-lg shadow-red-900/50">
            <span className="text-red-600 font-black text-3xl tracking-widest">DEAD</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default CharacterCard;