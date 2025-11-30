import React, { useState } from 'react';
import { Send, Play, Vote, Eye } from 'lucide-react';

const ActionPanel = ({ onAction, phase, characters, aliveStatus }) => {
    const [input, setInput] = useState('');
    const [selectedTarget, setSelectedTarget] = useState('');

    const handleSend = (e) => {
        e.preventDefault();
        if (!input.trim()) return;
        onAction('chat', { content: input });
        setInput('');
    };

    const handleVote = () => {
        if (!selectedTarget) return alert('대상을 선택하세요');
        if (confirm(`${selectedTarget}을(를) 팬텀으로 지목하시겠습니까?`)) {
            onAction('vote', { target: selectedTarget });
        }
    };

    const handleNext = () => {
        onAction('next');
    };

    const aliveCharacters = characters.filter(c => aliveStatus[c.name] !== false);

    return (
        <div className="glass-panel p-4">
            <div className="flex flex-col gap-4">
                {/* Chat Input */}
                <form onSubmit={handleSend} className="flex gap-2">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="대화에 참여하거나 명령어를 입력하세요..."
                        className="flex-1 bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-green-500 transition-colors"
                        disabled={phase === 'night' || phase === 'end'}
                    />
                    <button
                        type="submit"
                        className="btn-primary flex items-center gap-2"
                        disabled={phase === 'night' || phase === 'end'}
                    >
                        <Send size={16} />
                        전송
                    </button>
                </form>

                {/* Action Buttons */}
                <div className="flex items-center justify-between border-t border-gray-800 pt-4">
                    <div className="flex gap-2">
                        <select
                            className="bg-gray-900 border border-gray-700 rounded px-3 py-1 text-sm text-gray-300 focus:outline-none"
                            value={selectedTarget}
                            onChange={(e) => setSelectedTarget(e.target.value)}
                        >
                            <option value="">대상 선택...</option>
                            {aliveCharacters.map(c => (
                                <option key={c.name} value={c.name}>{c.name}</option>
                            ))}
                        </select>

                        <button
                            onClick={handleVote}
                            className="btn-secondary hover:bg-red-900/30 hover:text-red-400 hover:border-red-900 flex items-center gap-2"
                        >
                            <Vote size={16} />
                            지목
                        </button>
                    </div>

                    <button
                        onClick={handleNext}
                        className="btn-secondary flex items-center gap-2 hover:bg-blue-900/30 hover:text-blue-400 hover:border-blue-900"
                    >
                        <Play size={16} />
                        진행 (Next)
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ActionPanel;
