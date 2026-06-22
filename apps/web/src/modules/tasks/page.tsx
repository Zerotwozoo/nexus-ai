"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  Plus, ListTodo, Calendar as CalendarIcon, Layout,
  Clock, MoreHorizontal, User, Flag, CheckCircle2,
  Circle, AlertCircle, Sparkles,
} from "lucide-react";
import { motion } from "framer-motion";

type Task = {
  id: string;
  title: string;
  status: string;
  priority: string;
  due_date: string | null;
};

type Column = {
  id: string;
  title: string;
  tasks: Task[];
};

export default function TasksPage() {
  const [view, setView] = useState<"kanban" | "list" | "calendar">("kanban");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Tasks</h1>
          <div className="flex items-center gap-1 rounded-lg border bg-secondary p-0.5">
            <button
              onClick={() => setView("kanban")}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${
                view === "kanban" ? "bg-primary shadow-sm" : "text-text-secondary"
              }`}
            >
              <Layout className="mr-1.5 inline h-3.5 w-3.5" />
              Kanban
            </button>
            <button
              onClick={() => setView("list")}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${
                view === "list" ? "bg-primary shadow-sm" : "text-text-secondary"
              }`}
            >
              <ListTodo className="mr-1.5 inline h-3.5 w-3.5" />
              List
            </button>
            <button
              onClick={() => setView("calendar")}
              className={`rounded-md px-3 py-1.5 text-xs font-medium transition ${
                view === "calendar" ? "bg-primary shadow-sm" : "text-text-secondary"
              }`}
            >
              <CalendarIcon className="mr-1.5 inline h-3.5 w-3.5" />
              Calendar
            </button>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            AI Suggest
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            Add Task
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-x-auto p-6">
        <div className="flex h-full gap-4">
          {columns.map((column) => (
            <div key={column.id} className="flex w-72 shrink-0 flex-col rounded-xl border bg-secondary">
              <div className="flex items-center justify-between border-b px-4 py-3">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-semibold">{column.title}</h3>
                  <Badge variant="secondary" size="sm">{column.tasks.length}</Badge>
                </div>
                <Button variant="ghost" size="xs">
                  <Plus className="h-3.5 w-3.5" />
                </Button>
              </div>
              <div className="flex-1 space-y-2 overflow-y-auto p-3">
                {column.tasks.map((task) => (
                  <TaskCard key={task.id} task={task} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function TaskCard({ task }: { task: Task }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="group rounded-lg border bg-primary p-3 shadow-sm transition-all hover:shadow-md"
    >
      <div className="flex items-start gap-3">
        <button className="mt-0.5 shrink-0">
          <Circle className="h-4 w-4 text-text-tertiary transition-colors hover:text-accent" />
        </button>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium text-text-primary">{task.title}</p>
          {task.due_date && (
            <div className="mt-1.5 flex items-center gap-1.5 text-xs text-text-secondary">
              <Clock className="h-3 w-3" />
              {new Date(task.due_date).toLocaleDateString()}
            </div>
          )}
          <div className="mt-2 flex items-center gap-2">
            <PriorityBadge priority={task.priority} />
            <Badge variant="secondary" size="sm">
              <User className="mr-1 h-3 w-3" />
              Assign
            </Badge>
          </div>
        </div>
        <Button variant="ghost" size="xs" className="opacity-0 group-hover:opacity-100">
          <MoreHorizontal className="h-3.5 w-3.5" />
        </Button>
      </div>
    </motion.div>
  );
}

function PriorityBadge({ priority }: { priority: string }) {
  const config = {
    urgent: { icon: AlertCircle, color: "text-error", label: "Urgent" },
    high: { icon: Flag, color: "text-warning", label: "High" },
    medium: { icon: Circle, color: "text-info", label: "Medium" },
    low: { icon: Circle, color: "text-text-tertiary", label: "Low" },
  }[priority] || { icon: Circle, color: "text-text-tertiary", label: priority };

  const Icon = config.icon;
  return (
    <Badge variant="secondary" size="sm">
      <Icon className={`mr-1 h-3 w-3 ${config.color}`} />
      {config.label}
    </Badge>
  );
}

const columns: Column[] = [
  {
    id: "backlog",
    title: "Backlog",
    tasks: [
      { id: "1", title: "Research AI agents for automation", status: "backlog", priority: "high", due_date: "2026-07-01" },
      { id: "2", title: "Design new dashboard widgets", status: "backlog", priority: "medium", due_date: null },
    ],
  },
  {
    id: "todo",
    title: "To Do",
    tasks: [
      { id: "3", title: "Implement WebSocket reconnection", status: "todo", priority: "urgent", due_date: "2026-06-25" },
      { id: "4", title: "Add dark mode support", status: "todo", priority: "medium", due_date: null },
    ],
  },
  {
    id: "in_progress",
    title: "In Progress",
    tasks: [
      { id: "5", title: "Build note editor with slash commands", status: "in_progress", priority: "high", due_date: "2026-06-28" },
    ],
  },
  {
    id: "review",
    title: "Review",
    tasks: [
      { id: "6", title: "Refactor API client", status: "review", priority: "low", due_date: null },
    ],
  },
  {
    id: "done",
    title: "Done",
    tasks: [
      { id: "7", title: "Set up CI/CD pipeline", status: "done", priority: "high", due_date: "2026-06-20" },
      { id: "8", title: "Configure Docker Compose", status: "done", priority: "medium", due_date: "2026-06-19" },
    ],
  },
];
