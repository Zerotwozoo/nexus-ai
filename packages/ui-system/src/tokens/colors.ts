export const colors = {
  light: {
    bg: {
      primary: "#ffffff",
      secondary: "#f8f9fa",
      tertiary: "#f0f0f5",
      glass: "rgba(255, 255, 255, 0.7)",
    },
    border: "#e5e7eb",
    text: {
      primary: "#0a0a0f",
      secondary: "#6b7280",
      tertiary: "#9ca3af",
      inverse: "#ffffff",
    },
    accent: {
      DEFAULT: "#6366f1",
      hover: "#4f46e5",
      light: "#eef2ff",
      secondary: "#8b5cf6",
    },
    semantic: {
      success: "#10b981",
      successLight: "#d1fae5",
      warning: "#f59e0b",
      warningLight: "#fef3c7",
      error: "#ef4444",
      errorLight: "#fee2e2",
      info: "#3b82f6",
      infoLight: "#dbeafe",
    },
    chart: {
      line: "#6366f1",
      area: "rgba(99, 102, 241, 0.1)",
      bar: "#818cf8",
    },
  },
  dark: {
    bg: {
      primary: "#0a0a0f",
      secondary: "#12121a",
      tertiary: "#1a1a2e",
      glass: "rgba(10, 10, 15, 0.7)",
    },
    border: "#2a2a3e",
    text: {
      primary: "#f0f0f5",
      secondary: "#9ca3af",
      tertiary: "#6b7280",
      inverse: "#0a0a0f",
    },
    accent: {
      DEFAULT: "#818cf8",
      hover: "#6366f1",
      light: "rgba(99, 102, 241, 0.15)",
      secondary: "#a78bfa",
    },
    semantic: {
      success: "#34d399",
      successLight: "rgba(52, 211, 153, 0.15)",
      warning: "#fbbf24",
      warningLight: "rgba(251, 191, 36, 0.15)",
      error: "#f87171",
      errorLight: "rgba(248, 113, 113, 0.15)",
      info: "#60a5fa",
      infoLight: "rgba(96, 165, 250, 0.15)",
    },
    chart: {
      line: "#818cf8",
      area: "rgba(129, 140, 248, 0.1)",
      bar: "#6366f1",
    },
  },
} as const;
