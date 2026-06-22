"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  ChevronLeft, ChevronRight, Plus, Sparkles,
  Clock, MapPin, Video,
} from "lucide-react";
import { motion } from "framer-motion";

type CalendarView = "month" | "week" | "day" | "agenda";

type Event = {
  id: string;
  title: string;
  time: string;
  duration: string;
  type: "meeting" | "reminder" | "focus";
};

export default function CalendarPage() {
  const [view, setView] = useState<CalendarView>("month");
  const [currentDate, setCurrentDate] = useState(new Date());

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Calendar</h1>
          <div className="flex items-center gap-1 rounded-lg bg-secondary p-0.5">
            {(["month", "week", "day", "agenda"] as CalendarView[]).map((v) => (
              <button
                key={v}
                onClick={() => setView(v)}
                className={`rounded-md px-3 py-1.5 text-xs font-medium capitalize transition ${
                  view === v ? "bg-primary shadow-sm" : "text-text-secondary"
                }`}
              >
                {v}
              </button>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            AI Schedule
          </Button>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            New Event
          </Button>
        </div>
      </div>

      <div className="flex flex-1">
        <div className="flex-1 p-6">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Button variant="ghost" size="sm">
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <h2 className="text-xl font-semibold">
                {currentDate.toLocaleString("default", { month: "long", year: "numeric" })}
              </h2>
              <Button variant="ghost" size="sm">
                <ChevronRight className="h-4 w-4" />
              </Button>
              <Button variant="secondary" size="sm">Today</Button>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-px overflow-hidden rounded-xl border bg-border">
            {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
              <div key={day} className="bg-secondary px-3 py-2 text-xs font-medium text-text-secondary">
                {day}
              </div>
            ))}
            {Array.from({ length: 35 }, (_, i) => {
              const day = i - 2;
              const isToday = day === new Date().getDate() - 1;
              return (
                <div
                  key={i}
                  className={`min-h-[100px] bg-primary p-2 transition-colors hover:bg-secondary/50 ${
                    day < 0 || day > 28 ? "text-text-tertiary" : ""
                  }`}
                >
                  <span
                    className={`inline-flex h-7 w-7 items-center justify-center rounded-full text-sm ${
                      isToday ? "bg-accent text-white" : ""
                    }`}
                  >
                    {day + 1}
                  </span>
                  {events
                    .filter((_, idx) => idx === i % events.length)
                    .map((event) => (
                      <div
                        key={event.id}
                        className="mt-1 cursor-pointer rounded-md bg-accent/10 px-2 py-1 text-xs text-accent transition-colors hover:bg-accent/20"
                      >
                        {event.title}
                      </div>
                    ))}
                </div>
              );
            })}
          </div>
        </div>

        <div className="w-80 border-l p-4">
          <h3 className="mb-3 text-sm font-semibold">Upcoming</h3>
          <div className="space-y-3">
            {events.map((event) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="rounded-lg border bg-primary p-3 transition-shadow hover:shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <Badge variant={event.type === "meeting" ? "primary" : event.type === "focus" ? "success" : "info"} size="sm">
                    {event.type}
                  </Badge>
                </div>
                <p className="mt-2 text-sm font-medium">{event.title}</p>
                <div className="mt-1.5 flex items-center gap-3 text-xs text-text-secondary">
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3" />
                    {event.time}
                  </span>
                  <span className="flex items-center gap-1">
                    <Video className="h-3 w-3" />
                    {event.duration}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

const events: Event[] = [
  { id: "1", title: "Sprint Planning", time: "10:00 AM", duration: "1h", type: "meeting" },
  { id: "2", title: "Design Review", time: "2:00 PM", duration: "30m", type: "meeting" },
  { id: "3", title: "Focus Block", time: "9:00 AM", duration: "2h", type: "focus" },
  { id: "4", title: "Pay Bills", time: "All day", duration: "", type: "reminder" },
];
