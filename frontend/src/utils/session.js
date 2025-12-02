// 간단한 UUID 생성기 (라이브러리 없이 사용)
export const generateSessionId = () => {
  return 'session-' + Math.random().toString(36).substr(2, 9) + '-' + Date.now();
};