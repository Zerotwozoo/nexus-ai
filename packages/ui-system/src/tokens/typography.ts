export const typography = {
  fontFamily: {
    sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"].join(", "),
    mono: ['"JetBrains Mono"', '"Fira Code"', "monospace"].join(", "),
  },
  fontSize: {
    xs: ["0.75rem", { lineHeight: "1rem", letterSpacing: "0.01em" }],
    sm: ["0.875rem", { lineHeight: "1.25rem", letterSpacing: "0.01em" }],
    base: ["1rem", { lineHeight: "1.5rem", letterSpacing: "0" }],
    lg: ["1.125rem", { lineHeight: "1.75rem", letterSpacing: "0" }],
    xl: ["1.25rem", { lineHeight: "1.75rem", letterSpacing: "-0.01em" }],
    "2xl": ["1.5rem", { lineHeight: "2rem", letterSpacing: "-0.01em" }],
    "3xl": ["2rem", { lineHeight: "2.5rem", letterSpacing: "-0.02em" }],
    "4xl": ["2.5rem", { lineHeight: "3rem", letterSpacing: "-0.02em" }],
    "5xl": ["3rem", { lineHeight: "3.5rem", letterSpacing: "-0.03em" }],
  },
  fontWeight: {
    normal: "400",
    medium: "500",
    semibold: "600",
    bold: "700",
  },
} as const;
