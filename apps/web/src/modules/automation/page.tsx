"use client";

import { Button, Badge } from "@nexus/ui-system";
import {
  Zap, Plus, Play, MoreHorizontal, Webhook,
  Mail, MessageSquare, Clock, Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";

export default function AutomationPage() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <h1 className="text-lg font-semibold">Automation</h1>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            AI Suggestions
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            New Workflow
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid gap-4 lg:grid-cols-2">
          {workflows.map((wf, i) => (
            <motion.div
              key={wf.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="rounded-xl border bg-primary p-5 transition-all hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="rounded-lg bg-accent/10 p-2.5">
                    <Zap className="h-5 w-5 text-accent" />
                  </div>
                  <div>
                    <h3 className="font-medium">{wf.name}</h3>
                    <p className="text-sm text-text-secondary">{wf.trigger}</p>
                  </div>
                </div>
                <Badge variant={wf.active ? "success" : "secondary"} size="sm">
                  {wf.active ? "Active" : "Inactive"}
                </Badge>
              </div>

              <div className="mt-4 flex items-center gap-2">
                {wf.steps.map((step, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <div className="rounded-lg border bg-secondary px-3 py-1.5 text-xs font-medium">
                      {step}
                    </div>
                    {idx < wf.steps.length - 1 && (
                      <div className="text-text-tertiary">→</div>
                    )}
                  </div>
                ))}
              </div>

              <div className="mt-4 flex items-center justify-between border-t pt-3">
                <span className="text-xs text-text-tertiary">
                  Last run: {wf.lastRun}
                </span>
                <div className="flex items-center gap-1">
                  <Button variant="ghost" size="xs" leftIcon={<Play className="h-3 w-3" />}>
                    Run
                  </Button>
                  <Button variant="ghost" size="xs" leftIcon={<MoreHorizontal className="h-3 w-3" />} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

const workflows = [
  {
    id: "1", name: "Daily Email Digest", trigger: "Schedule: 8:00 AM daily",
    steps: ["Collect notes", "Generate summary", "Send email"], active: true, lastRun: "Today 8:00 AM",
  },
  {
    id: "2", name: "Slack Task Alerts", trigger: "When task is overdue",
    steps: ["Check tasks", "Format message", "Send to Slack"], active: true, lastRun: "Yesterday 3:15 PM",
  },
  {
    id: "3", name: "Auto-Categorize Transactions", trigger: "New transaction created",
    steps: ["Read description", "AI categorize", "Update record"], active: false, lastRun: "Never",
  },
];
