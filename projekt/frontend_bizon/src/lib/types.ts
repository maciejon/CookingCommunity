export interface User {
    id: number;
    username: string;
    email: string;
}

export interface ApiError {
    detail?: string;
    [key: string]: any;
}

export interface Recipe {
    id: number;
    name: string;
    description: string;
    // image_url?: string;
    // preparation_time?: number;
}