import React, { useEffect, useState } from 'react';
import { StockItem } from '../../types/stock';
import StockCard from './StockCard';
import stockService from '../../services/stockService';
import { toast } from 'react-toastify';

interface StockListProps {
    showLowStockOnly?: boolean;
}

const StockList: React.FC<StockListProps> = ({ showLowStockOnly = false }) => {
    const [stocks, setStocks] = useState<StockItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);

    const loadStocks = async () => {
        try {
            setLoading(true);
            const data = showLowStockOnly
                ? await stockService.getLowStock()
                : await stockService.checkStock();
            setStocks(data);
        } catch (error) {
            console.error('Stok bilgileri yüklenirken hata:', error);
            toast.error('Stok bilgileri yüklenemedi');
        } finally {
            setLoading(false);
        }
    };

    const handleSync = async () => {
        try {
            setSyncing(true);
            const result = await stockService.syncStock();
            if (result.success) {
                toast.success(`${result.updated_count} ürün başarıyla senkronize edildi`);
                if (result.failed_updates.length > 0) {
                    toast.warning(`${result.failed_updates.length} ürün senkronize edilemedi`);
                }
                await loadStocks();
            }
        } catch (error) {
            console.error('Stok senkronizasyonu sırasında hata:', error);
            toast.error('Stok senkronizasyonu başarısız oldu');
        } finally {
            setSyncing(false);
        }
    };

    const handleStockUpdate = async (productId: string, quantity: number) => {
        try {
            await stockService.updateStock(productId, quantity);
            toast.success('Stok başarıyla güncellendi');
            await loadStocks();
        } catch (error) {
            console.error('Stok güncellenirken hata:', error);
            toast.error('Stok güncellenemedi');
        }
    };

    useEffect(() => {
        loadStocks();
    }, [showLowStockOnly]);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                    {showLowStockOnly ? 'Düşük Stoklu Ürünler' : 'Tüm Ürünler'}
                </h2>
                <button
                    onClick={handleSync}
                    disabled={syncing}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                >
                    {syncing ? 'Senkronize Ediliyor...' : 'Senkronize Et'}
                </button>
            </div>

            {stocks.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                    {showLowStockOnly
                        ? 'Düşük stoklu ürün bulunmuyor'
                        : 'Henüz stok bilgisi bulunmuyor'}
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {stocks.map((stock) => (
                        <StockCard
                            key={stock.product_id}
                            stock={stock}
                            onUpdate={handleStockUpdate}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default StockList; 