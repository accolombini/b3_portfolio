import pluginJs from "@eslint/js";
import pluginReact from "eslint-plugin-react";
import globals from "globals";
import tseslint from "typescript-eslint";

export default [
  { files: ["**/*.{js,mjs,cjs,ts,tsx}"] },
  { ignores: ["dist/**", "vite.config.ts"] },  // Ignora builds e configs Vite
  { languageOptions: { globals: globals.browser } },
  pluginJs.configs.recommended,
  ...tseslint.configs.recommended,
  pluginReact.configs.flat.recommended,
  {
    settings: { react: { version: "18.3" } },
    rules: {
      "react/jsx-uses-react": "off",  // Desliga para React 18+ JSX runtime
      "react/react-in-jsx-scope": "off",
      "@typescript-eslint/no-unused-vars": "warn"  // Ajuste para warn se preferir
    },
  },
];
