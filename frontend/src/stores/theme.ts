import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false);

  const toggleTheme = () => {
    isDark.value = !isDark.value;
    updateDocumentTheme();
  };

  const setTheme = (dark: boolean) => {
    isDark.value = dark;
    updateDocumentTheme();
  };

  const updateDocumentTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Initialize theme on store creation
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme) {
      setTheme(savedTheme === 'dark');
    } else {
      setTheme(prefersDark);
    }
  };

  // Save theme preference
  const saveTheme = () => {
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light');
  };

  return {
    isDark,
    toggleTheme,
    setTheme,
    initTheme,
    saveTheme
  };
});