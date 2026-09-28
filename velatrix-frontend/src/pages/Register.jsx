import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { UserPlus, Loader2, ShieldCheck } from 'lucide-react';
import api from '../api';
import AmbientBackground from '../components/AmbientBackground';

const SECURITY_QUESTIONS = [
  { value: 'mother_name', label: "Onangizning ismi?" },
  { value: 'first_school', label: "Birinchi maktabingizning nomi?" },
  { value: 'favourite_book', label: "Sevimli kitobingiz nomi?" },
  { value: 'birth_city', label: "Tug'ilgan shahringiz?" },
  { value: 'first_pet', label: "Birinchi uy hayvoningiz turi?" },
];

export default function Register() {
  const [form, setForm] = useState({
    username: '', password: '', email: '',
    language_choice: 'uz', security_question: 'mother_name', security_answer: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); setLoading(true);
    try {
      await api.post('users/register/', form);
      const res = await api.post('users/login/', { username: form.username, password: form.password });
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      navigate('/dashboard');
    } catch (err) {
      const d = err.response?.data;
      setError(d ? Object.values(d).flat().join(' ') : "Xatolik yuz berdi.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen relative flex items-center justify-center px-4 py-10">
      <AmbientBackground />
      <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} className="halo-card glass rounded-3xl p-8 md:p-10 w-full max-w-md">
        <div className="flex items-center gap-2 mb-1">
          <UserPlus className="w-4 h-4 text-indigo-400" />
          <span className="text-xs font-mono text-indigo-400 uppercase tracking-widest">New account</span>
        </div>
        <h1 className="text-2xl font-bold mb-8">Ro'yxatdan o'tish</h1>

        {error && (
          <div className="mb-5 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input value={form.username} onChange={set('username')} placeholder="Username *" required
            className="input-field w-full px-4 py-3 rounded-xl text-white" />
          <input type="password" value={form.password} onChange={set('password')} placeholder="Parol * (min 8 belgi)" required minLength={8}
            className="input-field w-full px-4 py-3 rounded-xl text-white" />
          <input type="email" value={form.email} onChange={set('email')} placeholder="Email (ixtiyoriy)"
            className="input-field w-full px-4 py-3 rounded-xl text-white" />

          <select value={form.language_choice} onChange={set('language_choice')} className="input-field w-full px-4 py-3 rounded-xl text-white">
            <option value="uz" className="bg-[#14142B]">O'zbek</option>
            <option value="en" className="bg-[#14142B]">English</option>
          </select>

          <div className="pt-4 mt-2 border-t border-white/5">
            <div className="flex items-center gap-2 mb-3">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              <p className="text-xs text-gray-500 leading-relaxed">
                Bu savol parolingizni unutganda uni tiklashda yordam beradi.
              </p>
            </div>
            <select value={form.security_question} onChange={set('security_question')} className="input-field w-full px-4 py-3 rounded-xl text-white mb-3">
              {SECURITY_QUESTIONS.map((q) => <option key={q.value} value={q.value} className="bg-[#14142B]">{q.label}</option>)}
            </select>
            <input value={form.security_answer} onChange={set('security_answer')} placeholder="Javobingiz *" required
              className="input-field w-full px-4 py-3 rounded-xl text-white" />
          </div>

          <button type="submit" disabled={loading}
            className="glow-btn w-full py-3.5 rounded-xl font-semibold text-white flex items-center justify-center gap-2 disabled:opacity-60">
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            {loading ? 'Yaratilmoqda...' : "Ro'yxatdan o'tish"}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-6">
          Hisobingiz bormi? <Link to="/login" className="text-indigo-400 font-medium">Kirish</Link>
        </p>
      </motion.div>
    </div>
  );
}
