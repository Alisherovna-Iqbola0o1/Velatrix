import { useEffect, useState } from 'react';

export default function Typewriter({ lines, speed = 40 }) {
  const [displayed, setDisplayed] = useState('');
  const [lineIndex, setLineIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);

  useEffect(() => {
    if (lineIndex >= lines.length) return;
    if (charIndex < lines[lineIndex].length) {
      const t = setTimeout(() => {
        setDisplayed((d) => d + lines[lineIndex][charIndex]);
        setCharIndex((c) => c + 1);
      }, speed);
      return () => clearTimeout(t);
    } else {
      const t = setTimeout(() => {
        setDisplayed((d) => d + '\n');
        setLineIndex((l) => l + 1);
        setCharIndex(0);
      }, 500);
      return () => clearTimeout(t);
    }
  }, [charIndex, lineIndex, lines, speed]);

  return (
    <pre className="font-mono text-sm text-indigo-300/80 whitespace-pre-wrap leading-relaxed">
      {displayed}
      <span className="animate-pulse">▋</span>
    </pre>
  );
}
