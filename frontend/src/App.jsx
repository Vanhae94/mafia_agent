import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatLog from './components/ChatLog';
import CharacterStatus from './components/CharacterStatus';
import ActionPanel from './components/ActionPanel';
import { Ghost, Moon, Sun } from 'lucide-react';

function App() {
    const [gameState, setGameState] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Initialize game on load
    useEffect(() => {
        startNewGame();
    }, []);

    const startNewGame = async () => {
        setLoading(true);
        try {
            const res = await axios.post('/api/game/start', { player_name: 'User' });
            setGameState(res.data);
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
        <div className="min-h-screen bg-[url('/bg-grid.svg')] bg-fixed bg-cover text-gray-200 p-6 flex gap-6">
            {/* Left Panel: Game Info & Status */}
            <div className="w-1/4 flex flex-col gap-6">
                <div className="glass-panel p-6 flex flex-col items-center justify-center gap-2 border-green-500/30 shadow-[0_0_20px_rgba(0,255,157,0.1)]">
                    <h1 className="text-3xl font-bold neon-text-green tracking-wider flex items-center gap-3">
                        <Ghost /> PHANTOM LOG
                    </h1>
                    <div className="flex items-center gap-2 text-sm text-gray-400 mt-2">
                        {gameState.day_night === 'day' ? <Sun size={16} className="text-orange-400" /> : <Moon size={16} className="text-purple-400" />}
                        <span>Round {gameState.round_number} - {gameState.day_night.toUpperCase()}</span>
                    </div>
                </div>

                <CharacterStatus
                    characters={gameState.characters}
                    aliveStatus={gameState.alive_status}
                    suspicionCounts={gameState.suspicion_counts}
                />

                {/* Clues Panel */}
                <div className="glass-panel p-4 flex-1">
                    <h3 className="text-lg font-bold mb-4 neon-text-red border-b border-gray-700 pb-2">
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
            <div className="flex-1 flex flex-col">
                <ChatLog messages={gameState.messages} />
                <ActionPanel
                    onAction={handleAction}
                    phase={gameState.phase}
                    characters={gameState.characters}
                    aliveStatus={gameState.alive_status}
                />
            </div>

            {/* Game Over Overlay */}
            {gameState.game_over && (
                <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
                    <div className="glass-panel p-10 text-center max-w-lg w-full border-green-500 shadow-[0_0_50px_rgba(0,255,157,0.2)]">
                        <h2 className="text-4xl font-bold mb-6 neon-text-green">GAME OVER</h2>
                        <p className="text-xl mb-8">
                            팬텀의 정체는 <span className="font-bold text-red-500">{gameState.winner}</span>였습니다.
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
