import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, CheckCircle2, XCircle, Lightbulb, Loader2, Trophy } from 'lucide-react';
import api from '../api';
import AmbientBackground from '../components/AmbientBackground';

export default function Lesson() {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const [attemptId, setAttemptId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [blocked, setBlocked] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    api.post(`progress/lessons/${lessonId}/start/`)
      .then((r) => { setAttemptId(r.data.attempt_id); return api.get(`courses/lessons/${lessonId}/questions/`).catch(() => ({ data: [] })); })
      .then((r) => setQuestions(r.data || []))
      .catch((err) => setBlocked(err.response?.data?.detail || 'error'));
  }, [lessonId]);

  const submit = async () => {
    if (!answer.trim()) return;
    setLoading(true);
    try {
      const q = questions[current];
      const res = await api.post(`progress/attempts/${attemptId}/submit-answer/`, { question_id: q.id, answer });
      setFeedback(res.data);
      if (res.data.lesson_completed) setCompleted(true);
      else if (res.data.is_correct) setTimeout(() => { setCurrent((c) => c + 1); setAnswer(''); setFeedback(null); }, 1200);
    } finally { setLoading(false); }
  };

  if (blocked) {
    const msg = {
      daily_limit_reached: "Bugungi 4 ta darslik limitingiz tugadi. Ertaga yangi kun, yangi imkoniyat! 🌙",
      extremal_test_required: "Bugun 2 ta darsni tugatdingiz! Davom etish uchun ekstremal testdan o'ting.",
    }[blocked] || "Dars ochilmadi.";
    return (
      <div className="min-h-screen relative flex items-center justify-center px-4">
        <AmbientBackground />
        <div className="halo-card glass rounded-3xl p-10 max-w-md text-center">
          <p className="text-gray-300 mb-6 leading-relaxed">{msg}</p>
          <button onClick={() => navigate('/dashboard')} className="glow-btn px-6 py-3 rounded-xl font-semibold">Dashboard'ga qaytish</button>
        </div>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="min-h-screen relative flex items-center justify-center px-4">
        <AmbientBackground />
        <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} className="halo-card glass rounded-3xl p-12 max-w-md text-center">
          <Trophy className="w-16 h-16 text-yellow-400 mx-auto mb-5" />
          <h2 className="text-2xl font-extrabold mb-2">Dars tugallandi!</h2>
          <p className="text-gray-400 mb-8">Barakalla! XP hisobingizga qo'shildi.</p>
          <button onClick={() => navigate('/dashboard')} className="glow-btn px-8 py-3 rounded-xl font-semibold">Davom etish</button>
        </motion.div>
      </div>
    );
  }

  const q = questions[current];

  return (
    <div className="min-h-screen relative p-6 md:p-10">
      <AmbientBackground />
      <div className="max-w-3xl mx-auto">
        <button onClick={() => navigate('/dashboard')} className="flex items-center gap-2 text-gray-500 hover:text-white transition mb-8 text-sm">
          <ArrowLeft className="w-4 h-4" /> Orqaga
        </button>

        {questions.length > 0 && (
          <div className="mb-6">
            <div className="flex justify-between text-xs text-gray-500 mb-2 font-mono">
              <span>Savol {current + 1} / {questions.length}</span>
              <span>{Math.round((current / questions.length) * 100)}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
              <motion.div className="h-full glow-btn rounded-full" animate={{ width: `${(current / questions.length) * 100}%` }} />
            </div>
          </div>
        )}

        {!q ? (
          <div className="glass rounded-2xl p-10 text-center text-gray-500">
            <Loader2 className="w-6 h-6 animate-spin mx-auto mb-3" /> Yuklanmoqda...
          </div>
        ) : (
          <motion.div key={current} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="halo-card glass rounded-2xl p-8">
            <p className="text-lg font-medium mb-6 leading-relaxed">{q.question_text}</p>

            {q.question_type === 'multiple_choice' ? (
              <div className="space-y-2 mb-6">
                {q.choices?.map((ch) => (
                  <button key={ch.id} onClick={() => setAnswer(ch.id)}
                    className={`w-full text-left px-5 py-4 rounded-xl border transition ${answer === ch.id ? 'border-indigo-500 bg-indigo-500/10 text-indigo-300' : 'border-white/10 bg-white/[0.02] hover:border-white/20'}`}>
                    {ch.choice_text}
                  </button>
                ))}
              </div>
            ) : (
              <input value={answer} onChange={(e) => setAnswer(e.target.value)} placeholder="Javobingizni yozing..."
                className="input-field w-full px-5 py-4 rounded-xl text-white mb-6" />
            )}

            {feedback && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className={`mb-6 px-5 py-4 rounded-xl border flex items-start gap-3 ${feedback.is_correct ? 'bg-emerald-500/10 border-emerald-500/25 text-emerald-300' : 'bg-red-500/10 border-red-500/25 text-red-300'}`}>
                {feedback.is_correct ? <CheckCircle2 className="w-5 h-5 shrink-0 mt-0.5" /> : <XCircle className="w-5 h-5 shrink-0 mt-0.5" />}
                <div>
                  <p className="font-medium">{feedback.is_correct ? "To'g'ri!" : "Noto'g'ri, qaytadan urinib ko'ring."}</p>
                  {feedback.needs_help && (
                    <p className="text-sm mt-2 flex items-start gap-2 text-yellow-300">
                      <Lightbulb className="w-4 h-4 shrink-0 mt-0.5" /> {q.hint_text || "Bu mavzuni qaytadan ko'rib chiqishni tavsiya qilamiz."}
                    </p>
                  )}
                </div>
              </motion.div>
            )}

            <button onClick={submit} disabled={loading || !answer}
              className="glow-btn w-full py-3.5 rounded-xl font-semibold flex items-center justify-center gap-2 disabled:opacity-40">
              {loading && <Loader2 className="w-4 h-4 animate-spin" />} Javobni yuborish
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
