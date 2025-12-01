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