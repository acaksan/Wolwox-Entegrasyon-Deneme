import React, { useState } from 'react';
import './Settings.css';

const SystemLogs = () => {
  const [logs, setLogs] = useState([
    {
      id: 1,
      type: 'error',
      message: 'Veritabanı bağlantısı başarısız',
      timestamp: '2024-02-20 15:45:23',
      source: 'Database'
    },
    {
      id: 2,
      type: 'warning',
      message: 'API istek limiti aşıldı',
      timestamp: '2024-02-20 15:30:12',
      source: 'API'
    },
    {
      id: 3,
      type: 'info',
      message: 'Yeni kullanıcı kaydı oluşturuldu',
      timestamp: '2024-02-20 15:15:45',
      source: 'Auth'
    },
    {
      id: 4,
      type: 'success',
      message: 'Sistem yedeklemesi tamamlandı',
      timestamp: '2024-02-20 15:00:00',
      source: 'Backup'
    }
  ]);

  const [filters, setFilters] = useState({
    type: 'all',
    source: 'all',
    search: '',
    dateRange: 'today'
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleClearLogs = () => {
    // API çağrısı yapılacak
    console.log('Loglar temizlendi');
  };

  const handleExportLogs = () => {
    // API çağrısı yapılacak
    console.log('Loglar dışa aktarıldı');
  };

  const filteredLogs = logs.filter(log => {
    if (filters.type !== 'all' && log.type !== filters.type) return false;
    if (filters.source !== 'all' && log.source !== filters.source) return false;
    if (filters.search && !log.message.toLowerCase().includes(filters.search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="settings-container">
      <h1>Sistem Logları</h1>

      {/* Filtreler */}
      <div className="logs-filters">
        <div className="filters-grid">
          <div className="filter-group">
            <label htmlFor="type">Log Tipi</label>
            <select
              id="type"
              name="type"
              value={filters.type}
              onChange={handleFilterChange}
            >
              <option value="all">Tümü</option>
              <option value="error">Hata</option>
              <option value="warning">Uyarı</option>
              <option value="info">Bilgi</option>
              <option value="success">Başarılı</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="source">Kaynak</label>
            <select
              id="source"
              name="source"
              value={filters.source}
              onChange={handleFilterChange}
            >
              <option value="all">Tümü</option>
              <option value="Database">Veritabanı</option>
              <option value="API">API</option>
              <option value="Auth">Kimlik Doğrulama</option>
              <option value="Backup">Yedekleme</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="dateRange">Tarih Aralığı</label>
            <select
              id="dateRange"
              name="dateRange"
              value={filters.dateRange}
              onChange={handleFilterChange}
            >
              <option value="today">Bugün</option>
              <option value="yesterday">Dün</option>
              <option value="week">Son 7 Gün</option>
              <option value="month">Son 30 Gün</option>
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="search">Arama</label>
            <input
              type="text"
              id="search"
              name="search"
              value={filters.search}
              onChange={handleFilterChange}
              placeholder="Log mesajında ara..."
            />
          </div>
        </div>

        <div className="filters-actions">
          <button onClick={handleExportLogs} className="btn-export">
            Logları Dışa Aktar
          </button>
          <button onClick={handleClearLogs} className="btn-clear">
            Logları Temizle
          </button>
        </div>
      </div>

      {/* Log Listesi */}
      <div className="logs-list">
        {filteredLogs.map(log => (
          <div key={log.id} className={`log-item ${log.type}`}>
            <div className="log-header">
              <span className="log-timestamp">{log.timestamp}</span>
              <span className={`log-type ${log.type}`}>
                {log.type === 'error' ? 'Hata' :
                 log.type === 'warning' ? 'Uyarı' :
                 log.type === 'info' ? 'Bilgi' : 'Başarılı'}
              </span>
              <span className="log-source">{log.source}</span>
            </div>
            <div className="log-message">{log.message}</div>
          </div>
        ))}

        {filteredLogs.length === 0 && (
          <div className="no-logs">
            <p>Seçilen kriterlere uygun log bulunamadı.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default SystemLogs; 