import { defineConfig } from "eslint";
import react from "eslint-plugin-react-hooks";
import refresh from "eslint-plugin-react-refresh";

export default defineConfig([
  {
    files: ["**/*.{ts,tsx}"],
    plugins: {
      "react-hooks": react,
      "react-refresh": refresh,
    },
    rules: {
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true },
      ],
    },
  },
]);
