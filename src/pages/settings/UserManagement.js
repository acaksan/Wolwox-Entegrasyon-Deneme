import React, { useState } from 'react';
import './Settings.css';

const UserManagement = () => {
  const [users, setUsers] = useState([
    { id: 1, username: 'admin', email: 'admin@example.com', role: 'admin', status: 'active' },
    { id: 2, username: 'user1', email: 'user1@example.com', role: 'user', status: 'active' },
  ]);

  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    role: 'user',
    password: '',
    confirmPassword: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewUser(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // API çağrısı yapılacak
    console.log('Yeni kullanıcı:', newUser);
  };

  return (
    <div className="settings-container">
      <h1>Kullanıcı Yönetimi</h1>
      
      {/* Kullanıcı Listesi */}
      <div className="users-list">
        <h2>Mevcut Kullanıcılar</h2>
        <table className="users-table">
          <thead>
            <tr>
              <th>Kullanıcı Adı</th>
              <th>E-posta</th>
              <th>Rol</th>
              <th>Durum</th>
              <th>İşlemler</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id}>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.role === 'admin' ? 'Yönetici' : 'Kullanıcı'}</td>
                <td>{user.status === 'active' ? 'Aktif' : 'Pasif'}</td>
                <td>
                  <button className="btn-edit">Düzenle</button>
                  <button className="btn-delete">Sil</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Yeni Kullanıcı Formu */}
      <div className="new-user-form">
        <h2>Yeni Kullanıcı Ekle</h2>
        <form onSubmit={handleSubmit} className="settings-form">
          <div className="form-group">
            <label htmlFor="username">Kullanıcı Adı</label>
            <input
              type="text"
              id="username"
              name="username"
              value={newUser.username}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">E-posta</label>
            <input
              type="email"
              id="email"
              name="email"
              value={newUser.email}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Rol</label>
            <select
              id="role"
              name="role"
              value={newUser.role}
              onChange={handleInputChange}
            >
              <option value="user">Kullanıcı</option>
              <option value="admin">Yönetici</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="password">Şifre</label>
            <input
              type="password"
              id="password"
              name="password"
              value={newUser.password}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Şifre Tekrar</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={newUser.confirmPassword}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn-save">
              Kullanıcı Ekle
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserManagement; 