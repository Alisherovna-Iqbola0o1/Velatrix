export default function AmbientBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-[#0A0A14]">
      <div className="absolute top-[-15%] left-[-10%] w-[550px] h-[550px] bg-indigo-600/25 rounded-full blur-[130px] animate-blob" />
      <div className="absolute bottom-[-20%] right-[-5%] w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[130px] animate-blob [animation-delay:4s]" />
      <div className="absolute top-[35%] left-[55%] w-[350px] h-[350px] bg-fuchsia-600/15 rounded-full blur-[110px] animate-blob [animation-delay:8s]" />
      <div
        className="absolute inset-0 opacity-[0.4]"
        style={{
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)',
          backgroundSize: '48px 48px',
        }}
      />
    </div>
  );
}
