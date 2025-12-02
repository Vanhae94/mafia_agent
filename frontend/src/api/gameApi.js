import axios from 'axios';

const API_BASE_URL = "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const gameApi = {
  // 게임 시작 (Thread ID 필수)
  startGame: async (threadId) => {
    return await client.post('/api/game/start', { thread_id: threadId });
  },

  // 상태 조회
  getState: async (threadId) => {
    const response = await client.get(`/api/game/state/${threadId}`);
    return response.data;
  },

  // 액션 전송
  sendAction: async (threadId, actionType, content = null, target = null) => {
    return await client.post('/api/game/action', {
      thread_id: threadId,
      action_type: actionType,
      content: content,
      target: target
    });
  }
};