/**
 * Minimal YAML-like frontmatter parser for jojo-ai skills.
 * Supports: strings, numbers, booleans, and simple [a, b] arrays.
 * No external dependencies — zero install for the kit consumer.
 */

function parseScalar(raw) {
  const v = raw.trim();
  if (v === "true") return true;
  if (v === "false") return false;
  if (v === "null" || v === "~" || v === "") return null;
  if (/^-?\d+(\.\d+)?$/.test(v)) return Number(v);
  if (
    (v.startsWith('"') && v.endsWith('"')) ||
    (v.startsWith("'") && v.endsWith("'"))
  ) {
    return v.slice(1, -1);
  }
  if (v.startsWith("[") && v.endsWith("]")) {
    const inner = v.slice(1, -1).trim();
    if (!inner) return [];
    return inner.split(",").map((item) => parseScalar(item));
  }
  return v;
}

/**
 * @param {string} content
 * @returns {{ data: Record<string, unknown>, body: string, hasFrontmatter: boolean }}
 */
function parseFrontmatter(content) {
  const text = content.replace(/^\uFEFF/, "");
  if (!text.startsWith("---\n") && !text.startsWith("---\r\n")) {
    return { data: {}, body: text, hasFrontmatter: false };
  }

  const end = text.indexOf("\n---", 3);
  if (end === -1) {
    return { data: {}, body: text, hasFrontmatter: false };
  }

  const block = text.slice(4, end).replace(/\r/g, "");
  const body = text.slice(end + 4).replace(/^\r?\n/, "");
  const data = {};

  for (const line of block.split("\n")) {
    if (!line.trim() || line.trim().startsWith("#")) continue;
    const m = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!m) continue;
    data[m[1]] = parseScalar(m[2]);
  }

  return { data, body, hasFrontmatter: true };
}

module.exports = { parseFrontmatter, parseScalar };
