"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  TrendingUp, BarChart3, Plus, Target,
  Activity, DollarSign, Percent, Calculator,
  Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";

export default function TradingPage() {
  const [tab, setTab] = useState<"journal" | "analytics" | "risk">("journal");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Trading Journal</h1>
          <div className="flex items-center gap-1 rounded-lg bg-secondary p-0.5">
            {(["journal", "analytics", "risk"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`rounded-md px-3 py-1.5 text-xs font-medium capitalize transition ${
                  tab === t ? "bg-primary shadow-sm" : "text-text-secondary"
                }`}
              >
                {t}
              </button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            AI Analysis
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            New Trade
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard icon={<Activity className="h-5 w-5" />} label="Win Rate" value="68.5%" />
          <StatCard icon={<DollarSign className="h-5 w-5" />} label="Total P&L" value="+$4,250" />
          <StatCard icon={<BarChart3 className="h-5 w-5" />} label="Total Trades" value="156" />
          <StatCard icon={<Target className="h-5 w-5" />} label="Avg RR" value="1:2.4" />
        </div>

        <div className="mt-6 rounded-xl border bg-primary">
          <div className="border-b px-5 py-3">
            <h3 className="text-sm font-semibold">Recent Trades</h3>
          </div>
          <div className="divide-y">
            {trades.map((trade, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-center justify-between px-5 py-3.5 transition-colors hover:bg-secondary"
              >
                <div className="flex items-center gap-4">
                  <div>
                    <p className="text-sm font-medium">{trade.instrument}</p>
                    <p className="text-xs text-text-secondary">{trade.type}</p>
                  </div>
                  <Badge variant={trade.pnl > 0 ? "success" : "error"} size="sm">
                    {trade.pnl > 0 ? "+" : ""}${trade.pnl}
                  </Badge>
                </div>
                <div className="text-right text-sm">
                  <p className="text-text-secondary">Entry: ${trade.entry}</p>
                  <p className="text-text-secondary">Exit: ${trade.exit}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border bg-primary p-4 transition-shadow hover:shadow-md"
    >
      <div className="rounded-lg bg-accent/10 p-2.5 text-accent w-fit">
        {icon}
      </div>
      <p className="mt-3 text-sm text-text-secondary">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </motion.div>
  );
}

const trades = [
  { instrument: "BTC/USD", type: "Long", entry: 67450, exit: 68900, pnl: 1450 },
  { instrument: "EUR/USD", type: "Short", entry: 1.0840, exit: 1.0790, pnl: 500 },
  { instrument: "AAPL", type: "Long", entry: 218, exit: 225, pnl: 700 },
  { instrument: "TSLA", type: "Short", entry: 245, exit: 238, pnl: -350 },
];
