import { writable } from 'svelte/store';

const storedAccess = typeof window !== 'undefined' ? localStorage.getItem('access') : null;

export const auth = writable({
    isLoggedIn: !!storedAccess,
    accessToken: storedAccess,
    refreshToken: typeof window !== 'undefined' ? localStorage.getItem('refresh') : null,
});

export const logout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    auth.set({ isLoggedIn: false, accessToken: null, refreshToken: null });
};