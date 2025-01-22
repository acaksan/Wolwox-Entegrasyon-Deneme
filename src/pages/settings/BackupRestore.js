import React, { useState } from 'react';
import './Settings.css';

const BackupRestore = () => {
  const [backups, setBackups] = useState([
    {
      id: 1,
      name: 'Tam Yedek',
      date: '2024-02-20 15:30',
      size: '256 MB',
      type: 'full'
    },
    {
      id: 2,
      name: 'Veritabanı Yedeği',
      date: '2024-02-19 10:15',
      size: '128 MB',
      type: 'database'
    },
    {
      id: 3,
      name: 'Ayarlar Yedeği',
      date: '2024-02-18 08:45',
      size: '1.2 MB',
      type: 'settings'
    }
  ]);

  const [selectedBackup, setSelectedBackup] = useState(null);
  const [backupSettings, setBackupSettings] = useState({
    type: 'full',
    includeMedia: true,
    compression: 'high'
  });

  const handleBackupSettingsChange = (e) => {
    const { name, value, type, checked } = e.target;
    setBackupSettings(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleCreateBackup = (e) => {
    e.preventDefault();
    // API çağrısı yapılacak
    console.log('Yedekleme başlatıldı:', backupSettings);
  };

  const handleRestore = (backup) => {
    setSelectedBackup(backup);
    // Geri yükleme onay modalı açılacak
  };

  const handleDownload = (backup) => {
    // API çağrısı yapılacak
    console.log('Yedek indiriliyor:', backup);
  };

  const handleDelete = (backup) => {
    // API çağrısı yapılacak
    console.log('Yedek siliniyor:', backup);
  };

  return (
    <div className="settings-container">
      <h1>Yedekleme ve Geri Yükleme</h1>

      {/* Yeni Yedek Oluşturma */}
      <div className="backup-section">
        <h2>Yeni Yedek Oluştur</h2>
        <form onSubmit={handleCreateBackup} className="settings-form">
          <div className="form-group">
            <label htmlFor="type">Yedek Türü</label>
            <select
              id="type"
              name="type"
              value={backupSettings.type}
              onChange={handleBackupSettingsChange}
            >
              <option value="full">Tam Yedek</option>
              <option value="database">Sadece Veritabanı</option>
              <option value="settings">Sadece Ayarlar</option>
            </select>
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="includeMedia"
                checked={backupSettings.includeMedia}
                onChange={handleBackupSettingsChange}
              />
              <span>Medya Dosyalarını Dahil Et</span>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="compression">Sıkıştırma Seviyesi</label>
            <select
              id="compression"
              name="compression"
              value={backupSettings.compression}
              onChange={handleBackupSettingsChange}
            >
              <option value="none">Sıkıştırma Yok</option>
              <option value="low">Düşük</option>
              <option value="medium">Orta</option>
              <option value="high">Yüksek</option>
            </select>
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-save">
              Yedeklemeyi Başlat
            </button>
          </div>
        </form>
      </div>

      {/* Mevcut Yedekler */}
      <div className="backups-list">
        <h2>Mevcut Yedekler</h2>
        <div className="backups-grid">
          {backups.map(backup => (
            <div key={backup.id} className="backup-card">
              <div className="backup-info">
                <h3>{backup.name}</h3>
                <div className="backup-details">
                  <span className="backup-date">{backup.date}</span>
                  <span className="backup-size">{backup.size}</span>
                  <span className={`backup-type ${backup.type}`}>
                    {backup.type === 'full' ? 'Tam' : backup.type === 'database' ? 'VT' : 'Ayarlar'}
                  </span>
                </div>
              </div>
              <div className="backup-actions">
                <button
                  className="btn-restore"
                  onClick={() => handleRestore(backup)}
                >
                  Geri Yükle
                </button>
                <button
                  className="btn-download"
                  onClick={() => handleDownload(backup)}
                >
                  İndir
                </button>
                <button
                  className="btn-delete"
                  onClick={() => handleDelete(backup)}
                >
                  Sil
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Geri Yükleme Onay Modalı */}
      {selectedBackup && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>Geri Yükleme Onayı</h2>
            <p>
              <strong>{selectedBackup.name}</strong> yedeğini geri yüklemek istediğinizden emin misiniz?
              Bu işlem mevcut verilerin üzerine yazacaktır.
            </p>
            <div className="modal-actions">
              <button
                className="btn-cancel"
                onClick={() => setSelectedBackup(null)}
              >
                İptal
              </button>
              <button
                className="btn-confirm"
                onClick={() => {
                  console.log('Geri yükleme başlatıldı:', selectedBackup);
                  setSelectedBackup(null);
                }}
              >
                Geri Yükle
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BackupRestore; 