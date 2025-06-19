import axios from 'axios';
import type { Persona, ChatResponse } from '@/types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
});

// Add request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const chatApi = {
  async generatePersona(): Promise<Persona> {
    const response = await api.get('/generate_persona');
    return {
      id: response.data.id,
      description: response.data.description,
      isCustom: response.data.is_custom
    };
  },

  async addCustomPersona(description: string): Promise<Persona> {
    const response = await api.post('/add_persona', { description });
    return {
      id: response.data.id,
      description: response.data.description,
      isCustom: response.data.is_custom
    };
  },

  async sendMessage(data: {
    message: string;
    persona: string;
    mode: 'regular' | 'uncensored';
    sessionId: string;
  }): Promise<ChatResponse> {
    const response = await api.post('/chat', {
      message: data.message,
      persona: data.persona,
      mode: data.mode,
      conversation_history: []
    });
    return {
      message: response.data.response,
      filtered: response.data.filtered
    };
  },

  async getPersonas(): Promise<Persona[]> {
    const response = await api.get('/personas');
    return response.data.map((persona: any) => ({
      id: persona.id,
      description: persona.description,
      isCustom: persona.is_custom
    }));
  }
};