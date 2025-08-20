import apiClient from '@/lib/axios';

// ---- Format of the response from the /login/google endpoint 
interface AuthURLResponse{
    authorization_url: string;
}

// --- Fetches the Google OAuth Authorization URL ---
export const getGoogleLoginUrl = async () : Promise <string> => {
    const response = await apiClient.get<AuthURLResponse>('/api/v1/auth/login/google');
    return response.data.authorization_url;
}

// --- Sends a request to the backend to log the user out ---
export const logoutUser = async (): Promise<void> => {
  await apiClient.post('/api/v1/auth/logout');
};
