import { apiClient } from "@nexus/api-client";

export const api = apiClient;

export async function login(email: string, password: string) {
  const response = await api.post<{
    access_token: string;
    refresh_token: string;
  }>("/api/v1/auth/login", { email, password });
  api.setAccessToken(response.access_token);
  return response;
}

export async function register(
  email: string,
  password: string,
  display_name: string,
) {
  const response = await api.post<{
    access_token: string;
    refresh_token: string;
  }>("/api/v1/auth/register", { email, password, display_name });
  api.setAccessToken(response.access_token);
  return response;
}

export async function getMe() {
  return api.get<{
    id: string;
    email: string;
    display_name: string | null;
    avatar_url: string | null;
  }>("/api/v1/auth/me");
}
