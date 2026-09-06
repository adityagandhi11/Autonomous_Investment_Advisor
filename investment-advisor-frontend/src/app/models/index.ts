export interface Investment {
    id: number;
    name: string;
    amount: number;
    date: Date;
}

export interface User {
    id: number;
    username: string;
    email: string;
}

export interface ApiResponse<T> {
    data: T;
    message: string;
    success: boolean;
}