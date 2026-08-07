#!/usr/bin/env node
/**
 * Validates docs/skills/*.md against the kit skill checklist.
 * For kit maintainers / CI — not a user-facing step.
 *
 * Usage: node scripts/validate-skills.js [optional path to one skill]
 */

const fs = require("fs");
const path = require("path");
const { parseFrontmatter } = require("./lib/frontmatter");

const KIT_ROOT = path.join(__dirname, "..");
const REPO_ROOT = path.join(KIT_ROOT, "..");
const ROOT = KIT_ROOT; // for relative paths in messages
const SKILLS_DIR = path.join(KIT_ROOT, "docs", "skills");

const REQUIRED_META = ["name", "type", "category", "description"];
const RECOMMENDED_META = ["usedFor", "appliesTo", "requiredKnowledge"];
const ALLOWED_TYPES = [
  "development",
  "documentation",
  "design",
  "knowledge",
  "refinement",
  "architecture",
];
const ALLOWED_CATEGORIES = [
  "quality",
  "design",
  "organization",
  "documentation",
  "knowledge",
  "infra",
];

function hasSection(body, titles) {
  const lower = body.toLowerCase();
  return titles.some((t) => lower.includes(t.toLowerCase()));
}

function validateFile(fullPath) {
  const rel = path.relative(ROOT, fullPath);
  const content = fs.readFileSync(fullPath, "utf8");
  const { data, body, hasFrontmatter } = parseFrontmatter(content);
  const errors = [];
  const warnings = [];

  if (!hasFrontmatter) {
    errors.push("missing YAML frontmatter (--- ... ---)");
    return { rel, errors, warnings };
  }

  for (const key of REQUIRED_META) {
    if (data[key] === undefined || data[key] === null || data[key] === "") {
      errors.push(`missing required frontmatter: ${key}`);
    }
  }

  if (data.description && String(data.description).length > 1024) {
    errors.push("description must be < 1024 characters");
  }

  if (data.type && !ALLOWED_TYPES.includes(data.type)) {
    warnings.push(`type "${data.type}" not in standard set: ${ALLOWED_TYPES.join(", ")}`);
  }

  if (data.category && !ALLOWED_CATEGORIES.includes(data.category)) {
    warnings.push(
      `category "${data.category}" not in standard set: ${ALLOWED_CATEGORIES.join(", ")}`
    );
  }

  for (const key of RECOMMENDED_META) {
    if (data[key] === undefined) {
      warnings.push(`recommended frontmatter missing: ${key}`);
    }
  }

  if (!hasSection(body, ["## quando usar", "## when to use"])) {
    errors.push('missing "## Quando usar" (or When to use) section');
  }

  if (!hasSection(body, ["## quando não usar", "## when not to use", "## do not use"])) {
    errors.push('missing "## Quando NÃO usar" section (prevents skill overlap)');
  }

  // Soft checks
  if (!hasSection(body, ["exemplo", "checklist", "anti-padr", "anti-pattern"])) {
    warnings.push("consider adding examples, checklist, or anti-patterns");
  }

  if (/<[a-zA-Z][^>]*>/.test(body) && !body.includes("```")) {
    warnings.push("HTML-like tags outside code fences may confuse some agents");
  }

  return { rel, errors, warnings };
}

function listSkillFiles() {
  return fs
    .readdirSync(SKILLS_DIR)
    .filter((f) => f.endsWith(".md") && f !== "README.md")
    .map((f) => path.join(SKILLS_DIR, f));
}

function main() {
  const arg = process.argv[2];
  const files = arg
    ? [path.resolve(arg)]
    : listSkillFiles();

  let failed = 0;
  let warnCount = 0;

  for (const file of files) {
    if (!fs.existsSync(file)) {
      console.error(`FAIL ${file}: not found`);
      failed++;
      continue;
    }
    const { rel, errors, warnings } = validateFile(file);
    if (errors.length) {
      failed++;
      console.error(`FAIL ${rel}`);
      errors.forEach((e) => console.error(`  ✗ ${e}`));
    } else {
      console.log(`OK   ${rel}`);
    }
    warnings.forEach((w) => {
      warnCount++;
      console.warn(`  ⚠ ${w}`);
    });
  }

  console.log(
    `\nValidated ${files.length} skill(s): ${files.length - failed} ok, ${failed} failed, ${warnCount} warning(s)`
  );
  process.exit(failed ? 1 : 0);
}

main();
