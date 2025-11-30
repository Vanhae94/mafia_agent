import React, { useEffect, useRef } from 'react';
import { User, Bot } from 'lucide-react';

const ChatLog = ({ messages }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    return (
        <div className="flex-1 overflow-y-auto p-4 space-y-4 glass-panel mb-4 h-[60vh]">
            {messages.map((msg, idx) => {
                const isUser = msg.sender === '유저';
                const isSystem = msg.sender === 'System';

                if (isSystem) {
                    return (
                        <div key={idx} className="flex justify-center my-4">
                            <span className="text-xs text-gray-500 bg-gray-900 px-3 py-1 rounded-full border border-gray-800">
                                {msg.content}
                            </span>
                        </div>
                    );
                }

                return (
                    <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 
                ${isUser ? 'bg-blue-900 text-blue-200' : 'bg-green-900 text-green-200'}`}>
                                {isUser ? <User size={16} /> : <Bot size={16} />}
                            </div>

                            <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                                <span className="text-xs text-gray-400 mb-1">{msg.sender}</span>
                                <div className={`p-3 rounded-lg text-sm leading-relaxed
                  ${isUser
                                        ? 'bg-blue-900/30 border border-blue-500/30 text-blue-100 rounded-tr-none'
                                        : 'bg-green-900/30 border border-green-500/30 text-green-100 rounded-tl-none'
                                    }`}>
                                    {msg.content}
                                </div>
                            </div>
                        </div>
                    </div>
                );
            })}
            <div ref={bottomRef} />
        </div>
    );
};

export default ChatLog;
