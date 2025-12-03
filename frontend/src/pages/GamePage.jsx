import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatLog from '../components/ChatLog';
import CharacterCard from '../components/CharacterCard';
import RightPanel from '../components/RightPanel';
import { gameApi } from '../api/gameApi';
import { generateSessionId } from '../utils/session';
import { Loader2, RotateCcw, Trophy, Skull, Search } from 'lucide-react';

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

  // 추가된 상태
  const [showSummaryModal, setShowSummaryModal] = useState(false);
  const [showClueModal, setShowClueModal] = useState(false);
  const [roundSummaries, setRoundSummaries] = useState({});
  const [clues, setClues] = useState([]);

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
    setRoundSummaries({});
    setClues([]);
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
      setRoundSummaries(data.round_summaries || {});
      setClues(data.clues || []);

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

      {/* Modals */}
      {showSummaryModal && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setShowSummaryModal(false)}>
          <div className="bg-noir-800 border border-neon-cyan/30 rounded-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4 border-b border-noir-700 pb-2">
              <h2 className="text-xl font-bold text-neon-cyan flex items-center gap-2">
                <Trophy className="w-5 h-5" /> 지난 라운드 요약
              </h2>
              <button onClick={() => setShowSummaryModal(false)} className="text-gray-400 hover:text-white">✕</button>
            </div>
            <div className="space-y-4">
              {Object.keys(roundSummaries).length > 0 ? (
                Object.entries(roundSummaries).map(([round, summary]) => (
                  <div key={round} className="bg-noir-900/50 p-4 rounded-lg border border-noir-700">
                    <h3 className="text-sm font-bold text-gray-400 mb-2">ROUND {round}</h3>
                    <p className="text-sm text-gray-300 whitespace-pre-wrap leading-relaxed">{summary}</p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-8">아직 요약된 라운드가 없습니다.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {showClueModal && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setShowClueModal(false)}>
          <div className="bg-noir-800 border border-neon-cyan/30 rounded-xl max-w-lg w-full max-h-[80vh] overflow-y-auto p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center mb-4 border-b border-noir-700 pb-2">
              <h2 className="text-xl font-bold text-neon-cyan flex items-center gap-2">
                <Search className="w-5 h-5" /> 발견된 단서
              </h2>
              <button onClick={() => setShowClueModal(false)} className="text-gray-400 hover:text-white">✕</button>
            </div>
            <div className="space-y-3">
              {clues.length > 0 ? (
                clues.map((clue, idx) => (
                  <div key={idx} className="bg-noir-900/50 p-3 rounded-lg border border-noir-700 flex gap-3 items-start">
                    <span className="text-neon-cyan font-mono text-sm mt-1">#{idx + 1}</span>
                    <p className="text-sm text-gray-300">{clue}</p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-8">아직 발견된 단서가 없습니다.</p>
              )}
            </div>
          </div>
        </div>
      )}

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

      {/* Left Sidebar - Characters */}
      <div className="w-72 bg-noir-800/50 border-r border-noir-700 flex flex-col flex-shrink-0">
        <div className="p-4 border-b border-noir-700 bg-noir-900/50">
          <h2 className="text-lg font-bold text-neon-cyan flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-neon-cyan animate-pulse"></span>
            PARTICIPANTS
          </h2>
          <p className="text-xs text-gray-500 mt-1">
            SESSION: {threadId.split('-')[1]}
          </p>
        </div>

        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
          <div className="space-y-4">
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

      {/* Center Zone - Chat & Input */}
      <div className="flex-1 flex flex-col min-w-0 bg-noir-900/30 relative">
        {/* Chat Log */}
        <div className="flex-1 relative overflow-hidden">
          <ChatLog messages={messages} />
        </div>

        {/* Input */}
        <div className="p-4 bg-noir-800/80 border-t border-noir-700 backdrop-blur-sm">
          <form onSubmit={handleSendMessage} className="relative max-w-4xl mx-auto">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Type your deduction..."
              className="w-full bg-noir-900/90 border border-noir-600 rounded-xl p-4 pl-6 pr-14 text-gray-100 placeholder-gray-600 focus:border-neon-cyan focus:ring-1 focus:ring-neon-cyan focus:outline-none transition-all shadow-lg"
              disabled={loading || !!gameOverInfo}
            />
            <button type="submit" disabled={loading} className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-neon-cyan transition-colors disabled:opacity-50">
              <span className="text-xl">↵</span>
            </button>
          </form>
        </div>
      </div>

      {/* Right Zone - Game Info */}
      <div className="w-80 bg-noir-900 flex-shrink-0 border-l border-noir-700">
        <RightPanel
          phase={phase}
          survivorCount={characters.filter(c => c.status === 'alive').length}
          onNextTurn={() => handleAction('next')}
          onNightStart={() => handleAction('night_start')}
          onDiscuss={() => handleAction('discuss')}
          onEndDiscuss={() => handleAction('end_discuss')}
          onContinue={() => handleAction('next')}
          onShowSummary={() => setShowSummaryModal(true)}
          onShowClues={() => setShowClueModal(true)}
        />
      </div>
    </div>
  );
};

export default GamePage;