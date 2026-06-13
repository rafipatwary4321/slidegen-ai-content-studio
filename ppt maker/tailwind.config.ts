import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./hooks/**/*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 0 0 1px rgba(139, 92, 246, 0.5), 0 8px 40px rgba(59, 130, 246, 0.35)"
      },
      backgroundImage: {
        "hero-gradient": "radial-gradient(circle at 20% -10%, rgba(147,51,234,0.45), transparent 36%), radial-gradient(circle at 88% 10%, rgba(6,182,212,0.35), transparent 32%), linear-gradient(180deg, #09090f 0%, #030712 100%)"
      }
    }
  },
  plugins: []
};

export default config;
