import {create} from 'zustand';

type AppState = {
  isReady: boolean;
  markReady: () => void;
};

export const useAppStore = create<AppState>(set => ({
  isReady: false,
  markReady: () => set({isReady: true}),
}));
