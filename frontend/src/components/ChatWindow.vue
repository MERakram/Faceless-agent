<template>
  <div :class="[
    'rounded-lg shadow-lg flex flex-col transition-colors duration-300',
    'h-[calc(100vh-180px)]', // Fixed height to prevent scrolling issues
    isDark ? 'bg-gray-800 border border-gray-700' : 'bg-white'
  ]">
    <!-- Chat Header -->
    <div :class="[
      'p-4 rounded-t-lg flex justify-between items-center transition-colors duration-300',
      isDark 
        ? 'bg-gradient-to-r from-gray-700 via-gray-600 to-gray-700 text-white' 
        : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
    ]">
      <div class="flex-1 min-w-0">
        <h3 class="text-lg font-semibold">Chat Session</h3>
        <p class="text-sm opacity-90 truncate" v-if="currentPersona">
          {{ currentPersona.description }}
        </p>
        <p class="text-sm opacity-75" v-else>
          Generate a persona to start chatting
        </p>
      </div>
      <div class="flex space-x-2 ml-4">
        <button
          @click="downloadChat"
          :disabled="messages.length === 0"
          class="bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 text-white px-3 py-1 rounded text-sm transition-all duration-200 flex items-center space-x-1"
          title="Download chat history"
        >
          <span>📥</span>
          <span class="hidden sm:inline">Download</span>
        </button>
        <button
          @click="clearChat"
          :disabled="messages.length === 0"
          class="bg-white bg-opacity-20 hover:bg-opacity-30 disabled:bg-opacity-10 text-white px-3 py-1 rounded text-sm transition-all duration-200 flex items-center space-x-1"
          title="Clear chat"
        >
          <span>🗑️</span>
          <span class="hidden sm:inline">Clear</span>
        </button>
      </div>
    </div>

    <!-- Messages Container -->
    <div 
      ref="messagesContainer"
      :class="[
        'flex-1 overflow-y-auto p-4 space-y-4 transition-colors duration-300',
        isDark ? 'bg-gray-900/50' : 'bg-gray-50'
      ]"
    >
      <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="text-6xl mb-4 animate-bounce-gentle">🤖</div>
          <p :class="[
            'text-lg font-medium mb-2 transition-colors duration-300',
            isDark ? 'text-gray-300' : 'text-gray-500'
          ]">
            Ready to chat!
          </p>
          <p :class="[
            'text-sm transition-colors duration-300',
            isDark ? 'text-gray-400' : 'text-gray-600'
          ]">
            {{ currentPersona ? 'Start a conversation below' : 'Generate a persona first, then start chatting' }}
          </p>
        </div>
      </div>

      <div
        v-for="message in messages"
        :key="message.id"
        :class="[
          'flex animate-fade-in',
          message.isUser ? 'justify-end' : 'justify-start'
        ]"
      >
        <div
          :class="[
            'max-w-xs md:max-w-md lg:max-w-lg xl:max-w-2xl px-4 py-3 rounded-lg shadow-sm transition-all duration-200 hover:shadow-md',
            message.isUser 
              ? (isDark 
                  ? 'bg-blue-600 text-white rounded-br-sm' 
                  : 'bg-blue-600 text-white rounded-br-sm')
              : (isDark 
                  ? 'bg-gray-700 text-gray-100 border border-gray-600 rounded-bl-sm' 
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-sm')
          ]"
        >
          <p class="whitespace-pre-wrap leading-relaxed">{{ message.content }}</p>
          <p 
            :class="[
              'text-xs mt-2 opacity-70',
              message.isUser 
                ? (isDark ? 'text-blue-100' : 'text-blue-100')
                : (isDark ? 'text-gray-400' : 'text-gray-500')
            ]"
          >
            {{ formatTime(message.timestamp) }}
          </p>
        </div>
      </div>

      <!-- Loading indicator -->
      <div v-if="isLoading && messages.length > 0" class="flex justify-start animate-slide-up">
        <div :class="[
          'px-4 py-3 rounded-lg rounded-bl-sm max-w-xs shadow-sm transition-colors duration-300',
          isDark 
            ? 'bg-gray-700 text-gray-100 border border-gray-600' 
            : 'bg-white text-gray-800 border border-gray-200'
        ]">
          <div class="flex items-center space-x-3">
            <div class="flex space-x-1">
              <div :class="[
                'w-2 h-2 rounded-full animate-bounce',
                isDark ? 'bg-gray-400' : 'bg-gray-400'
              ]"></div>
              <div :class="[
                'w-2 h-2 rounded-full animate-bounce',
                isDark ? 'bg-gray-400' : 'bg-gray-400'
              ]" style="animation-delay: 0.1s"></div>
              <div :class="[
                'w-2 h-2 rounded-full animate-bounce',
                isDark ? 'bg-gray-400' : 'bg-gray-400'
              ]" style="animation-delay: 0.2s"></div>
            </div>
            <span :class="[
              'text-sm transition-colors duration-300',
              isDark ? 'text-gray-400' : 'text-gray-500'
            ]">
              AI is thinking...
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Message Input -->
    <div :class="[
      'border-t p-4 rounded-b-lg transition-colors duration-300',
      isDark ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
    ]">
      <form @submit.prevent="sendMessage" class="flex space-x-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          :disabled="!currentPersona || isLoading"
          :class="[
            'flex-1 px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200',
            isDark 
              ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
              : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500',
            '!disabled:opacity-50'
          ]"
          @keydown.enter.prevent="sendMessage"
        />
        <button
          type="submit"
          :disabled="!newMessage.trim() || !currentPersona || isLoading"
          :class="[
            'px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 hover:scale-105 active:scale-95',
            isDark 
              ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white' 
              : 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white'
          ]"
        >
          <span v-if="isLoading" class="animate-spin">⏳</span>
          <span v-else>🚀</span>
          <span class="hidden sm:inline">{{ isLoading ? 'Sending...' : 'Send' }}</span>
        </button>
      </form>
      <div v-if="!currentPersona" :class="[
        'mt-2 text-sm transition-colors duration-300',
        isDark ? 'text-red-400' : 'text-red-600'
      ]">
        Please generate a persona before chatting
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';
import { storeToRefs } from 'pinia';
import { useChatStore } from '@/stores/chat';
import { useThemeStore } from '@/stores/theme';

const chatStore = useChatStore();
const themeStore = useThemeStore();
const { currentPersona, messages, isLoading } = storeToRefs(chatStore);
const { isDark } = storeToRefs(themeStore);

const newMessage = ref('');
const messagesContainer = ref<HTMLElement>();

const sendMessage = async () => {
  if (!newMessage.value.trim() || !currentPersona.value || isLoading.value) return;

  try {
    await chatStore.sendMessage(newMessage.value.trim());
    newMessage.value = '';
    await nextTick();
    scrollToBottom();
  } catch (error) {
    console.error('Failed to send message:', error);
  }
};

const downloadChat = () => {
  chatStore.downloadChatHistory();
};

const clearChat = () => {
  if (confirm('Are you sure you want to clear the chat history?')) {
    chatStore.startNewSession(currentPersona.value || undefined);
  }
};

const formatTime = (timestamp: Date) => {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// Auto-scroll when new messages are added
watch(messages, () => {
  nextTick(() => scrollToBottom());
}, { deep: true });
</script>