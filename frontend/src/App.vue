<template>
  <div id="app" :class="[
    'min-h-screen transition-colors duration-300',
    isDark 
      ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900' 
      : 'bg-gradient-to-br from-blue-50 to-purple-50'
  ]">
    <!-- Theme Toggle Button -->
    <div class="fixed top-4 right-4 z-50">
      <button
        @click="toggleTheme"
        :class="[
          'p-3 rounded-full shadow-lg transition-all duration-300 hover:scale-110',
          isDark 
            ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' 
            : 'bg-white text-gray-600 hover:bg-gray-50'
        ]"
        title="Toggle theme"
      >
        <svg v-if="isDark" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
        </svg>
        <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
        </svg>
      </button>
    </div>

    <div class="container mx-auto px-2 py-6">
      <header class="text-center mb-8">
        <h1 :class="[
          'text-4xl font-bold mb-2 transition-colors duration-300',
          isDark ? 'text-white' : 'text-gray-800'
        ]">
          Faceless Agent
        </h1>
        <p :class="[
          'text-lg transition-colors duration-300',
          isDark ? 'text-gray-300' : 'text-gray-600'
        ]">
          Persona-Shifting AI Chat Companion
        </p>
      </header>

      <!-- Changed from max-w-7xl to max-w-none and added more responsive breakpoints -->
      <div class="max-w-none mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-7 xl:grid-cols-9 2xl:grid-cols-11 gap-6 h-[calc(100vh-180px)]">
          <!-- Left Column: Controls - More responsive width allocation -->
          <div class="lg:col-span-3 xl:col-span-3 2xl:col-span-4 space-y-4 overflow-y-auto max-h-full">
            <PersonaGenerator />
            <CustomPersonaInput />
            <ModeToggle />
          </div>

          <!-- Right Column: Chat - Takes remaining space efficiently -->
          <div class="lg:col-span-4 xl:col-span-6 2xl:col-span-7 h-full">
            <ChatWindow />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { storeToRefs } from 'pinia';
import PersonaGenerator from '@/components/PersonaGenerator.vue';
import CustomPersonaInput from '@/components/CustomPersonaInput.vue';
import ModeToggle from '@/components/ModeToggle.vue';
import ChatWindow from '@/components/ChatWindow.vue';
import { useThemeStore } from '@/stores/theme';

const themeStore = useThemeStore();
const { isDark } = storeToRefs(themeStore);

const toggleTheme = () => {
  themeStore.toggleTheme();
  themeStore.saveTheme();
};

onMounted(() => {
  themeStore.initTheme();
});

// Watch for theme changes and update document class
watch(isDark, () => {
  themeStore.updateDocumentTheme();
});
</script>

<style>
#app {
  font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar for dark theme */
.dark ::-webkit-scrollbar {
  width: 8px;
}

.dark ::-webkit-scrollbar-track {
  @apply bg-gray-800;
}

.dark ::-webkit-scrollbar-thumb {
  @apply bg-gray-600 rounded-full;
}

.dark ::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-500;
}

/* Light theme scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  @apply bg-gray-100;
}

::-webkit-scrollbar-thumb {
  @apply bg-gray-300 rounded-full;
}

::-webkit-scrollbar-thumb:hover {
  @apply bg-gray-400;
}
</style>