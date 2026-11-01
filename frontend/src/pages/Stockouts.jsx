import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import {
  AlertOctagon,
  AlertTriangle,
  CheckCircle2,
  Clock,
  ShieldAlert,
  ArrowRight
} from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Stockouts() {
  const [risks, setRisks] = useState([]);
  const [summary, setSummary] = useState(null);
  const [filterLevel, setFilterLevel] = useState('ALL');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [rData, sData] = await Promise.all([
          apiRequest('/api/stockouts'),
          apiRequest('/api/stockouts/summary')
        ]);
        setRisks(rData);
        setSummary(sData);
      } catch (err) {
        console.error('Failed to load stockout risks:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const filteredRisks = filterLevel === 'ALL'
    ? risks
    : risks.filter(r => r.risk_level === filterLevel);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Stockout Risk Prediction Matrix</h1>
          <p className="text-xs text-gray-400 mt-1">
            Dynamic risk assessment factoring lead times, maintenance schedules, current inventory, and consumption rates.
          </p>
        </div>

        <Link
          to="/reorder"
          className="flex items-center space-x-2 px-3.5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-lg shadow-cyan-500/20"
        >
          <span>Open Reorder Proposals</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Summary Risk Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <button
          onClick={() => setFilterLevel(filterLevel === 'Critical' ? 'ALL' : 'Critical')}
          className={`p-4 rounded-2xl border text-left transition ${
            filterLevel === 'Critical'
              ? 'bg-red-500/20 border-red-500 ring-2 ring-red-500/30'
              : 'bg-[#111827] border-red-500/20 hover:border-red-500/40'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-red-400 uppercase tracking-wider">Critical Risk</span>
            <AlertOctagon className="w-5 h-5 text-red-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">{summary?.Critical || 0}</div>
          <p className="text-[11px] text-gray-400 mt-1">Coverage &lt; Supplier Lead Time</p>
        </button>

        <button
          onClick={() => setFilterLevel(filterLevel === 'High' ? 'ALL' : 'High')}
          className={`p-4 rounded-2xl border text-left transition ${
            filterLevel === 'High'
              ? 'bg-amber-500/20 border-amber-500 ring-2 ring-amber-500/30'
              : 'bg-[#111827] border-amber-500/20 hover:border-amber-500/40'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">High Risk</span>
            <AlertTriangle className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">{summary?.High || 0}</div>
          <p className="text-[11px] text-gray-400 mt-1">Coverage &lt; 1.5x Lead Time</p>
        </button>

        <button
          onClick={() => setFilterLevel(filterLevel === 'Medium' ? 'ALL' : 'Medium')}
          className={`p-4 rounded-2xl border text-left transition ${
            filterLevel === 'Medium'
              ? 'bg-blue-500/20 border-blue-500 ring-2 ring-blue-500/30'
              : 'bg-[#111827] border-blue-500/20 hover:border-blue-500/40'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-blue-400 uppercase tracking-wider">Medium Risk</span>
            <Clock className="w-5 h-5 text-blue-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">{summary?.Medium || 0}</div>
          <p className="text-[11px] text-gray-400 mt-1">Buffer adequate, monitor lead times</p>
        </button>

        <button
          onClick={() => setFilterLevel(filterLevel === 'Low' ? 'ALL' : 'Low')}
          className={`p-4 rounded-2xl border text-left transition ${
            filterLevel === 'Low'
              ? 'bg-emerald-500/20 border-emerald-500 ring-2 ring-emerald-500/30'
              : 'bg-[#111827] border-emerald-500/20 hover:border-emerald-500/40'
          }`}
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Low Risk</span>
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white mt-2">{summary?.Low || 0}</div>
          <p className="text-[11px] text-gray-400 mt-1">Sufficient inventory runway</p>
        </button>
      </div>

      {/* Risk Table */}
      <div className="rounded-2xl bg-[#111827] border border-gray-800 overflow-hidden shadow-sm">
        <div className="p-4 border-b border-gray-800 flex items-center justify-between">
          <div className="text-xs font-semibold text-gray-300">
            Showing {filteredRisks.length} of {risks.length} components
          </div>
          {filterLevel !== 'ALL' && (
            <button
              onClick={() => setFilterLevel('ALL')}
              className="text-xs text-cyan-400 hover:underline"
            >
              Clear Filter
            </button>
          )}
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-900/60 text-gray-400 border-b border-gray-800">
              <tr>
                <th className="py-3 px-4 font-semibold">Spare Part Identifier</th>
                <th className="py-3 px-4 font-semibold">Current Stock</th>
                <th className="py-3 px-4 font-semibold">Incoming PO</th>
                <th className="py-3 px-4 font-semibold">Lead Time</th>
                <th className="py-3 px-4 font-semibold">Days of Coverage</th>
                <th className="py-3 px-4 font-semibold">Risk Classification</th>
                <th className="py-3 px-4 font-semibold">Diagnostic Reasoning</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {filteredRisks.map((r) => {
                const badgeThemes = {
                  Critical: 'bg-red-500/10 text-red-400 border-red-500/20',
                  High: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
                  Medium: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
                  Low: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                };

                return (
                  <tr key={r.part_id} className="hover:bg-gray-800/30 transition">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-gray-200">{r.part_name}</div>
                      <div className="text-[11px] text-gray-500">{r.part_id} • {r.category}</div>
                    </td>
                    <td className="py-3.5 px-4 font-bold text-white">{r.current_stock}</td>
                    <td className="py-3.5 px-4 text-cyan-400 font-medium">+{r.incoming_po_qty}</td>
                    <td className="py-3.5 px-4 text-gray-300">{r.supplier_lead_time} days</td>
                    <td className="py-3.5 px-4">
                      <span className={`font-bold ${
                        r.days_of_supply <= r.supplier_lead_time ? 'text-red-400' : 'text-gray-200'
                      }`}>
                        {r.days_of_supply} days
                      </span>
                    </td>
                    <td className="py-3.5 px-4">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${badgeThemes[r.risk_level]}`}>
                          {r.risk_level.toUpperCase()}
                        </span>
                        <span className="text-[11px] text-gray-400 font-mono">
                          ({(r.risk_score * 100).toFixed(0)}%)
                        </span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4 max-w-md text-gray-400 text-[11px] leading-relaxed">
                      {r.risk_reason}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

