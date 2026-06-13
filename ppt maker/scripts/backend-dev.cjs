"use strict";

/**
 * Ensures backend/.venv exists, installs requirements, then runs uvicorn on :8000.
 * Cross-platform (Windows / macOS / Linux).
 */
const { spawn, spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const backend = path.join(root, "backend");
const isWin = process.platform === "win32";
const venvDir = path.join(backend, ".venv");
const pyExe = isWin ? path.join(venvDir, "Scripts", "python.exe") : path.join(venvDir, "bin", "python");
const pipExe = isWin ? path.join(venvDir, "Scripts", "pip.exe") : path.join(venvDir, "bin", "pip");

function run(cmd, args, options = {}) {
  const r = spawnSync(cmd, args, {
    stdio: "inherit",
    cwd: backend,
    env: process.env,
    ...options,
  });
  return (r.status ?? 1) === 0;
}

function ensureVenv() {
  if (fs.existsSync(pyExe)) {
    return true;
  }
  console.log("[SlideGen] Creating backend/.venv …");
  const attempts = [
    ["python", ["-m", "venv", ".venv"]],
    ["py", ["-3", "-m", "venv", ".venv"]],
    ["python3", ["-m", "venv", ".venv"]],
  ];
  for (const [cmd, args] of attempts) {
    if (run(cmd, args, { shell: isWin && cmd === "py" })) {
      break;
    }
  }
  if (!fs.existsSync(pyExe)) {
    console.error("[SlideGen] Install Python 3.10+ and ensure `python` is on PATH, then retry.");
    process.exit(1);
  }
  return true;
}

function ensureDeps() {
  console.log("[SlideGen] pip install -r requirements.txt …");
  if (!fs.existsSync(pipExe)) {
    console.error("[SlideGen] pip not found in venv.");
    process.exit(1);
  }
  if (!run(pipExe, ["install", "-r", "requirements.txt"])) {
    process.exit(1);
  }
}

function main() {
  const installOnly = process.argv.includes("--install-only");
  ensureVenv();
  ensureDeps();
  if (installOnly) {
    console.log("[SlideGen] Backend dependencies ready.");
    process.exit(0);
  }

  console.log("[SlideGen] Starting API at http://127.0.0.1:8000 …");
  const proc = spawn(pyExe, ["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"], {
    cwd: backend,
    stdio: "inherit",
    env: process.env,
  });
  proc.on("exit", (code) => process.exit(code ?? 1));
}

main();
