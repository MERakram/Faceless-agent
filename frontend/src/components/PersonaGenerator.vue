<template>
  <div :class="[
    'rounded-lg shadow-lg p-6 mb-6 transition-colors duration-300',
    isDark ? 'bg-gray-800 border border-gray-700' : 'bg-white'
  ]">
    <!-- Header -->
    <div class="text-center mb-6">
      <h2 :class="[
        'text-2xl font-bold mb-2 transition-colors duration-300',
        isDark ? 'text-white' : 'text-gray-800'
      ]">
        AI Persona Generator
      </h2>
      <p :class="[
        'text-sm transition-colors duration-300',
        isDark ? 'text-gray-300' : 'text-gray-600'
      ]">
        Create sophisticated AI personas with depth and personality
      </p>
    </div>

    <!-- Generation Mode Tabs -->
    <div class="mb-6">
      <div :class="[
        'flex rounded-lg p-1 transition-colors duration-300',
        isDark ? 'bg-gray-700' : 'bg-gray-100'
      ]">
        <button
          v-for="mode in generationModes"
          :key="mode.id"
          @click="activeMode = mode.id"
          :class="[
            'flex-1 py-2 px-3 text-sm font-medium rounded-md transition-all duration-200',
            activeMode === mode.id
              ? (isDark ? 'bg-blue-600 text-white shadow-md' : 'bg-white text-blue-600 shadow-md')
              : (isDark ? 'text-gray-300 hover:text-white' : 'text-gray-600 hover:text-gray-800')
          ]"
        >
          {{ mode.name }}
        </button>
      </div>
    </div>

    <!-- Quick Generate Mode -->
    <div v-if="activeMode === 'quick'" class="space-y-4">
      <div class="flex flex-col items-center space-y-4">
        <button
          @click="handleQuickGenerate"
          :disabled="isLoading"
          :class="[
            'w-full py-3 px-6 font-bold rounded-lg transition-all duration-200 flex items-center justify-center space-x-2',
            isDark 
              ? 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white' 
              : 'bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white'
          ]"
        >
          <svg v-if="isLoading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <span>{{ isLoading ? 'Generating...' : '🎲 Quick Generate' }}</span>
        </button>
      </div>
    </div>

    <!-- Advanced Generate Mode -->
    <div v-if="activeMode === 'advanced'" class="space-y-6">
      <!-- Category Selection -->
      <div>
        <label :class="[
          'block text-sm font-medium mb-3 transition-colors duration-300',
          isDark ? 'text-gray-200' : 'text-gray-700'
        ]">
          Choose Category
        </label>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="category in personaCategories"
            :key="category.id"
            @click="selectedCategory = category.id"
            :class="[
              'p-3 rounded-lg border-2 transition-all duration-200 text-left',
              selectedCategory === category.id
                ? (isDark ? 'border-blue-500 bg-blue-900/20' : 'border-blue-500 bg-blue-50')
                : (isDark ? 'border-gray-600 hover:border-gray-500 bg-gray-700/50' : 'border-gray-200 hover:border-gray-300 bg-gray-50')
            ]"
          >
            <div class="flex items-center space-x-2">
              <span class="text-lg">{{ category.icon }}</span>
              <div>
                <div :class="[
                  'font-medium text-sm transition-colors duration-300',
                  isDark ? 'text-white' : 'text-gray-800'
                ]">
                  {{ category.name }}
                </div>
                <div :class="[
                  'text-xs transition-colors duration-300',
                  isDark ? 'text-gray-400' : 'text-gray-500'
                ]">
                  {{ category.description }}
                </div>
              </div>
            </div>
          </button>
        </div>
      </div>

      <!-- Trait Selection -->
      <div v-if="selectedCategory">
        <label :class="[
          'block text-sm font-medium mb-3 transition-colors duration-300',
          isDark ? 'text-gray-200' : 'text-gray-700'
        ]">
          Select Traits (Optional)
        </label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="trait in getTraitsForCategory(selectedCategory)"
            :key="trait"
            @click="toggleTrait(trait)"
            :class="[
              'px-3 py-1 text-xs rounded-full border transition-all duration-200',
              selectedTraits.includes(trait)
                ? (isDark ? 'bg-blue-600 border-blue-600 text-white' : 'bg-blue-600 border-blue-600 text-white')
                : (isDark ? 'border-gray-600 text-gray-300 hover:border-gray-500' : 'border-gray-300 text-gray-600 hover:border-gray-400')
            ]"
          >
            {{ trait }}
          </button>
        </div>
      </div>

      <!-- Generate Button -->
      <button
        @click="handleAdvancedGenerate"
        :disabled="isLoading || !selectedCategory"
        :class="[
          'w-full py-3 px-6 font-bold rounded-lg transition-all duration-200 flex items-center justify-center space-x-2',
          isDark 
            ? 'bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white' 
            : 'bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white'
        ]"
      >
        <svg v-if="isLoading" class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        <span>{{ isLoading ? 'Crafting Persona...' : '✨ Generate Advanced Persona' }}</span>
      </button>
    </div>

    <!-- Template Mode -->
    <div v-if="activeMode === 'template'" class="space-y-4">
      <div class="grid gap-3">
        <button
          v-for="template in personaTemplates"
          :key="template.id"
          @click="handleTemplateSelect(template)"
          :class="[
            'p-4 rounded-lg border text-left transition-all duration-200 hover:scale-105',
            isDark ? 'border-gray-600 bg-gray-700/50 hover:bg-gray-700' : 'border-gray-200 bg-gray-50 hover:bg-gray-100'
          ]"
        >
          <div :class="[
            'font-semibold text-sm mb-1 transition-colors duration-300',
            isDark ? 'text-white' : 'text-gray-800'
          ]">
            {{ template.name }}
          </div>
          <div :class="[
            'text-xs transition-colors duration-300',
            isDark ? 'text-gray-400' : 'text-gray-600'
          ]">
            {{ template.description }}
          </div>
          <div class="flex flex-wrap gap-1 mt-2">
            <span
              v-for="trait in template.traits.slice(0, 3)"
              :key="trait"
              :class="[
                'px-2 py-1 text-xs rounded-full transition-colors duration-300',
                isDark ? 'bg-gray-600 text-gray-300' : 'bg-gray-200 text-gray-600'
              ]"
            >
              {{ trait }}
            </span>
            <span v-if="template.traits.length > 3" :class="[
              'px-2 py-1 text-xs rounded-full transition-colors duration-300',
              isDark ? 'bg-gray-600 text-gray-300' : 'bg-gray-200 text-gray-600'
            ]">
              +{{ template.traits.length - 3 }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <!-- Current Persona Display -->
    <div v-if="currentPersona" :class="[
      'mt-6 p-4 rounded-lg border-l-4 transition-colors duration-300',
      isDark ? 'bg-blue-900/20 border-blue-500' : 'bg-blue-50 border-blue-500'
    ]">
      <h3 :class="[
        'font-semibold mb-2 transition-colors duration-300',
        isDark ? 'text-blue-300' : 'text-blue-800'
      ]">
        Current Persona:
      </h3>
      <p :class="[
        'text-sm transition-colors duration-300',
        isDark ? 'text-blue-200' : 'text-blue-700'
      ]">
        {{ currentPersona.description }}
      </p>
    </div>

    <!-- Error Display -->
    <div v-if="error" :class="[
      'mt-4 p-4 rounded-lg border-l-4 transition-colors duration-300',
      isDark ? 'bg-red-900/20 border-red-500' : 'bg-red-50 border-red-500'
    ]">
      <p :class="[
        'text-sm transition-colors duration-300',
        isDark ? 'text-red-300' : 'text-red-700'
      ]">
        {{ error }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useChatStore } from '@/stores/chat';
import { useThemeStore } from '@/stores/theme';
import type { PersonaCategory, PersonaTemplate } from '@/types';

const chatStore = useChatStore();
const themeStore = useThemeStore();
const { currentPersona, isLoading, error } = storeToRefs(chatStore);
const { isDark } = storeToRefs(themeStore);

const activeMode = ref('quick');
const selectedCategory = ref('');
const selectedTraits = ref<string[]>([]);

const generationModes = [
  { id: 'quick', name: 'Quick' },
  { id: 'advanced', name: 'Advanced' },
  { id: 'template', name: 'Templates' }
];

const personaCategories: PersonaCategory[] = [
  {
    id: 'historical',
    name: 'Historical',
    icon: '🏛️',
    description: 'Characters from different eras',
    traits: ['wise', 'traditional', 'experienced', 'philosophical', 'formal', 'dignified']
  },
  {
    id: 'fantasy',
    name: 'Fantasy',
    icon: '🧙‍♂️',
    description: 'Magical and mythical beings',
    traits: ['mystical', 'powerful', 'ancient', 'mysterious', 'magical', 'otherworldly']
  },
  {
    id: 'sci-fi',
    name: 'Sci-Fi',
    icon: '🚀',
    description: 'Futuristic and technological',
    traits: ['advanced', 'logical', 'innovative', 'analytical', 'precise', 'futuristic']
  },
  {
    id: 'professional',
    name: 'Professional',
    icon: '💼',
    description: 'Career-focused personas',
    traits: ['expert', 'knowledgeable', 'professional', 'efficient', 'dedicated', 'skilled']
  },
  {
    id: 'creative',
    name: 'Creative',
    icon: '🎨',
    description: 'Artistic and imaginative',
    traits: ['artistic', 'imaginative', 'expressive', 'passionate', 'creative', 'inspiring']
  },
  {
    id: 'quirky',
    name: 'Quirky',
    icon: '🤪',
    description: 'Unique and eccentric',
    traits: ['eccentric', 'unpredictable', 'humorous', 'quirky', 'unconventional', 'playful']
  }
];

const personaTemplates: PersonaTemplate[] = [
  {
    id: 'detective',
    name: 'Time-Traveling Detective',
    category: 'historical',
    description: 'A sharp-minded investigator who solves crimes across different time periods',
    traits: ['analytical', 'observant', 'determined'],
    personality: ['methodical', 'curious', 'justice-driven'],
    speechPattern: 'Uses deductive reasoning and period-appropriate language',
    background: 'Experienced detective with knowledge of multiple historical eras'
  },
  {
    id: 'wizard',
    name: 'Grumpy Ancient Wizard',
    category: 'fantasy',
    description: 'An old wizard who has seen too much and is tired of explaining magic to novices',
    traits: ['ancient', 'grumpy', 'wise'],
    personality: ['impatient', 'knowledgeable', 'sarcastic'],
    speechPattern: 'Uses archaic language with frequent complaints',
    background: 'Centuries of magical experience, prefers solitude'
  },
  {
    id: 'ai-chef',
    name: 'Sassy AI Chef',
    category: 'sci-fi',
    description: 'A sophisticated AI that has mastered culinary arts and has strong opinions about food',
    traits: ['sophisticated', 'opinionated', 'culinary'],
    personality: ['passionate', 'perfectionist', 'witty'],
    speechPattern: 'Uses cooking metaphors and culinary terminology',
    background: 'Advanced AI with extensive culinary database and strong preferences'
  }
];

const getTraitsForCategory = (categoryId: string) => {
  return personaCategories.find(cat => cat.id === categoryId)?.traits || [];
};

const toggleTrait = (trait: string) => {
  const index = selectedTraits.value.indexOf(trait);
  if (index > -1) {
    selectedTraits.value.splice(index, 1);
  } else {
    selectedTraits.value.push(trait);
  }
};

const handleQuickGenerate = () => {
  chatStore.generatePersona();
};

const handleAdvancedGenerate = async () => {
  if (!selectedCategory.value) return;
  
  const category = personaCategories.find(cat => cat.id === selectedCategory.value);
  if (!category) return;

  // Create a more sophisticated persona description based on category and traits
  const basePersona = `A ${category.name.toLowerCase()} character`;
  const traitDescription = selectedTraits.value.length > 0 
    ? ` who is ${selectedTraits.value.join(', ')}` 
    : '';
  
  const sophisticatedDescription = `${basePersona}${traitDescription} with a unique personality and background. This persona has depth, specific speech patterns, and engaging quirks that make conversations interesting and memorable.`;

  // Use the custom persona functionality
  const customPersona = {
    id: Date.now(),
    description: sophisticatedDescription,
    isCustom: true
  };
  
  chatStore.startNewSession(customPersona);
  
  // Reset selections
  selectedCategory.value = '';
  selectedTraits.value = [];
};

const handleTemplateSelect = (template: PersonaTemplate) => {
  const detailedDescription = `${template.description}. ${template.background}. Personality: ${template.personality.join(', ')}. Speech pattern: ${template.speechPattern}.`;
  
  const templatePersona = {
    id: Date.now(),
    description: detailedDescription,
    isCustom: true
  };
  
  chatStore.startNewSession(templatePersona);
};
</script>