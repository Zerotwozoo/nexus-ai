"use client";

import { Button } from "@nexus/ui-system";
import { Sparkles, Zap, BarChart3, Plus } from "lucide-react";
import { motion } from "framer-motion";

export default function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-primary">
      <aside className="fixed left-0 top-0 z-40 flex h-full w-64 flex-col border-r bg-secondary">
        <div className="flex h-16 items-center gap-2 border-b px-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
            <Sparkles className="h-4 w-4 text-white" />
          </div>
          <span className="font-semibold">Nexus AI</span>
        </div>
        <nav className="flex-1 space-y-1 p-3">
          <SidebarItem icon={<BarChart3 className="h-4 w-4" />} label="Dashboard" active />
          <SidebarItem icon={<Zap className="h-4 w-4" />} label="AI Assistant" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Notes" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Tasks" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Calendar" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Finance" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Trading" />
          <SidebarItem icon={<Plus className="h-4 w-4" />} label="Automation" />
        </nav>
      </aside>

      <main className="ml-64 flex-1">
        <header className="flex h-16 items-center justify-between border-b px-6">
          <h1 className="text-lg font-semibold">Dashboard</h1>
          <Button size="sm">
            <Plus className="h-4 w-4" />
            New Note
          </Button>
        </header>

        <div className="p-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="grid gap-6 md:grid-cols-2 lg:grid-cols-3"
          >
            <Widget title="Productivity Score" value="87%" />
            <Widget title="Active Tasks" value="12" />
            <Widget title="Upcoming Events" value="3" />
          </motion.div>
        </div>
      </main>
    </div>
  );
}

function SidebarItem({
  icon,
  label,
  active,
}: {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
}) {
  return (
    <button
      className={`flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
        active
          ? "bg-accent text-white"
          : "text-text-secondary hover:bg-tertiary hover:text-text-primary"
      }`}
    >
      {icon}
      {label}
    </button>
  );
}

function Widget({ title, value }: { title: string; value: string }) {
  return (
    <div className="rounded-xl border bg-primary p-6 transition-shadow hover:shadow-md">
      <p className="text-sm text-text-secondary">{title}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}
