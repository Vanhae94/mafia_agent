import React from 'react';
import { Skull, HeartPulse } from 'lucide-react';

const CharacterStatus = ({ characters, aliveStatus, suspicionCounts }) => {
    return (
        <div className="glass-panel p-4 h-full">
            <h3 className="text-lg font-bold mb-4 neon-text-blue border-b border-gray-700 pb-2">
                참가자 현황
            </h3>
            <div className="space-y-3">
                {characters.map((char) => {
                    const isAlive = aliveStatus[char.name] !== false;
                    const suspicion = suspicionCounts[char.name] || 0;

                    return (
                        <div key={char.name} className={`flex items-center justify-between p-3 rounded-lg border transition-all
              ${isAlive
                                ? 'bg-gray-800/50 border-gray-700 hover:border-gray-500'
                                : 'bg-red-900/10 border-red-900/30 opacity-60'
                            }`}>
                            <div className="flex items-center gap-3">
                                <div className={`w-2 h-2 rounded-full ${isAlive ? 'bg-green-500 shadow-[0_0_5px_#00ff9d]' : 'bg-red-500'}`} />
                                <div>
                                    <div className="font-medium text-sm text-gray-200">
                                        {char.name}
                                        {!isAlive && <span className="ml-2 text-xs text-red-400">(사망)</span>}
                                    </div>
                                    <div className="text-xs text-gray-500">{char.job}</div>
                                </div>
                            </div>

                            <div className="flex items-center gap-2" title="의심 수치">
                                <span className="text-xs text-gray-600">의심</span>
                                <div className={`px-2 py-0.5 rounded text-xs font-bold
                  ${suspicion > 3 ? 'bg-red-500/20 text-red-400' : 'bg-gray-700 text-gray-400'}`}>
                                    {suspicion}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default CharacterStatus;
