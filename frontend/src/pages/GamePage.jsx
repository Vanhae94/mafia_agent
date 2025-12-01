import React, { useState } from 'react';
import CharacterStatus from '../components/CharacterStatus';
import ChatLog from '../components/ChatLog';
import ActionPanel from '../components/ActionPanel';
import { Terminal } from 'lucide-react';

const INITIAL_CHARACTERS = [
  { name: 'Artist', job: '예술가', suspicion: 10, status: 'alive', isTalking: false },
  { name: 'Chef', job: '요리사', suspicion: 45, status: 'alive', isTalking: true },
  { name: 'Worker', job: '회사원', suspicion: 20, status: 'alive', isTalking: false },
  { name: 'Student', job: '대학생', suspicion: 5, status: 'alive', isTalking: false },
  { name: 'Teacher', job: '선생님', suspicion: 80, status: 'dead', isTalking: false },
];

const GamePage = () => {
  const [messages, setMessages] = useState([
    { sender: 'System', text: '게임을 시작합니다. 팬텀은 이들 중에 숨어있습니다.', type: 'system' },
    { sender: 'Chef', text: '저는 아까 주방에만 있었다니까요? 칼질하느라 바빴어요.', type: 'agent' },
  ]);
  const [characters, setCharacters] = useState(INITIAL_CHARACTERS);
  const [phase, setPhase] = useState('Discussion');

  return (
    <div className="flex h-screen bg-noir-900 text-gray-200 overflow-hidden">
      <aside className="w-80 border-r border-noir-700 bg-noir-800/30 flex flex-col">
        <div className="p-6 border-b border-noir-700 flex items-center gap-2">
          <Terminal className="w-5 h-5 text-neon-cyan" />
          <h2 className="font-mono text-lg font-bold tracking-wider text-neon-cyan">SUSPECTS_LOG</h2>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {characters.map((char, idx) => <CharacterStatus key={idx} character={char} />)}
        </div>
      </aside>
      <main className="flex-1 flex flex-col relative">
        <header className="h-16 border-b border-noir-700 flex items-center justify-between px-6 bg-noir-900/80 backdrop-blur-sm z-10">
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 rounded-full border border-noir-700 text-xs font-mono bg-noir-800">
              PHASE: <span className="text-white font-bold">{phase.toUpperCase()}</span>
            </span>
            <span className="text-xs text-gray-500 font-mono">SESSION_ID: #XA-9921</span>
          </div>
          <div className="text-neon-pink text-sm animate-pulse font-bold">
            ⚠ PHANTOM ACTIVE
          </div>
        </header>
        <div className="flex-1 overflow-hidden relative">
           <ChatLog messages={messages} />
        </div>
        <div className="h-auto border-t border-noir-700 bg-noir-800 p-6">
          <ActionPanel phase={phase} />
        </div>
      </main>
    </div>
  );
};
export default GamePage;