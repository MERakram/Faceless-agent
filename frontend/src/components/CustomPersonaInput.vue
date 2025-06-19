<template>
  <div :class="[
    'rounded-lg shadow-lg p-6 mb-6 transition-colors duration-300',
    isDark ? 'bg-gray-800 border border-gray-700' : 'bg-white'
  ]">
    <h3 :class="[
      'text-lg font-semibold mb-4 transition-colors duration-300',
      isDark ? 'text-white' : 'text-gray-800'
    ]">
      Create Custom Persona
    </h3>
    
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label for="persona-description" :class="[
          'block text-sm font-medium mb-2 transition-colors duration-300',
          isDark ? 'text-gray-200' : 'text-gray-700'
        ]">
          Persona Description
        </label>
        <textarea
          id="persona-description"
          v-model="description"
          placeholder="e.g., A grumpy wizard who speaks in riddles and loves brewing potions..."
          rows="3"
          :class="[
            'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-300',
            isDark 
              ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400' 
              : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500'
          ]"
          :disabled="isSubmitting"
        ></textarea>
      </div>
      
      <div class="flex flex-col sm:flex-row gap-3">
        <button
          type="submit"
          :disabled="!description.trim() || isSubmitting"
          :class="[
            'flex-1 font-medium py-2 px-4 rounded-md transition-all duration-200 flex items-center justify-center space-x-2',
            isDark 
              ? 'bg-green-600 hover:bg-green-700 disabled:bg-gray-600 text-white' 
              : 'bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white'
          ]"
        >
          <span v-if="isSubmitting" class="animate-spin">⏳</span>
          <span>{{ isSubmitting ? 'Adding...' : '💾 Add to Library' }}</span>
        </button>
        
        <button
          type="button"
          @click="useCustomPersona"
          :disabled="!description.trim() || isSubmitting"
          :class="[
            'flex-1 font-medium py-2 px-4 rounded-md transition-all duration-200 flex items-center justify-center space-x-2',
            isDark 
              ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white' 
              : 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white'
          ]"
        >
          <span>🚀 Use Now</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useChatStore } from '@/stores/chat';
import { useThemeStore } from '@/stores/theme';

const chatStore = useChatStore();
const themeStore = useThemeStore();
const { isDark } = storeToRefs(themeStore);

const description = ref('');
const isSubmitting = ref(false);

const handleSubmit = async () => {
  if (!description.value.trim()) return;
  
  try {
    isSubmitting.value = true;
    await chatStore.addCustomPersona(description.value.trim());
    description.value = '';
  } catch (error) {
    console.error('Failed to add custom persona:', error);
  } finally {
    isSubmitting.value = false;
  }
};

const useCustomPersona = () => {
  if (!description.value.trim()) return;
  
  const customPersona = {
    id: Date.now(),
    description: description.value.trim(),
    isCustom: true
  };
  
  chatStore.startNewSession(customPersona);
  description.value = '';
};
</script>