import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import { Truck, Star, Phone, Mail, MapPin, Clock, ShieldCheck } from 'lucide-react';

export default function Suppliers() {
  const [suppliers, setSuppliers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSuppliers() {
      try {
        const data = await apiRequest('/api/suppliers');
        setSuppliers(data);
      } catch (err) {
        console.error('Failed to load suppliers:', err);
      } finally {
        setLoading(false);
      }
    }
    loadSuppliers();
  }, []);

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
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Industrial Suppliers Intelligence</h1>
        <p className="text-xs text-gray-400 mt-1">
          Monitor vendor fulfillment lead times, reliability performance ratings, and verified procurement channels.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {suppliers.map((supp) => (
          <div key={supp.supplier_id} className="p-6 rounded-2xl bg-[#111827] border border-gray-800 shadow-sm relative">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] font-mono text-cyan-400 uppercase tracking-wider">{supp.supplier_id}</span>
                <h3 className="text-sm font-bold text-white mt-1">{supp.name}</h3>
                <span className="text-xs text-gray-400">{supp.contact_person}</span>
              </div>
              <div className="flex items-center space-x-1 px-2.5 py-1 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 font-bold text-xs">
                <Star className="w-3.5 h-3.5 fill-current" />
                <span>{supp.rating}</span>
              </div>
            </div>

            <div className="mt-5 pt-4 border-t border-gray-800/80 space-y-2.5 text-xs text-gray-300">
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-cyan-400" />
                <span>Standard Lead Time: <strong className="text-white">{supp.lead_time_days} Days</strong></span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4 text-gray-400" />
                <span>{supp.location}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Mail className="w-4 h-4 text-gray-400" />
                <span className="text-cyan-400 truncate">{supp.email}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4 text-gray-400" />
                <span>{supp.phone}</span>
              </div>
            </div>

            <div className="mt-4 p-2.5 rounded-xl bg-gray-900/60 border border-gray-800/80 flex items-center justify-between text-[11px]">
              <span className="text-gray-400">On-Time Reliability</span>
              <span className="font-bold text-emerald-400">97.8% Fulfilled</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

