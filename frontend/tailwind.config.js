/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Deep teal — the primary brand color. Chosen for a calm, clinical-but-warm
        // feel appropriate to a medical complaint system, rather than a generic
        // SaaS blue or an AI-cliche cream/terracotta palette.
        teal: {
          50: "#EAF3F1",
          100: "#CFE4DF",
          400: "#3A8C7E",
          500: "#1F6F63",
          600: "#195A51",
          700: "#134640",
        },
        // Warm coral — reserved ONLY for urgent/critical priority indicators,
        // so it stays meaningful instead of decorative.
        coral: {
          50: "#FDECE7",
          400: "#E4572E",
          500: "#C94A25",
        },
        ink: "#1B1F1D",
        paper: "#F7F8F7",
      },
      fontFamily: {
        display: ["Newsreader", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
