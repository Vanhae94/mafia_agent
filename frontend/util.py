import os

file_contents = {
    # ---------------------------------------------------------
    # 1. GamePage (레이아웃 구조 전면 개편)
    # ---------------------------------------------------------
    "src/pages/GamePage.jsx": """
import React, { useState } from 'react';
import ChatLog from '../components/ChatLog';
import CharacterCard from '../components/CharacterCard';
import RightPanel from '../components/RightPanel';

// Mock Data
const INITIAL_CHARACTERS = [
  { id: 1, name: '김민수', job: '요리사', traits: '열정적, 솔직함', suspicion: 10, status: 'alive' },
  { id: 2, name: '이서연', job: '예술가', traits: '감성적, 예민함', suspicion: 0, status: 'alive' },
  { id: 3, name: '박준호', job: '회사원', traits: '논리적, 분석적', suspicion: 20, status: 'alive' },
  { id: 4, name: '최유진', job: '대학생', traits: '발랄함, 눈치빠름', suspicion: 5, status: 'alive' },
  { id: 5, name: '정태우', job: '선생님', traits: '차분함, 리더십', suspicion: 80, status: 'dead' },
];

const GamePage = () => {
  const [messages, setMessages] = useState([
    { sender: 'System', text: '게임이 시작되었습니다. 5명 중 1명이 팬텀(범인)입니다. 대화를 통해 범인을 찾아내세요!', type: 'system' },
    { sender: '김민수', text: '안녕하세요 여러분. 저는 요리사 김민수입니다. 이런 상황이 믿기지 않네요...', type: 'agent', job: '요리사' },
    { sender: '이서연', text: '정말 무서운 상황이에요. 우리 중 누군가가 범인이라니... 서로 솔직하게 대화해봐요.', type: 'agent', job: '예술가' },
  ]);
  const [characters, setCharacters] = useState(INITIAL_CHARACTERS);
  const [phase, setPhase] = useState('Day - Discussion'); // Day, Night, Vote

  return (
    <div className="flex h-screen bg-noir-900 text-gray-200 overflow-hidden font-sans">
      
      {/* Left Zone: Chat & Characters (Flex Col) */}
      <div className="flex-1 flex flex-col min-w-0 border-r border-noir-700">
        
        {/* Top: Chat Log */}
        <div className="flex-[4] relative border-b border-noir-700 bg-noir-900/50">
           <div className="absolute top-4 left-6 z-10 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-neon-cyan animate-pulse"></span>
              <span className="text-xs font-mono text-neon-cyan tracking-wider">LIVE LOG</span>
           </div>
           <ChatLog messages={messages} />
        </div>

        {/* Bottom: Character Grid */}
        <div className="flex-[3] p-6 bg-noir-800/30 overflow-y-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 h-full content-start">
            {characters.map((char) => (
              <CharacterCard key={char.id} character={char} />
            ))}
          </div>
        </div>
      </div>

      {/* Right Zone: Dashboard */}
      <div className="w-80 bg-noir-900 flex-shrink-0">
        <RightPanel phase={phase} survivorCount={characters.filter(c => c.status === 'alive').length} />
      </div>

    </div>
  );
};

export default GamePage;
""",

    # ---------------------------------------------------------
    # 2. ChatLog (스타일 조정)
    # ---------------------------------------------------------
    "src/components/ChatLog.jsx": """
import React, { useEffect, useRef } from 'react';
import { User } from 'lucide-react';

const ChatLog = ({ messages }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={scrollRef} className="absolute inset-0 overflow-y-auto p-6 pt-12 space-y-4 scrollbar-hide">
      {messages.map((msg, idx) => (
        <div key={idx} className={`flex w-full ${msg.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
          <div className={`flex max-w-[80%] gap-3 ${msg.type === 'system' ? 'w-full max-w-none' : ''}`}>
            
            {/* Avatar for Agents */}
            {msg.type === 'agent' && (
              <div className="w-8 h-8 rounded-full bg-noir-800 border border-noir-700 flex items-center justify-center shrink-0 mt-1">
                 <span className="text-xs font-bold text-gray-400">{msg.sender[0]}</span>
              </div>
            )}

            <div className={`flex flex-col ${msg.type === 'system' ? 'items-center w-full' : ''}`}>
               {/* Sender Info */}
               {msg.type === 'agent' && (
                  <span className="text-xs text-gray-400 mb-1 ml-1">
                    <span className="text-neon-cyan font-bold">{msg.sender}</span> 
                    <span className="opacity-50 mx-1">|</span> 
                    <span className="text-gray-500">{msg.job}</span>
                  </span>
               )}

               {/* Message Bubble */}
               {msg.type === 'system' ? (
                 <div className="flex items-center gap-3 my-4 w-full">
                    <div className="h-px bg-noir-700 flex-1"></div>
                    <span className="text-xs font-mono text-neon-pink border border-neon-pink/30 px-3 py-1 rounded-full bg-neon-pink/5">
                      SYSTEM ALERT: {msg.text}
                    </span>
                    <div className="h-px bg-noir-700 flex-1"></div>
                 </div>
               ) : (
                 <div className={`p-3 rounded-lg text-sm leading-relaxed border backdrop-blur-sm shadow-sm
                   ${msg.sender === 'User' 
                     ? 'bg-neon-cyan/10 border-neon-cyan/30 text-cyan-50 rounded-tr-none' 
                     : 'bg-noir-800 border-noir-700 text-gray-300 rounded-tl-none'
                   }`}>
                   {msg.text}
                 </div>
               )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatLog;
""",

    # ---------------------------------------------------------
    # 3. CharacterCard (새로운 카드 형태 디자인)
    # ---------------------------------------------------------
    "src/components/CharacterCard.jsx": """
import React from 'react';
import { Skull, MessageSquare, Target, Vote } from 'lucide-react';

const CharacterCard = ({ character }) => {
  const isDead = character.status === 'dead';
  const isSuspicious = character.suspicion >= 50;

  return (
    <div className={`relative flex flex-col p-4 rounded-xl border transition-all duration-300 group
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
              <p className="text-[10px] text-neon-cyan font-mono">{character.job}</p>
            </div>
          </div>
        </div>
        {/* Status Badge */}
        {isDead && <Skull className="w-5 h-5 text-gray-600" />}
      </div>

      {/* Traits */}
      <div className="mb-3">
        <p className="text-xs text-gray-500 line-clamp-2 min-h-[2.5em]">
          "{character.traits}"
        </p>
      </div>

      {/* Suspicion Meter */}
      <div className="mt-auto space-y-2">
        <div className="flex justify-between text-[10px] font-mono text-gray-400">
          <span className="flex items-center gap-1 text-neon-pink">
             ⚠ 의심도
          </span>
          <span>{character.suspicion}/100</span>
        </div>
        <div className="w-full bg-noir-900 rounded-full h-1.5 overflow-hidden border border-noir-700">
          <div 
            className={`h-full transition-all duration-500 ${isSuspicious ? 'bg-neon-pink' : 'bg-orange-400'}`}
            style={{ width: `${character.suspicion}%` }}
          />
        </div>

        {/* Action Buttons (Wait User State Interaction) */}
        {!isDead && (
            <div className="grid grid-cols-3 gap-1 mt-3 pt-3 border-t border-noir-700/50">
                <button className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-neon-pink/10 group/btn">
                    <Target className="w-3 h-3 text-gray-500 group-hover/btn:text-neon-pink" />
                    <span className="text-[9px] text-gray-500 group-hover/btn:text-neon-pink">의심</span>
                </button>
                <button className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-neon-cyan/10 group/btn">
                    <MessageSquare className="w-3 h-3 text-gray-500 group-hover/btn:text-neon-cyan" />
                    <span className="text-[9px] text-gray-500 group-hover/btn:text-neon-cyan">1:1</span>
                </button>
                <button className="flex flex-col items-center justify-center gap-1 py-1 rounded hover:bg-white/10 group/btn">
                    <Vote className="w-3 h-3 text-gray-500 group-hover/btn:text-white" />
                    <span className="text-[9px] text-gray-500 group-hover/btn:text-white">투표</span>
                </button>
            </div>
        )}
      </div>

      {isDead && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/40 backdrop-blur-[1px] rounded-xl z-10 pointer-events-none">
           <span className="text-red-700/80 font-black text-2xl rotate-[-15deg] border-4 border-red-700/80 px-2 py-1">OUT</span>
        </div>
      )}
    </div>
  );
};

export default CharacterCard;
""",

    # ---------------------------------------------------------
    # 4. RightPanel (우측 정보 및 컨트롤 패널)
    # ---------------------------------------------------------
    "src/components/RightPanel.jsx": """
import React from 'react';
import { Sun, Moon, Search, Play, FolderOpen } from 'lucide-react';

const RightPanel = ({ phase, survivorCount }) => {
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
           <div className="flex justify-between items-center text-sm">
              <span className="text-gray-400">현재 라운드</span>
              <span className="text-white font-mono">Round 1</span>
           </div>
        </div>
      </div>

      {/* Phase Indicator */}
      <div className="bg-gradient-to-b from-noir-800 to-noir-900 border border-noir-700 rounded-xl p-6 text-center shadow-lg relative overflow-hidden group">
         <div className="absolute inset-0 bg-neon-cyan/5 group-hover:bg-neon-cyan/10 transition-colors" />
         
         <div className="relative z-10 flex flex-col items-center gap-2">
            {phase.includes('Day') ? (
                <Sun className="w-10 h-10 text-yellow-500 animate-pulse" />
            ) : (
                <Moon className="w-10 h-10 text-purple-400 animate-pulse" />
            )}
            <h3 className="font-bold text-lg text-white mt-1">{phase}</h3>
            <p className="text-xs text-gray-500">AI와 대화하며 범인을 찾아보세요</p>
         </div>
      </div>

      {/* Control Actions (Next Turn) */}
      <div className="space-y-3">
         <button className="w-full py-4 bg-gradient-to-r from-neon-pink to-pink-600 rounded-lg text-white font-bold shadow-lg shadow-neon-pink/20 hover:shadow-neon-pink/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2">
            <Play className="w-4 h-4 fill-current" />
            다음 턴으로 (Next)
         </button>
         
         <button className="w-full py-3 bg-noir-800 border border-noir-600 rounded-lg text-gray-300 hover:text-white hover:border-gray-400 transition-colors flex items-center justify-center gap-2 text-sm">
            <Search className="w-4 h-4" />
            단서 정밀 분석
         </button>
      </div>

      {/* Clue List Area */}
      <div className="flex-1 overflow-hidden flex flex-col">
         <h3 className="text-xs font-mono text-gray-500 mb-2 uppercase flex items-center gap-1">
            <Search className="w-3 h-3" /> Discovered Clues
         </h3>
         <div className="flex-1 overflow-y-auto space-y-2 pr-1 scrollbar-hide">
            <div className="p-3 bg-noir-900/80 border border-l-2 border-noir-700 border-l-neon-cyan rounded text-xs text-gray-400 leading-relaxed hover:bg-noir-800 transition-colors cursor-pointer">
               현장에서 요리용 칼이 발견되었습니다. (지문 불명)
            </div>
            <div className="p-3 bg-noir-900/80 border border-l-2 border-noir-700 border-l-purple-500 rounded text-xs text-gray-400 leading-relaxed hover:bg-noir-800 transition-colors cursor-pointer">
               밤 11시경 누군가의 발자국 소리가 들렸다는 증언이 있습니다.
            </div>
         </div>
      </div>

    </div>
  );
};

export default RightPanel;
"""
}

def create_files():
    print("🕵️  Restructuring UI for Tactical Dashboard Layout (V3)...")
    
    for file_path, content in file_contents.items():
        # 디렉토리 생성
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # 파일 쓰기
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
            print(f"   -> Updated: {file_path}")
            
    print("\n✅ V3 Layout Applied.")
    print("👉 Refresh your browser (http://localhost:5173)")

if __name__ == "__main__":
    create_files()