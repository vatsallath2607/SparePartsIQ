import React from 'react';

export default function MetricCard({ title, value, subtitle, icon: Icon, color = "cyan", badge }) {
  const colorThemes = {
    cyan: "from-cyan-500/10 to-blue-500/10 text-cyan-400 border-cyan-500/20",
    red: "from-red-500/10 to-rose-500/10 text-red-400 border-red-500/20",
    amber: "from-amber-500/10 to-orange-500/10 text-amber-400 border-amber-500/20",
    emerald: "from-emerald-500/10 to-teal-500/10 text-emerald-400 border-emerald-500/20",
    purple: "from-purple-500/10 to-indigo-500/10 text-purple-400 border-purple-500/20"
  };

  const theme = colorThemes[color] || colorThemes.cyan;

  return (
    <div className={`p-5 rounded-2xl bg-[#111827] border border-gray-800 relative overflow-hidden shadow-sm`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2.5 rounded-xl bg-gradient-to-br ${theme} border`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-3 flex items-baseline space-x-2">
        <span className="text-2xl font-bold text-white tracking-tight">{value}</span>
        {badge && (
          <span className="text-[11px] font-medium px-2 py-0.5 rounded-full bg-gray-800 text-gray-300 border border-gray-700">
            {badge}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-1 text-xs text-gray-400">{subtitle}</p>
      )}
    </div>
  );
}

