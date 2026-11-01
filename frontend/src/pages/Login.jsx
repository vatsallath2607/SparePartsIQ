import React, { useState } from 'react';
import { useAuth, DEMO_ACCOUNTS } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Shield, Lock, Mail, ArrowRight, UserCheck } from 'lucide-react';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [selectedRole, setSelectedRole] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setSubmitting(false);
    }
  };

  const handleSelectRole = (acc) => {
    setEmail(acc.email);
    setPassword('');
    setSelectedRole(acc.role);
    setError('');
    const passwordInput = document.getElementById('password-input');
    if (passwordInput) {
      passwordInput.focus();
    }
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-[#111827] border border-gray-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
        {/* Background glow */}
        <div className="absolute -top-24 -left-24 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

        {/* Brand Header */}
        <div className="text-center">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-cyan-600 to-blue-500 flex items-center justify-center font-bold text-white text-xl mx-auto shadow-lg shadow-blue-500/20">
            IQ
          </div>
          <h1 className="text-xl font-bold text-white mt-4 tracking-tight">SpareParts<span className="text-cyan-400">IQ</span></h1>
          <p className="text-xs text-gray-400 mt-1">Autonomous Industrial Spare Parts Intelligence Platform</p>
        </div>

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-xs text-red-400 text-center">
            {error}
          </div>
        )}

        {/* Role Account Quick Selection */}
        <div className="mt-6">
          <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wider block text-center mb-2.5">
            Select Role Account to Sign In
          </span>
          <div className="grid grid-cols-1 gap-2">
            {DEMO_ACCOUNTS.map((acc) => (
              <button
                key={acc.role}
                type="button"
                onClick={() => handleSelectRole(acc)}
                className={`flex items-center justify-between p-2.5 rounded-xl border text-left transition group ${
                  selectedRole === acc.role
                    ? 'bg-cyan-950/40 border-cyan-500/60 ring-1 ring-cyan-500/40'
                    : 'bg-gray-800/80 hover:bg-gray-700/80 border-gray-700/80'
                }`}
              >
                <div>
                  <div className="text-xs font-semibold text-gray-200 group-hover:text-cyan-300">{acc.role}</div>
                  <div className="text-[10px] text-gray-400">{acc.name} • {acc.department}</div>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-gray-500 group-hover:text-cyan-400 transition transform group-hover:translate-x-0.5" />
              </button>
            ))}
          </div>
        </div>

        <div className="my-6 flex items-center space-x-3">
          <div className="flex-1 h-px bg-gray-800"></div>
          <span className="text-[10px] text-gray-500 uppercase">Or Standard Login</span>
          <div className="flex-1 h-px bg-gray-800"></div>
        </div>

        {/* Credentials Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="text-gray-400">Enterprise Email</label>
            <div className="mt-1 relative">
              <Mail className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@sparepartsiq.com"
                className="w-full pl-9 pr-3 py-2 bg-gray-900 border border-gray-800 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>
          </div>

          <div>
            <label className="text-gray-400">Password</label>
            <div className="mt-1 relative">
              <Lock className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                id="password-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 bg-gray-900 border border-gray-800 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full mt-2 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-gray-950 font-bold text-xs rounded-xl transition shadow-lg shadow-cyan-500/20 disabled:opacity-50"
          >
            {submitting ? 'Authenticating...' : 'Sign In to Dashboard'}
          </button>
        </form>

        <div className="mt-6 text-center text-[10px] text-gray-500">
          Industrial Grade Authentication • AWS IAM Bound
        </div>
      </div>
    </div>
  );
}

