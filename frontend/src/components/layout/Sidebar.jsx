import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Boxes,
  TrendingUp,
  AlertOctagon,
  ShoppingCart,
  Wrench,
  Truck,
  FileText,
  Cpu,
  LogOut
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Inventory Catalog', path: '/inventory', icon: Boxes },
  { name: 'AI Demand Forecast', path: '/forecasting', icon: TrendingUp },
  { name: 'Stockout Risk Matrix', path: '/stockouts', icon: AlertOctagon },
  { name: 'Reorder Engine', path: '/reorder', icon: ShoppingCart },
  { name: 'Maintenance Planning', path: '/maintenance', icon: Wrench },
  { name: 'Purchase Orders', path: '/purchase-orders', icon: FileText },
  { name: 'Suppliers Directory', path: '/suppliers', icon: Truck },
  { name: 'ML Model Evaluation', path: '/model-evaluation', icon: Cpu },
];

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="w-64 bg-[#0d131f] border-r border-gray-800 flex flex-col justify-between shrink-0 h-screen sticky top-0">
      <div>
        {/* Brand Area */}
        <div className="h-16 flex items-center px-6 border-b border-gray-800/80">
          <div className="text-xs uppercase tracking-wider font-semibold text-gray-400">
            Navigation Menu
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-3 space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 shadow-sm'
                      : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Footer / System Status */}
      <div className="p-4 border-t border-gray-800/80 bg-gray-900/40">
        <div className="bg-gray-800/60 rounded-xl p-3 border border-gray-700/50">
          <div className="text-[11px] font-semibold text-gray-300 flex items-center justify-between">
            <span>Serverless Stack</span>
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
          </div>
          <div className="text-[10px] text-gray-400 mt-1">
            DynamoDB • S3 • SNS • EventBridge
          </div>
        </div>

        <button
          onClick={logout}
          className="w-full mt-3 flex items-center justify-center space-x-2 px-3 py-2 text-xs text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Sign Out</span>
        </button>
      </div>
    </aside>
  );
}

