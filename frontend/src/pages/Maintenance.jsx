import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { useAuth } from '../context/AuthContext';
import {
  Wrench,
  AlertTriangle,
  Calendar,
  CheckCircle,
  Plus,
  Clock,
  Cpu,
  Layers,
  X
} from 'lucide-react';

export default function Maintenance() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('schedules'); // 'schedules', 'at_risk', 'machines'
  const [schedules, setSchedules] = useState([]);
  const [atRisk, setAtRisk] = useState([]);
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(true);

  // New Schedule Modal
  const [showAddModal, setShowAddModal] = useState(false);
  const [formData, setFormData] = useState({
    machine_id: 'MCH-CNC-001',
    machine_name: '5-Axis CNC Milling Center',
    maintenance_type: 'Preventive Spindle Bearing Replacement',
    scheduled_date: '2026-11-20',
    estimated_hours: 8,
    assigned_technician: 'Rajesh Kumar',
    priority: 'High',
    required_parts_raw: 'PRT-BRG-1001:2, PRT-SRV-5005:1'
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const [sRes, aRes, mRes] = await Promise.all([
        apiRequest('/api/maintenance/schedules'),
        apiRequest('/api/maintenance/at-risk'),
        apiRequest('/api/maintenance/machines')
      ]);
      setSchedules(sRes);
      setAtRisk(aRes);
      setMachines(mRes);
    } catch (err) {
      console.error('Failed to load maintenance data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateSchedule = async (e) => {
    e.preventDefault();
    try {
      const reqParts = formData.required_parts_raw.split(',').map(item => {
        const [pid, qty] = item.split(':').map(s => s.trim());
        return {
          part_id: pid,
          part_name: pid,
          quantity_required: parseInt(qty) || 1
        };
      });

      await apiRequest('/api/maintenance/schedules', {
        method: 'POST',
        body: JSON.stringify({
          machine_id: formData.machine_id,
          machine_name: formData.machine_name,
          maintenance_type: formData.maintenance_type,
          scheduled_date: formData.scheduled_date,
          estimated_hours: parseInt(formData.estimated_hours),
          assigned_technician: formData.assigned_technician,
          priority: formData.priority,
          required_parts: reqParts
        })
      });

      setShowAddModal(false);
      loadData();
    } catch (err) {
      alert(`Error scheduling maintenance: ${err.message}`);
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
          <h1 className="text-2xl font-bold text-white tracking-tight">Maintenance-Based Inventory Planning</h1>
          <p className="text-xs text-gray-400 mt-1">
            Synchronize scheduled equipment overhauls with spare parts stock availability to eliminate maintenance downtime.
          </p>
        </div>

        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center space-x-2 px-3.5 py-2 text-xs font-semibold bg-cyan-500 hover:bg-cyan-400 text-gray-950 rounded-xl transition shadow-lg shadow-cyan-500/20"
        >
          <Plus className="w-4 h-4" />
          <span>Schedule Maintenance</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex bg-gray-900 p-1.5 rounded-2xl border border-gray-800 space-x-2 w-fit">
        <button
          onClick={() => setActiveTab('schedules')}
          className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-xl transition ${
            activeTab === 'schedules' ? 'bg-cyan-500 text-gray-950 font-bold' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          <Calendar className="w-4 h-4" />
          <span>Scheduled Work Orders ({schedules.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('at_risk')}
          className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-xl transition ${
            activeTab === 'at_risk' ? 'bg-red-500 text-white font-bold' : 'text-red-400 hover:bg-red-500/10'
          }`}
        >
          <AlertTriangle className="w-4 h-4" />
          <span>At-Risk Activities ({atRisk.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('machines')}
          className={`flex items-center space-x-2 px-4 py-2 text-xs font-medium rounded-xl transition ${
            activeTab === 'machines' ? 'bg-cyan-500 text-gray-950 font-bold' : 'text-gray-400 hover:text-gray-200'
          }`}
        >
          <Cpu className="w-4 h-4" />
          <span>Machine Directory ({machines.length})</span>
        </button>
      </div>

      {/* Tab Content: Schedules */}
      {activeTab === 'schedules' && (
        <div className="rounded-2xl bg-[#111827] border border-gray-800 overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-gray-900/60 text-gray-400 border-b border-gray-800">
                <tr>
                  <th className="py-3 px-4 font-semibold">Work Order / Machine</th>
                  <th className="py-3 px-4 font-semibold">Maintenance Type</th>
                  <th className="py-3 px-4 font-semibold">Scheduled Date</th>
                  <th className="py-3 px-4 font-semibold">Est. Duration</th>
                  <th className="py-3 px-4 font-semibold">Assigned Lead</th>
                  <th className="py-3 px-4 font-semibold">Required Spare Parts</th>
                  <th className="py-3 px-4 font-semibold">Priority</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/60">
                {schedules.map((sch) => (
                  <tr key={sch.schedule_id} className="hover:bg-gray-800/30 transition">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-gray-200">{sch.machine_name}</div>
                      <div className="text-[11px] text-gray-500">{sch.schedule_id} • {sch.machine_id}</div>
                    </td>
                    <td className="py-3.5 px-4 text-gray-300 font-medium">{sch.maintenance_type}</td>
                    <td className="py-3.5 px-4 text-cyan-400 font-bold">{sch.scheduled_date}</td>
                    <td className="py-3.5 px-4 text-gray-400">{sch.estimated_hours} hours</td>
                    <td className="py-3.5 px-4 text-gray-300">{sch.assigned_technician}</td>
                    <td className="py-3.5 px-4">
                      <div className="space-y-1">
                        {(sch.required_parts || []).map((rp, idx) => (
                          <div key={idx} className="text-[11px] text-gray-400 flex items-center space-x-1">
                            <span className="text-gray-200">• {rp.part_name || rp.part_id}:</span>
                            <span className="font-semibold text-cyan-400">({rp.quantity_required}x)</span>
                          </div>
                        ))}
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                        sch.priority === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                        sch.priority === 'High' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                        'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                      }`}>
                        {sch.priority}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Tab Content: At Risk */}
      {activeTab === 'at_risk' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-xs text-red-300">
            <strong>Maintenance Interruption Warning:</strong> The work orders below are missing required spare parts in current inventory. Without immediate replenishment, maintenance schedules will be delayed.
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {atRisk.length === 0 ? (
              <div className="col-span-2 p-12 text-center text-xs text-gray-500 bg-[#111827] rounded-2xl border border-gray-800">
                All scheduled maintenance activities currently have sufficient parts in stock.
              </div>
            ) : (
              atRisk.map((item) => (
                <div key={item.schedule_id} className="p-5 rounded-2xl bg-[#111827] border border-red-500/30">
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[10px] text-red-400 font-bold uppercase tracking-wider">DEFICIT ALERT</span>
                      <h3 className="text-sm font-bold text-white mt-0.5">{item.machine_name}</h3>
                      <div className="text-xs text-gray-400">{item.maintenance_type}</div>
                    </div>
                    <span className="text-xs font-bold text-red-400">{item.scheduled_date}</span>
                  </div>

                  <div className="mt-4 pt-3 border-t border-gray-800">
                    <span className="text-xs font-semibold text-gray-300">Deficit Components:</span>
                    <div className="mt-2 space-y-2">
                      {item.missing_parts.map((mp, i) => (
                        <div key={i} className="p-2.5 rounded-xl bg-gray-900/60 border border-gray-800 flex items-center justify-between text-xs">
                          <div>
                            <div className="font-medium text-gray-200">{mp.part_name}</div>
                            <div className="text-[10px] text-gray-500">Lead time: {mp.supplier_lead_time} days</div>
                          </div>
                          <div className="text-right">
                            <div className="text-red-400 font-bold">Shortage: -{mp.shortage} units</div>
                            <div className="text-[10px] text-gray-400">Stock: {mp.current_stock} / Req: {mp.quantity_required}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab Content: Machines */}
      {activeTab === 'machines' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {machines.map((m) => (
            <div key={m.machine_id} className="p-5 rounded-2xl bg-[#111827] border border-gray-800">
              <div className="flex items-start justify-between">
                <span className="text-[10px] font-mono text-cyan-400">{m.machine_id}</span>
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold ${
                  m.criticality === 'Critical' ? 'bg-red-500/10 text-red-400 border border-red-500/20' :
                  m.criticality === 'High' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                  'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                }`}>
                  {m.criticality}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white mt-2">{m.name}</h3>
              <p className="text-xs text-gray-400 mt-1">{m.location}</p>
            </div>
          ))}
        </div>
      )}

      {/* Schedule Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-lg bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-gray-800">
              <h3 className="text-sm font-bold text-white">Register Scheduled Maintenance</h3>
              <button onClick={() => setShowAddModal(false)} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateSchedule} className="mt-4 space-y-3 text-xs">
              <div>
                <label className="text-gray-400">Machine Target</label>
                <select
                  value={formData.machine_id}
                  onChange={(e) => {
                    const m = machines.find(x => x.machine_id === e.target.value);
                    setFormData({ ...formData, machine_id: e.target.value, machine_name: m ? m.name : '' });
                  }}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                >
                  {machines.map(m => (
                    <option key={m.machine_id} value={m.machine_id}>{m.name} ({m.machine_id})</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="text-gray-400">Maintenance Activity</label>
                <input
                  type="text"
                  value={formData.maintenance_type}
                  onChange={(e) => setFormData({ ...formData, maintenance_type: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-gray-400">Scheduled Date</label>
                  <input
                    type="date"
                    value={formData.scheduled_date}
                    onChange={(e) => setFormData({ ...formData, scheduled_date: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                    required
                  />
                </div>
                <div>
                  <label className="text-gray-400">Estimated Duration (Hrs)</label>
                  <input
                    type="number"
                    value={formData.estimated_hours}
                    onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                    required
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-gray-400">Assigned Technician</label>
                  <input
                    type="text"
                    value={formData.assigned_technician}
                    onChange={(e) => setFormData({ ...formData, assigned_technician: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                    required
                  />
                </div>
                <div>
                  <label className="text-gray-400">Priority</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white"
                  >
                    <option value="Critical">Critical</option>
                    <option value="High">High</option>
                    <option value="Medium">Medium</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-gray-400">Required Spare Parts (format: PartID:Qty, PartID:Qty)</label>
                <input
                  type="text"
                  value={formData.required_parts_raw}
                  onChange={(e) => setFormData({ ...formData, required_parts_raw: e.target.value })}
                  className="w-full mt-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-xl text-white font-mono"
                  required
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
                  Save Schedule
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

