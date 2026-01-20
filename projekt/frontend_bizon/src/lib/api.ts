const BASE_URL = 'http://localhost:8000/';
import { type ApiError, type Recipe } from "./types.js";

export async function apiFetch<T>(
    endpoint: string, 
    options: RequestInit = {}
): Promise<T> {
    options.credentials = 'include';
    options.headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    let response = await fetch(`${BASE_URL}${endpoint}`, options);

    if (response.status === 401 && endpoint !== '/token/' && endpoint !== '/token/refresh/') {
        const refreshed = await tryRefresh();
        
        if (refreshed) {
            response = await fetch(`${BASE_URL}${endpoint}`, options);
        } else {
            throw new Error('Session expired');
        }
    }

    if (!response.ok) {
        const errorData: ApiError = await response.json().catch(() => ({}));
        throw errorData;
    }

    if (response.status === 204 || response.headers.get('content-length') === '0') {
        return {} as T;
    }

    return response.json();
}

async function tryRefresh(): Promise<boolean> {
    try {
        const res = await fetch(`${BASE_URL}/token/refresh/`, {
            method: 'POST',
            credentials: 'include',
        });
        return res.ok;
    } catch {
        return false;
    }
}

/**
 * @param query
 */
export async function searchRecipes(query: string): Promise<Recipe[]> {
    if (!query.trim()) return [];

    const API_URL = `http://localhost:8000/search/?query=${encodeURIComponent(query)}`;

    try {
        const response = await fetch(API_URL, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`Błąd serwera: ${response.status}`);
        }

        const data: Recipe[] = await response.json();
        return data;
    } catch (error) {
        console.error("Błąd podczas wyszukiwania przepisów:", error);
        return [];
    }
}

export function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
}

export async function createReview(text: string, recipeId: number, stars: number) {
    const response = await fetch(`${BASE_URL}create_review/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify({ 
            stars: stars,
            text: text,
            recipe_id: recipeId 
        })
    });

    console.log(JSON.stringify({ 
            stars: 5,
            text: text,
            recipe_id: recipeId 
        }))
    return response.ok ? await response.json() : Promise.reject(response);
}

export async function updateReview(text: string, reviewId: number, stars: number) {
    const response = await fetch(`${BASE_URL}update_review/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
        },
        credentials: 'include',
        body: JSON.stringify({
            stars: stars, 
            review_text: text,
            review_id: reviewId 
        })
    });
    return response.ok ? await response.json() : Promise.reject(response);
}