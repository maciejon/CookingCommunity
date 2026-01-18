export interface User {
    id: number;
    username: string;
    email: string;
}

export interface ApiError {
    detail?: string;
    [key: string]: any;
}