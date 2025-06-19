<template>
  <div :class="[
    'rounded-lg shadow-lg p-6 mb-6 transition-colors duration-300',
    isDark ? 'bg-gray-800 border border-gray-700' : 'bg-white'
  ]">
    <div class="flex items-center justify-between">
      <div>
        <h3 :class="[
          'text-lg font-semibold transition-colors duration-300',
          isDark ? 'text-white' : 'text-gray-800'
        ]">
          Chat Mode
        </h3>
        <p :class="[
          'text-sm mt-1 transition-colors duration-300',
          isDark ? 'text-gray-300' : 'text-gray-600'
        ]">
          {{ currentMode === 'regular' ? 'Family-friendly responses' : 'Creative, unfiltered responses' }}
        </p>
      </div>
      
      <button
        @click="toggleMode"
        :class="[
          'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2',
          currentMode === 'regular' 
            ? (isDark ? 'bg-gray-600 focus:ring-gray-500' : 'bg-gray-200 focus:ring-blue-500')
            : (isDark ? 'bg-blue-600 focus:ring-blue-500' : 'bg-blue-600 focus:ring-blue-500'),
          isDark ? 'focus:ring-offset-gray-800' : 'focus:ring-offset-white'
        ]"
      >
        <span
          :class="[
            'inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-lg',
            currentMode === 'regular' ? 'translate-x-1' : 'translate-x-6'
          ]"
        />
      </button>
    </div>
    
    <div class="mt-4 flex space-x-4 text-sm">
      <div class="flex items-center space-x-2">
        <span class="text-lg">🛡️</span>
        <span :class="[
          'transition-colors duration-300',
          currentMode === 'regular' 
            ? (isDark ? 'text-blue-400 font-medium' : 'text-blue-600 font-medium')
            : (isDark ? 'text-gray-400' : 'text-gray-500')
        ]">
          Regular Mode
        </span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-lg">🔥</span>
        <span :class="[
          'transition-colors duration-300',
          currentMode === 'uncensored' 
            ? (isDark ? 'text-blue-400 font-medium' : 'text-blue-600 font-medium')
            : (isDark ? 'text-gray-400' : 'text-gray-500')
        ]">
          Uncensored Mode
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useChatStore } from '@/stores/chat';
import { useThemeStore } from '@/stores/theme';

const chatStore = useChatStore();
const themeStore = useThemeStore();
const { currentMode } = storeToRefs(chatStore);
const { isDark } = storeToRefs(themeStore);

const toggleMode = () => {
  chatStore.toggleMode();
};
</script>