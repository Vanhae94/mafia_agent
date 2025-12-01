import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatLog from './components/ChatLog';
import CharacterStatus from './components/CharacterStatus';
import ActionPanel from './components/ActionPanel';
import Modal from './components/Modal';
import StartScreen from './components/StartScreen';
import { Ghost, Moon, Sun, BookOpen, ScrollText } from 'lucide-react';

function App() {
    const [gameStarted, setGameStarted] = useState(false);
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showRoundSummary, setShowRoundSummary] = useState(false);
    const [showNightLog, setShowNightLog] = useState(false);

    // Initialize game on load - REMOVED to allow manual start
    // useEffect(() => {
    //     startNewGame();
    // }, []);

    const startNewGame = async (playerName = 'User') => {
        setLoading(true);
        try {
            const res = await axios.post('/api/game/start', { player_name: playerName });
            setGameState(res.data);
            setGameStarted(true);
        } catch (err) {
            console.error(err);
            setError('게임 서버에 연결할 수 없습니다.');
        } finally {
            setLoading(false);
        }
    };

    const handleAction = async (type, payload = {}) => {
        if (!gameState) return;

        // Optimistic update or loading state could be added here
        try {
            const res = await axios.post('/api/game/action', {
                thread_id: gameState.thread_id,
                action_type: type,
                ...payload
            });
            setGameState(res.data);
        } catch (err) {
            console.error(err);
            alert('액션 처리 중 오류가 발생했습니다.');
        }
    };

    if (!gameStarted) {
        return <StartScreen onStart={startNewGame} />;
    }

    if (!gameState && loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-black text-green-500">
                <div className="animate-pulse flex flex-col items-center gap-4">
                    <Ghost size={48} />
                    <span className="text-xl font-mono">SYSTEM BOOTING...</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center h-screen bg-black text-red-500">
                <div className="text-center">
                    <h1 className="text-2xl font-bold mb-2">SYSTEM ERROR</h1>
                    <p>{error}</p>
                    <button onClick={startNewGame} className="mt-4 btn-secondary">RETRY</button>
                </div>
            </div>
        );
    }

    if (!gameState) return null;

    return (
        <div className="h-screen min-h-[800px] bg-[url('/bg-grid.svg')] bg-fixed bg-cover text-gray-200 p-6 flex gap-6 overflow-hidden">
            {/* Left Panel: Game Info & Status */}
            <div className="w-1/4 flex flex-col gap-6 h-full overflow-y-auto pr-2">
                <div className="glass-panel p-6 flex flex-col items-center justify-center gap-2 border-cyan-500/30 shadow-[0_0_20px_rgba(0,243,255,0.1)] shrink-0">
                    <h1 className="text-3xl font-bold noir-text-cyan tracking-wider flex items-center gap-3">
                        <Ghost /> PHANTOM LOG
                    </h1>
                    <div className="flex items-center gap-2 text-sm text-gray-400 mt-2">
                        {gameState.day_night === 'day' ? <Sun size={16} className="text-orange-400" /> : <Moon size={16} className="text-purple-400" />}
                        <span>Round {gameState.round_number} - {gameState.day_night.toUpperCase()}</span>
                    </div>
                </div>

                <div className="flex gap-2 shrink-0">
                    <button
                        onClick={() => setShowRoundSummary(true)}
                        className="flex-1 btn-secondary flex items-center justify-center gap-2 text-xs py-2"
                    >
                        <BookOpen size={14} /> 라운드 요약
                    </button>
                    <button
                        onClick={() => setShowNightLog(true)}
                        className="flex-1 btn-secondary flex items-center justify-center gap-2 text-xs py-2"
                    >
                        <ScrollText size={14} /> 밤 행동 로그
                    </button>
                </div>

                <CharacterStatus
                    characters={gameState.characters}
                    aliveStatus={gameState.alive_status}
                    suspicionCounts={gameState.suspicion_counts}
                />

                {/* Clues Panel */}
                <div className="glass-panel p-4 flex-1 overflow-y-auto min-h-[200px]">
                    <h3 className="text-lg font-bold mb-4 noir-text-crimson border-b border-gray-700 pb-2 sticky top-0 bg-black/50 backdrop-blur-sm">
                        현장 증거 (Clues)
                    </h3>
                    <div className="space-y-2 text-sm text-gray-400">
                        {gameState.clues.length > 0 ? (
                            gameState.clues.map((clue, idx) => (
                                <div key={idx} className="p-2 bg-gray-900/50 rounded border-l-2 border-red-500">
                                    {clue}
                                </div>
                            ))
                        ) : (
                            <div className="text-center italic opacity-50 py-4">아직 발견된 단서가 없습니다.</div>
                        )}
                    </div>
                </div>
            </div>

            {/* Right Panel: Chat & Actions */}
            <div className="flex-1 flex flex-col h-full overflow-hidden gap-4">
                <ChatLog messages={gameState.messages} />
                <ActionPanel
                    onAction={handleAction}
                    phase={gameState.phase}
                    characters={gameState.characters}
                    aliveStatus={gameState.alive_status}
                />
            </div>

            {/* Modals */}
            <Modal
                isOpen={showRoundSummary}
                onClose={() => setShowRoundSummary(false)}
                title="📜 라운드 요약"
            >
                <div className="space-y-4">
                    {gameState.round_summaries && Object.keys(gameState.round_summaries).length > 0 ? (
                        Object.entries(gameState.round_summaries).map(([round, summary]) => (
                            <div key={round} className="p-4 bg-gray-900/50 rounded border border-gray-700">
                                <h3 className="noir-text-cyan font-bold mb-2">Round {round}</h3>
                                <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap">
                                    {summary}
                                </p>
                            </div>
                        ))
                    ) : (
                        <p className="text-gray-500 text-center py-8">
                            아직 기록된 라운드 요약이 없습니다.
                        </p>
                    )}
                </div>
            </Modal>

            <Modal
                isOpen={showNightLog}
                onClose={() => setShowNightLog(false)}
                title="🌙 밤 행동 로그"
            >
                <div className="space-y-2">
                    {gameState.night_logs && gameState.night_logs.length > 0 ? (
                        gameState.night_logs.map((log, idx) => (
                            <div key={idx} className="p-3 bg-gray-900/50 rounded border border-gray-700 text-gray-300">
                                {log}
                            </div>
                        ))
                    ) : (
                        <div className="text-center text-gray-500 py-8">
                            기록된 밤 행동이 없습니다.
                        </div>
                    )}
                </div>
            </Modal>

            {/* Game Over Overlay */}
            {gameState.game_over && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
                    <div className="glass-panel p-10 text-center max-w-lg w-full border-cyan-500 shadow-[0_0_50px_rgba(0,243,255,0.2)]">
                        <h2 className="text-4xl font-bold mb-6 noir-text-cyan">GAME OVER</h2>
                        <p className="text-xl mb-8">
                            팬텀의 정체는 <span className="font-bold noir-text-crimson">{gameState.winner}</span>였습니다.
                        </p>
                        <button onClick={startNewGame} className="btn-primary w-full py-3 text-lg">
                            다시 시작하기
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
