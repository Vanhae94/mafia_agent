import React, { useState } from 'react';
import { Send, Play, Vote, Eye, MessageSquare, Users, UserMinus } from 'lucide-react';

const ActionPanel = ({ onAction, phase, characters, aliveStatus }) => {
    const [activeTab, setActiveTab] = useState('chat'); // chat, one_on_one, suspect, vote
    const [input, setInput] = useState('');
    const [selectedTarget, setSelectedTarget] = useState('');

    const aliveCharacters = characters.filter(c => aliveStatus[c.name] !== false);

    const handleSend = (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        if (activeTab === 'one_on_one') {
            if (!selectedTarget) return alert('대화할 상대를 선택하세요.');
            // 1:1 대화 형식: "[이름에게] 메시지"
            onAction('chat', { content: `[${selectedTarget}에게] ${input}` });
        } else {
            onAction('chat', { content: input });
        }
        setInput('');
    };

    const handleVote = () => {
        if (!selectedTarget) return alert('대상을 선택하세요');
        if (confirm(`${selectedTarget}을(를) 팬텀으로 지목하시겠습니까?`)) {
            onAction('vote', { target: selectedTarget });
        }
    };

    const handleSuspect = () => {
        if (!selectedTarget) return alert('대상을 선택하세요');
        onAction('suspect', { target: selectedTarget });
        alert(`${selectedTarget}을(를) 의심했습니다.`);
    };

    const handleNext = () => {
        onAction('next');
    };

    // 탭 변경 시 입력값 초기화
    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setSelectedTarget('');
        setInput('');
    };

    return (
        <div className="glass-panel p-0 overflow-hidden flex flex-col">
            {/* Tabs */}
            <div className="flex border-b border-gray-700 bg-gray-900/50">
                <button
                    onClick={() => handleTabChange('chat')}
                    className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors
            ${activeTab === 'chat' ? 'text-cyan-400 border-b-2 border-cyan-500 bg-cyan-900/10' : 'text-gray-400 hover:text-gray-200'}`}
                >
                    <Users size={16} /> 전체 대화
                </button>
                <button
                    onClick={() => handleTabChange('one_on_one')}
                    className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors
            ${activeTab === 'one_on_one' ? 'text-blue-400 border-b-2 border-blue-500 bg-blue-900/10' : 'text-gray-400 hover:text-gray-200'}`}
                >
                    <MessageSquare size={16} /> 1:1 대화
                </button>
                <button
                    onClick={() => handleTabChange('suspect')}
                    className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors
            ${activeTab === 'suspect' ? 'text-yellow-400 border-b-2 border-yellow-500 bg-yellow-900/10' : 'text-gray-400 hover:text-gray-200'}`}
                >
                    <Eye size={16} /> 의심하기
                </button>
                <button
                    onClick={() => handleTabChange('vote')}
                    className={`flex-1 py-3 text-sm font-medium flex items-center justify-center gap-2 transition-colors
            ${activeTab === 'vote' ? 'text-red-400 border-b-2 border-red-500 bg-red-900/10' : 'text-gray-400 hover:text-gray-200'}`}
                >
                    <Vote size={16} /> 투표
                </button>
            </div>

            {/* Content Area */}
            <div className="p-4 flex-1 flex flex-col gap-4">

                {/* 1. Chat Tab */}
                {activeTab === 'chat' && (
                    <form onSubmit={handleSend} className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="모두에게 할 말을 입력하세요..."
                            className="flex-1 bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-cyan-500 transition-colors"
                            disabled={phase === 'night' || phase === 'end'}
                        />
                        <button
                            type="submit"
                            className="btn-primary flex items-center gap-2"
                            disabled={phase === 'night' || phase === 'end'}
                        >
                            <Send size={16} /> 전송
                        </button>
                    </form>
                )}

                {/* 2. 1:1 Chat Tab */}
                {activeTab === 'one_on_one' && (
                    <div className="flex flex-col gap-3">
                        <select
                            className="bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-blue-500"
                            value={selectedTarget}
                            onChange={(e) => setSelectedTarget(e.target.value)}
                        >
                            <option value="">대화할 상대 선택...</option>
                            {aliveCharacters.map(c => (
                                <option key={c.name} value={c.name}>{c.name} ({c.job})</option>
                            ))}
                        </select>
                        <form onSubmit={handleSend} className="flex gap-2">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder={selectedTarget ? `${selectedTarget}에게 귓속말...` : "상대를 먼저 선택하세요"}
                                className="flex-1 bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-blue-500 transition-colors"
                                disabled={!selectedTarget || phase === 'night' || phase === 'end'}
                            />
                            <button
                                type="submit"
                                className="btn-secondary flex items-center gap-2 text-blue-400 border-blue-900 hover:bg-blue-900/30"
                                disabled={!selectedTarget || phase === 'night' || phase === 'end'}
                            >
                                <Send size={16} /> 전송
                            </button>
                        </form>
                        <p className="text-xs text-gray-500">* 1:1 대화는 다른 사람에게 들리지 않습니다.</p>
                    </div>
                )}

                {/* 3. Suspect Tab */}
                {activeTab === 'suspect' && (
                    <div className="flex flex-col gap-3">
                        <div className="text-sm text-gray-400 mb-1">
                            의심스러운 행동을 하는 사람을 지목하여 압박하세요. 의심 수치가 올라갑니다.
                        </div>
                        <div className="flex gap-2">
                            <select
                                className="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-yellow-500"
                                value={selectedTarget}
                                onChange={(e) => setSelectedTarget(e.target.value)}
                            >
                                <option value="">의심할 대상 선택...</option>
                                {aliveCharacters.map(c => (
                                    <option key={c.name} value={c.name}>{c.name}</option>
                                ))}
                            </select>
                            <button
                                onClick={handleSuspect}
                                className="btn-secondary flex items-center gap-2 text-yellow-400 border-yellow-900 hover:bg-yellow-900/30"
                                disabled={!selectedTarget || phase === 'night' || phase === 'end'}
                            >
                                <Eye size={16} /> 의심하기
                            </button>
                        </div>
                    </div>
                )}

                {/* 4. Vote Tab */}
                {activeTab === 'vote' && (
                    <div className="flex flex-col gap-3">
                        <div className="text-sm text-red-400 mb-1 font-bold">
                            ⚠️ 주의: 투표는 되돌릴 수 없으며, 즉시 게임의 승패가 결정됩니다.
                        </div>
                        <div className="flex gap-2">
                            <select
                                className="flex-1 bg-gray-900 border border-gray-700 rounded px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-red-500"
                                value={selectedTarget}
                                onChange={(e) => setSelectedTarget(e.target.value)}
                            >
                                <option value="">팬텀으로 지목할 대상...</option>
                                {aliveCharacters.map(c => (
                                    <option key={c.name} value={c.name}>{c.name}</option>
                                ))}
                            </select>
                            <button
                                onClick={handleVote}
                                className="btn-secondary flex items-center gap-2 text-red-400 border-red-900 hover:bg-red-900/30"
                                disabled={!selectedTarget || phase === 'night' || phase === 'end'}
                            >
                                <Vote size={16} /> 최후 변론 없이 투표
                            </button>
                        </div>
                    </div>
                )}

                {/* Common Action: Next Turn */}
                <div className="border-t border-gray-800 pt-3 mt-auto">
                    <button
                        onClick={handleNext}
                        className="w-full btn-secondary flex items-center justify-center gap-2 hover:bg-gray-800"
                        disabled={phase === 'night' || phase === 'end'}
                    >
                        <Play size={16} /> 다음 대화 진행 (Enter)
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ActionPanel;
