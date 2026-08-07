#!/usr/bin/env node
/**
 * Scans kit/docs/skills/*.md → kit/generated/skills-registry.json
 * Agent-facing only — users never edit the registry.
 *
 * Usage (from kit/): npm run generate:registry
 *        (from repo root): node kit/scripts/generate-registry.js
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { parseFrontmatter } = require("./lib/frontmatter");

const KIT_ROOT = path.join(__dirname, "..");
const REPO_ROOT = path.join(KIT_ROOT, "..");
const SKILLS_DIR = path.join(KIT_ROOT, "docs", "skills");
const OUT = path.join(KIT_ROOT, "generated", "skills-registry.json");

const REQUIRED = ["name", "type", "category", "description"];

function loadSkills() {
  if (!fs.existsSync(SKILLS_DIR)) {
    console.error(`Missing skills dir: ${SKILLS_DIR}`);
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(OUT), { recursive: true });

  const files = fs
    .readdirSync(SKILLS_DIR)
    .filter((f) => f.endsWith(".md") && f !== "README.md")
    .sort();

  const skills = [];
  const errors = [];

  for (const file of files) {
    const relFromRepo = path.join("kit", "docs", "skills", file);
    const full = path.join(REPO_ROOT, relFromRepo);
    const content = fs.readFileSync(full, "utf8");
    const { data, hasFrontmatter } = parseFrontmatter(content);
    const hash = crypto.createHash("sha256").update(content).digest("hex").slice(0, 12);

    if (!hasFrontmatter) {
      errors.push(`${relFromRepo}: missing YAML frontmatter`);
      continue;
    }

    for (const key of REQUIRED) {
      if (data[key] === undefined || data[key] === null || data[key] === "") {
        errors.push(`${relFromRepo}: missing frontmatter field "${key}"`);
      }
    }

    skills.push({
      id: file.replace(/\.md$/, ""),
      name: data.name,
      type: data.type,
      category: data.category,
      description: data.description,
      usedFor: data.usedFor || [],
      appliesTo: data.appliesTo || [],
      requiredKnowledge: data.requiredKnowledge || [],
      conflicts: data.conflicts || [],
      mandatory: Boolean(data.mandatory),
      path: relFromRepo.replace(/\\/g, "/"),
      hash: `sha256:${hash}`,
    });
  }

  return { skills, errors };
}

function main() {
  const { skills, errors } = loadSkills();

  if (errors.length) {
    console.error("Registry generation failed:\n" + errors.map((e) => `  - ${e}`).join("\n"));
    process.exit(1);
  }

  const registry = {
    version: "1.0",
    generated: new Date().toISOString(),
    sourceOfTruth: "kit/docs/skills/*.md (agents only; humans edit agents.md + system-design.md + CHANGELOG.md)",
    skills,
  };

  fs.writeFileSync(OUT, JSON.stringify(registry, null, 2) + "\n", "utf8");
  console.log(`Wrote kit/generated/skills-registry.json (${skills.length} skills)`);
}

main();
