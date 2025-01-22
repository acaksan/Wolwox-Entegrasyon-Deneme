import React, { useState } from 'react';
import './Settings.css';

const GeneralSettings = () => {
  const [settings, setSettings] = useState({
    companyName: '',
    email: '',
    phone: '',
    address: '',
    taxNumber: '',
    language: 'tr',
    timezone: 'Europe/Istanbul'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // API çağrısı yapılacak
    console.log('Ayarlar kaydedildi:', settings);
  };

  return (
    <div className="settings-container">
      <h1>Genel Ayarlar</h1>
      <form onSubmit={handleSubmit} className="settings-form">
        <div className="form-group">
          <label htmlFor="companyName">Firma Adı</label>
          <input
            type="text"
            id="companyName"
            name="companyName"
            value={settings.companyName}
            onChange={handleChange}
            placeholder="Firma adını giriniz"
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">E-posta</label>
          <input
            type="email"
            id="email"
            name="email"
            value={settings.email}
            onChange={handleChange}
            placeholder="E-posta adresini giriniz"
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone">Telefon</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={settings.phone}
            onChange={handleChange}
            placeholder="Telefon numarasını giriniz"
          />
        </div>

        <div className="form-group">
          <label htmlFor="address">Adres</label>
          <textarea
            id="address"
            name="address"
            value={settings.address}
            onChange={handleChange}
            placeholder="Adres bilgilerini giriniz"
          />
        </div>

        <div className="form-group">
          <label htmlFor="taxNumber">Vergi Numarası</label>
          <input
            type="text"
            id="taxNumber"
            name="taxNumber"
            value={settings.taxNumber}
            onChange={handleChange}
            placeholder="Vergi numarasını giriniz"
          />
        </div>

        <div className="form-group">
          <label htmlFor="language">Dil</label>
          <select
            id="language"
            name="language"
            value={settings.language}
            onChange={handleChange}
          >
            <option value="tr">Türkçe</option>
            <option value="en">English</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="timezone">Saat Dilimi</label>
          <select
            id="timezone"
            name="timezone"
            value={settings.timezone}
            onChange={handleChange}
          >
            <option value="Europe/Istanbul">İstanbul (UTC+3)</option>
            <option value="Europe/London">Londra (UTC+0)</option>
          </select>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-save">
            Kaydet
          </button>
          <button type="button" className="btn-cancel">
            İptal
          </button>
        </div>
      </form>
    </div>
  );
};

export default GeneralSettings; 