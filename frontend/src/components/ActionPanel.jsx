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