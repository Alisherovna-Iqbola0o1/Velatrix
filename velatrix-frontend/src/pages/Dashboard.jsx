import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LogOut, Zap, Flame, BookOpen, Terminal, ChevronRight } from 'lucide-react';
import api from '../api';
import AmbientBackground from '../components/AmbientBackground';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [courses, setCourses] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('users/profile/').then((r) => setProfile(r.data)).catch(() => {});
    api.get('courses/').then((r) => setCourses(r.data)).catch(() => {});
  }, []);

  const logout = () => { localStorage.clear(); navigate('/login'); };

  const stats = [
    { label: 'Umumiy XP', value: profile?.total_xp ?? 0, icon: Zap, color: 'text-yellow-400' },
    { label: 'Streak', value: `${profile?.current_streak ?? 0} kun`, icon: Flame, color: 'text-orange-400' },
    { label: 'Kurslar', value: courses.length, icon: BookOpen, color: 'text-indigo-400' },
  ];

  return (
    <div className="min-h-screen relative p-6 md:p-10">
      <AmbientBackground />
      <div className="max-w-6xl mx-auto">
        <header className="flex justify-between items-center mb-10">
          <div className="flex items-center gap-3">
            <div className="relative">
              <div className="absolute inset-0 bg-indigo-500 rounded-xl blur-lg opacity-40" />
              <div className="relative p-2.5 rounded-xl glow-btn"><Terminal className="w-5 h-5 text-white" /></div>
            </div>
            <div>
              <h1 className="text-xl font-extrabold tracking-tight">Velatrix</h1>
              <p className="text-xs text-gray-500 font-mono">Salom, {profile?.username ?? '...'}</p>
            </div>
          </div>
          <button onClick={logout} className="glass flex items-center gap-2 px-4 py-2.5 rounded-xl text-gray-400 hover:text-red-400 hover:border-red-500/20 transition text-sm">
            <LogOut className="w-4 h-4" /> Chiqish
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-10">
          {stats.map((s, i) => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}
              whileHover={{ y: -3 }} className="glass rounded-2xl p-6 transition-colors hover:border-indigo-500/30">
              <div className="flex justify-between items-start mb-4">
                <span className="text-sm text-gray-400">{s.label}</span>
                <s.icon className={`w-5 h-5 ${s.color}`} />
              </div>
              <h3 className="text-3xl font-extrabold font-mono">{s.value}</h3>
            </motion.div>
          ))}
        </div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.25 }}>
          <h2 className="text-lg font-bold mb-5">Kurslar</h2>
          <div className="space-y-3">
            {courses.length === 0 && (
              <div className="glass rounded-2xl p-8 text-center text-gray-500 text-sm">Hozircha kurslar mavjud emas.</div>
            )}
            {courses.map((c) => (
              <div key={c.id} className="glass rounded-2xl p-5 hover:border-indigo-500/30 transition">
                <div className="flex justify-between items-center mb-1">
                  <div className="flex items-center gap-3">
                    <h3 className="font-semibold">{c.title}</h3>
                    <span className="text-[10px] uppercase tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-400 border border-indigo-500/25">
                      {c.difficulty_level}
                    </span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-gray-600" />
                </div>
                <p className="text-sm text-gray-500 mb-4">{c.description}</p>

                <div className="space-y-3">
                  {c.sections?.map((s) => (
                    <div key={s.id} className="pl-4 border-l border-white/10">
                      <p className="text-sm text-gray-300 mb-2">{s.title}</p>
                      <div className="flex flex-wrap gap-2">
                        {s.lessons?.map((l) => (
                          <button key={l.id} onClick={() => navigate(`/lesson/${l.id}`)}
                            className="text-xs px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 hover:border-indigo-500/40 hover:text-indigo-300 transition font-mono">
                            {l.title} · {l.xp_reward}xp
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
