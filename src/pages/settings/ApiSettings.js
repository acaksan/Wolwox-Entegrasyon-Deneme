import React, { useState } from 'react';
import './Settings.css';

const ApiSettings = () => {
  const [apiKeys, setApiKeys] = useState([
    { id: 1, name: 'Wolvox API', key: '********-****-****-****-************', status: 'active' },
    { id: 2, name: 'Trendyol API', key: '********-****-****-****-************', status: 'active' },
    { id: 3, name: 'N11 API', key: '********-****-****-****-************', status: 'inactive' }
  ]);

  const [newApiKey, setNewApiKey] = useState({
    name: '',
    key: '',
    description: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewApiKey(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // API çağrısı yapılacak
    console.log('Yeni API Anahtarı:', newApiKey);
  };

  const handleReveal = (id) => {
    // Gerçek uygulamada API'den şifrelenmiş anahtarın açık hali çekilecek
    console.log('API Anahtarı gösterildi:', id);
  };

  const handleDelete = (id) => {
    // API çağrısı yapılacak
    console.log('API Anahtarı silindi:', id);
  };

  return (
    <div className="settings-container">
      <h1>API Ayarları</h1>

      {/* Mevcut API Anahtarları */}
      <div className="api-keys-list">
        <h2>API Anahtarları</h2>
        <div className="api-keys-grid">
          {apiKeys.map(api => (
            <div key={api.id} className="api-key-card">
              <div className="api-key-header">
                <h3>{api.name}</h3>
                <span className={`status-badge ${api.status}`}>
                  {api.status === 'active' ? 'Aktif' : 'Pasif'}
                </span>
              </div>
              <div className="api-key-content">
                <div className="api-key-value">
                  <span>{api.key}</span>
                  <button
                    className="btn-reveal"
                    onClick={() => handleReveal(api.id)}
                  >
                    Göster
                  </button>
                </div>
                <div className="api-key-actions">
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(api.id)}
                  >
                    Sil
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Yeni API Anahtarı Formu */}
      <div className="new-api-key">
        <h2>Yeni API Anahtarı Ekle</h2>
        <form onSubmit={handleSubmit} className="settings-form">
          <div className="form-group">
            <label htmlFor="name">API Adı</label>
            <input
              type="text"
              id="name"
              name="name"
              value={newApiKey.name}
              onChange={handleInputChange}
              required
              placeholder="Örn: Wolvox API"
            />
          </div>

          <div className="form-group">
            <label htmlFor="key">API Anahtarı</label>
            <input
              type="text"
              id="key"
              name="key"
              value={newApiKey.key}
              onChange={handleInputChange}
              required
              placeholder="API anahtarını girin"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Açıklama</label>
            <textarea
              id="description"
              name="description"
              value={newApiKey.description}
              onChange={handleInputChange}
              placeholder="API kullanım amacını açıklayın"
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-save">
              API Anahtarı Ekle
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ApiSettings; 