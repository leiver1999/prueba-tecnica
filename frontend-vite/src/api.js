import { createApi } from './api-core.js';
export const api = createApi(import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000');
