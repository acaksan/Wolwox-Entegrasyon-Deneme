import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { menuConfig } from '../config/menu-structure';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const location = useLocation();
  const [openSections, setOpenSections] = useState({});

  const toggleSection = (sectionId) => {
    setOpenSections(prev => ({
      ...prev,
      [sectionId]: !prev[sectionId]
    }));
  };

  const renderMenuItem = (item) => {
    const isActive = location.pathname.startsWith(item.path);

    return (
      <li key={item.id} className={`menu-item ${isActive ? 'active' : ''}`}>
        <Link to={item.path}>
          <i className={item.icon}></i>
          <span>{item.name}</span>
        </Link>
      </li>
    );
  };

  const renderMenuSection = (section) => {
    const isOpen = openSections[section.id];

    return (
      <div key={section.id} className="menu-section">
        <h3 
          className={`menu-title ${isOpen ? 'open' : ''}`} 
          onClick={() => toggleSection(section.id)}
        >
          <div className="menu-title-content">
            <i className={section.icon}></i>
            <span>{section.title}</span>
          </div>
          <i className={`fas fa-chevron-${isOpen ? 'down' : 'right'} menu-arrow`}></i>
        </h3>
        <ul className={`menu-items ${isOpen ? 'open' : ''}`}>
          {section.items.map(renderMenuItem)}
        </ul>
      </div>
    );
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h1>Wolvox Entegrasyon</h1>
      </div>
      <nav className="sidebar-nav">
        {menuConfig.items.map(renderMenuSection)}
      </nav>
    </aside>
  );
};

export default Sidebar; 