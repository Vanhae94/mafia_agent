import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatLog from '../components/ChatLog';
import CharacterCard from '../components/CharacterCard';
import RightPanel from '../components/RightPanel';
import { gameApi } from '../api/gameApi';
import { generateSessionId } from '../utils/session';
import { Loader2, RotateCcw, Trophy, Skull } from 'lucide-react';

const GamePage = () => {
  const navigate = useNavigate();

  // 상태 관리
  const [threadId, setThreadId] = useState('');
  const [messages, setMessages] = useState([]);
  const [characters, setCharacters] = useState([]);
  const [phase, setPhase] = useState('Initializing...');
  const [loading, setLoading] = useState(false);
  const [userInput, setUserInput] = useState('');
  const [gameOverInfo, setGameOverInfo] = useState(null); // 게임 종료 정보

  // 1. 컴포넌트 마운트 시 최초 게임 시작
  useEffect(() => {
    startNewGame();
  }, []);

  // 새로운 게임 시작 (세션 초기화)
  const startNewGame = async () => {
    const newSessionId = generateSessionId();
    setThreadId(newSessionId);

    // UI 초기화
    setMessages([]);
    setCharacters([]);
    setPhase('Initializing...');
    setGameOverInfo(null);
    setUserInput('');
    setLoading(true);

    try {
      console.log("🚀 Starting new game session:", newSessionId);
      await gameApi.startGame(newSessionId);
      await fetchGameState(newSessionId);
    } catch (error) {
      console.error("Failed to start game:", error);
      alert("게임 서버 연결 실패. 백엔드 실행 여부를 확인하세요.");
    } finally {
      setLoading(false);
    }
  };

  // 상태 불러오기
  const fetchGameState = async (currentId) => {
    try {
      // currentId가 없으면 state의 threadId 사용 (비동기 처리 안전장치)
      const targetId = currentId || threadId;
      if (!targetId) return;

      const data = await gameApi.getState(targetId);

      // 데이터 매핑
      const rawCharacters = Array.isArray(data.characters) ? data.characters : [];
      const mappedCharacters = rawCharacters.map(char => ({
        ...char,
        suspicion: data.suspicion_counts?.[char.name] ?? 0,
        status: data.alive_status?.[char.name] === false ? 'dead' : 'alive'
      }));
      setCharacters(mappedCharacters);

      const rawMessages = Array.isArray(data.messages) ? data.messages : [];
      const formattedMessages = rawMessages.map(msg => {
        const safeSender = msg.sender || msg.name || 'Unknown';
        const speaker = mappedCharacters.find(c => c.name === safeSender);
        return {
          sender: safeSender,
          text: msg.content || msg.text || '...',
          type: (safeSender === 'System' || msg.type === 'system') ? 'system' : 'agent',
          job: speaker?.job || 'Unknown'
        };
      });
      setMessages(formattedMessages);
      setPhase(data.phase || 'Unknown');

      // 게임 종료 체크 (Backend에서 game_over 플래그나 phase가 'end'일 때)
      if (data.game_over || data.phase === 'end') {
        setGameOverInfo({
          phantom: data.phantom_name || 'Unknown',
          result: 'Mission Complete' // 승패 로직에 따라 변경 가능
        });
      }

    } catch (error) {
      console.error("Fetch error:", error);
    }
  };

  const handleAction = async (actionType, content = null, target = null) => {
    if (!threadId) return;
    try {
      setLoading(true);
      await gameApi.sendAction(threadId, actionType, content, target);
      await fetchGameState(threadId);
    } catch (error) {
      console.error("Action error:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;
    handleAction('chat', userInput);
    setUserInput('');
  };

  return (
    <div className="flex h-screen bg-noir-900 text-gray-200 overflow-hidden font-sans relative">

      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-black/50 z-40 flex items-center justify-center backdrop-blur-sm">
          <Loader2 className="w-10 h-10 text-neon-cyan animate-spin" />
        </div>
      )}

      {/* Game Over Modal */}
      {gameOverInfo && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md">
          <div className="bg-noir-800 border border-neon-cyan/50 p-8 rounded-2xl shadow-[0_0_50px_rgba(6,182,212,0.2)] max-w-md w-full text-center space-y-6">
            <div className="flex justify-center">
              <Trophy className="w-16 h-16 text-yellow-500 animate-bounce" />
            </div>
            <div>
              <h2 className="text-3xl font-bold text-white font-mono mb-2">OPERATION ENDED</h2>
              <p className="text-gray-400">모든 추리가 종료되었습니다.</p>
            </div>

            <div className="bg-noir-900/50 p-4 rounded-lg border border-noir-700">
              <p className="text-sm text-gray-500 mb-1">IDENTIFIED PHANTOM</p>
              <div className="text-2xl font-bold text-neon-pink flex items-center justify-center gap-2">
                <Skull className="w-6 h-6" />
                {gameOverInfo.phantom}
              </div>
            </div>

            <div className="flex gap-3 pt-4">
              <button
                onClick={() => navigate('/')}
                className="flex-1 py-3 rounded-lg border border-noir-600 text-gray-400 hover:bg-noir-700 hover:text-white transition-colors"
              >
                메인으로
              </button>
              <button
                onClick={startNewGame}
                className="flex-1 py-3 rounded-lg bg-neon-cyan text-black font-bold hover:bg-cyan-400 shadow-lg shadow-cyan-500/20 transition-all flex items-center justify-center gap-2"
              >
                <RotateCcw className="w-4 h-4" />
                다시 시작
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Left Zone */}
      <div className="flex-1 flex flex-col min-w-0 border-r border-noir-700">
        {/* Chat Log */}
        <div className="flex-[4] relative border-b border-noir-700 bg-noir-900/50">
          <div className="absolute top-4 left-6 z-10 flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${loading ? 'bg-yellow-500' : 'bg-neon-cyan'} animate-pulse`}></span>
            <span className="text-xs font-mono text-neon-cyan tracking-wider">
              SESSION: {threadId.split('-')[1]}
            </span>
          </div>
          <ChatLog messages={messages} />
        </div>

        {/* Input */}
        <div className="p-4 bg-noir-800 border-b border-noir-700">
          <form onSubmit={handleSendMessage} className="relative">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your deduction..."
              className="w-full bg-noir-900 border border-noir-700 rounded p-3 pl-4 pr-12 text-sm focus:border-neon-cyan focus:outline-none"
              disabled={loading || !!gameOverInfo}
            />
            <button type="submit" disabled={loading} className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-neon-cyan">↵</button>
          </form>
        </div>

        {/* Characters */}
        <div className="flex-[3] p-6 bg-noir-800/30 overflow-y-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4 h-full content-start">
            {characters.map((char, idx) => (
              <CharacterCard
                key={idx}
                character={char}
                onAction={(type) => handleAction(type, null, char.name)}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Right Zone */}
      <div className="w-80 bg-noir-900 flex-shrink-0">
        <RightPanel
          phase={phase}
          survivorCount={characters.filter(c => c.status === 'alive').length}
          onNextTurn={() => handleAction('next')}
          onDiscuss={() => handleAction('discuss')}
          onEndDiscuss={() => handleAction('end_discuss')}
          onContinue={() => handleAction('next')}
        />
      </div>
    </div>
  );
};

export default GamePage;