import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, DEMO_ACCOUNTS } from '../../context/AuthContext';
import { Bell, ShieldCheck, UserCheck, Cloud, RefreshCw, CheckCircle, AlertTriangle } from 'lucide-react';
import { apiRequest } from '../../api/client';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [showNotifMenu, setShowNotifMenu] = useState(false);
  const [showRoleMenu, setShowRoleMenu] = useState(false);
  const [backendMode, setBackendMode] = useState('unknown');

  const checkHealth = async () => {
    try {
      const data = await apiRequest('/api/health');
      setBackendMode(data.mode || 'sqlite');
    } catch (e) {
      setBackendMode('offline');
    }
  };

  const fetchNotifs = async () => {
    try {
      const data = await apiRequest('/api/notifications');
      setNotifications(data);
    } catch (e) {
      console.log('Notif error:', e);
    }
  };

  useEffect(() => {
    checkHealth();
    fetchNotifs();
    const interval = setInterval(() => {
      fetchNotifs();
      checkHealth();
    }, 30000);
    return () => clearInterval(interval);
  }, [user]);

  const unreadCount = notifications.filter(n => !n.read).length;

  const markRead = async (id) => {
    try {
      await apiRequest(`/api/notifications/${id}/read`, { method: 'PUT' });
      setNotifications(prev => prev.map(n => n.notification_id === id ? { ...n, read: true } : n));
    } catch (e) {}
  };

  return (
    <header className="h-16 bg-[#111827] border-b border-gray-800 flex items-center justify-between px-6 z-20">
      {/* Left: Brand Identity & Environment */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
            IQ
          </div>
          <span className="text-xl font-bold tracking-tight text-white">
            SpareParts<span className="text-cyan-400">IQ</span>
          </span>
        </div>
        {backendMode === 'aws' ? (
          <span className="hidden md:inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 shadow-sm shadow-emerald-500/10">
            <span className="w-2 h-2 rounded-full bg-emerald-400 mr-2 animate-pulse"></span>
            AWS CONNECTED (ap-south-1)
          </span>
        ) : (
          <span className="hidden md:inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30 shadow-sm shadow-amber-500/10">
            <span className="w-2 h-2 rounded-full bg-amber-400 mr-2"></span>
            LOCAL DEVELOPMENT MODE
          </span>
        )}
      </div>

      {/* Right: Role Switcher, Alerts, User Profile */}
      <div className="flex items-center space-x-4">
        {/* Fast Role Switcher */}
        <div className="relative">
          <button
            onClick={() => setShowRoleMenu(!showRoleMenu)}
            className="flex items-center space-x-2 text-xs bg-gray-800/80 hover:bg-gray-700 text-gray-200 px-3 py-1.5 rounded-lg border border-gray-700 transition"
            title="Switch demo user role"
          >
            <UserCheck className="w-4 h-4 text-cyan-400" />
            <span className="font-medium">{user?.role || 'Switch Role'}</span>
            <span className="text-gray-400 text-[10px]">▼</span>
          </button>

          {showRoleMenu && (
            <div className="absolute right-0 mt-2 w-64 bg-gray-900 border border-gray-800 rounded-xl shadow-2xl py-2 z-50">
              <div className="px-3 py-1.5 text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
                Select Active User Role
              </div>
              {DEMO_ACCOUNTS.map(acc => (
                <button
                  key={acc.role}
                  onClick={() => {
                    logout();
                    navigate('/login');
                    setShowRoleMenu(false);
                  }}
                  className={`w-full text-left px-3 py-2 text-xs flex flex-col hover:bg-gray-800 transition ${
                    user?.role === acc.role ? 'bg-cyan-950/40 border-l-2 border-cyan-400 text-cyan-300' : 'text-gray-300'
                  }`}
                >
                  <span className="font-semibold">{acc.role}</span>
                  <span className="text-[11px] text-gray-400">{acc.name} ({acc.department})</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifMenu(!showNotifMenu)}
            className="relative p-2 rounded-lg bg-gray-800/80 hover:bg-gray-700 text-gray-300 transition"
            title="Alerts & Notifications"
          >
            <Bell className="w-5 h-5" />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white rounded-full text-[10px] flex items-center justify-center font-bold animate-pulse">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifMenu && (
            <div className="absolute right-0 mt-2 w-80 md:w-96 bg-gray-900 border border-gray-800 rounded-xl shadow-2xl z-50 overflow-hidden">
              <div className="px-4 py-3 bg-gray-800/80 border-b border-gray-700/80 flex items-center justify-between">
                <span className="text-sm font-semibold text-white">System Alerts</span>
                <span className="text-xs text-gray-400">{unreadCount} unread</span>
              </div>
              <div className="max-h-80 overflow-y-auto divide-y divide-gray-800">
                {notifications.length === 0 ? (
                  <div className="p-4 text-center text-xs text-gray-400">No active alerts</div>
                ) : (
                  notifications.map(n => (
                    <div
                      key={n.notification_id}
                      onClick={() => markRead(n.notification_id)}
                      className={`p-3 text-xs cursor-pointer hover:bg-gray-800/70 transition flex items-start space-x-2 ${
                        !n.read ? 'bg-cyan-950/20' : 'opacity-70'
                      }`}
                    >
                      {n.priority === 'CRITICAL' ? (
                        <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                      ) : (
                        <CheckCircle className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1">
                        <div className="font-semibold text-gray-200">{n.title}</div>
                        <div className="text-gray-400 text-[11px] mt-0.5 line-clamp-2">{n.message}</div>
                        <div className="text-[10px] text-gray-500 mt-1">{new Date(n.created_at).toLocaleTimeString()}</div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Badge */}
        <div className="flex items-center space-x-2 pl-2 border-l border-gray-800">
          <div className="w-8 h-8 rounded-full bg-cyan-900/60 text-cyan-300 border border-cyan-700/50 flex items-center justify-center font-bold text-xs">
            {user?.name ? user.name.charAt(0) : 'U'}
          </div>
          <div className="hidden lg:block text-left">
            <div className="text-xs font-semibold text-gray-200">{user?.name || 'Authorized User'}</div>
            <div className="text-[10px] text-cyan-400">{user?.role}</div>
          </div>
        </div>
      </div>
    </header>
  );
}

