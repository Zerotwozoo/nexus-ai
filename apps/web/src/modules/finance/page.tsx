"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  DollarSign, TrendingUp, TrendingDown, Wallet,
  Plus, CreditCard, PieChart, ArrowUpRight,
  ArrowDownRight, Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";

export default function FinancePage() {
  const [tab, setTab] = useState<"overview" | "transactions" | "budgets" | "subscriptions">("overview");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Finance</h1>
          <div className="flex items-center gap-1 rounded-lg bg-secondary p-0.5">
            {(["overview", "transactions", "budgets", "subscriptions"] as const).map((t) => (
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
            AI Forecast
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            Add Transaction
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            icon={<DollarSign className="h-5 w-5" />}
            label="Total Balance"
            value="$12,450"
            change="+5.2%"
            positive
          />
          <StatCard
            icon={<TrendingUp className="h-5 w-5" />}
            label="Income"
            value="$8,200"
            change="+12.3%"
            positive
          />
          <StatCard
            icon={<TrendingDown className="h-5 w-5" />}
            label="Expenses"
            value="$5,300"
            change="-3.1%"
            positive={false}
          />
          <StatCard
            icon={<Wallet className="h-5 w-5" />}
            label="Savings Rate"
            value="35.4%"
            change="+2.1%"
            positive
          />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border bg-primary p-5">
            <h3 className="mb-4 text-sm font-semibold">Recent Transactions</h3>
            <div className="space-y-3">
              {transactions.map((tx, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="flex items-center justify-between"
                >
                  <div className="flex items-center gap-3">
                    <div className={`rounded-lg p-2 ${
                      tx.type === "income" ? "bg-success-light" : "bg-error-light"
                    }`}>
                      {tx.type === "income"
                        ? <ArrowUpRight className="h-4 w-4 text-success" />
                        : <ArrowDownRight className="h-4 w-4 text-error" />
                      }
                    </div>
                    <div>
                      <p className="text-sm font-medium">{tx.description}</p>
                      <p className="text-xs text-text-secondary">{tx.category}</p>
                    </div>
                  </div>
                  <span className={`text-sm font-medium ${
                    tx.type === "income" ? "text-success" : "text-error"
                  }`}>
                    {tx.type === "income" ? "+" : "-"}${tx.amount}
                  </span>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="rounded-xl border bg-primary p-5">
            <h3 className="mb-4 text-sm font-semibold">Budget Overview</h3>
            <div className="space-y-4">
              {budgets.map((budget, i) => (
                <div key={i}>
                  <div className="mb-1 flex items-center justify-between text-sm">
                    <span>{budget.category}</span>
                    <span className="text-text-secondary">
                      ${budget.spent} / ${budget.limit}
                    </span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-secondary">
                    <div
                      className={`h-full rounded-full transition-all ${
                        budget.percent > 90 ? "bg-error" : budget.percent > 70 ? "bg-warning" : "bg-success"
                      }`}
                      style={{ width: `${Math.min(budget.percent, 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({
  icon, label, value, change, positive,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  change: string;
  positive: boolean;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border bg-primary p-4 transition-shadow hover:shadow-md"
    >
      <div className="flex items-center justify-between">
        <div className="rounded-lg bg-accent/10 p-2.5 text-accent">
          {icon}
        </div>
        <Badge variant={positive ? "success" : "error"} size="sm">
          {change}
        </Badge>
      </div>
      <p className="mt-3 text-sm text-text-secondary">{label}</p>
      <p className="text-2xl font-bold">{value}</p>
    </motion.div>
  );
}

const transactions = [
  { description: "Freelance Payment", category: "Income", amount: 2500, type: "income" },
  { description: "Rent Payment", category: "Housing", amount: 1200, type: "expense" },
  { description: "Groceries", category: "Food", amount: 185, type: "expense" },
  { description: "Dividend", category: "Investment", amount: 75, type: "income" },
];

const budgets = [
  { category: "Housing", spent: 1200, limit: 1500, percent: 80 },
  { category: "Food", spent: 450, limit: 500, percent: 90 },
  { category: "Transport", spent: 120, limit: 200, percent: 60 },
  { category: "Entertainment", spent: 80, limit: 150, percent: 53 },
];
