import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListSubheader,
  Typography,
  Collapse,
  IconButton
} from '@mui/material';
import {
  Storage as StorageIcon,
  Sync as SyncIcon,
  Dashboard as DashboardIcon,
  Category as CategoryIcon,
  Inventory as InventoryIcon,
  AttachMoney as MoneyIcon,
  Store as StoreIcon,
  Assessment as AssessmentIcon,
  ExpandLess,
  ExpandMore,
  Business as BusinessIcon,
  Settings as SettingsIcon,
  Compare as CompareIcon
} from '@mui/icons-material';

const drawerWidth = 280;

const MainLayout = () => {
  const navigate = useNavigate();
  const [openMenus, setOpenMenus] = useState({});

  const toggleMenu = (title) => {
    setOpenMenus(prev => ({
      ...prev,
      [title]: !prev[title]
    }));
  };

  const menuItems = [
    {
      title: 'ENTEGRASYONLAR',
      icon: <SyncIcon />,
      items: [
        {
          name: 'Akınsoft Wolvox',
          path: '/wolvox',
          icon: <BusinessIcon />,
          subitems: [
            { name: 'Bağlantı Ayarları', path: '/wolvox/connection' },
            { name: 'Ürün Senkronizasyonu', path: '/wolvox/products' },
            { name: 'Stok Senkronizasyonu', path: '/wolvox/stock' },
            { name: 'Sipariş Senkronizasyonu', path: '/wolvox/orders' },
            { name: 'Ürün Karşılaştırma', path: '/wolvox/comparison' }
          ]
        },
        {
          name: 'WooCommerce',
          path: '/woocommerce',
          icon: <StoreIcon />,
          subitems: [
            { name: 'WooCommerce Ayarları', path: '/woocommerce/settings' },
            { name: 'Ürün Aktarımı', path: '/woocommerce/products' },
            { name: 'Stok Aktarımı', path: '/woocommerce/stock' },
            { name: 'Sipariş Aktarımı', path: '/woocommerce/orders' }
          ]
        }
      ]
    },
    {
      title: 'ÜRÜN YÖNETİMİ',
      icon: <InventoryIcon />,
      items: [
        { name: 'Ürün Listesi', path: '/products/list', icon: <InventoryIcon /> },
        { name: 'Kategori Yönetimi', path: '/categories', icon: <CategoryIcon /> },
        { name: 'Ürün Karşılaştırma', path: '/products/comparison', icon: <CompareIcon /> }
      ]
    },
    {
      title: 'STOK YÖNETİMİ',
      icon: <StorageIcon />,
      items: [
        { name: 'Stok Durumu', path: '/inventory/status', icon: <StorageIcon /> },
        { name: 'Stok Hareketleri', path: '/inventory/movements', icon: <SyncIcon /> }
      ]
    },
    {
      title: 'RAPORLAR',
      icon: <AssessmentIcon />,
      items: [
        { name: 'Satış Raporları', path: '/reports/sales', icon: <AssessmentIcon /> },
        { name: 'Stok Raporları', path: '/reports/inventory', icon: <StorageIcon /> }
      ]
    },
    {
      title: 'AYARLAR',
      icon: <SettingsIcon />,
      items: [
        { name: 'Genel Ayarlar', path: '/settings/general', icon: <SettingsIcon /> },
        { name: 'Sistem Logları', path: '/settings/logs', icon: <AssessmentIcon /> }
      ]
    }
  ];

  const renderMenuItem = (item, depth = 0) => {
    const hasSubItems = item.subitems && item.subitems.length > 0;
    const isOpen = openMenus[item.name];

    return (
      <React.Fragment key={item.path}>
        <ListItem
          button
          onClick={() => {
            if (hasSubItems) {
              toggleMenu(item.name);
            } else {
              navigate(item.path);
            }
          }}
          sx={{ pl: 2 + depth * 2 }}
        >
          {item.icon && <ListItemIcon>{item.icon}</ListItemIcon>}
          <ListItemText primary={item.name} />
          {hasSubItems && (
            <IconButton size="small">
              {isOpen ? <ExpandLess /> : <ExpandMore />}
            </IconButton>
          )}
        </ListItem>
        
        {hasSubItems && (
          <Collapse in={isOpen} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.subitems.map(subitem => renderMenuItem(subitem, depth + 1))}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        <Box sx={{ overflow: 'auto', mt: 2 }}>
          <Typography variant="h6" sx={{ px: 2, mb: 2 }}>
            Lastik Entegrasyon
          </Typography>
          
          {menuItems.map((section) => (
            <List
              key={section.title}
              subheader={
                <ListSubheader>
                  {section.icon} {section.title}
                </ListSubheader>
              }
            >
              {section.items.map(item => renderMenuItem(item))}
            </List>
          ))}
        </Box>
      </Drawer>
      
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout; 