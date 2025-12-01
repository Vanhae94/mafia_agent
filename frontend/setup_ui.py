import os

# 파일 내용 정의
file_contents = {
    # ---------------------------------------------------------
    # 1. 필수 설정 파일 (npm run dev 에러 해결용)
    # ---------------------------------------------------------
    "package.json": """
{
  "name": "phantom-log-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint .",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.22.0",
    "framer-motion": "^11.0.0",
    "lucide-react": "^0.344.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.56",
    "@types/react-dom": "^18.2.19",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.17",
    "eslint": "^8.56.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "vite": "^5.1.4"
  }
}
""",
    "vite.config.js": """
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
""",
    "index.html": """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Phantom Log</title>
  </head>
  <body class="bg-noir-900">
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""",
    "postcss.config.js": """
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""",
    "tailwind.config.js": """
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        noir: {
          900: '#09090b', // Main Background
          800: '#18181b', // Panel Background
          700: '#27272a', // Border
        },
        neon: {
          cyan: '#06b6d4', // Safe/System
          pink: '#f43f5e', // Danger/Suspect
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glow-cyan': '0 0 10px rgba(6, 182, 212, 0.5)',
        'glow-pink': '0 0 10px rgba(244, 63, 94, 0.5)',
      }
    },
  },
  plugins: [],
}
""",

    # ---------------------------------------------------------
    # 2. 스타일 파일 (요청하신대로 styles 폴더로 이동)
    # ---------------------------------------------------------
    "src/styles/index.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom Scrollbar for Webkit */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #09090b; 
}
::-webkit-scrollbar-thumb {
  background: #27272a; 
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #06b6d4; 
}
""",

    # ---------------------------------------------------------
    # 3. React 메인 진입점 (변경된 CSS 경로 적용)
    # ---------------------------------------------------------
    "src/main.jsx": """
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/index.css'  // 경로 변경됨!

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
""",

    # ---------------------------------------------------------
    # 4. React 컴포넌트 및 페이지 (기존 코드 유지)
    # ---------------------------------------------------------
    "src/App.jsx": """
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import StartPage from './pages/StartPage';
import GamePage from './pages/GamePage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-noir-900 text-gray-300 font-sans selection:bg-neon-cyan selection:text-black">
        <Routes>
          <Route path="/" element={<StartPage />} />
          <Route path="/game" element={<GamePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
""",
    "src/pages/StartPage.jsx": """
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
""",
    "src/pages/GamePage.jsx": """
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
""",
    "src/components/CharacterStatus.jsx": """
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
""",
    "src/components/ChatLog.jsx": """
import React, { useEffect, useRef } from 'react';

const ChatLog = ({ messages }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={scrollRef} className="absolute inset-0 overflow-y-auto p-6 space-y-4 scrollbar-hide">
      {messages.map((msg, idx) => (
        <div key={idx} className={`flex ${msg.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
          <div className={`max-w-[70%] ${msg.type === 'system' ? 'w-full max-w-none text-center' : ''}`}>
            {msg.type !== 'system' && msg.sender !== 'User' && (
              <span className="text-xs font-mono text-neon-cyan mb-1 block pl-1">> {msg.sender}</span>
            )}
            <div className={`p-4 rounded-lg text-sm leading-relaxed border backdrop-blur-sm ${msg.type === 'system' ? 'bg-transparent border-none text-gray-500 text-xs font-mono my-4' : msg.sender === 'User' ? 'bg-neon-cyan/10 border-neon-cyan/30 text-cyan-50 rounded-br-none' : 'bg-noir-800 border-noir-700 text-gray-300 rounded-tl-none shadow-lg'}`}>
              {msg.text}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
export default ChatLog;
""",
    "src/components/ActionPanel.jsx": """
import React, { useState } from 'react';
import { Send, Eye, MessageSquare, Vote } from 'lucide-react';

const ActionPanel = ({ phase }) => {
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    setInput('');
  };

  return (
    <div className="max-w-4xl mx-auto w-full">
      <div className="flex gap-2 mb-4 justify-center">
        <button className="flex items-center gap-2 px-4 py-2 rounded bg-noir-900 border border-noir-700 text-xs text-gray-400 hover:text-neon-cyan hover:border-neon-cyan transition-colors cursor-pointer">
          <Eye className="w-4 h-4" /> 의심하기
        </button>
        <button className="flex items-center gap-2 px-4 py-2 rounded bg-noir-900 border border-noir-700 text-xs text-gray-400 hover:text-white hover:border-white transition-colors cursor-pointer">
          <MessageSquare className="w-4 h-4" /> 1:1 대화
        </button>
        {phase === 'voting' && (
             <button className="flex items-center gap-2 px-4 py-2 rounded bg-red-900/20 border border-red-900 text-xs text-red-500 hover:bg-red-900/40 hover:text-red-400 transition-colors animate-pulse cursor-pointer">
             <Vote className="w-4 h-4" /> 투표하기
           </button>
        )}
      </div>

      <form onSubmit={handleSend} className="relative group">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your deduction here..."
          className="w-full bg-noir-900/50 border border-noir-700 rounded-lg pl-4 pr-12 py-4 text-gray-200 focus:outline-none focus:border-neon-cyan focus:ring-1 focus:ring-neon-cyan transition-all font-mono text-sm placeholder:text-gray-600"
        />
        <button 
          type="submit"
          className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-md text-gray-500 hover:text-neon-cyan transition-colors cursor-pointer"
        >
          <Send className="w-5 h-5" />
        </button>
      </form>
    </div>
  );
};
export default ActionPanel;
"""
}

def create_files():
    print("🕵️  System Reboot: Phantom Log Interface V2...")
    print("📂 Creating 'styles' directory and configuration files...")
    
    for file_path, content in file_contents.items():
        # 디렉토리 생성
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   + Directory: {directory}")
        
        # 파일 쓰기
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
            print(f"   -> Generated: {file_path}")
            
    print("\n✅ Setup Complete.")
    print("👉 Next Steps:")
    print("   1. npm install (To install the new package.json dependencies)")
    print("   2. npm run dev")

if __name__ == "__main__":
    create_files()