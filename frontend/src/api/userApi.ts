import apiClient from '@/lib/axios';

export interface User {
    id: string;
    email:string;
    full_name: string | null;
    is_active: boolean;
}

// --- Fetches the profile --- 
export const getCurrentUser = async (): Promise<User> => {
    const response = await apiClient.get<User>('/api/v1/users/me');
    return response.data;
}
