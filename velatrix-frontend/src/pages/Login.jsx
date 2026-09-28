import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Terminal, Loader2, Sparkles } from 'lucide-react';
import api from '../api';
import AmbientBackground from '../components/AmbientBackground';
import Typewriter from '../components/Typewriter';

const CODE_LINES = [
  '> initializing velatrix.system...',
  '> loading tech_stacks [frontend, backend, ai]...',
  '> compiling future_skills.exe...',
  '> status: ready to code the future...',
];

export default function Login() {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      const res = await api.post('users/login/', form);
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      navigate('/dashboard');
    } catch {
      setError("Login yoki parol noto'g'ri.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center px-4">
      <AmbientBackground />
      <div className="w-full max-w-5xl grid md:grid-cols-2 gap-8 items-center">
        <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6 }} className="hidden md:block">
          <div className="flex items-center gap-3 mb-6">
            <div className="relative">
              <div className="absolute inset-0 bg-indigo-500 rounded-2xl blur-xl opacity-50 animate-pulse" />
              <div className="relative p-3 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-2xl">
                <Terminal className="w-7 h-7 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight">Velatrix</h1>
              <p className="text-xs text-gray-500 font-mono">v1.0.0 · ICT LMS</p>
            </div>
          </div>
          <h2 className="text-4xl font-extrabold leading-tight mb-4 bg-gradient-to-r from-white via-indigo-200 to-purple-300 bg-clip-text text-transparent">
            Kod yozing.<br />Bilim quring.<br />Kelajakni yarating.
          </h2>
          <p className="text-gray-400 mb-8 max-w-md leading-relaxed">
            Dasturlash Tillari, Backend, xavfsizlik va zamonaviy dasturlashni chuqur, amaliy va bosqichma-bosqich o'rganing.
          </p>
          <div className="glass rounded-2xl p-5 max-w-md">
            <div className="flex items-center gap-2 mb-3 text-xs text-gray-500">
              <div className="w-2.5 h-2.5 rounded-full bg-red-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/60" />
              <div className="w-2.5 h-2.5 rounded-full bg-green-500/60" />
              <span className="ml-2 font-mono">terminal</span>
            </div>
            <Typewriter lines={CODE_LINES} />
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.6, delay: 0.1 }}>
          <div className="halo-card glass rounded-3xl p-8 md:p-10">
            <div className="flex items-center gap-2 mb-1">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span className="text-xs font-mono text-indigo-400 uppercase tracking-widest">Welcome back</span>
            </div>
            <h2 className="text-2xl font-bold mb-8">Hisobingizga kiring</h2>

            {error && (
              <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="mb-5 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                {error}
              </motion.div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="text-xs text-gray-400 mb-1.5 block font-mono">username</label>
                <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })}
                  className="input-field w-full px-4 py-3.5 rounded-xl text-white" placeholder="velatrix_dev" required />
              </div>
              <div>
                <label className="text-xs text-gray-400 mb-1.5 block font-mono">password</label>
                <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
                  className="input-field w-full px-4 py-3.5 rounded-xl text-white" placeholder="••••••••••" required />
              </div>
              <button type="submit" disabled={loading}
                className="glow-btn w-full py-3.5 rounded-xl font-semibold text-white flex items-center justify-center gap-2 disabled:opacity-60 mt-2">
                {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                {loading ? 'Kirilmoqda...' : 'Tizimga kirish →'}
              </button>
            </form>

            <p className="text-center text-sm text-gray-500 mt-7">
              Hisobingiz yo'qmi? <Link to="/register" className="text-indigo-400 hover:text-indigo-300 font-medium">Ro'yxatdan o'ting</Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
