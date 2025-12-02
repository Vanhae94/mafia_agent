import React, { useEffect, useRef } from 'react';

const ChatLog = ({ messages }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={scrollRef} className="absolute inset-0 overflow-y-auto p-6 pt-12 space-y-4 scrollbar-hide">
      {messages.map((msg, idx) => {
        // [수정] sender가 없거나 문자열이 아닐 경우를 대비한 안전한 변수 생성
        const safeSender = (msg.sender && typeof msg.sender === 'string') ? msg.sender : 'Unknown';
        const initial = safeSender[0] || '?'; 

        return (
          <div key={idx} className={`flex w-full ${msg.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] gap-3 ${msg.type === 'system' ? 'w-full max-w-none' : ''}`}>
              
              {/* Avatar for Agents */}
              {msg.type === 'agent' && (
                <div className="w-8 h-8 rounded-full bg-noir-800 border border-noir-700 flex items-center justify-center shrink-0 mt-1">
                   {/* [수정] 여기서 에러가 났었습니다. 안전한 변수(initial) 사용 */}
                   <span className="text-xs font-bold text-gray-400">{initial}</span>
                </div>
              )}

              <div className={`flex flex-col ${msg.type === 'system' ? 'items-center w-full' : ''}`}>
                 {/* Sender Info */}
                 {msg.type === 'agent' && (
                    <span className="text-xs text-gray-400 mb-1 ml-1">
                      <span className="text-neon-cyan font-bold">{safeSender}</span> 
                      <span className="opacity-50 mx-1">|</span> 
                      <span className="text-gray-500">{msg.job || 'Unknown'}</span>
                    </span>
                 )}

                 {/* Message Bubble */}
                 {msg.type === 'system' ? (
                   <div className="flex items-center gap-3 my-4 w-full">
                      <div className="h-px bg-noir-700 flex-1"></div>
                      <span className="text-xs font-mono text-neon-pink border border-neon-pink/30 px-3 py-1 rounded-full bg-neon-pink/5">
                        SYSTEM: {msg.text}
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
        );
      })}
    </div>
  );
};

export default ChatLog;