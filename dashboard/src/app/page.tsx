'use client';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function Dashboard() {
  const [signals, setSignals] = useState([]);
  const [symbol, setSymbol] = useState("");
  const [sentiment, setSentiment] = useState("");

  const fetchSignals = async () => {
    const res = await axios.get("http://localhost:8000/signals");
    setSignals(res.data);
  };

  const addSignal = async () => {
    await axios.post(`http://localhost:8000/add_signal?symbol=${symbol}&sentiment=${sentiment}`);
    fetchSignals();
  };

  useEffect(() => {
    fetchSignals();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">📈 Live Signals</h1>

      <div className="flex gap-2 mb-4">
        <Input placeholder="Symbol (e.g. AAPL)" value={symbol} onChange={e => setSymbol(e.target.value)} />
        <Input placeholder="Sentiment (e.g. positive)" value={sentiment} onChange={e => setSentiment(e.target.value)} />
        <Button onClick={addSignal}>Add Signal</Button>
      </div>

      <table className="w-full text-left border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="px-4 py-2">Symbol</th>
            <th className="px-4 py-2">Sentiment</th>
            <th className="px-4 py-2">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {signals.map((s: any, i) => (
            <tr key={i} className="border-t">
              <td className="px-4 py-2">{s.symbol}</td>
              <td className="px-4 py-2">{s.sentiment}</td>
              <td className="px-4 py-2">{new Date(s.timestamp).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
