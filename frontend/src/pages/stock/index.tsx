import React, { useState } from 'react';
import Head from 'next/head';
import { Tab } from '@headlessui/react';
import StockList from '../../components/stock/StockList';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const StockManagement: React.FC = () => {
    const tabs = [
        { name: 'Tüm Ürünler', content: <StockList showLowStockOnly={false} /> },
        { name: 'Düşük Stoklu Ürünler', content: <StockList showLowStockOnly={true} /> },
    ];

    return (
        <div className="min-h-screen bg-gray-100">
            <Head>
                <title>Stok Yönetimi - Wolvox WooCommerce Entegrasyonu</title>
                <meta name="description" content="Wolvox ve WooCommerce stok yönetimi" />
            </Head>

            <main className="container mx-auto px-4 py-8">
                <div className="bg-white rounded-lg shadow-md p-6">
                    <h1 className="text-3xl font-bold text-gray-900 mb-8">
                        Stok Yönetimi
                    </h1>

                    <Tab.Group>
                        <Tab.List className="flex space-x-1 rounded-xl bg-blue-900/20 p-1 mb-6">
                            {tabs.map((tab) => (
                                <Tab
                                    key={tab.name}
                                    className={({ selected }) =>
                                        `w-full rounded-lg py-2.5 text-sm font-medium leading-5 
                                        ${selected
                                            ? 'bg-white text-blue-700 shadow'
                                            : 'text-gray-600 hover:bg-white/[0.12] hover:text-blue-600'
                                        }
                                        ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400
                                        focus:outline-none focus:ring-2`
                                    }
                                >
                                    {tab.name}
                                </Tab>
                            ))}
                        </Tab.List>
                        <Tab.Panels>
                            {tabs.map((tab, idx) => (
                                <Tab.Panel
                                    key={idx}
                                    className={`rounded-xl bg-white p-3
                                        ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400
                                        focus:outline-none focus:ring-2`}
                                >
                                    {tab.content}
                                </Tab.Panel>
                            ))}
                        </Tab.Panels>
                    </Tab.Group>
                </div>
            </main>

            <ToastContainer
                position="bottom-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />
        </div>
    );
};

export default StockManagement; 