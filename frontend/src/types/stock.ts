export type StockStatus = 'normal' | 'low' | 'out_of_stock';

export interface StockItem {
    product_id: string;
    product_name: string;
    sku?: string;
    quantity: number;
    threshold?: number;
    status: StockStatus;
}

export interface StockUpdate {
    quantity: number;
}

export interface StockSyncResult {
    success: boolean;
    updated_count: number;
    failed_updates: Array<{
        product_id: string;
        error: string;
    }>;
}

export interface StockUpdateResponse {
    message: string;
    product_id: string;
    quantity: number;
} 