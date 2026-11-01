import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  ShoppingCart,
  CheckCircle,
  XCircle,
  Truck,
  DollarSign,
  Calendar,
  AlertCircle,
  ShieldCheck,
  FileCheck
} from 'lucide-react';

export default function Reorder() {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState([]);
  const [filter, setFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const q = filter !== 'ALL' ? `?status_filter=${filter}` : '';
      const data = await apiRequest(`/api/reorders${q}`);
      setRecommendations(data);
    } catch (err) {
      console.error('Failed to load recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [filter]);

  const isPurchaseManager = user?.role === 'Purchase Manager';

  const handleDecision = async (id, action) => {
    try {
      const notes = prompt(`Enter notes for ${action.toLowerCase()} (optional):`, `Manual ${action} by ${user?.name}`);
      if (notes === null) return; // user cancelled prompt

      const endpoint = `/api/reorders/${id}/${action.toLowerCase()}`;
      const res = await apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify({ decision_notes: notes })
      });

      setActionSuccess(`Recommendation ${action.toLowerCase()}ed successfully! ${res.purchase_order ? `Created PO #${res.purchase_order.po_id}` : ''}`);
      setTimeout(() => setActionSuccess(''), 6000);
      loadData();
    } catch (err) {
      alert(`Action failed: ${err.message}`);
    }
  };

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
          <h1 className="text-2xl font-bold text-white tracking-tight">Intelligent Reorder Engine</h1>
          <p className="text-xs text-gray-400 mt-1">
            Reorder calculations powered by lead-time demand forecasting, safety stock buffer, and scheduled maintenance.
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="flex bg-gray-900 p-1 rounded-xl border border-gray-800">
          {['ALL', 'Pending', 'Approved', 'Rejected'].map((st) => (
            <button
              key={st}
              onClick={() => setFilter(st)}
              className={`px-3 py-1.5 text-xs font-medium rounded-lg transition ${
                filter === st ? 'bg-cyan-500 text-gray-950 font-bold' : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {actionSuccess && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center space-x-2">
          <CheckCircle className="w-4 h-4 shrink-0" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Role Permission Notice */}
      {!isPurchaseManager && (
        <div className="p-3.5 rounded-xl bg-gray-800/40 border border-gray-700/50 text-xs text-gray-300 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-cyan-400" />
            <span>Viewing as <strong>{user?.role}</strong>. Approval & PO dispatch permissions belong to the <strong>Purchase Manager</strong>.</span>
          </div>
          <span className="text-[11px] text-cyan-400 font-semibold cursor-pointer" onClick={() => alert("Use the role switcher in the top right to switch to Purchase Manager.")}>
            Switch to Purchase Manager
          </span>
        </div>
      )}

      {/* Recommendation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.length === 0 ? (
          <div className="col-span-2 p-12 text-center text-xs text-gray-500 rounded-2xl bg-[#111827] border border-gray-800">
            No reorder recommendations matching the selected status.
          </div>
        ) : (
          recommendations.map((rec) => {
            const isPending = rec.status === 'Pending';
            const isApproved = rec.status === 'Approved';

            return (
              <div
                key={rec.recommendation_id}
                className={`p-5 rounded-2xl bg-[#111827] border transition ${
                  isPending
                    ? 'border-cyan-500/30 shadow-lg shadow-cyan-950/10'
                    : isApproved
                    ? 'border-emerald-500/20 bg-emerald-950/5'
                    : 'border-gray-800 opacity-70'
                }`}
              >
                {/* Card Header */}
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider">{rec.part_id}</span>
                    <h3 className="text-sm font-bold text-white mt-0.5">{rec.part_name}</h3>
                    <span className="text-[11px] text-gray-400">{rec.category}</span>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                    isPending ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' :
                    isApproved ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                    'bg-red-500/10 text-red-400 border-red-500/20'
                  }`}>
                    {rec.status}
                  </span>
                </div>

                {/* Quantitative Details Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 py-4 my-3 border-y border-gray-800/80 text-xs">
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase">Current Stock</span>
                    <div className="font-bold text-gray-200 mt-0.5">{rec.current_stock} units</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase">Recommended Qty</span>
                    <div className="font-bold text-cyan-400 mt-0.5">{rec.recommended_quantity} units</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase">Unit Cost</span>
                    <div className="font-bold text-gray-200 mt-0.5">${rec.unit_cost.toFixed(2)}</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase">Estimated Total</span>
                    <div className="font-bold text-emerald-400 mt-0.5">${rec.estimated_procurement_cost.toLocaleString()}</div>
                  </div>
                </div>

                {/* Supplier & Lead Time */}
                <div className="text-xs text-gray-300 space-y-1">
                  <div className="flex items-center space-x-2">
                    <Truck className="w-3.5 h-3.5 text-gray-400" />
                    <span>Supplier: <strong className="text-white">{rec.supplier_name}</strong></span>
                    <span className="text-[11px] text-emerald-400">★ {rec.supplier_rating}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <Calendar className="w-3.5 h-3.5 text-gray-400" />
                    <span>Target Order Date: <strong className="text-gray-200">{rec.recommended_reorder_date}</strong> ({rec.supplier_lead_time}d lead time)</span>
                  </div>
                </div>

                {/* Analytical Reason */}
                <div className="mt-3 p-2.5 rounded-xl bg-gray-900/60 border border-gray-800 text-[11px] text-gray-400">
                  <strong className="text-gray-300">Algorithm Logic: </strong>
                  {rec.reason}
                </div>

                {/* Purchase Manager Actions */}
                {isPending && isPurchaseManager && (
                  <div className="mt-4 pt-3 border-t border-gray-800 flex items-center justify-end space-x-2">
                    <button
                      onClick={() => handleDecision(rec.recommendation_id, 'REJECT')}
                      className="flex items-center space-x-1.5 px-3 py-1.5 text-xs text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject</span>
                    </button>
                    <button
                      onClick={() => handleDecision(rec.recommendation_id, 'APPROVE')}
                      className="flex items-center space-x-1.5 px-4 py-1.5 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-md shadow-cyan-500/20"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Approve & Dispatch PO</span>
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

