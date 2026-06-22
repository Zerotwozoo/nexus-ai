"use client";

import { useState } from "react";
import { Button, Badge } from "@nexus/ui-system";
import {
  FileText, Plus, Search, MoreHorizontal, Star,
  Archive, Trash2, Sparkles, Folder,
} from "lucide-react";
import { motion } from "framer-motion";

type Note = {
  id: string;
  title: string;
  icon: string | null;
  color: string | null;
  updated_at: string;
  is_archived: boolean;
};

export default function NotesPage() {
  const [search, setSearch] = useState("");
  const [selectedNote, setSelectedNote] = useState<string | null>(null);

  return (
    <div className="flex h-full">
      <div className="flex w-80 flex-col border-r">
        <div className="flex items-center justify-between border-b px-4 py-3">
          <h2 className="text-sm font-semibold text-text-primary">Notes</h2>
          <Button size="sm" leftIcon={<Plus className="h-3.5 w-3.5" />}>
            New Note
          </Button>
        </div>

        <div className="border-b px-4 py-2">
          <div className="flex items-center gap-2 rounded-lg border bg-secondary px-3 py-1.5">
            <Search className="h-4 w-4 text-text-tertiary" />
            <input
              className="flex-1 bg-transparent text-sm outline-none placeholder:text-text-tertiary"
              placeholder="Search notes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto">
          <div className="space-y-0.5 p-2">
            {notes.map((note) => (
              <motion.button
                key={note.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => setSelectedNote(note.id)}
                className={`w-full rounded-lg px-3 py-2.5 text-left transition-all ${
                  selectedNote === note.id
                    ? "bg-accent text-white"
                    : "hover:bg-secondary"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Folder className="h-4 w-4 shrink-0 text-text-tertiary" />
                  <div className="min-w-0 flex-1">
                    <p className={`truncate text-sm font-medium ${
                      selectedNote === note.id ? "text-white" : "text-text-primary"
                    }`}>
                      {note.title}
                    </p>
                    <p className={`truncate text-xs ${
                      selectedNote === note.id ? "text-white/70" : "text-text-tertiary"
                    }`}>
                      {new Date(note.updated_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </div>

        <div className="border-t p-2">
          <div className="flex items-center gap-1">
            <Button variant="ghost" size="sm" fullWidth leftIcon={<Archive className="h-3.5 w-3.5" />}>
              Archive
            </Button>
            <Button variant="ghost" size="sm" fullWidth leftIcon={<Trash2 className="h-3.5 w-3.5" />}>
              Trash
            </Button>
          </div>
        </div>
      </div>

      <div className="flex flex-1 flex-col">
        {selectedNote ? (
          <>
            <div className="flex items-center justify-between border-b px-6 py-3">
              <div className="flex items-center gap-2">
                <Badge variant="primary" size="sm">
                  <Sparkles className="mr-1 h-3 w-3" />
                  AI
                </Badge>
                <Button variant="ghost" size="sm">Summarize</Button>
                <Button variant="ghost" size="sm">Rewrite</Button>
                <Button variant="ghost" size="sm">Translate</Button>
              </div>
              <div className="flex items-center gap-1">
                <Button variant="ghost" size="sm">
                  <Star className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-6">
              <div className="mx-auto max-w-3xl">
                <div className="mb-1 text-xs text-text-tertiary">
                  Updated just now
                </div>
                <input
                  className="mb-6 w-full text-3xl font-bold outline-none placeholder:text-text-tertiary"
                  placeholder="Untitled"
                  defaultValue="Welcome to Nexus AI Notes"
                />
                <div
                  className="prose prose-sm max-w-none text-text-primary"
                  contentEditable
                  suppressContentEditableWarning
                >
                  <p>Start writing here... Use <code>/</code> for commands.</p>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="flex flex-1 items-center justify-center">
            <div className="text-center">
              <FileText className="mx-auto h-12 w-12 text-text-tertiary" />
              <h3 className="mt-4 text-lg font-medium">Select a note</h3>
              <p className="mt-1 text-sm text-text-secondary">
                Choose a note from the list or create a new one
              </p>
              <Button className="mt-4" leftIcon={<Plus className="h-4 w-4" />}>
                New Note
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const notes: Note[] = [
  { id: "1", title: "Welcome to Nexus AI Notes", icon: null, color: null, updated_at: new Date().toISOString(), is_archived: false },
  { id: "2", title: "Project Architecture Decisions", icon: null, color: "blue", updated_at: new Date(Date.now() - 3600000).toISOString(), is_archived: false },
  { id: "3", title: "Meeting Notes - Q3 Planning", icon: null, color: "green", updated_at: new Date(Date.now() - 7200000).toISOString(), is_archived: false },
];
