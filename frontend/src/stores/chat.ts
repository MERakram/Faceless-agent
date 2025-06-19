import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Persona, ChatMessage, ChatSession } from '@/types';
import { chatApi } from '@/services/api';

export const useChatStore = defineStore('chat', () => {
  const currentSession = ref<ChatSession | null>(null);
  const availablePersonas = ref<Persona[]>([]);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const currentPersona = computed(() => currentSession.value?.persona);
  const currentMode = computed(() => currentSession.value?.mode || 'regular');
  const messages = computed(() => currentSession.value?.messages || []);

  const generatePersona = async () => {
    try {
      isLoading.value = true;
      error.value = null;
      const persona = await chatApi.generatePersona();
      
      if (currentSession.value) {
        currentSession.value.persona = persona;
      } else {
        startNewSession(persona);
      }
    } catch (err) {
      error.value = 'Failed to generate persona';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  };

  const addCustomPersona = async (description: string) => {
    try {
      const persona = await chatApi.addCustomPersona(description);
      availablePersonas.value.push(persona);
      return persona;
    } catch (err) {
      error.value = 'Failed to add custom persona';
      throw err;
    }
  };

  const sendMessage = async (content: string) => {
    if (!currentSession.value || !currentPersona.value) {
      throw new Error('No active session or persona');
    }

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content,
      isUser: true,
      timestamp: new Date()
    };

    currentSession.value.messages.push(userMessage);

    try {
      isLoading.value = true;
      const response = await chatApi.sendMessage({
        message: content,
        persona: currentPersona.value.description,
        mode: currentMode.value,
        sessionId: currentSession.value.id
      });

      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response.message,
        isUser: false,
        timestamp: new Date()
      };

      currentSession.value.messages.push(aiMessage);
    } catch (err) {
      error.value = 'Failed to send message';
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const toggleMode = () => {
    if (currentSession.value) {
      currentSession.value.mode = currentSession.value.mode === 'regular' ? 'uncensored' : 'regular';
    }
  };

  const startNewSession = (persona?: Persona) => {
    currentSession.value = {
      id: Date.now().toString(),
      persona: persona || null,
      mode: 'regular',
      messages: [],
      createdAt: new Date()
    };
  };

  const downloadChatHistory = () => {
    if (!currentSession.value || messages.value.length === 0) return;

    const chatText = messages.value
      .map(msg => `${msg.isUser ? 'User' : 'AI'}: ${msg.content}`)
      .join('\n\n');

    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${currentSession.value.id}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return {
    currentSession,
    availablePersonas,
    isLoading,
    error,
    currentPersona,
    currentMode,
    messages,
    generatePersona,
    addCustomPersona,
    sendMessage,
    toggleMode,
    startNewSession,
    downloadChatHistory
  };
});