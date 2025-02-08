import React from 'react';
import { StockItem } from '../../types/stock';

interface StockCardProps {
    stock: StockItem;
    onUpdate: (productId: string, quantity: number) => Promise<void>;
}

const StockCard: React.FC<StockCardProps> = ({ stock, onUpdate }) => {
    const [quantity, setQuantity] = React.useState(stock.quantity);
    const [isEditing, setIsEditing] = React.useState(false);
    const [isUpdating, setIsUpdating] = React.useState(false);

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'normal':
                return 'bg-green-100 text-green-800';
            case 'low':
                return 'bg-yellow-100 text-yellow-800';
            case 'out_of_stock':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const handleUpdate = async () => {
        try {
            setIsUpdating(true);
            await onUpdate(stock.product_id, quantity);
            setIsEditing(false);
        } catch (error) {
            console.error('Stok güncellenirken hata:', error);
        } finally {
            setIsUpdating(false);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-4">
            <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-gray-800">{stock.product_name}</h3>
                <span className={`px-2 py-1 rounded-full text-sm ${getStatusColor(stock.status)}`}>
                    {stock.status === 'normal' ? 'Normal'
                        : stock.status === 'low' ? 'Düşük'
                        : 'Stokta Yok'}
                </span>
            </div>
            
            {stock.sku && (
                <p className="text-sm text-gray-600 mb-2">
                    SKU: {stock.sku}
                </p>
            )}
            
            <div className="flex items-center justify-between mt-4">
                <div className="flex items-center">
                    <span className="text-gray-600 mr-2">Miktar:</span>
                    {isEditing ? (
                        <input
                            type="number"
                            value={quantity}
                            onChange={(e) => setQuantity(Number(e.target.value))}
                            className="w-20 px-2 py-1 border rounded"
                            min="0"
                        />
                    ) : (
                        <span className="font-semibold">{quantity}</span>
                    )}
                </div>
                
                <div className="flex space-x-2">
                    {isEditing ? (
                        <>
                            <button
                                onClick={handleUpdate}
                                disabled={isUpdating}
                                className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
                            >
                                {isUpdating ? 'Güncelleniyor...' : 'Kaydet'}
                            </button>
                            <button
                                onClick={() => {
                                    setIsEditing(false);
                                    setQuantity(stock.quantity);
                                }}
                                disabled={isUpdating}
                                className="px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 disabled:opacity-50"
                            >
                                İptal
                            </button>
                        </>
                    ) : (
                        <button
                            onClick={() => setIsEditing(true)}
                            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                        >
                            Düzenle
                        </button>
                    )}
                </div>
            </div>
            
            {stock.threshold && (
                <div className="mt-2 text-sm text-gray-600">
                    Eşik Değeri: {stock.threshold}
                </div>
            )}
        </div>
    );
};

export default StockCard; 