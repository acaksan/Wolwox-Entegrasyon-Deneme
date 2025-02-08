import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Ürün API'leri
export const productAPI = {
    sync: () => api.post('/api/v1/products/sync'),
    list: () => api.get('/api/v1/products'),
    getById: (id: string) => api.get(`/api/v1/products/${id}`),
    update: (id: string, data: any) => api.put(`/api/v1/products/${id}`, data),
};

// Sipariş API'leri
export const orderAPI = {
    sync: () => api.post('/api/v1/orders/sync'),
    list: () => api.get('/api/v1/orders'),
    getById: (id: string) => api.get(`/api/v1/orders/${id}`),
    update: (id: string, data: any) => api.put(`/api/v1/orders/${id}`, data),
};

// Stok API'leri
export const stockAPI = {
    sync: () => api.post('/api/v1/stock/sync'),
    check: () => api.get('/api/v1/stock/check'),
    update: (productId: string, quantity: number) => 
        api.put(`/api/v1/stock/${productId}`, { quantity }),
};

// Interceptor'lar
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Token geçersiz, kullanıcıyı login sayfasına yönlendir
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
