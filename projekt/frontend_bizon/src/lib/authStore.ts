import { writable } from 'svelte/store';
import type { User } from './types';
import { apiFetch } from '$lib/api.ts';

export const user = writable<User | null>(null);
export const isAuthenticated = writable<boolean>(false);

export async function logout() {
        try {
            await apiFetch('/logout/', { method: 'POST' });
        } finally {
            user.set(null);
            isAuthenticated.set(false);
        }
    }