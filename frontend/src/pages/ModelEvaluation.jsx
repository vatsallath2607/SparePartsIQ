import React, { useState, useEffect } from 'react';
import { apiRequest } from '../api/client';
import {
  Cpu,
  CheckCircle2,
  BarChart2,
  ShieldCheck,
  Calendar,
  Layers,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';

export default function ModelEvaluation() {
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReport() {
      try {
        const data = await apiRequest('/api/forecasts/evaluation/metrics');
        setReport(data);
      } catch (err) {
        console.error('Failed to load evaluation report:', err);
      } finally {
        setLoading(false);
      }
    }
    loadReport();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-400"></div>
      </div>
    );
  }

  const modelsEvaluated = report?.models_evaluated || {};

  const chartData = Object.keys(modelsEvaluated).map(name => ({
    name: name.replace(/_/g, ' '),
    val_rmse: modelsEvaluated[name]?.validation?.RMSE,
    test_rmse: modelsEvaluated[name]?.test?.RMSE,
    val_mae: modelsEvaluated[name]?.validation?.MAE,
    test_mae: modelsEvaluated[name]?.test?.MAE
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight">Machine Learning Model Evaluation & Benchmark</h1>
        <p className="text-xs text-gray-400 mt-1">
          Rigorous out-of-sample performance validation preventing lookahead data leakage via chronological time splits.
        </p>
      </div>

      {/* Methodology Highlight Banner */}
      <div className="p-5 rounded-2xl bg-[#111827] border border-cyan-500/20 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider flex items-center space-x-1.5">
            <ShieldCheck className="w-4 h-4" />
            <span>Time-Series Split Methodology</span>
          </span>
          <h2 className="text-base font-bold text-white mt-1">Chronological 70% Train • 15% Validation • 15% Test Split</h2>
          <p className="text-xs text-gray-400 mt-1 max-w-2xl leading-relaxed">
            Data points were partitioned chronologically without random shuffling to prevent future lookahead data leakage.
            Explainable baselines (Simple Moving Average and Exponential Smoothing) were systematically evaluated against
            tree-based ensemble regressors (Random Forest and Gradient Boosting).
          </p>
        </div>

        <div className="p-3 rounded-xl bg-gray-900 border border-gray-800 shrink-0 text-center">
          <span className="text-[10px] text-gray-400 uppercase font-semibold">Champion Model</span>
          <div className="text-sm font-bold text-emerald-400 mt-0.5">{report?.champion_model?.replace(/_/g, ' ')}</div>
          <span className="text-[10px] text-gray-500">Serialized in S3 Bucket</span>
        </div>
      </div>

      {/* Comparative Evaluation Table */}
      <div className="rounded-2xl bg-[#111827] border border-gray-800 overflow-hidden shadow-sm">
        <div className="p-4 border-b border-gray-800 flex items-center justify-between">
          <h2 className="text-xs font-bold text-white uppercase tracking-wider">Out-Of-Sample Validation Performance Matrix</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-900/60 text-gray-400 border-b border-gray-800">
              <tr>
                <th className="py-3 px-4 font-semibold">Forecasting Algorithm</th>
                <th className="py-3 px-4 font-semibold">Model Class</th>
                <th className="py-3 px-4 font-semibold">Val MAE</th>
                <th className="py-3 px-4 font-semibold">Val RMSE</th>
                <th className="py-3 px-4 font-semibold">Test MAE</th>
                <th className="py-3 px-4 font-semibold">Test RMSE</th>
                <th className="py-3 px-4 font-semibold">Test MAPE</th>
                <th className="py-3 px-4 font-semibold text-right">Production Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {Object.keys(modelsEvaluated).map(name => {
                const isChampion = name === report?.champion_model;
                const m = modelsEvaluated[name];
                const isBaseline = name.includes('Average') || name.includes('Exponential');

                return (
                  <tr key={name} className={`hover:bg-gray-800/30 transition ${isChampion ? 'bg-cyan-950/20' : ''}`}>
                    <td className="py-3.5 px-4 font-bold text-white">
                      {name.replace(/_/g, ' ')}
                    </td>
                    <td className="py-3.5 px-4 text-gray-400">
                      {isBaseline ? 'Explainable Baseline' : 'Tree Ensemble Regressor'}
                    </td>
                    <td className="py-3.5 px-4 text-gray-200">{m?.validation?.MAE}</td>
                    <td className="py-3.5 px-4 font-bold text-cyan-400">{m?.validation?.RMSE}</td>
                    <td className="py-3.5 px-4 text-gray-200">{m?.test?.MAE}</td>
                    <td className="py-3.5 px-4 font-bold text-emerald-400">{m?.test?.RMSE}</td>
                    <td className="py-3.5 px-4 text-gray-300">{m?.test?.MAPE_pct}%</td>
                    <td className="py-3.5 px-4 text-right">
                      {isChampion ? (
                        <span className="inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                          <CheckCircle2 className="w-3 h-3" />
                          <span>CHAMPION</span>
                        </span>
                      ) : (
                        <span className="text-[10px] text-gray-500">Evaluated</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* RMSE Comparison Chart */}
      <div className="p-5 rounded-2xl bg-[#111827] border border-gray-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-semibold text-white">RMSE Error Comparison Across Models</h2>
            <p className="text-xs text-gray-400">Lower Root Mean Squared Error denotes superior forecast precision</p>
          </div>
          <BarChart2 className="w-4 h-4 text-cyan-400" />
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#4b5563" fontSize={11} />
              <YAxis stroke="#4b5563" fontSize={11} domain={[0, 1.0]} />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.75rem', fontSize: '11px' }}
              />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="val_rmse" fill="#3b82f6" name="Validation RMSE" radius={[4, 4, 0, 0]} />
              <Bar dataKey="test_rmse" fill="#06b6d4" name="Out-Of-Sample Test RMSE" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

