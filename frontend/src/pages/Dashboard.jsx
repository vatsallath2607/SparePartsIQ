import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import MetricCard from '../components/common/MetricCard';
import {
  Boxes,
  DollarSign,
  AlertTriangle,
  AlertOctagon,
  Wrench,
  ShoppingCart,
  TrendingUp,
  Truck,
  ArrowRight
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { Link } from 'react-router-dom';

const COLORS = ['#06b6d4', '#3b82f6', '#8b5cf6', '#10b981', '#f59e0b'];

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await apiRequest('/api/analytics/dashboard');
        setData(res);
      } catch (err) {
        console.error('Failed to load dashboard:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
      </div>
    );
  }

  const kpis = data?.kpis || {};

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Executive Inventory Intelligence</h1>
          <p className="text-xs text-gray-400 mt-1">
            Real-time telemetry, AI demand forecasts, stockout risks, and automated replenishment recommendations.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            to="/reorder"
            className="flex items-center space-x-2 px-3.5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-lg shadow-cyan-500/20"
          >
            <ShoppingCart className="w-4 h-4" />
            <span>Review Reorders ({kpis.pending_reorders_count || 0})</span>
          </Link>
        </div>
      </div>

      {/* KPI Metric Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <MetricCard
          title="Spare Parts"
          value={kpis.total_spare_parts || 0}
          subtitle="Catalog active items"
          icon={Boxes}
          color="cyan"
        />
        <MetricCard
          title="Inventory Value"
          value={`$${(kpis.total_inventory_value || 0).toLocaleString()}`}
          subtitle="Total asset valuation"
          icon={DollarSign}
          color="emerald"
        />
        <MetricCard
          title="Low Stock"
          value={kpis.low_stock_count || 0}
          subtitle="Below reorder point"
          icon={AlertTriangle}
          color="amber"
          badge="Attention"
        />
        <MetricCard
          title="Critical Stockouts"
          value={kpis.critical_stockouts_count || 0}
          subtitle="Deficit during lead time"
          icon={AlertOctagon}
          color="red"
          badge="Action Req."
        />
        <MetricCard
          title="Upcoming Maint."
          value={kpis.upcoming_maintenance_count || 0}
          subtitle="Next 90 days scheduled"
          icon={Wrench}
          color="purple"
        />
        <MetricCard
          title="Pending Reorders"
          value={kpis.pending_reorders_count || 0}
          subtitle="Optimal batch proposals"
          icon={ShoppingCart}
          color="cyan"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Consumption Trend */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white">Consumption & Expenditure Trends</h2>
              <p className="text-xs text-gray-400">Monthly aggregate part units and procurement cost</p>
            </div>
            <TrendingUp className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.consumption_trend || []}>
                <defs>
                  <linearGradient id="consumptionGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" stroke="#4b5563" fontSize={11} />
                <YAxis stroke="#4b5563" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '11px' }}
                />
                <Area type="monotone" dataKey="consumption_units" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#consumptionGrad)" name="Units Consumed" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Asset Valuation Breakdown */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white">Asset Valuation by Category</h2>
              <p className="text-xs text-gray-400">Inventory capital allocation across components</p>
            </div>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data?.category_distribution || []}>
                <XAxis dataKey="category" stroke="#4b5563" fontSize={10} tickFormatter={(val) => val.split(' ')[0]} />
                <YAxis stroke="#4b5563" fontSize={11} tickFormatter={(val) => `$${val}`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '11px' }}
                />
                <Bar dataKey="total_value" fill="#3b82f6" radius={[6, 6, 0, 0]} name="Valuation ($)">
                  {(data?.category_distribution || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Lower Row: At-Risk Parts & Supplier Scorecard */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* At-Risk Inventory Parts */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-[#111827] border border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white">Top Attention Components</h2>
              <p className="text-xs text-gray-400">Parts currently operating below safety reorder threshold</p>
            </div>
            <Link to="/inventory" className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center space-x-1">
              <span>View Catalog</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-gray-400 border-b border-gray-800">
                <tr>
                  <th className="pb-3 font-semibold">Part Identifier</th>
                  <th className="pb-3 font-semibold">Category</th>
                  <th className="pb-3 font-semibold">Current Stock</th>
                  <th className="pb-3 font-semibold">Reorder Point</th>
                  <th className="pb-3 font-semibold">Criticality</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60">
                {(data?.top_at_risk_parts || []).map((part) => (
                  <tr key={part.part_id} className="hover:bg-gray-800/30 transition">
                    <td className="py-3">
                      <div className="font-semibold text-gray-200">{part.part_name}</div>
                      <div className="text-[11px] text-gray-500">{part.part_id}</div>
                    </td>
                    <td className="py-3 text-gray-400">{part.category}</td>
                    <td className="py-3 font-bold text-red-400">{part.current_stock} units</td>
                    <td className="py-3 text-gray-300">{part.reorder_point} units</td>
                    <td className="py-3">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                        part.criticality_level === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                        'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                      }`}>
                        {part.criticality_level}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Supplier Scorecard */}
        <div className="p-5 rounded-2xl bg-[#111827] border border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold text-white">Supplier Performance</h2>
              <p className="text-xs text-gray-400">Lead times and reliability ratings</p>
            </div>
            <Truck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="space-y-3">
            {(data?.supplier_scorecard || []).slice(0, 4).map((supp) => (
              <div key={supp.supplier_id} className="p-3 rounded-xl bg-gray-800/40 border border-gray-700/40 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-xs text-gray-200">{supp.name}</div>
                  <div className="text-[10px] text-gray-400 mt-0.5">
                    Lead time: <span className="text-cyan-400 font-semibold">{supp.lead_time_days} days</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-xs font-bold text-emerald-400">★ {supp.rating}</div>
                  <div className="text-[10px] text-gray-500">{supp.on_time_delivery_rate}% On-Time</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

