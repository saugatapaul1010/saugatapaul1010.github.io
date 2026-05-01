# Blog — "The Top-1% Claude Code Setup"

**Generated:** 2026-04-26 (UTC)
**Author:** Saugata Paul
**Target venue:** Medium (also publishable on dev.to / personal blog / Substack)

This folder contains the published artifact + every source asset that built it. Self-contained — clone or copy this folder anywhere and you can re-publish, re-render, or remix.

---

## What's here

```
Blog/
├── README.md                              ← this file
├── top-1-claude-code-setup.md             ← the blog itself (~12K words)
├── diagrams/                              ← 10 PNGs referenced from the blog
│   ├── 01-iceberg.png
│   ├── 02-hook-fire-order.png
│   ├── 03-statusline-anatomy.png
│   ├── 04-memory-ladder.png
│   ├── 05-skill-invocation-flow.png
│   ├── 06-agent-decision-tree.png
│   ├── 07-mcp-fleet-topology.png
│   ├── 08-mission-lifecycle.png
│   ├── 09-weekly-composition.png
│   └── 10-setup-architecture.png
└── source/                                ← editable diagram sources
    ├── 01-iceberg.html                    ← HTML mockup → PNG via headless chrome
    ├── 02-hook-fire-order.mmd             ← Mermaid → PNG via mmdc
    ├── 03-statusline-anatomy.html
    ├── 04-memory-ladder.mmd
    ├── 05-skill-invocation-flow.mmd
    ├── 06-agent-decision-tree.mmd
    ├── 07-mcp-fleet-topology.mmd
    ├── 08-mission-lifecycle.mmd
    ├── 09-weekly-composition.html
    ├── 10-setup-architecture.mmd
    ├── mermaid-config.json                ← Mermaid theme overrides
    └── puppeteer-config.json              ← Points mmdc at the installed chrome
```

---

## Reading order

If you're a **developer who wants to replicate the setup**: open `top-1-claude-code-setup.md`. Follow Layer 9 to build the kit and run the 12-step recipe. Expected time: 60–90 minutes.

If you're a **technical writer or editor**: open `top-1-claude-code-setup.md` and read top-to-bottom. The Table of Contents at the top maps the 11 layers (Layer 0 → Layer 10 + 3 appendices).

If you're a **content creator looking for inspiration**: see how the post composes hooks + statusline + memory + skills + agents + MCPs. Each layer is independently useful but the value compounds.

---

## Publishing to Medium

Medium renders standard CommonMark + image embeds. The post is already structured for that:

1. **Cover image:** use `diagrams/01-iceberg.png` (1500×1300 px). Medium auto-crops landscape; the iceberg has its visual weight in the upper third, which renders well after crop.
2. **Subtitle:** `"Hooks, statusline, layered memory, 36 specialist agents, 5 MCPs, project bootstrap — the full stack, in one post, for any language and any project."`
3. **Tags / hashtags:** `#ClaudeCode` `#AICoding` `#DeveloperTools` `#LLMs` `#AnthropicAPI` `#AgenticAI` `#Productivity`
4. **Image upload:** Medium hosts images on its own CDN. Either upload each PNG manually as you scroll past the reference, or use the Medium API import flow (which fetches `diagrams/*.png` from a public URL).
5. **Code blocks:** Medium supports fenced code with syntax highlighting. The post uses `bash`, `json`, `python`, `yaml`, and `markdown` fences — all render natively.

---

## Re-rendering the diagrams

Tooling required (one-time):

```bash
# mermaid-cli (renders .mmd → .png)
npm install -g @mermaid-js/mermaid-cli

# puppeteer's bundled chrome (mmdc needs this)
npx puppeteer browsers install chrome-headless-shell

# any chrome / chromium / chrome-headless-shell binary for HTML mockups
```

Then to re-render everything:

```bash
cd Blog/

# Mermaid diagrams → PNG
for src in source/*.mmd; do
  base=$(basename "$src" .mmd)
  mmdc -i "$src" -o "diagrams/${base}.png" \
    -c source/mermaid-config.json \
    -p source/puppeteer-config.json \
    -b white -s 2 -w 1600
done

# HTML mockups → PNG (chromium headless)
CHROME=$(find ~/.cache/puppeteer -name 'chrome-headless-shell' -type f | head -1)
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1500,1300 --screenshot=diagrams/01-iceberg.png \
  --virtual-time-budget=3000 \
  "file://$(realpath source/01-iceberg.html)"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=2000,1100 --screenshot=diagrams/03-statusline-anatomy.png \
  --virtual-time-budget=3000 \
  "file://$(realpath source/03-statusline-anatomy.html)"
"$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1500,1700 --screenshot=diagrams/09-weekly-composition.png \
  --virtual-time-budget=3000 \
  "file://$(realpath source/09-weekly-composition.html)"
```

The `puppeteer-config.json` exists because newer versions of the puppeteer-bundled chrome may not match the version mmdc was compiled against. The config points mmdc at whichever chrome-headless-shell is installed under `~/.cache/puppeteer/`. If your puppeteer version drifts, regenerate the config file:

```bash
CHROME=$(find ~/.cache/puppeteer -name 'chrome-headless-shell' -type f | head -1)
cat > source/puppeteer-config.json <<EOF
{
  "executablePath": "$CHROME",
  "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
}
EOF
```

---

## Editing the diagrams

- **Mermaid (`.mmd`)** — edit in any text editor, re-render via `mmdc`. The Mermaid Live Editor (https://mermaid.live) is useful for previewing without re-running the CLI.
- **HTML mockups (`.html`)** — open in a browser to preview while editing. Re-screenshot with chromium headless when done. Layout is hand-tuned CSS Grid + flexbox; widen the body or window if you add content.
- **Theme** — `source/mermaid-config.json` defines the color palette. The HTML mockups have inline `<style>` blocks; edit there for color/font changes.

---

## Editing the blog itself

Three things to know:

1. **Word budget.** The post is currently ~11,900 words. Below 8K loses depth; above 18K loses readers. Add or trim accordingly.
2. **Structure.** Layered (Layer 0 → Layer 10) and each layer is independently digestible. Reorganizing within a layer is fine; reorganizing across layers breaks the narrative.
3. **Voice.** First-person, opinionated, story-driven. The opening `.env` story is the hook — replace it only with another concrete failure story, not a generic intro.

Code blocks should always:
- Be tested on a real machine before publishing.
- Use absolute paths (`~/.claude/...`) so they're copy-pasteable.
- Annotate non-obvious lines with brief inline comments.

---

## Provenance

Built end-to-end during one Claude Code session on 2026-04-26 by:

1. Three parallel `Explore` agents inventoried the user's `~/.claude/` setup, MCP servers, plugins, archive, replication kit.
2. Plan file written + reviewed via plan mode.
3. Source files read verbatim (settings.json, all 4 hooks, statusline.sh, project-bootstrap SKILL.md, gemini server.py, replication recipe).
4. 10 diagram sources authored (7 Mermaid + 3 HTML).
5. Diagrams rendered to PNG (mermaid-cli + chromium headless).
6. Main blog markdown written referencing the diagrams.
7. Adversarial second-opinion via `gemini_second_opinion` (or `gemini_long_context` against the full markdown).
8. README.md (this file) authored last.

Total time end-to-end: ~75 minutes. Full session transcript will be archived to `~/claude-archive/2026/04/Claude_Total_Replication/<session-id>/` by the Stop hook on `/exit`.

---

## License

The blog post is shared in the spirit that good developer setups should be public.  Use it. Adapt it. Improve it. Credit if you want; don't sweat it if you don't. The configurations, scripts, and diagrams in this folder are provided "as-is" with no warranty — test on a non-critical machine first.

— Saugata Paul · saugata.paul1010@gmail.com
