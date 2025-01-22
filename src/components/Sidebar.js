import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { menuConfig } from '../config/menu-structure';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [openSections, setOpenSections] = useState([]);
  const location = useLocation();

  const toggleSection = (sectionId) => {
    setOpenSections(prev => 
      prev.includes(sectionId) 
        ? prev.filter(id => id !== sectionId)
        : [...prev, sectionId]
    );
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        <div className="logo-container">
          <img src="/logo.png" alt="Logo" className="logo" />
          {!isCollapsed && (
            <div className="title-container">
              <h1>Lastik Entegrasyon</h1>
              <p>Wolvox - WooCommerce</p>
            </div>
          )}
        </div>
        <button onClick={() => setIsCollapsed(!isCollapsed)} className="collapse-btn">
          <i className={`fas fa-chevron-${isCollapsed ? 'right' : 'left'}`} />
        </button>
      </div>

      <div className="sidebar-nav">
        {menuConfig.items.map((section) => (
          <div key={section.id} className="menu-section">
            <div 
              className={`menu-title ${openSections.includes(section.id) ? 'open' : ''}`}
              onClick={() => toggleSection(section.id)}
            >
              <div className="menu-title-content">
                <i className={section.icon} />
                {!isCollapsed && <span>{section.title}</span>}
              </div>
              {!isCollapsed && (
                <i className={`fas fa-chevron-${openSections.includes(section.id) ? 'down' : 'right'} menu-arrow`} />
              )}
            </div>

            {(openSections.includes(section.id) || isCollapsed) && (
              <div className={`menu-items ${isCollapsed ? 'collapsed' : ''}`}>
                {section.items.map((item) => (
                  <div key={item.id} className="menu-item-container">
                    {item.items ? (
                      <div className="submenu-trigger">
                        <div className="menu-item">
                          <i className={item.icon} />
                          {!isCollapsed && <span>{item.name}</span>}
                        </div>
                        {item.items && (
                          <div className="submenu">
                            {item.items.map((subItem) => (
                              <Link
                                key={subItem.id}
                                to={subItem.path}
                                className={`menu-item ${isActive(subItem.path) ? 'active' : ''}`}
                              >
                                <i className={subItem.icon} />
                                <span>{subItem.name}</span>
                              </Link>
                            ))}
                          </div>
                        )}
                      </div>
                    ) : (
                      <Link
                        to={item.path}
                        className={`menu-item ${isActive(item.path) ? 'active' : ''}`}
                      >
                        <i className={item.icon} />
                        {!isCollapsed && <span>{item.name}</span>}
                      </Link>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </nav>
  );
};

export default Sidebar; 