import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  Boxes,
  Search,
  Filter,
  Plus,
  ArrowDownRight,
  ArrowUpRight,
  Edit2,
  Trash2,
  X,
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react';

export default function Inventory() {
  const { user } = useAuth();
  const [parts, setParts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [criticalityFilter, setCriticalityFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('all'); // all, low, overstocked

  // Modals
  const [showAddModal, setShowAddModal] = useState(false);
  const [showTxModal, setShowTxModal] = useState(false);
  const [selectedPart, setSelectedPart] = useState(null);
  const [txType, setTxType] = useState('IN');
  const [txQuantity, setTxQuantity] = useState(1);
  const [txReason, setTxReason] = useState('Routine restock');

  // New Part Form
  const [formData, setFormData] = useState({
    part_id: '',
    part_name: '',
    category: 'Mechanical & Bearings',
    description: '',
    manufacturer: '',
    supplier_id: 'SUP-001',
    unit_cost: 150.0,
    supplier_lead_time: 14,
    machine_compatibility: 'MCH-CNC-001',
    criticality_level: 'High',
    warehouse_location: 'Aisle 1, Rack A-01',
    min_stock: 5,
    max_stock: 30,
    reorder_point: 10,
    current_stock: 12
  });

  const loadParts = async () => {
    setLoading(true);
    try {
      let query = [];
      if (search) query.push(`search=${encodeURIComponent(search)}`);
      if (categoryFilter) query.push(`category=${encodeURIComponent(categoryFilter)}`);
      if (criticalityFilter) query.push(`criticality=${encodeURIComponent(criticalityFilter)}`);
      if (statusFilter === 'low') query.push(`stock_status=low`);
      if (statusFilter === 'overstocked') query.push(`stock_status=overstocked`);

      const qStr = query.length ? `?${query.join('&')}` : '';
      const data = await apiRequest(`/api/inventory${qStr}`);
      setParts(data);
    } catch (err) {
      console.error('Failed to load parts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadParts();
  }, [categoryFilter, criticalityFilter, statusFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadParts();
  };

  const handleAddPart = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        unit_cost: parseFloat(formData.unit_cost),
        supplier_lead_time: parseInt(formData.supplier_lead_time),
        min_stock: parseInt(formData.min_stock),
        max_stock: parseInt(formData.max_stock),
        reorder_point: parseInt(formData.reorder_point),
        current_stock: parseInt(formData.current_stock),
        machine_compatibility: formData.machine_compatibility.split(',').map(s => s.trim())
      };
      await apiRequest('/api/inventory', {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      setShowAddModal(false);
      loadParts();
    } catch (err) {
      alert(`Error creating part: ${err.message}`);
    }
  };

  const handleStockTx = async (e) => {
    e.preventDefault();
    if (!selectedPart) return;
    try {
      await apiRequest(`/api/inventory/${selectedPart.part_id}/transaction`, {
        method: 'POST',
        body: JSON.stringify({
          transaction_type: txType,
          quantity: parseInt(txQuantity),
          reason: txReason
        })
      });
      setShowTxModal(false);
      loadParts();
    } catch (err) {
      alert(`Transaction failed: ${err.message}`);
    }
  };

  const handleDelete = async (partId) => {
    if (!window.confirm(`Are you sure you want to delete spare part ${partId}?`)) return;
    try {
      await apiRequest(`/api/inventory/${partId}`, { method: 'DELETE' });
      loadParts();
    } catch (err) {
      alert(`Error deleting part: ${err.message}`);
    }
  };

  const isInventoryManager = user?.role === 'Inventory Manager';

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Spare Parts Inventory Management</h1>
          <p className="text-xs text-gray-400 mt-1">
            Complete industrial asset catalog, warehouse locations, lead times, and real-time inventory adjustments.
          </p>
        </div>

        {isInventoryManager && (
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center space-x-2 px-3.5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-lg shadow-cyan-500/20"
          >
            <Plus className="w-4 h-4" />
            <span>Add Spare Part</span>
          </button>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-[#111827] border border-gray-800 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="flex-1 relative">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search by part ID, component name, manufacturer..."
            className="w-full pl-9 pr-4 py-2 bg-gray-900 border border-gray-700/80 rounded-xl text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition"
          />
        </form>

        {/* Filters */}
        <div className="flex items-center space-x-3 overflow-x-auto pb-1 md:pb-0">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-gray-900 border border-gray-700/80 text-xs text-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Categories</option>
            <option value="Mechanical & Bearings">Mechanical & Bearings</option>
            <option value="Hydraulics & Pneumatics">Hydraulics & Pneumatics</option>
            <option value="Electrical & Automation">Electrical & Automation</option>
            <option value="Thermal & HVAC">Thermal & HVAC</option>
            <option value="Valves & Piping">Valves & Piping</option>
          </select>

          <select
            value={criticalityFilter}
            onChange={(e) => setCriticalityFilter(e.target.value)}
            className="bg-gray-900 border border-gray-700/80 text-xs text-gray-300 rounded-xl px-3 py-2 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Criticalities</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          {/* Quick status tabs */}
          <div className="flex bg-gray-900 p-1 rounded-xl border border-gray-700/80">
            {['all', 'low', 'overstocked'].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1 text-[11px] font-medium rounded-lg capitalize transition ${
                  statusFilter === st ? 'bg-cyan-500 text-gray-950 font-bold' : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                {st}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Parts Table */}
      <div className="rounded-2xl bg-[#111827] border border-gray-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-900/60 text-gray-400 border-b border-gray-800">
              <tr>
                <th className="py-3.5 px-4 font-semibold">Part / Specs</th>
                <th className="py-3.5 px-4 font-semibold">Category</th>
                <th className="py-3.5 px-4 font-semibold">Current Stock</th>
                <th className="py-3.5 px-4 font-semibold">ROP / Bounds</th>
                <th className="py-3.5 px-4 font-semibold">Unit Cost</th>
                <th className="py-3.5 px-4 font-semibold">Lead Time</th>
                <th className="py-3.5 px-4 font-semibold">Location</th>
                <th className="py-3.5 px-4 font-semibold">Criticality</th>
                <th className="py-3.5 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {loading ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-gray-500">
                    Loading inventory data...
                  </td>
                </tr>
              ) : parts.length === 0 ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-gray-500">
                    No spare parts found matching the selected criteria.
                  </td>
                </tr>
              ) : (
                parts.map((p) => {
                  const isLow = p.current_stock <= p.reorder_point;
                  const isOver = p.current_stock > p.max_stock;

                  return (
                    <tr key={p.part_id} className="hover:bg-gray-800/30 transition">
                      <td className="py-3 px-4">
                        <div className="font-semibold text-gray-200">{p.part_name}</div>
                        <div className="text-[11px] text-gray-500 flex items-center space-x-2 mt-0.5">
                          <span>{p.part_id}</span>
                          <span>•</span>
                          <span>{p.manufacturer}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-400">{p.category}</td>
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2">
                          <span className={`font-bold ${isLow ? 'text-red-400' : isOver ? 'text-purple-400' : 'text-gray-200'}`}>
                            {p.current_stock}
                          </span>
                          {isLow && (
                            <span className="text-[10px] bg-red-500/10 text-red-400 border border-red-500/20 px-1.5 py-0.2 rounded font-semibold">
                              LOW
                            </span>
                          )}
                          {isOver && (
                            <span className="text-[10px] bg-purple-500/10 text-purple-400 border border-purple-500/20 px-1.5 py-0.2 rounded font-semibold">
                              OVER
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-3 px-4 text-gray-300">
                        <div>ROP: <span className="font-semibold">{p.reorder_point}</span></div>
                        <div className="text-[10px] text-gray-500">[{p.min_stock} - {p.max_stock}]</div>
                      </td>
                      <td className="py-3 px-4 font-medium text-gray-200">${p.unit_cost.toFixed(2)}</td>
                      <td className="py-3 px-4 text-gray-400">{p.supplier_lead_time} days</td>
                      <td className="py-3 px-4 text-gray-400 text-[11px]">{p.warehouse_location}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                          p.criticality_level === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                          p.criticality_level === 'High' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                          p.criticality_level === 'Medium' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' :
                          'bg-gray-500/10 text-gray-400 border border-gray-500/20'
                        }`}>
                          {p.criticality_level}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <div className="flex items-center justify-end space-x-2">
                          <button
                            onClick={() => {
                              setSelectedPart(p);
                              setShowTxModal(true);
                            }}
                            className="p-1.5 rounded-lg bg-gray-800 hover:bg-cyan-500/20 text-gray-300 hover:text-cyan-400 transition"
                            title="Adjust Stock (In/Out)"
                          >
                            <ArrowDownRight className="w-3.5 h-3.5" />
                          </button>
                          {isInventoryManager && (
                            <button
                              onClick={() => handleDelete(p.part_id)}
                              className="p-1.5 rounded-lg bg-gray-800 hover:bg-red-500/20 text-gray-400 hover:text-red-400 transition"
                              title="Delete Part"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Stock Transaction Modal */}
      {showTxModal && selectedPart && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-gray-800">
              <h3 className="text-sm font-bold text-white">Record Stock Movement</h3>
              <button onClick={() => setShowTxModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="py-3 text-xs text-gray-300">
              Part: <span className="font-semibold text-white">{selectedPart.part_name}</span> ({selectedPart.part_id})
              <div className="text-gray-400 mt-1">Current Stock: <span className="font-bold text-cyan-400">{selectedPart.current_stock}</span> units</div>
            </div>

            <form onSubmit={handleStockTx} className="space-y-4">
              <div>
                <label className="text-xs text-gray-400">Movement Type</label>
                <div className="grid grid-cols-3 gap-2 mt-1">
                  {['IN', 'OUT', 'ADJUSTMENT'].map((type) => (
                    <button
                      type="button"
                      key={type}
                      onClick={() => setTxType(type)}
                      className={`py-2 text-xs font-semibold rounded-xl border transition ${
                        txType === type
                          ? 'bg-cyan-500 text-gray-950 border-cyan-400'
                          : 'bg-gray-800 text-gray-300 border-gray-700 hover:bg-gray-750'
                      }`}
                    >
                      {type === 'IN' ? 'Restock (IN)' : type === 'OUT' ? 'Consume (OUT)' : 'Adjust'}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs text-gray-400">Quantity</label>
                <input
                  type="number"
                  min="1"
                  value={txQuantity}
                  onChange={(e) => setTxQuantity(e.target.value)}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-500"
                  required
                />
              </div>

              <div>
                <label className="text-xs text-gray-400">Reason / Reference</label>
                <input
                  type="text"
                  value={txReason}
                  onChange={(e) => setTxReason(e.target.value)}
                  placeholder="e.g., Routine replenishment, MCH-CNC-001 Spindle service"
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-500"
                  required
                />
              </div>

              <div className="pt-2 flex items-center justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowTxModal(false)}
                  className="px-4 py-2 text-xs text-gray-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition"
                >
                  Confirm Movement
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Part Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-2xl bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-4 border-b border-gray-800">
              <h3 className="text-sm font-bold text-white">Register New Spare Part</h3>
              <button onClick={() => setShowAddModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleAddPart} className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="text-gray-400">Part Identifier</label>
                <input
                  type="text"
                  value={formData.part_id}
                  onChange={(e) => setFormData({ ...formData, part_id: e.target.value })}
                  placeholder="e.g., PRT-SEN-9901 (or auto-generate)"
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white focus:border-cyan-500"
                />
              </div>
              <div>
                <label className="text-gray-400">Part Name *</label>
                <input
                  type="text"
                  value={formData.part_name}
                  onChange={(e) => setFormData({ ...formData, part_name: e.target.value })}
                  placeholder="Full component designation"
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white focus:border-cyan-500"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white focus:border-cyan-500"
                >
                  <option value="Mechanical & Bearings">Mechanical & Bearings</option>
                  <option value="Hydraulics & Pneumatics">Hydraulics & Pneumatics</option>
                  <option value="Electrical & Automation">Electrical & Automation</option>
                  <option value="Thermal & HVAC">Thermal & HVAC</option>
                  <option value="Valves & Piping">Valves & Piping</option>
                </select>
              </div>

              <div>
                <label className="text-gray-400">Criticality</label>
                <select
                  value={formData.criticality_level}
                  onChange={(e) => setFormData({ ...formData, criticality_level: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white focus:border-cyan-500"
                >
                  <option value="Critical">Critical</option>
                  <option value="High">High</option>
                  <option value="Medium">Medium</option>
                  <option value="Low">Low</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="text-gray-400">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={2}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white focus:border-cyan-500"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Manufacturer</label>
                <input
                  type="text"
                  value={formData.manufacturer}
                  onChange={(e) => setFormData({ ...formData, manufacturer: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Warehouse Location</label>
                <input
                  type="text"
                  value={formData.warehouse_location}
                  onChange={(e) => setFormData({ ...formData, warehouse_location: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Unit Cost ($)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.unit_cost}
                  onChange={(e) => setFormData({ ...formData, unit_cost: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Supplier Lead Time (Days)</label>
                <input
                  type="number"
                  value={formData.supplier_lead_time}
                  onChange={(e) => setFormData({ ...formData, supplier_lead_time: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Current Stock</label>
                <input
                  type="number"
                  value={formData.current_stock}
                  onChange={(e) => setFormData({ ...formData, current_stock: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div>
                <label className="text-gray-400">Reorder Point (ROP)</label>
                <input
                  type="number"
                  value={formData.reorder_point}
                  onChange={(e) => setFormData({ ...formData, reorder_point: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div className="md:col-span-2 pt-4 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 text-xs text-gray-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition"
                >
                  Register Component
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

