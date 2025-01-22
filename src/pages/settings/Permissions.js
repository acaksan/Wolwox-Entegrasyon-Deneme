import React, { useState } from 'react';
import './Settings.css';

const Permissions = () => {
  const [roles, setRoles] = useState([
    { id: 1, name: 'admin', description: 'Yönetici' },
    { id: 2, name: 'user', description: 'Normal Kullanıcı' },
    { id: 3, name: 'editor', description: 'Editör' }
  ]);

  const [permissions, setPermissions] = useState([
    { id: 1, module: 'Ürünler', actions: ['görüntüleme', 'ekleme', 'düzenleme', 'silme'] },
    { id: 2, module: 'Siparişler', actions: ['görüntüleme', 'onaylama', 'iptal'] },
    { id: 3, module: 'Raporlar', actions: ['görüntüleme', 'indirme'] },
    { id: 4, module: 'Ayarlar', actions: ['görüntüleme', 'düzenleme'] }
  ]);

  const [selectedRole, setSelectedRole] = useState(null);
  const [rolePermissions, setRolePermissions] = useState({});

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
    // Gerçek uygulamada API'den rol izinleri çekilecek
    setRolePermissions({
      'Ürünler': ['görüntüleme', 'ekleme'],
      'Siparişler': ['görüntüleme'],
      'Raporlar': ['görüntüleme'],
      'Ayarlar': []
    });
  };

  const handlePermissionChange = (module, action) => {
    setRolePermissions(prev => {
      const modulePermissions = prev[module] || [];
      const newPermissions = modulePermissions.includes(action)
        ? modulePermissions.filter(p => p !== action)
        : [...modulePermissions, action];
      
      return {
        ...prev,
        [module]: newPermissions
      };
    });
  };

  const handleSave = () => {
    if (selectedRole) {
      // API çağrısı yapılacak
      console.log('Rol izinleri kaydedildi:', {
        role: selectedRole,
        permissions: rolePermissions
      });
    }
  };

  return (
    <div className="settings-container">
      <h1>İzin Yönetimi</h1>

      {/* Rol Seçimi */}
      <div className="roles-list">
        <h2>Roller</h2>
        <div className="roles-grid">
          {roles.map(role => (
            <div
              key={role.id}
              className={`role-card ${selectedRole?.id === role.id ? 'selected' : ''}`}
              onClick={() => handleRoleSelect(role)}
            >
              <h3>{role.description}</h3>
              <p>{role.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* İzin Matrisi */}
      {selectedRole && (
        <div className="permissions-matrix">
          <h2>İzinler - {selectedRole.description}</h2>
          <div className="matrix-container">
            <table className="permissions-table">
              <thead>
                <tr>
                  <th>Modül</th>
                  <th>İzinler</th>
                </tr>
              </thead>
              <tbody>
                {permissions.map(permission => (
                  <tr key={permission.id}>
                    <td>{permission.module}</td>
                    <td>
                      <div className="permissions-actions">
                        {permission.actions.map(action => (
                          <label key={action} className="permission-checkbox">
                            <input
                              type="checkbox"
                              checked={(rolePermissions[permission.module] || []).includes(action)}
                              onChange={() => handlePermissionChange(permission.module, action)}
                            />
                            <span>{action}</span>
                          </label>
                        ))}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="form-actions">
            <button onClick={handleSave} className="btn-save">
              İzinleri Kaydet
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Permissions; 