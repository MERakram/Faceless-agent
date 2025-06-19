export interface Persona {
  id: number;
  description: string;
  isCustom: boolean;
}

export interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
}

export interface ChatMode {
  regular: boolean;
  uncensored: boolean;
}

export interface ChatSession {
  id: string;
  persona: Persona | null;
  mode: 'regular' | 'uncensored';
  messages: ChatMessage[];
  createdAt: Date;
}

export interface ChatResponse {
  message: string;
  filtered?: boolean;
}

export interface ApiError {
  message: string;
  code?: string;
}

export interface PersonaCategory {
  id: string;
  name: string;
  icon: string;
  description: string;
  traits: string[];
}

export interface PersonaTrait {
  id: string;
  name: string;
  category: string;
  description: string;
}

export interface PersonaTemplate {
  id: string;
  name: string;
  category: string;
  description: string;
  traits: string[];
  personality: string[];
  speechPattern: string;
  background: string;
}