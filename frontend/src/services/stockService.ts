import { AxiosResponse } from 'axios';
import api from './api';
import { StockItem, StockUpdate, StockSyncResult, StockUpdateResponse } from '../types/stock';

class StockService {
    private readonly baseUrl = '/api/v1/stock';

    async checkStock(): Promise<StockItem[]> {
        try {
            const response: AxiosResponse<StockItem[]> = await api.get(`${this.baseUrl}/check`);
            return response.data;
        } catch (error) {
            console.error('Stok kontrolü sırasında hata:', error);
            throw error;
        }
    }

    async syncStock(): Promise<StockSyncResult> {
        try {
            const response: AxiosResponse<StockSyncResult> = await api.post(`${this.baseUrl}/sync`);
            return response.data;
        } catch (error) {
            console.error('Stok senkronizasyonu sırasında hata:', error);
            throw error;
        }
    }

    async updateStock(productId: string, quantity: number): Promise<StockUpdateResponse> {
        try {
            const response: AxiosResponse<StockUpdateResponse> = await api.put(
                `${this.baseUrl}/${productId}`,
                { quantity }
            );
            return response.data;
        } catch (error) {
            console.error('Stok güncellemesi sırasında hata:', error);
            throw error;
        }
    }

    async getLowStock(): Promise<StockItem[]> {
        try {
            const response: AxiosResponse<StockItem[]> = await api.get(`${this.baseUrl}/low`);
            return response.data;
        } catch (error) {
            console.error('Düşük stok kontrolü sırasında hata:', error);
            throw error;
        }
    }
}

export const stockService = new StockService();
export default stockService; 