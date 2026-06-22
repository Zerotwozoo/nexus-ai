"use client";

import { Button, Badge } from "@nexus/ui-system";
import {
  FileText, Upload, Search, Download, Trash2,
  Sparkles, FileImage, File,
} from "lucide-react";
import { motion } from "framer-motion";

export default function DocumentsPage() {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-6 py-3">
        <h1 className="text-lg font-semibold">Documents</h1>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
            AI Analyze
          </Button>
          <Button size="sm" leftIcon={<Upload className="h-3.5 w-3.5" />}>
            Upload
          </Button>
        </div>
      </div>

      <div className="border-b px-6 py-3">
        <div className="flex items-center gap-2 rounded-lg border bg-secondary px-3 py-1.5">
          <Search className="h-4 w-4 text-text-tertiary" />
          <input
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-text-tertiary"
            placeholder="Search documents..."
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {documents.map((doc, i) => (
            <motion.div
              key={doc.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="group rounded-xl border bg-primary p-4 transition-all hover:shadow-md"
            >
              <div className="mb-3 flex items-start justify-between">
                <div className="rounded-lg bg-accent/10 p-2.5">
                  <FileText className="h-6 w-6 text-accent" />
                </div>
                <Button variant="ghost" size="xs" className="opacity-0 group-hover:opacity-100">
                  <Trash2 className="h-3.5 w-3.5 text-text-secondary" />
                </Button>
              </div>
              <h3 className="truncate text-sm font-medium">{doc.name}</h3>
              <div className="mt-1 flex items-center gap-2 text-xs text-text-secondary">
                <span>{doc.size}</span>
                <span>·</span>
                <Badge variant="secondary" size="sm">{doc.type}</Badge>
              </div>
              <div className="mt-3 flex items-center gap-1">
                <Button variant="ghost" size="xs" fullWidth leftIcon={<Download className="h-3 w-3" />}>
                  Download
                </Button>
                <Button variant="ghost" size="xs" leftIcon={<Sparkles className="h-3 w-3" />}>
                  AI
                </Button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

const documents = [
  { id: "1", name: "Q3 Financial Report.pdf", size: "2.4 MB", type: "PDF" },
  { id: "2", name: "Project Proposal.docx", size: "1.1 MB", type: "DOCX" },
  { id: "3", name: "Meeting Notes - 2026-06-15", size: "234 KB", type: "TXT" },
  { id: "4", name: "Architecture Diagram.png", size: "3.7 MB", type: "PNG" },
];
