"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  Lock, Plus, Search, Copy, Eye, EyeOff,
  Trash2, Globe, Shield, Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";

export default function PasswordsPage() {
  const [search, setSearch] = useState("");
  const [showPasswords, setShowPasswords] = useState(false);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Password Manager</h1>
          <Shield className="h-4 w-4 text-accent" />
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            Security Report
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            Add Password
          </Button>
        </div>
      </div>

      <div className="border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <div className="flex flex-1 items-center gap-2 rounded-lg border bg-secondary px-3 py-1.5">
            <Search className="h-4 w-4 text-text-tertiary" />
            <input
              className="flex-1 bg-transparent text-sm outline-none placeholder:text-text-tertiary"
              placeholder="Search passwords..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <button
            onClick={() => setShowPasswords(!showPasswords)}
            className="rounded-lg border bg-secondary p-2.5 transition-colors hover:bg-tertiary"
          >
            {showPasswords ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="space-y-2">
          {items.map((item, i) => (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="group flex items-center gap-4 rounded-xl border bg-primary p-4 transition-all hover:shadow-md"
            >
              <div className="rounded-lg bg-accent/10 p-3">
                <Globe className="h-5 w-5 text-accent" />
              </div>
              <div className="min-w-0 flex-1">
                <p className="font-medium">{item.name}</p>
                <p className="text-sm text-text-secondary">{item.username}</p>
              </div>
              <div className="flex items-center gap-2">
                <Badge
                  variant={item.strength === "strong" ? "success" : item.strength === "medium" ? "warning" : "error"}
                  size="sm"
                >
                  {item.strength}
                </Badge>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => navigator.clipboard.writeText(item.password)}
                >
                  <Copy className="h-3.5 w-3.5" />
                </Button>
                <Button variant="ghost" size="xs" className="opacity-0 group-hover:opacity-100">
                  <Trash2 className="h-3.5 w-3.5 text-error" />
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

const items = [
  { id: "1", name: "Google", username: "user@gmail.com", password: "pass123", strength: "strong" },
  { id: "2", name: "GitHub", username: "devuser", password: "ghp_token", strength: "strong" },
  { id: "3", name: "Netflix", username: "user@email.com", password: "netflix123", strength: "medium" },
  { id: "4", name: "Twitter/X", username: "@user", password: "tweet_pass", strength: "weak" },
];
