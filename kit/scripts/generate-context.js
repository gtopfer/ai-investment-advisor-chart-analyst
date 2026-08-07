#!/usr/bin/env node
/**
 * Derives kit/generated/project-context.json from root agents.md + system-design.md.
 *
 * Humans edit: agents.md, system-design.md, CHANGELOG.md (repo root only).
 *
 * Usage (from kit/): npm run generate:context
 */

const fs = require("fs");
const path = require("path");

const KIT_ROOT = path.join(__dirname, "..");
const REPO_ROOT = path.join(KIT_ROOT, "..");
const DEFAULT_AGENTS = path.join(REPO_ROOT, "agents.md");
const SYSTEM_DESIGN = path.join(REPO_ROOT, "system-design.md");
const OUT = path.join(KIT_ROOT, "generated", "project-context.json");
const REGISTRY = path.join(KIT_ROOT, "generated", "skills-registry.json");

function sectionAfter(text, headingRe, stopRe) {
  const m = text.match(headingRe);
  if (!m) return "";
  const start = m.index + m[0].length;
  const rest = text.slice(start);
  const stop = rest.search(stopRe);
  return (stop === -1 ? rest : rest.slice(0, stop)).trim();
}

function bullets(block) {
  return block
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l.startsWith("- "))
    .map((l) => l.replace(/^- /, "").trim())
    .filter(Boolean);
}

function labeledList(block) {
  const out = {};
  for (const line of bullets(block)) {
    const m = line.match(/^([^:]+):\s*(.*)$/);
    if (m) out[m[1].trim().toLowerCase()] = m[2].trim();
    else out[line.toLowerCase()] = true;
  }
  return out;
}

function extractProjectName(section1) {
  const m = section1.match(/###\s*Projeto:\s*(.+)/i);
  return m ? m[1].trim() : "unnamed-project";
}

function extractLabeledParagraph(section1, label) {
  const re = new RegExp(
    `\\*\\*${label}:\\*\\*\\s*\\n([\\s\\S]*?)(?=\\n\\*\\*[A-Za-zÀ-ú ]+:\\*\\*|\\n### |$)`,
    "i"
  );
  const m = section1.match(re);
  if (!m) return "";
  return m[1].trim();
}

function extractStack(section1) {
  return labeledList(extractLabeledParagraph(section1, "Stack"));
}

function extractUsers(section1) {
  const block = extractLabeledParagraph(section1, "Usuários");
  const lines = bullets(block);
  if (lines.length) return lines;
  const plain = block.replace(/\n+/g, " ").trim();
  return plain ? [plain] : [];
}

function extractGuardrails(section1) {
  const block =
    extractLabeledParagraph(section1, "Guardrails Obrigatórios") ||
    extractLabeledParagraph(section1, "Guardrails");
  return bullets(block);
}

function extractConventions(section1) {
  return labeledList(extractLabeledParagraph(section1, "Convenções"));
}

function extractContext(section1) {
  return extractLabeledParagraph(section1, "Contexto");
}

function loadSkillIds() {
  if (!fs.existsSync(REGISTRY)) return [];
  try {
    const reg = JSON.parse(fs.readFileSync(REGISTRY, "utf8"));
    return (reg.skills || []).map((s) => s.id);
  } catch {
    return [];
  }
}

function main() {
  const agentsPath = path.resolve(process.argv[2] || DEFAULT_AGENTS);
  if (!fs.existsSync(agentsPath)) {
    console.error(`agents.md not found: ${agentsPath}`);
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(OUT), { recursive: true });

  const text = fs.readFileSync(agentsPath, "utf8");
  const section1 = sectionAfter(
    text,
    /##[^\n]*SEÇÃO 1[^\n]*\n/i,
    /\n##[^\n]*SEÇÃO 2/i
  );

  if (!section1) {
    console.error("Could not find SEÇÃO 1 in agents.md");
    process.exit(1);
  }

  const name = extractProjectName(section1);
  const stack = extractStack(section1);
  const context = extractContext(section1);
  const users = extractUsers(section1);
  const guardrails = extractGuardrails(section1);
  const conventions = extractConventions(section1);
  const skills = loadSkillIds();
  const hasSystemDesign = fs.existsSync(SYSTEM_DESIGN);
  let systemDesignStatus = "missing";
  if (hasSystemDesign) {
    const sd = fs.readFileSync(SYSTEM_DESIGN, "utf8");
    const placeholder =
      /\[Nome do Projeto\]|\[1–3 frases\]|\[tecnologia\]|Preencha as seções/i.test(sd);
    systemDesignStatus = placeholder ? "template-unfilled" : "present";
  }

  const projectContext = {
    version: "1.2",
    generated: new Date().toISOString(),
    sourceOfTruth: {
      product: "agents.md",
      systemDesign: "system-design.md",
      changelog: "CHANGELOG.md",
    },
    userConfigSurface: ["agents.md", "system-design.md", "CHANGELOG.md"],
    kitRoot: "kit/",
    name,
    description: context,
    stack,
    users,
    conventions,
    guardrails: {
      mustHave: guardrails.filter((g) => !/^sem |não |do not |never /i.test(g)),
      mustNOT: guardrails.filter((g) => /^sem |não |do not |never /i.test(g)),
      all: guardrails,
    },
    systemDesign: {
      path: "system-design.md",
      status: systemDesignStatus,
      note: "Agents must read system-design.md for architecture (§2) and design system (§3).",
    },
    skills,
    notes: [
      "Generated — do not hand-edit.",
      "Humans only edit root: agents.md, system-design.md, CHANGELOG.md.",
      "Kit lives under kit/. Regenerate: cd kit && npm run generate:context",
    ],
  };

  fs.writeFileSync(OUT, JSON.stringify(projectContext, null, 2) + "\n", "utf8");
  console.log(`Wrote kit/generated/project-context.json (project: ${name})`);
}

main();
