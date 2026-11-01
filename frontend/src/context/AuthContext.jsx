import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiRequest } from '../api/client';

const AuthContext = createContext(null);

export const DEMO_ACCOUNTS = [
  {
    role: "Inventory Manager",
    email: "inventory@sparepartsiq.com",
    name: "Vikramaditya Rao",
    department: "Supply Chain & Warehouse"
  },
  {
    role: "Maintenance Team",
    email: "maintenance@sparepartsiq.com",
    name: "Suresh Sen",
    department: "Plant Maintenance & Reliability"
  },
  {
    role: "Purchase Manager",
    email: "purchase@sparepartsiq.com",
    name: "Meera Kulkarni",
    department: "Procurement & Sourcing"
  }
];

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('sparepartsiq_user');
    const token = localStorage.getItem('sparepartsiq_token');
    if (savedUser && token) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('sparepartsiq_user');
        localStorage.removeItem('sparepartsiq_token');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await apiRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    localStorage.setItem('sparepartsiq_token', data.access_token);
    localStorage.setItem('sparepartsiq_user', JSON.stringify(data.user));
    setUser(data.user);
    return data.user;
  };

  const logout = () => {
    localStorage.removeItem('sparepartsiq_token');
    localStorage.removeItem('sparepartsiq_user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

