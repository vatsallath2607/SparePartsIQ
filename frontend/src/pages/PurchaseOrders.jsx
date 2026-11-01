import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  FileText,
  Plus,
  Truck,
  CheckCircle2,
  Calendar,
  DollarSign,
  PackageCheck,
  X
} from 'lucide-react';

export default function PurchaseOrders() {
  const { user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [showAddModal, setShowAddModal] = useState(false);

  // New PO Form
  const [formData, setFormData] = useState({
    part_id: 'PRT-BRG-1001',
    part_name: 'High-Precision Angular Contact Bearing (7210-B)',
    supplier_id: 'SUP-004',
    supplier_name: 'SKF Motion Technologies Partner',
    quantity: 10,
    unit_price: 285.00,
    notes: 'Urgent direct procurement'
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const q = statusFilter !== 'ALL' ? `?status_filter=${statusFilter}` : '';
      const data = await apiRequest(`/api/purchase-orders${q}`);
      setOrders(data);
    } catch (err) {
      console.error('Failed to load orders:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [statusFilter]);

  const handleCreatePO = async (e) => {
    e.preventDefault();
    try {
      await apiRequest('/api/purchase-orders', {
        method: 'POST',
        body: JSON.stringify({
          ...formData,
          quantity: parseInt(formData.quantity),
          unit_price: parseFloat(formData.unit_price)
        })
      });
      setShowAddModal(false);
      loadData();
    } catch (err) {
      alert(`Error creating PO: ${err.message}`);
    }
  };

  const handleMarkReceived = async (poId) => {
    if (!window.confirm(`Confirm receipt of Purchase Order ${poId}? This will automatically replenish inventory stock.`)) return;
    try {
      await apiRequest(`/api/purchase-orders/${poId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status: 'Received', notes: `Verified delivery received by ${user?.name}` })
      });
      alert(`Shipment received and inventory stock automatically replenished!`);
      loadData();
    } catch (err) {
      alert(`Failed to update PO: ${err.message}`);
    }
  };

  const isPurchaseManager = user?.role === 'Purchase Manager';

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
          <h1 className="text-2xl font-bold text-white tracking-tight">Purchase Orders & Procurement Pipeline</h1>
          <p className="text-xs text-gray-400 mt-1">
            Track outbound purchase orders, monitor supplier delivery milestones, and receive stock replenishments.
          </p>
        </div>

        {isPurchaseManager && (
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center space-x-2 px-3.5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-lg shadow-cyan-500/20"
          >
            <Plus className="w-4 h-4" />
            <span>Create Purchase Order</span>
          </button>
        )}
      </div>

      {/* Filter Tabs */}
      <div className="flex bg-gray-900 p-1 rounded-xl border border-gray-800 space-x-1 w-fit">
        {['ALL', 'Ordered', 'In-Transit', 'Received'].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3 py-1.5 text-xs font-medium rounded-lg transition ${
              statusFilter === st ? 'bg-cyan-500 text-gray-950 font-bold' : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* PO Table */}
      <div className="rounded-2xl bg-[#111827] border border-gray-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-900/60 text-gray-400 border-b border-gray-800">
              <tr>
                <th className="py-3 px-4 font-semibold">PO Number</th>
                <th className="py-3 px-4 font-semibold">Spare Part Item</th>
                <th className="py-3 px-4 font-semibold">Supplier</th>
                <th className="py-3 px-4 font-semibold">Quantity</th>
                <th className="py-3 px-4 font-semibold">Total Price</th>
                <th className="py-3 px-4 font-semibold">Ordered Date</th>
                <th className="py-3 px-4 font-semibold">Expected Delivery</th>
                <th className="py-3 px-4 font-semibold">Status</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {orders.length === 0 ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-gray-500">
                    No purchase orders found.
                  </td>
                </tr>
              ) : (
                orders.map((po) => {
                  const isReceived = po.status === 'Received';
                  const isInTransit = po.status === 'In-Transit';

                  return (
                    <tr key={po.po_id} className="hover:bg-gray-800/30 transition">
                      <td className="py-3.5 px-4 font-bold text-cyan-400 font-mono">{po.po_id}</td>
                      <td className="py-3.5 px-4">
                        <div className="font-semibold text-gray-200">{po.part_name}</div>
                        <div className="text-[11px] text-gray-500">{po.part_id}</div>
                      </td>
                      <td className="py-3.5 px-4 text-gray-300">{po.supplier_name}</td>
                      <td className="py-3.5 px-4 font-bold text-white">{po.quantity} units</td>
                      <td className="py-3.5 px-4 font-medium text-emerald-400">${po.total_price.toLocaleString()}</td>
                      <td className="py-3.5 px-4 text-gray-400">{po.order_date}</td>
                      <td className="py-3.5 px-4 text-gray-300 font-medium">{po.expected_delivery_date}</td>
                      <td className="py-3.5 px-4">
                        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                          isReceived ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                          isInTransit ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                          'bg-cyan-500/10 text-cyan-400 border-cyan-500/20'
                        }`}>
                          {po.status}
                        </span>
                      </td>
                      <td className="py-3.5 px-4 text-right">
                        {!isReceived && (
                          <button
                            onClick={() => handleMarkReceived(po.po_id)}
                            className="flex items-center space-x-1.5 ml-auto px-2.5 py-1 text-xs font-semibold bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-lg transition"
                          >
                            <PackageCheck className="w-3.5 h-3.5" />
                            <span>Mark Received</span>
                          </button>
                        )}
                        {isReceived && (
                          <span className="text-[11px] text-gray-500 flex items-center justify-end space-x-1">
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                            <span>Stock Updated</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Create PO Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-gray-800">
              <h3 className="text-sm font-bold text-white">Issue Direct Purchase Order</h3>
              <button onClick={() => setShowAddModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreatePO} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="text-gray-400">Part Identifier</label>
                <input
                  type="text"
                  value={formData.part_id}
                  onChange={(e) => setFormData({ ...formData, part_id: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Part Name</label>
                <input
                  type="text"
                  value={formData.part_name}
                  onChange={(e) => setFormData({ ...formData, part_name: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Supplier Name</label>
                <input
                  type="text"
                  value={formData.supplier_name}
                  onChange={(e) => setFormData({ ...formData, supplier_name: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-gray-400">Quantity</label>
                  <input
                    type="number"
                    min="1"
                    value={formData.quantity}
                    onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                    required
                  />
                </div>
                <div>
                  <label className="text-gray-400">Unit Price ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.unit_price}
                    onChange={(e) => setFormData({ ...formData, unit_price: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="text-gray-400">Procurement Notes</label>
                <input
                  type="text"
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                />
              </div>

              <div className="pt-3 flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-xs text-gray-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition"
                >
                  Issue Purchase Order
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

