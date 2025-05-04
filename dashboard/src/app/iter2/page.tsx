'use client';
import { useEffect, useState } from 'react';
import { getSentimentFeed } from '../../../lib/api';

type Signal = {
  symbol: string;
  sentiment: string;
  timestamp: string;
};

export default function Dashboard() {
  const [signals, setSignals] = useState<Signal[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getSentimentFeed();
        setSignals(data);
      } catch (err) {
        console.error('Error loading sentiment feed:', err);
      }
    };
    load();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">📡 Sentiment Feed</h1>
      <ul className="space-y-3">
        {signals.map((s, idx) => (
          <li key={idx} className="p-4 bg-white rounded shadow border">
            <strong>{s.symbol}</strong> – {s.sentiment} <br />
            <span className="text-xs text-gray-500">{s.timestamp}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
