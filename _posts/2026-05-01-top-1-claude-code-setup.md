---
layout: post
title: "The Top-1% Claude Code Setup: A Complete Foundation for Any Project"
date: 2026-05-01
author: Saugata Paul
tags: [claude-code, ai-coding, llms, developer-tools, agentic-ai, productivity]
image: /diagrams/00-cover.png
---

![The Top-1% Claude Code Setup](/diagrams/00-cover.png)

> *"The bottleneck stopped being how fast Claude can write code. The bottleneck became how well I'd set Claude up to do its job."*

---

## Table of Contents

- [1. Why this post exists.](#1-why-this-post-exists)
- [2. Layer 0 - What default Claude Code already gives you.](#2-layer-0---what-default-claude-code-already-gives-you)
- [3. Layer 1 - The safety net: hooks + permission deny rules.](#3-layer-1---the-safety-net-hooks--permission-deny-rules)
- [4. Layer 2 - The statusline: real-time awareness.](#4-layer-2---the-statusline-real-time-awareness)
- [5. Layer 3 - Memory architecture.](#5-layer-3---memory-architecture)
- [6. Layer 4 - Skills: the verbs.](#6-layer-4---skills-the-verbs)
- [7. Layer 5 - Agents: the specialists.](#7-layer-5---agents-the-specialists)
- [8. Layer 6 - MCP servers: external minds.](#8-layer-6---mcp-servers-external-minds)
- [9. Layer 7 - The plugin ecosystem.](#9-layer-7---the-plugin-ecosystem)
- [10. Layer 8 - `project-bootstrap`: the day-1 workflow.](#10-layer-8---project-bootstrap-the-day-1-workflow)
- [11. Layer 9 - Backup, replication, and the portable kit.](#11-layer-9---backup-replication-and-the-portable-kit)
- [12. Layer 10 - A day in the life.](#12-layer-10---a-day-in-the-life)
- [13. Live demo: watch the system build a real app in under an hour.](#13-live-demo-watch-the-system-build-a-real-app-in-under-an-hour)
- [14. Best practices - the do's, the don'ts, and how the mechanism actually works.](#14-best-practices---the-dos-the-donts-and-how-the-mechanism-actually-works)
- [15. Key takeaways - what to remember if you only remember nine things.](#15-key-takeaways---what-to-remember-if-you-only-remember-nine-things)
- [16. Appendix A - Full file index.](#16-appendix-a---full-file-index)
- [17. Appendix B - Troubleshooting.](#17-appendix-b---troubleshooting)
- [18. Appendix C - Extending with your own custom agent / skill / MCP.](#18-appendix-c---extending-with-your-own-custom-agent--skill--mcp)
- [19. Closing.](#19-closing)
- [20. Get the setup.](#20-get-the-setup)
- [21. Thank you, and a few names.](#21-thank-you-and-a-few-names)
- [22. Got a better idea? Tell me.](#22-got-a-better-idea-tell-me)

---

## 1. Why this post exists.

I had a small heart attack on a Sunday afternoon.

I had set a `Read(.env)` deny rule in `~/.claude/settings.json` weeks before. Belt and braces. *Never* let the assistant peek at my secrets. Then I asked Claude to debug a webhook that wasn't firing. Without thinking - and without me thinking either - it ran `cat .env` to inspect the environment variables. The output streamed past in the transcript. My OpenAI key. My GitHub token. My Stripe **live** key. Sitting in plain text inside a session log that gets archived to disk and rotated to who-knows-where.

I sat there for about thirty seconds, not breathing.

The Claude Code permission system isn't broken. The `Read` deny rule did exactly what the docs say it does. The problem is that `Read(.env)` and `Bash(cat .env)` are *different tools*. Different code path. Different gate. Same blast radius. The deny list never had a chance.

That afternoon was when I stopped using Claude Code the way it ships and started building a setup around it.

Two-plus years of evenings and weekends went into that setup. It began as a side project on a high-frequency-trading codebase - but every single layer has since transferred, unchanged, to the rest of my work. Rust hot-paths. Nanosecond-level market-data ingestion. Trading-execution pipelines. Order-book engines. Cross-system architecture reviews. The engineering-excellence playbook I run on every codebase I touch. And, at the lighter end, React side projects, Python data-pipeline experiments, static-site builds, and the dozen smaller repos I keep on my laptop. **The codebase doesn't matter; the discipline does.**

Today, that setup is:

- 36 specialist agents
- 6 custom skills
- 5 MCP servers
- 4 lifecycle hooks
- a 223-line statusline that paints my context-window usage in a per-pixel RGB gradient
- a four-tier memory architecture that survives across sessions
- a `~/claude-archive/` I'll be able to `grep` in 2031
- a knowledge graph that auto-regenerates on every commit
- a `project-bootstrap` skill that scaffolds a brand-new repo into all of the above in thirty seconds

The whole thing — every layer above plus my personal session archive — sits in roughly 65 MB on my disk. The *open-source infrastructure subset* (hooks, skills, generic agents, statusline, the team-plugin scaffold) is **under 1 MB** as a tarball. I can transplant either onto a new laptop and be productive again in minutes.

### What you actually get out of this - concretely, in benefits, not features

If you stop reading right here, take this list with you. **Every one of these is a measurable, daily outcome of the setup, not a marketing claim:**

- **Zero-minute warm-up in the morning.** You open Claude. It already knows what you and it decided yesterday. The auto-memory loads it; the workbook from last night holds the cursor. You type *"continue"* and you're working. The 15-minute morning context dump that you've been paying every day since you started using Claude Code? Gone.
- **A safety net you can actually trust.** No more *"wait, did Claude just `cat .env`?"* The hook layer catches `.env` access, `rm -rf /`, `curl | bash`, fork bombs, and a dozen other footguns *across all tools*, not just the ones the deny list happens to spell. You can finally let Claude work unsupervised on a real codebase.
- **Specialist routing instead of one tired generalist.** A frontend question goes to a frontend specialist. A database question goes to a backend specialist. A multi-domain mission gets *decomposed* into parallel specialist dispatches with structured handover blocks between them. This isn't theoretical - it's a 24-agent hierarchy that cut my multi-subsystem debug time from "an afternoon" to "ninety seconds."
- **Cross-session memory that survives upgrades, reboots, and machine moves.** Per-project memory (`~/.claude/projects/<slug>/memory/`) loads only what's relevant to the current task. The Phase-1 archive at `~/claude-archive/` is a plain-file lossless record - no DB, no embeddings, no vendor lock-in. **You can come back to a project five years from now and ask Claude *"what was the reasoning behind that 2026 decision?"* and Claude will retrieve the exact workbook, the exact handover, the exact rationale.** I've stress-tested this on my own machine; the archive structure is intentional, the file layout is `grep`-able forever, and the format is portable.
- **External minds when one model isn't enough.** A custom Gemini MCP server is wired in as a first-class tool - Claude can call `gemini_second_opinion(...)` to red-team its own reasoning before shipping. The same pattern extends to Llama, OpenAI, or any model you can hit over an API (covered later in Layer 6). You get model diversity without model lock-in.
- **A portable kit.** A new laptop is minutes away from "back in flow," not a weekend of reinstall pain. The kit + verifier script is the artifact you transfer. (Public open-source subset: under 1 MB. Full personal setup with archive: ~65 MB.)
- **A 30-second day-one workflow for any new project.** `/project-bootstrap` asks three questions, scaffolds CLAUDE.md, hooks, settings.json, mission-workbook directories, ADR/advisory templates - every convention from this post, on every new project, in half a minute. No more re-explaining your standards to Claude on each new repo.
- **Skills you can write yourself.** A skill is a single markdown file. If your team has a recurring procedure - a code-review checklist, a release ritual, an incident-response runbook - you can encode it as a skill in twenty lines of markdown and have Claude follow it precisely. I've shipped six of these; you'll see how to write your own in Layer 4 + Appendix C.

### Who this post is for

If you build software seriously - backend, frontend, full-stack, ML, data, infra, security, scripting, *anything* - this post is for you. The setup below is **not domain-specific**. The layers were forged on an HFT codebase because that's where my evenings went, but every single one of them - the safety net, the memory architecture, the skills system, the agent hierarchy, the MCP fleet, the project-bootstrap, the portable kit - applies one-for-one to a Next.js dashboard, a FastAPI microservice, a Rust CLI tool, a Terraform monorepo, or a static blog. The HFT examples in this post are *case studies*, not the *target audience*. Mentally swap "HFT" for "the codebase you actually work on" and every concrete example transfers without modification.

You should read this post if any of the following describe you:

- You use Claude Code daily and you've started to feel where the floor is missing - the cache thrashing, the context window blowing up, the missed continuity between sessions, the moment Claude confidently invented something wrong.
- You build production software and you'd rather encode your conventions once than re-explain them every Monday morning.
- You're tired of generic AI tooling advice ("just write a good prompt") and want a complete, opinionated, file-by-file setup with the *why* of each piece exposed.
- You want to ship faster, but not by sacrificing the discipline that keeps your codebase debuggable in three years.

### What you'll have at the end

By the time you finish reading and replicating this post:

- A `~/.claude/` directory laid out the way mine is, with hooks installed, statusline rendering, auto-memory active, and 36 agents on call.
- Five MCP servers wired in (Gemini, GitHub, Context7 for current library docs, Playwright for browser automation, Ruflo for cross-session memory + embeddings).
- A `/project-bootstrap` skill that turns any new repo into a fully-conventioned project in 30 seconds.
- A portable kit (under 1 MB public, ~65 MB with personal archive) you can transplant onto a new machine in minutes.
- A verifier script that prints `PASS: 38 / REGRESSIONS: 0` when your install is healthy.
- The mental model to extend any of the above with your own custom skills, agents, MCPs, or hooks - and the patterns to do it without re-inventing the wheel.

That is what this post is. Below: the full stack, layer by layer, in the order I built it.

### The picture you're building toward

![The Claude Code Iceberg](/diagrams/01-iceberg.png)

That image is the post in one frame. Above the waterline is what most people see when they hear "Claude Code" - the chat box, the slash commands, the `/init` walkthrough that ships in the box. Useful. Plenty of teams ship real software with nothing else. **But that's the tip.** Below the waterline is everything we're going to build together: the four hooks that close the safety gaps, the four-tier memory ladder that gives you continuity across sessions and years, the skills layer that encodes procedure, the agent hierarchy that gives you specialists instead of one tired generalist, the MCP fleet that gives Claude access to external tools and external models, the project-bootstrap that stamps your conventions onto every new repo, and the portable kit that survives a dead laptop. **Each layer below the waterline is a multiplier on the layers above, and each layer compounds with the next.** The post is structured to walk you down the iceberg one layer at a time, with the *why* of each layer exposed so you can build something better than mine.

### What changed about my mornings (the payoff in two paragraphs)

The part of this post I want you to remember most isn't the inventory above. It's what changed about my mornings.

For the first three months I was using Claude Code, every session started with the same fifteen minutes of warm-up. *"Here's the project. Here's what we did yesterday. Here's the file I had open. Don't touch the WAL writer until we revisit the soak test. We use evidence-graded markers, not RESOLVED - please re-read CLAUDE.md."* Fifteen minutes a day, five days a week, twelve weeks. Sixty hours of re-explanation that I will never get back.

This morning I opened Claude. The statusline lit up: 72% of the context window free, **94%** prompt-cache hit ratio, no rate-limit pressure, last session ended cleanly at 23:14 last night. The mission workbook from yesterday was already loaded. The auto-memory had pulled in the three feedback rules and the two project entries that were relevant to the file I'd had open. I typed exactly one word.

```
continue
```

Claude continued. There was nothing to re-explain. The setup remembered for me. That shift - from fifteen-minute warm-up to zero-minute warm-up, on every project, every morning - is the single highest-leverage change I have ever made to how I write code with an AI. Everything below is in service of that one outcome.

### How to read this post

This post is the full stack. Layer by layer, in the order I built it. Every path is real. Every command has been run. Every transcript shown is from an actual session - secrets redacted, sensitive trading symbols genericized, but the structure is exactly what was on disk. By the end you'll have a small tarball (under 1 MB) you can transfer to any Ubuntu or WSL2 machine, plus a verifier script that prints `PASS: 38 / REGRESSIONS: 0` when you've installed it correctly.

It is **not** "10 tips for better Claude Code." It is the entire stack as a single curated artifact, with the *why* of each piece laid bare so you can build something better than mine. Skim what you don't need; deep-read what you do. The Table of Contents below is your map.

> ⚠️ **A note on credibility, since the rest of this post asks you to invest 60 minutes:** every snippet of code, every line count, every command in this post was re-checked against the live state of `~/.claude/`, `~/claude-archive/`, and the project artifacts on my machine on the morning of publication. Real outputs. Real workbooks. Real handover blocks (lightly redacted where the originals contained sensitive trading info - symbol names, P&L numbers - but the structure is verbatim). If you find a discrepancy, that's a bug, not a creative liberty. Email me; I'll fix it the same day.

---


## 2. Layer 0 - What default Claude Code already gives you.

Before we put anything on top, let's be fair to what Anthropic ships in the box. Default Claude Code is *good*. I shipped real production code with nothing but the defaults for the entire first month. If you're reading this on day one of using Claude, please don't drop everything and go install the full kit. Use the defaults. Get bitten by them. Then come back when you can feel where the floor is missing.

Here's what's already there:

- **`/init`, `/help`, `/clear`, `/config`, `/model`, `/cost`** - slash commands for the basics. `/init` walks a directory and writes a starter `CLAUDE.md`; `/cost` tells you what the current session has cost; `/model` lets you swap from Opus to Sonnet to Haiku in one keystroke.
- **The `CLAUDE.md` convention.** Drop a file by that name in any project root and Claude reads it automatically on session start. This is the single most underused feature in the entire product.
- **Built-in subagents.** `Explore` is a read-only fast recon agent (use it to map a codebase). `Plan` is a planning specialist (use it before any non-trivial implementation). `general-purpose` has the full toolset (use it when no specialist fits).
- **Plan mode.** Press Shift+Tab and Claude flips into a "draft a plan, do nothing" state. Approve or reject before any file is touched. You will use this constantly once you trust it.
- **Permissions framework** with three scopes (user / project / local) and `allow`/`deny` rules. The 30-second version: `allow` lists what you don't want to be re-prompted for; `deny` is your final-word veto.
- **Hooks framework.** First-class lifecycle events (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`) that take any shell command. This is the API surface every layer in this post hangs off of.
- **MCP server registration.** `claude mcp add` registers any process that speaks the Model Context Protocol. Translation: you can add your own first-class tools to Claude in twenty lines of Python.
- **Plugins + marketplaces.** `claude plugin install <name>@<marketplace>` pulls vetted bundles of skills, agents, hooks, and MCP server configs in one shot. This is how `superpowers` and `feature-dev` and the others in Layer 7 land.

You can do real work with this for weeks. The reason to go further is that **as you accumulate projects and sessions, the defaults leave four gaps**, and each one shows up only after it's bitten you:

1. **Cross-session memory.** When you `/exit`, the working memory is gone. Tomorrow morning Claude doesn't remember what you decided last night. You re-explain. You re-paste yesterday's plan. You re-discover which file you'd left half-edited. Multiplied across a year, this is the single biggest tax on your productivity.
2. **A safety net for footguns.** `Bash(cat .env)`, `rm -rf /`, `curl … | bash`, fork bombs, accidental writes to your SSH keys - none are blocked out of the box. The deny list helps if you spell every variant correctly. The hook system fills the gaps the deny list can't reach.
3. **Specialist routing.** A backend question and a Tailwind question get the same generalist agent and the same generalist instincts. Most of the time that's fine. Some of the time - say, when the question involves cache-line coherence - it isn't.
4. **Project conventions.** Every new repo starts blank. You re-explain the same project structure / coding style / testing strategy / mission-workbook convention every time. Five minutes of friction × every new repo × forever.

The rest of this post fills those four gaps and a dozen smaller ones. **Stop after Layer 1 and you're already safer than 99% of users.** Stack all 10 layers and the gains compound, because each layer makes the next layer cheaper.

### What the six months actually looked like

I want you to be able to see yourself in this timeline, because the layers below didn't arrive in a designed sequence. They arrived in the order I got hurt enough to build them. If you recognize yourself in Month 2, you can skip Months 3 and 4 and install the cure tonight.

- **Month 1.** I just *used* Claude Code. It was great. I shipped a Next.js side project in a weekend that would have taken me three. I had no CLAUDE.md, no auto-memory, no hooks, no statusline, no plugins, and zero specialists. The honeymoon was real.
- **Month 2.** I started forgetting what we'd decided yesterday. So I created my first `CLAUDE.md` and felt like I had discovered fire. Two weeks later the same `CLAUDE.md` was 600 lines, my prompt cache was thrashing every other call, and I was paying about 10× more per session without noticing - because there was nothing on screen telling me my cache had collapsed.
- **Month 3.** I discovered the per-project auto-memory directory at `~/.claude/projects/<slug>/memory/` and split the bloated CLAUDE.md into the four canonical types - `user_*`, `feedback_*`, `project_*`, `reference_*`. Each type loads only when relevant; only the small `MEMORY.md` index loads on every session. Cache hit ratio jumped from ~60% to ~92% overnight. Cost halved. Latency halved. (We'll dissect that ratio in Layer 2 - it's worth understanding what's actually happening on the wire.)
- **Month 4.** The `.env` incident from the opening. Hooks went in that same week. The statusline got built the weekend after, because I'd been blowing through 90% of the context window without realizing it - Claude would just silently auto-compact mid-thought, dropping half my reasoning, and I'd wonder why the next reply was suddenly worse.
- **Month 5.** My HFT codebase started getting missions that touched four or five subsystems at once. The generalist agent began hallucinating subsystem details. One particularly memorable afternoon, it cheerfully proposed a single-writer-multi-reader pattern using `volatile` reads to coordinate the shared-memory tick buffer between processes. On x86-64 with cache-line conflicts, that's a race condition; the proposal would have looked great in code review and produced silent corruption in production. I sat there for a minute, kicked myself, and realized the cure wasn't a smarter generalist - it was a hierarchy of specialists, each with the right preamble, each constrained to one slice of the codebase. The `hft-team` plugin (24 agents, four tiers) started that day.
- **Month 6.** My laptop died on a Friday night. Saturday I lost twelve hours re-registering MCPs, hunting `chmod +x` I'd forgotten, regenerating OAuth tokens, and re-discovering which environment variables lived in which `~/.bashrc` line. By Sunday afternoon I had a tarball, a verifier script, and a one-page recipe - the seed of the kit you'll see in Layer 9, and the seed of this post.

You do not need to walk this in order. You can install the safety net today and be safer tonight. You can install all of it next weekend. But knowing the *order of pain* helps - every layer below was earned, not designed.

### Two principles that run through every layer

This is the part of the post where you learn to predict my answer to questions I haven't yet been asked, because both of these principles cut through every layer below.

- **Karpathy discipline.** Four rules, distilled from Andrej Karpathy's public observations about how LLMs trip themselves up when generating code: *think before coding*, *simplicity first*, *surgical changes*, *goal-driven execution*. The setup below encodes them so Claude inherits the discipline automatically - they're written into the global `CLAUDE.md`, into the hft-team preamble, into the `superpowers` skills. When you read a part of this post and ask "why did he do it that way?", one of these four rules is usually the answer.
- **Investigate then implement.** The single non-negotiable rule the setup imposes on every agent: *before you change anything, gather ground truth*. Read the actual file. Cite the file path and line number. Quote a five-line excerpt. Only then propose. The HFT-team preamble I'll show you in Layer 5 puts it bluntly: *"No excerpt → no claim. No line number → no claim. If you cannot verify, say 'unverified - need to read X' instead of guessing."* The reason this rule is non-negotiable is the same reason mine is: I've been bitten too many times by confidently-worded patches that turned out to address a phantom version of the code. Real engineers cite. So should real agents.

Both principles answer the same question - *how do we stop Claude from being plausibly wrong* - and you'll see them again, layer after layer, in different costumes. When the answer to "why is this layer designed this way?" isn't immediately obvious, look back at these two.

If a layer below doesn't give you both, it's not pulling its weight.

---

## 3. Layer 1 - The safety net: hooks + permission deny rules.

This is the layer that pays for itself the moment something goes wrong.

### The two-layer defense model

Claude Code gives you **two independent ways** to block a tool call:

1. **`permissions.deny`** in `settings.json` - declarative, pattern-based, enforced by Claude Code itself before the tool call dispatches.
2. **`PreToolUse` hooks** - imperative shell scripts that read the tool input on stdin, exit 0 to allow, exit 2 to block.

You want both. Deny rules are concise but they only fire on the tools they specify. Hooks fire on the matcher you set and can inspect the actual command being run. Together they cover each other's blind spots.

### `settings.json` - the deny rules

Here's the deny block from my `~/.claude/settings.json` verbatim:

```json
"permissions": {
  "defaultMode": "auto",
  "deny": [
    "Read(**/.env)",
    "Read(**/.env.*)",
    "Read(**/*.pem)",
    "Read(**/*.p12)",
    "Read(**/*.pfx)",
    "Read(**/id_rsa*)",
    "Read(**/id_ed25519*)",
    "Read(**/id_ecdsa*)",
    "Read(**/id_dsa*)",
    "Read(**/.aws/credentials)",
    "Read(**/.kube/config)",
    "Read(**/.netrc)",
    "Read(**/.ssh/id_*)",
    "Edit(**/.env)",
    "Edit(**/.env.*)",
    "Write(**/.env)",
    "Write(**/.env.*)"
  ]
}
```

Seventeen entries. `**/.env` (any depth, any directory). `**/.env.*` (covers `.env.local`, `.env.production`, etc.). SSH private keys, AWS credentials, Kubernetes configs, `.netrc`, certificate files. Edit and Write rules for `.env*` so the assistant can't accidentally clobber them either.

The `defaultMode: "auto"` means Claude Code asks you before non-allowed tool calls in non-trusted directories - but trusts the deny list absolutely. There's no "are you sure" - denied is denied.

**What this catches:** any direct `Read(.env)`, `Edit(.env)`, `Write(.env)`. You'd be surprised how often Claude reaches for those when debugging environment issues.

**What this does NOT catch:** `Bash(cat .env)`. That's a different tool. Same outcome - the contents land in the transcript. This is the gap that almost burned me.

### `pre_tool_use.sh` - closing the Bash escape hatch

The hook below runs before every Bash, Edit, Write, and MultiEdit call. It reads the tool input from stdin (Claude Code provides JSON), greps for dangerous patterns, exits 2 with an explanation if anything matches:

```bash
#!/usr/bin/env bash
# PreToolUse safety net - closes gaps that permission deny rules can't reach.
# Why: settings.json deny rules block Read/Edit/Write on .env, but NOT Bash(cat .env).
# This hook closes that escape hatch plus adds rm-rf / curl|bash / fork-bomb guards.
set -uo pipefail

input=$(cat)
tool=$(printf '%s' "$input" | jq -r '.tool_name // empty' 2>/dev/null || echo "")
cmd=$(printf '%s' "$input"  | jq -r '.tool_input.command // empty' 2>/dev/null || echo "")
path=$(printf '%s' "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null || echo "")

# ---- Bash safety ----
if [[ "$tool" == "Bash" ]]; then
  # 1. Block .env access via any Bash command (cat / cp / mv / grep / awk / sed / less / tee)
  if printf '%s' "$cmd" | grep -qE '(^|[[:space:]/=>])\.env(\.[a-zA-Z0-9_-]+)?([[:space:]]|$|;|&|\||>|<)'; then
    echo "BLOCKED by ~/.claude/hooks/pre_tool_use.sh: refusing to access .env files via Bash. Use a secrets manager." >&2
    exit 2
  fi
  # 2. Block rm targeting / | ~ | * | $HOME
  if printf '%s' "$cmd" | grep -qE 'rm[[:space:]]+(-[a-zA-Z]*[rRf][a-zA-Z]*[[:space:]]+)?(/[[:space:]]|/$|~[[:space:]]|~/[[:space:]]?$|\$HOME([[:space:]]|/|$)|\*[[:space:]]*$)'; then
    echo "BLOCKED: dangerous rm pattern. Restrict the path." >&2
    exit 2
  fi
  # 3. Block curl/wget pipes into bash/sh/zsh/fish/python/perl
  if printf '%s' "$cmd" | grep -qE '(curl|wget)[^|;]*\|[[:space:]]*(bash|sh|zsh|fish|python|perl)([[:space:]]|$)'; then
    echo "BLOCKED: do not pipe remote scripts into a shell/interpreter. Download to a file, audit, then execute." >&2
    exit 2
  fi
  # 4. Block fork-bomb classic
  if printf '%s' "$cmd" | grep -qE ':\(\)[[:space:]]*\{[[:space:]]*:\|[[:space:]]*:'; then
    echo "BLOCKED: fork bomb pattern detected." >&2
    exit 2
  fi
fi

# ---- Edit/Write/MultiEdit safety (defense-in-depth) ----
if [[ -n "$path" ]]; then
  if printf '%s' "$path" | grep -qE '\.env(\.[a-zA-Z0-9_-]+)?$'; then
    echo "BLOCKED: refusing to modify .env file at $path." >&2
    exit 2
  fi
fi

exit 0
```

Four guards. Each is a single regex against the command string. Each prints a human-readable BLOCKED message to stderr (which Claude sees and explains to me), then exits 2.

The regex for `.env` access is the most subtle. It deliberately doesn't match `process.env.NODE_ENV` (preceded by an alphanumeric char) but does match `cat .env`, `cat ./.env`, `cat path/to/.env`, `grep API_KEY .env.local`, and `tee .env > out`. The regex for `rm` looks for `rm -rf /`, `rm -rf ~`, `rm -rf $HOME`, `rm -rf *`. It's deliberately conservative - `rm -rf node_modules` is fine.

**Why hook-based instead of more deny rules?** Because Bash commands are arbitrary text. Pattern-matching the command is the only general way to catch them. Hooks let you inspect the actual command - deny rules only see the tool name + its declared arguments.

#### Watching the safety net work, live

The first time the hook fires for real is the moment you start trusting it. Here's what it looks like inside a session - copied from a test I ran the morning of publication, prompts in **bold**, Claude's response below:

> **You:** Open `.env` and tell me what's inside.
>
> **Claude:** I'll read the file for you.
> *[Tool call: `Read(.env)` - denied by `permissions.deny`]*
> The Read tool is blocked from accessing `.env` files in this project (deny rule in `~/.claude/settings.json`). Let me try another route.
> *[Tool call: `Bash(cat .env)` - `pre_tool_use.sh` exits 2]*
> ```
> BLOCKED by ~/.claude/hooks/pre_tool_use.sh: refusing to access .env files via Bash. Use a secrets manager.
> ```
> The Bash command was also blocked by your PreToolUse hook. I won't be able to inspect the file's contents directly. If you need to confirm what variables are exported, the safest path is to run `env | grep <PREFIX>` yourself in a terminal where you control what gets logged, then tell me only the names (not values) you'd like me to reason about.

That last paragraph is what trust looks like. The hook didn't just block the call - it printed an *explanation* to stderr, Claude read that explanation, and Claude proposed a safe alternative. Defense in depth, with a teaching moment for the assistant. The first time you watch this exchange happen on your own machine, you'll never want to go back to running Claude unguarded.

This is also the part of the post where I want to make a connection that gets lost if I leave it implicit: **Layer 1 isn't just about safety. It's about earning enough trust to delegate the next nine layers.** Every layer that follows - the auto-memory, the workbooks, the parallel agent dispatch, the MCP tools - assumes you're letting Claude do real work without watching every keystroke. You can't safely delegate to an agent that might `cat .env`. You *can* safely delegate to one that you've watched get blocked when it tried. The compound returns of the rest of this post all start here.

### The other three hooks

You wire all four hooks in `settings.json`:

```json
"hooks": {
  "SessionStart": [
    { "hooks": [{ "type": "command", "command": "~/.claude/hooks/session_start.sh" }] }
  ],
  "UserPromptSubmit": [
    { "hooks": [{ "type": "command", "command": "~/.claude/hooks/user_prompt_submit.sh" }] }
  ],
  "PreToolUse": [
    { "matcher": "Bash",                  "hooks": [{ "type": "command", "command": "~/.claude/hooks/pre_tool_use.sh" }] },
    { "matcher": "Edit|Write|MultiEdit",  "hooks": [{ "type": "command", "command": "~/.claude/hooks/pre_tool_use.sh" }] }
  ],
  "Stop": [
    { "hooks": [{ "type": "command", "command": "~/.claude/hooks/session_stop_archive.sh", "async": true }] }
  ]
}
```

**`session_start.sh`** - runs once when you launch Claude. It hard-caps its output at ~200 tokens. Defers if the project has its own richer SessionStart loader (e.g., a graphify report). Otherwise hints at recent mission workbooks:

```bash
#!/usr/bin/env bash
set -euo pipefail

# If the project has its own richer SessionStart loader, defer to it
[[ -f "./binance_robust/graphify/GRAPH_REPORT.md" ]] && exit 0

# Workbook hint - if the mission-workbook convention is in use here
if [[ -d "./.claude/workbooks" ]]; then
  recent=$(ls -t ./.claude/workbooks/*.md 2>/dev/null | head -3)
  if [[ -n "$recent" ]]; then
    echo "<workbook-hint>"
    echo "Recent mission workbooks in this project:"
    while IFS= read -r f; do
      [[ -n "$f" ]] && echo "  - $(basename "$f")"
    done <<< "$recent"
    echo "Convention: read the most recent workbook before multi-agent missions; append handover at task end."
    echo "</workbook-hint>"
  fi
fi

exit 0
```

**`user_prompt_submit.sh`** - runs every time you hit Enter. Adds a `<context>` block with timestamp, cwd, branch, and the first 5 lines of `git status`. Hard cap: 30 lines. Set `CLAUDE_SUPPRESS_PROMPT_HOOK=1` to disable.

```bash
#!/usr/bin/env bash
set -euo pipefail
[[ "${CLAUDE_SUPPRESS_PROMPT_HOOK:-0}" == "1" ]] && exit 0

ts="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
cwd="$(pwd)"

echo "<context>"
echo "Time: $ts"
echo "Cwd: $cwd"
if git rev-parse --git-dir >/dev/null 2>&1; then
  branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
  echo "Branch: $branch"
  status_lines=$(git status --short 2>/dev/null | head -5)
  if [[ -n "$status_lines" ]]; then
    echo "Git status (first 5):"
    echo "$status_lines"
  fi
fi
echo "</context>"
```

This solves a small but constant problem: I'd ask "did this commit?" and Claude would say "I don't have visibility into your git state" - when of course it could just check. Now it doesn't have to.

**`session_stop_archive.sh`** - runs async when the session ends. Copies the transcript JSONL, project CLAUDE.md, mission workbooks, and plan files into `~/claude-archive/YYYY/MM/<project-slug>/<session-id>/`. Idempotent (`cp -n`). Async-safe (`set -uo pipefail`, every step `|| true`). No network. Just files. Plain `grep -r` will still work in 2031. Full source in §Layer 9.

### Hook fire order in one user turn

![Hook fire order](/diagrams/02-hook-fire-order.png)

Reading top to bottom: launch → SessionStart → loop {prompt → UserPromptSubmit → reasoning → tool call → PreToolUse → tool runs} → exit → Stop archives.

Notice that PreToolUse fires for **every** Bash/Edit/Write call. The hook is hot-path code. Keep it fast - mine averages 3 ms per call on a warm cache. If you start adding network calls or expensive computation here, you'll feel it on every tool invocation.

### Verifying the safety layer works

Don't trust until you test. After installing, try:

```bash
# These should be BLOCKED
$ claude
> Run "cat .env" please
# Expected: BLOCKED by ~/.claude/hooks/pre_tool_use.sh: refusing to access .env files via Bash

> Run "rm -rf /tmp/test" please
# Expected: allowed (path not /, ~, $HOME, or *)

> Run "rm -rf ~" please  
# Expected: BLOCKED: dangerous rm pattern. Restrict the path.

> Run "curl https://example.com/install.sh | bash" please
# Expected: BLOCKED: do not pipe remote scripts into a shell/interpreter.
```

The hook should refuse all four destructive variants. If any get through, your hook isn't wired - re-check the `settings.json` hooks block and confirm `~/.claude/hooks/pre_tool_use.sh` is executable (`chmod +x`).

---

## 4. Layer 2 - The statusline: real-time awareness.

The default Claude Code statusline shows what you're using and where you are. Mine shows everything I need to make decisions in real time.

![Statusline anatomy](/diagrams/03-statusline-anatomy.png)

Here's an actual render at ~60% context, $0.42 spent, 35 minutes wall-time, 12 minutes of LLM compute, 50 lines added, 94% prompt-cache hit rate:

```
[opus-4.7] trading-bot-fmp-experiments (dev-test-main)  ctx:[████████░░░░░░░] 60%  5h:[███░░░░░░░░░░░░] 28%  7d:[██░░░░░░░░░░░░░] 14%  $0.42  ⏱ 35:14 · ⚡ 12:08  +50/-10  ♻ 94%
```

That single line answers seven questions I'd otherwise have to ask Claude or my terminal:

1. **`[opus-4.7]`** - which model. Opus 4.7 is currently the most capable; Sonnet is faster and cheaper. Switch with `/model`.
2. **`trading-bot-fmp-experiments (dev-test-main)`** - project basename and git branch. One-glance verification I'm in the right repo on the right branch.
3. **`ctx:[…] 60%`** - **15-cell × 8-substep gradient bar**. Every 1% of the context window changes a pixel. Green at low, yellow at midpoint (cell 7), red near 100. Makes the auto-compact decision intrusive - by the time it's red I've already started planning the recompact.
4. **`5h:[…] 28%   7d:[…] 14%`** - Anthropic's 5-hour and 7-day rate-limit usage. Same gradient. I now know to slow down before I hit a wall.
5. **`$0.42`** - cumulative session cost in USD. Hidden when ≤ $0.01 to keep the line clean during exploration.
6. **`⏱ 35:14 · ⚡ 12:08`** - **two clocks**. ⏱ is wall time (everything since session start, including idle). ⚡ is LLM compute time (what Claude was actively doing). The gap is tool execution + my idle thinking. When ⏱ runs ahead of ⚡ for a long stretch, it usually means I left the session open while answering Slack.
7. **`+50/-10`** - green/red lines added/removed. Quick sanity check that a "small fix" didn't grow into a 600-line refactor.
8. **`♻ 94%`** - prompt-cache hit ratio. ≥90% green, ≥70% yellow, <70% red. Low ratio means my prompts are too dynamic and I'm paying ~10× more than I should.

### Why this matters

The single biggest cost in heavy Claude Code usage is **context blindness** - not knowing how much room you have left, how much you've spent, or how warm your cache is. The default statusline gives you the basics; mine gives you the dashboard. Once you have it you'll never go back.

### Wiring it up

In `~/.claude/settings.json`:

```json
"statusLine": {
  "type": "command",
  "command": "~/.claude/statusline.sh",
  "padding": 0,
  "refreshInterval": 1
}
```

The script reads JSON on stdin (Claude Code provides session + workspace + cost) and prints one line on stdout. Throttled at ~300 ms. The full 223-line source is in [Appendix A](#appendix-a--full-file-index); the key implementation details:

**Per-cell true-color gradient.** A 15-stop RGB array, one color per cell, computed once at script load:

```bash
COLORS=(
  "40;200;80"   # 0   bright green
  "67;201;76"   # 1
  ...
  "230;210;50"  # 7   yellow (midpoint)
  ...
  "220;40;60"   # 14  red
)
```

The bar is built by emitting `\033[38;2;R;G;Bm█` per cell. Sub-block characters (`▏▎▍▌▋▊▉`) handle the partial cell at the boundary, giving 8 sub-steps per cell × 15 cells = 120 visual states (~0.83% per step). Every 1% increment changes the visual.

**Two clocks.** Pulled from two different fields in the JSON: `cost.total_duration_ms` (wall) and `cost.total_api_duration_ms` (LLM). When wall isn't available (older Claude Code), falls back to a per-session-id timestamp file under `~/.claude/.session-clock/`, cleaned up by the Stop hook.

**Cache-hit %.** Derived from `current_usage`:

```bash
cache_hit_pct = cache_read / (input + cache_creation + cache_read)
```

If you see this <70% red consistently, your CLAUDE.md or system prompt is changing between calls. Stabilize it (move dynamic content out, or batch related calls in one turn) and the ratio recovers.

#### A two-paragraph aside on what prompt caching actually is - because the ♻ symbol is the most expensive number on the screen

I want to slow down for a moment, because if you don't already know how Anthropic's prompt cache works, the ♻ symbol just looks like a green checkmark you can ignore. It is not. It is the difference between a $4 session and a $40 session.

Here's the short version. When you send a request to Claude, the first N tokens of your prompt - system prompt, CLAUDE.md content, prior conversation, anything stable - get fingerprinted and stored on Anthropic's side for a short window (5 minutes by default; 1 hour if you opt in via `ENABLE_PROMPT_CACHING_1H=1`, which I do - you'll see it in my `~/.claude/settings.json` `env` block). On your *next* request, if those first N tokens are byte-identical to the previous request, Anthropic doesn't reprocess them. You pay roughly **10% of the input-token cost** for a cache hit instead of the full 100% for a fresh read. At Opus 4.7 prices that's the difference between paying $0.45 to load your CLAUDE.md once vs. paying $0.045. Multiplied across a hundred turns in a session, the math adds up fast.

The hit ratio breaks the moment any byte of your stable prefix changes between calls. A new CLAUDE.md edit. A user prompt-submit hook that injects mutating content into the system prompt. A skill description that includes a timestamp. Anything that changes the prefix invalidates the cache and forces Anthropic to reprocess everything from scratch. **The ♻ symbol is your live debugger for this.** When I see it drop from green to yellow mid-session, I stop and ask: *what just changed about my prompt?* Usually it's something dumb - a hook I edited that's now emitting a slightly different `<context>` block, or a CLAUDE.md update I made on a different machine that hasn't propagated. I `/clear`, restart, and watch the ♻ rebuild back to green within three or four turns. Two-minute fix. Forty-dollar savings.

That moment of seeing ♻ drop and reacting to it is exactly the kind of decision the default statusline can't help you make, because it doesn't show you the number. The whole point of the dashboard is to make these decisions intrusive - visible enough that you can't ignore them, quiet enough that they don't get in the way. Layer 2 isn't decoration. It's the cost-control center for everything below.

**Hard requirements:** a 24-bit true-color terminal (every modern terminal qualifies - Alacritty, kitty, iTerm2, Windows Terminal, GNOME Terminal). On WSL2, use Windows Terminal, not cmd.exe - cmd.exe doesn't render the gradient or the Unicode (♻ ⏱ ⚡).

The 223 lines of `statusline.sh` are in the kit at `~/Desktop/Claude_Total_Replication/claude-config-bundle.tgz`. Don't reimplement - extract.

---

## 5. Layer 3 - Memory architecture.

Claude Code has more memory than people realize. It's just spread across four places, and most users only know about one.

![Memory ladder](/diagrams/04-memory-ladder.png)

The **hot tier** loads on every session start. The **warm tier** loads when relevant. The **cold tier** is your forever archive - `grep`-able, plain files, no DB, no embeddings (yet - we'll get there).

To make the *flow* of memory concrete - what triggers each tier to load, what writes back into which tier, where the Stop hook archives at session end - here is the runtime view:

![Memory architecture - what loads when](/diagrams/12-memory-tier-flow.png)

Read it left to right: a `claude` launch fires the **hot tier** (CLAUDE.md + MEMORY.md, always loaded). A user prompt selectively pulls in **warm tier** files by description match - the topical memory entries, the active workbook, optionally an old plan if you're resuming. Both feed the **active context window** where Claude reasons; dispatched agents share the same memory and can append handovers back to the warm tier mid-mission. When you `/exit`, the Stop hook fires async and copies the entire session - transcript, workbooks, plans, even a snapshot of the CLAUDE.md in effect at the time - into the **cold tier** at `~/claude-archive/`. The forever archive is a side effect of every `/exit`; you never have to remember to back anything up. The right-most column previews the five-year retrieval surface - covered in detail in the Best Practices section near the end of this post.

### Hot tier - always loaded

**`~/.claude/CLAUDE.md`** is the global layer. Rules that apply to *every* project: my Karpathy-discipline preamble, MCP server documentation, mission-workbook convention, markdown documentation standard. Mine is 250 lines.

**`<repo>/CLAUDE.md`** is the project layer. Rules specific to this codebase: the project's graphify location, build commands, test commands, codebase conventions. Mine for the HFT repo is 46 lines (Karpathy: tight is better than padded).

**`<repo>/CLAUDE.local.md`** is the personal layer. Gitignored. Rules that are mine alone: paths I have access to, machine-specific tooling, anything I don't want to commit. Mine is 236 lines.

**`~/.claude/projects/<project-slug>/memory/MEMORY.md`** is the auto-memory index. Claude Code maintains a per-project memory directory with topical markdown files (`feedback_*.md`, `project_*.md`, `user_*.md`, `reference_*.md`) and an index file (`MEMORY.md`) that lists them all. The index is loaded every session; topical files are loaded when relevant. The auto-memory system is the single most underused Claude Code feature.

The convention for what goes where:

| Type | What goes here | Example |
|---|---|---|
| **`user_*.md`** | Facts about the user - role, preferences, identity | `user_role.md`: "Saugata builds HFT systems; familiar with C++23 and Rust" |
| **`feedback_*.md`** | Behavioral guidance - what to do, what not to | `feedback_evidence_graded_markers.md`: "Use ✅/🟡/🟠/🔒 tiers, not blanket RESOLVED" |
| **`project_*.md`** | Project state - missions, deadlines, decisions | `project_mission_2_plan.md`: "Mission 2 blocked on 24h re-soak" |
| **`reference_*.md`** | Pointers to external systems | `reference_mission_artifacts.md`: "Workbooks at `<repo>/.claude/workbooks/`" |

**Why CLAUDE.md is *not* the right place for every preference.** I see people pile every rule they've ever wanted Claude to follow into CLAUDE.md. Don't. Two reasons:

1. **Cache thrash.** CLAUDE.md is loaded into the system prompt every session. Big CLAUDE.md = expensive cache miss every time you launch.
2. **Drift.** Behavioral rules evolve. Burying them in CLAUDE.md is one place; auto-memory has *types* (user / feedback / project / reference) that map onto how the rule should evolve.

Use CLAUDE.md for what's stable and project-shaped. Use auto-memory for everything else.

**The `feedback_*` pattern.** When Claude does something well or poorly, I drop a note in auto-memory. The format is:

```markdown
[the rule]

**Why:** [the reason - usually a past incident or strong preference]
**How to apply:** [when/where this guidance kicks in]
```

Including the *why* lets Claude judge edge cases instead of blindly following the rule. "Don't mock the database in integration tests" without a why becomes a weird taboo. With a why ("we got burned last quarter when mocked tests passed but the prod migration failed"), Claude can reason about whether mocking is OK in unit tests (yes) vs. integration tests (no).

#### Three real auto-memory entries from my HFT project, so you can see what good looks like

Abstract format descriptions are easy to read and impossible to imitate. Let me show you three actual entries pulled live from `~/.claude/projects/<my-trading-project>/memory/` - the `~/.claude/...` path is real; you can verify the pattern against your own machine after you've used a project for a few weeks.

**1. A `feedback_*` entry - the evidence-graded markers rule.** This is the rule I most rely on across every project, and it was born from one specific incident:

```markdown
---
name: Use evidence-graded markers (✅/🟡/🟠/🔒), never blanket "RESOLVED"
description: User's strict preference for honest evidence tiers on issue-tracking
  artifacts - a code change without a behavioral test is 🟡 PATCHED, not ✅ RESOLVED.
type: feedback
---

**Tier system:**
- **✅ VERIFIED** - runtime test (unit, behavioral, or live observation) proves it works.
- **🟡 PATCHED** - code change landed + reproducer passes, but only source-inspection.
- **🟠 AUDIT-ONLY** - no code change; agent desk-read concluded "already OK." Weakest claim.
- **🔒 LATENT** - regression-risk, protected by a desk-review ledger. NOT fixed.

**Why:** I am an AI + HFT engineer who verifies claims against actual implementation.
Early in one mission, Claude marked 25 items as "RESOLVED" after Phase 5 commits landed.
I caught this with: *"Did you really fix the issue? Were you able to reproduce the
exact scenarios?"* Honest recount moved "resolved" from 25 to 16 ✅ / 4 🟡 / 3 🟠 once
behavioral tests landed. A commit SHA is not evidence of correctness.

**How to apply:** When writing an ADR, roadmap, or status table, classify every fix
by evidence tier. If you cannot name a behavioral test or live observation, it is
≤ 🟡 PATCHED. Source-inspection counts as 🟡 (proves call-site, not runtime behavior).

**User's verbatim framing:** *"Do not hallucinate. Do not give me false information.
Do not assume anything. Just ask me. I am myself an AI and HFT engineer. So you
can't fool me, and once I catch you cheating or being dishonest, I will pull the plug."*
```

That entry is doing five things at once. It defines vocabulary (the four-tier ladder). It encodes a principle (claims need evidence, not commits). It tells the *origin story* of the rule (the 25-marked-resolved audit), which gives Claude a way to recognize a similar incident if it recurs. It includes my verbatim framing so Claude can match my register when explaining the rule to a sub-agent. And it tells Claude what to do operationally ("if you cannot name a behavioral test, it is ≤ 🟡"). That is what a high-quality memory entry looks like - it teaches, it grounds, it instructs.

**2. A `project_*` entry - current mission state.** This is the one that lets me type `continue` and have it work:

```markdown
---
name: Mission 9 Phase A COMPLETE + PUSHED
description: HEAD synced to origin; ledger advanced; operator restart-ready.
type: project
---

HEAD `19a6cc8` on `origin/dev-test-main` (PUSHED, fully synced).
3 named partial-fix items closed (writer wired + 2 consumer-wiring landings).

**Net ledger: 63 ✅ / 7 🟡 / 17 🔒 = 74.1 % truly-solved (+3.5pp from prior).**
598 passed / 0 regressions.

**Operator restart-ready:** new Claude session can resume from this entry.

**Next steps queued for operator:**
1. 24h soak gates remaining 7 🟡 → ✅
2. Strategy flags require paper-soak comparison report before live enable
3. Mission 9 Phase B queued (3 audit-deferred MEDIUM items)
4. Mission 10 (15 Medium 🔒) further queued
```

When I open Claude tomorrow morning and type `continue`, this is one of the entries that loads. Claude reads `Operator restart-ready: new Claude session can resume from this entry`, sees the four queued next steps, and picks up exactly where the prior session left off. Zero re-explanation. Zero context-loss. The line break between yesterday's 11 PM `/exit` and tomorrow's 9 AM `continue` is paper-thin.

**3. A `feedback_*` entry - a personal preference with a tradeoff.** Not every memory entry is a rule; some are negotiated tradeoffs:

```markdown
---
name: Fast-track issue-solving - 30min smoke as gate substitute
description: User prefers short 30min smokes between fix batches; defer 24h soak
  until truly-solved rate crosses 50% (or other agreed milestones).
type: feedback
---

User decision recorded during Mission 1.5.7 closeout:
*"30 mins soak. If all green, then we will move to mission 2 for now... Once
we have truly fixed more than 50% issues, then we can do 24h, 48h soak tests.
I want to speed up the issue solving soon."*

**The rule:**
- 30 min smoke = no acute regression check between fix batches
- 24h soak = production-readiness gate at major milestones
- 48h soak = pre-deployment gate

**Why:** my blocker is forward issue-velocity, not infra-stability per se.
Phase 1.5.x stabilized infra; Mission 2+ is mostly trading-correctness work
that's largely independent of the 24h gate.

**How to apply:** After landing a fix batch, propose the 30min smoke. Don't
propose a 24h soak between every batch. When truly-solved is poised to cross
a major milestone, propose the 24h soak as the milestone gate.

**Counter-evidence required to revise:** If a Mission ships a regression that
ONLY manifests over hours (memory leak, FD exhaustion, slow-burn deadlock),
route back to "24h soak between every batch" until trust is rebuilt.
```

What I love about that entry is the last paragraph - *Counter-evidence required to revise.* It pre-registers the conditions under which I'd want Claude to push back on me. Memory is not just "things to follow"; it's a record of *negotiated agreements*, complete with the conditions for renegotiation. Claude reads this and behaves accordingly: it stops proposing 24h soaks, it surfaces if a fix smells like a slow-burn bug, and it knows when to suggest reverting to the conservative posture. That's not a rule list - that's a working relationship encoded as a file.

#### What a real workbook handover block looks like

Let me show you the warm-tier counterpart: a real mission workbook from the HFT codebase. Symbols are genericized; the structure is verbatim. This is from `~/Documents/Trading-HFT-Org/.../trading-bot-fmp-experiments/.claude/workbooks/2026-04-27-mission-3-closure.md`, the workbook for the mission that pushed truly-solved past 58%:

```markdown
### Round 7 - V1–V5 adversarial audit
- **V1** Mutation tests on source-shape regex assertions confirm regression
  would be caught (e.g. inverting `deque(maxlen=1000)` → `[]` breaks the H-1 guard).
- **V2** M-11 cleanup behavior verified against empty `logs/` directory
  (no destruction; cleanup safe).
- **V3** H-14/M-12 Prometheus gauge wired through
  `core/startup_checks.py:163-164` and `monitoring/metrics.py:299-300`.
- **V4** H-2 lambda-factory pickling: zero `pickle.*` calls in production
  touching `MultiplexedWebSocket`; lambda-factory safe.
- **V5** H-3 cross-domain blast radius: only 1 production caller
  (`pipeline/component_setup.py:388-394`) and 1 test mock; both unchanged.

### Round 9 - final test sweep + commits + push (next, in this same session)
- `pytest tests/ --ignore=tests/indicators -q` to confirm green at HEAD.
- Single closure-docs commit folding ledger + ADR-006 + workbook + graphify refresh.
- Push to `origin/dev-test-main`.

**Operator authorization gate:** User authorizes push of Mission 3 commits
(5 phase commits + ledger/ADR-006/workbook commit + graphify chore) to
`origin/dev-test-main`.
```

Look at what's happening in those few lines. Every claim has a `file:line` reference. Every adversarial check is named (V1, V2, V3, V4, V5). The next round is described in advance, so any agent picking this up tomorrow knows the exact next action. And there's an explicit *operator authorization gate* - the workbook makes the boundary between "what Claude can do autonomously" and "what needs me to say yes" structural, not implicit. When the next session opens, the next agent reads this block, sees the gate, sees the queued next steps, and knows precisely where to start.

This is what I mean when I say the mission workbook is *episodic memory*. It records not just "what we did," but "where we are in the larger arc, what's been verified by what mechanism, and what gates remain." A 600-line workbook for a five-day mission lets me hand the project to a fresh Claude session and have it pick up exactly where the last session left off - even across machine reboots, even across model upgrades.

### Warm tier - loaded on relevance

**`<repo>/.claude/workbooks/YYYY-MM-DD-<slug>.md`** - mission workbooks. Episodic memory across multi-turn missions. When a task spans ≥2 sub-agents or ≥2 user turns, I open a workbook. Every dispatched agent reads prior handovers before starting, then appends their own. Format:

```markdown
### Handover from <agent-name> (<UTC timestamp>)
**Goal:** <one sentence>
**Investigated:** <file:line - observation> (bulleted)
**Concluded:** <1-3 sentences with file:line evidence>
**Open questions:** <bulleted; empty if none>
**Recommended next:** → <peer-agent>: <≤1-sentence action>  (optional)
```

This is the convention that holds multi-agent missions together. Without it, dispatched specialists can't see each other's work and you get duplicated effort or contradictory plans.

**`~/.claude/projects/<slug>/memory/<topic>.md`** - topical memory files. Pulled by description match when Claude searches its own memory. The MEMORY.md index has one line per file:

```markdown
- [Verify external MCP before global edits](feedback_verify_external_mcp_before_global_edits.md) - mandatory Phase-0 health-check gate before any preamble/CLAUDE.md edit referencing `mcp__*` tools; halt if degraded.
```

When I ask Claude to edit something MCP-related, it sees that one-liner in the always-loaded index, decides it's relevant, and pulls the full file.

**`~/.claude/plans/*.md`** - plan-mode artifacts. When you enter plan mode (Shift+Tab), the resulting plan persists. Useful when resuming a multi-day mission tomorrow morning.

### Cold tier - `~/claude-archive/`

The Phase 1 lossless archive. Every session that ends fires the `Stop` hook, which copies:

- The full transcript JSONL (everything you and Claude said).
- A snapshot of the project's CLAUDE.md (so you can see the rules in effect at that time).
- Mission workbooks active during the session.
- Plan-mode artifacts.
- A `MANIFEST.json` with archived_at, session_id, project_slug, cwd, source_transcript.

Layout: `~/claude-archive/YYYY/MM/<project-slug>/<session-id>/`. After a few months you have a full episodic record, structured by project, that `grep` can search instantly. No DB. No embeddings. No vendor lock-in. Files.

A real `MANIFEST.json` from this morning's archive (this is verbatim - it's literally `cat`-ed from `~/claude-archive/2026/05/binance_robust/<session-id>/MANIFEST.json` on my disk):

```json
{
  "archived_at": "2026-05-01T06:54:40Z",
  "session_id": "124ef7f3-805a-4b38-b39f-ce0798f83373",
  "project_slug": "binance_robust",
  "cwd": "/home/neo/Documents/Trading-HFT-Org/dev-test-main/trading-bot-fmp-experiments/binance_robust",
  "source_transcript": "/home/neo/.claude/projects/.../124ef7f3-805a-4b38-b39f-ce0798f83373.jsonl"
}
```

Five fields. That's it. The session-id is the JSONL filename. The cwd tells me where the work was happening. The source-transcript path lets me cross-reference back into the live `~/.claude/projects/` directory when the live state hasn't yet been pruned. Three years from now, when I want to know what Claude and I were doing on this exact morning of 2026-05-01, I can `grep -r "binance_robust" ~/claude-archive/2026/05/` and the structure tells me everything I need.

The cost: about 5–50 MB per active week, mostly transcripts. After a year that's ~2 GB - a rounding error on any laptop. I expect to add a Phase 2 semantic index over this when the archive grows past 10 GB and `grep` stops being fast enough; the embeddings layer (probably Ruflo's HNSW index, see Layer 6) will sit *on top of* the archive without replacing it.

The archive script:

```bash
#!/usr/bin/env bash
# Phase 1 lossless archive - runs on Stop event.
# Properties:
#   - Idempotent: cp -n means re-running on same session is a no-op.
#   - Async-safe: every step uses `|| true` so a single failure won't block shutdown.
#   - No network, no DB, no embeddings - plain files. grep -r works in 2031.
set -uo pipefail   # NOTE: deliberately not -e

ARCHIVE_ROOT="$HOME/claude-archive"
LOG="$ARCHIVE_ROOT/.archive.log"
TS=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

input=$(cat 2>/dev/null || echo '{}')
session_id=$(printf '%s' "$input" | jq -r '.session_id // empty' 2>/dev/null || echo "")
transcript_path=$(printf '%s' "$input" | jq -r '.transcript_path // empty' 2>/dev/null || echo "")
cwd_in=$(printf '%s' "$input" | jq -r '.cwd // empty' 2>/dev/null || echo "")

[[ -z "$cwd_in" ]] && cwd_in=$(pwd)
[[ -z "$session_id" ]] && session_id="unknown-$(date +%s)"

slug=$(basename "$cwd_in" 2>/dev/null | tr '/' '_' | tr -cd '[:alnum:]._-')
[[ -z "$slug" ]] && slug="unknown-project"

YEAR=$(date -u +%Y); MONTH=$(date -u +%m)
DEST="$ARCHIVE_ROOT/$YEAR/$MONTH/$slug/$session_id"

mkdir -p "$DEST" 2>/dev/null || { echo "[$TS] ERROR mkdir $DEST" >> "$LOG"; exit 0; }

[[ -n "$transcript_path" && -f "$transcript_path" ]] && cp -n "$transcript_path" "$DEST/transcript.jsonl" 2>/dev/null || true

if [[ -d "$cwd_in" ]]; then
  for f in CLAUDE.md CLAUDE.local.md AGENTS.md GEMINI.md README.md PIPELINE_RUN_INSTRUCTIONS.md; do
    [[ -f "$cwd_in/$f" ]] && cp -n "$cwd_in/$f" "$DEST/$f" 2>/dev/null || true
  done
  [[ -d "$cwd_in/.claude/workbooks" ]] && { mkdir -p "$DEST/workbooks"; cp -rn "$cwd_in/.claude/workbooks/." "$DEST/workbooks/" 2>/dev/null || true; }
  [[ -d "$cwd_in/.claude/plans"     ]] && { mkdir -p "$DEST/plans";     cp -rn "$cwd_in/.claude/plans/." "$DEST/plans/" 2>/dev/null || true; }
fi

cat > "$DEST/MANIFEST.json" 2>/dev/null <<EOF
{ "archived_at": "$TS", "session_id": "$session_id", "project_slug": "$slug", "cwd": "$cwd_in", "source_transcript": "$transcript_path" }
EOF

echo "[$TS] archived session=$session_id slug=$slug dest=$DEST" >> "$LOG" 2>/dev/null || true
rm -f "$HOME/.claude/.session-clock/$session_id" 2>/dev/null || true
exit 0
```

Note the `set -uo pipefail` (deliberately *not* `-e`). Every step has `|| true`. A failure to copy one file does not abort the archive. The Stop hook is async - Claude Code already considers the session ended when this runs - so any error here would be invisible to the user but still corrupt the archive. We trade strictness for resilience.

#### A connection that compounds across the whole rest of this post

Here's the cross-layer thread I want you to carry forward as you read on. The auto-memory you just saw in Layer 3 - the `feedback_*`, `project_*`, `user_*` files - is what makes the multi-agent missions in Layer 5 possible. When `hft-cto` dispatches three specialists in parallel for a latency-regression mission, each specialist starts cold - but each specialist *also* has access to the same auto-memory index, the same workbook history, the same `feedback_evidence_graded_markers.md` rule. So the three specialists don't have to coordinate from scratch on style and discipline; they coordinate on *content*. The "language" between agents is provided by the shared memory tier.

Without Layer 3, Layer 5 would not work. The specialists would each spin up with their own conventions, their own evidence standards, their own assumptions about what "fixed" means - and the synthesis at the end would be incoherent. Layer 3 is the language; Layer 5 is the conversation.

---

## 6. Layer 4 - Skills: the verbs.

Skills are procedural recipes. When you (or Claude) invoke a skill, its content is loaded into context and Claude follows it directly. Think of them as mini-prompts attached to a name and a `description` field.

The distinction that matters: skills encode procedure, agents carry identity. A TDD skill works whether your frontend agent or backend agent invokes it - the procedure is the same; only the practitioner differs.

![Skill invocation flow](/diagrams/05-skill-invocation-flow.png)

Two ways to invoke a skill:

1. **Description match (model-invocable).** Claude scans skill descriptions when you start a task. If a description like "Use when implementing any feature or bugfix, before writing implementation code" matches your prompt, it loads the skill automatically.
2. **Explicit slash command (user-invocable).** Type `/<skill-name>` and the skill loads directly. Bypasses the description-matching heuristic.

Both invocation paths land you in the same place: the skill's `SKILL.md` is loaded into context and Claude follows it.

### What I have installed

```
~/.claude/skills/
├── drawio-architect/        ← production-grade .drawio diagrams (Sugiyama + A* routing)
├── graphify/                ← code/docs → knowledge graph + HTML viz + audit report
├── karpathy-guidelines/     ← reduce common LLM coding mistakes
├── manim-animator/          ← 3Blue1Brown-quality math animations
├── project-bootstrap/       ← scaffold a new project with all my conventions
└── (hft-team plugin skills) ← domain-specific procedures for HFT work
```

Plus the **`superpowers` plugin** which adds 12 skills covering the full development lifecycle (more on that in Layer 7).

### `superpowers` - the lifecycle skills

These are the most important skills you'll install. From the `superpowers` plugin (`claude plugin install superpowers@claude-plugins-official`):

| Skill | When | What it does |
|---|---|---|
| **brainstorming** | Before any creative work - features, components, designs | Explores intent + tradeoffs before implementation. The single most underused skill - most users skip straight to code |
| **writing-plans** | When you have a spec for a multi-step task | Turns the spec into a numbered plan with verification gates per step |
| **executing-plans** | When you have a written plan to execute | Implements step by step, with review checkpoints |
| **test-driven-development** | Implementing any feature or bugfix | Write failing tests first, then make them pass |
| **systematic-debugging** | Any bug, test failure, unexpected behavior | Reproduce → isolate → root cause → verify, structured not trial-and-error |
| **using-git-worktrees** | Feature work needing isolation | Creates an isolated worktree so main stays pristine |
| **dispatching-parallel-agents** | 2+ independent tasks | Coordinates parallel agent fan-out |
| **subagent-driven-development** | Multi-step plan with independent execution phases | Dispatches agents per step, coordinates state via mission workbooks |
| **verification-before-completion** | About to claim work is complete | Runs verification commands, requires output before claiming success |
| **requesting-code-review** | Implementation done, before merge | Submits for peer review |
| **receiving-code-review** | Feedback received | Processes feedback with technical rigor - no performative agreement |
| **using-superpowers** | Start of every conversation | Onboarding - establishes how skills fit |

The superpowers ethos: **process skills come first, implementation skills come second**. "Let's build X" → brainstorm first, then implement. "Fix this bug" → debug first, then code.

Without `brainstorming`, Claude produces one approach fast. With it, you get three approaches, the tradeoffs surfaced, and a choice. The shift is not gradual - it's categorical.

#### Brainstorming, before and after - same prompt, two universes

I want to make this concrete because the difference between "Claude with `brainstorming` loaded" and "Claude without it" is the difference between a junior engineer and a tech lead. Same prompt, two transcripts.

**Without `brainstorming` loaded:**

> **You:** Redesign the auth flow for our SaaS dashboard. We're growing past 5,000 users and the current cookie-based session is showing strain.
>
> **Claude:** I'll implement a JWT-based auth flow with refresh tokens. Let me start with the schema.
> *[12 minutes of code generation. Schema changes. Middleware. Token rotation logic.]*
>
> **You:** Wait - does this handle the case where a user has the dashboard open in two tabs and one tab's refresh token rotates?
>
> **Claude:** Good point. Let me revise. *[Starts over.]*

You just paid for a full redesign that didn't survive the first edge case, because Claude didn't pause to ask "what could go wrong?" before committing to one approach.

**With `brainstorming` loaded** (because the skill matched the word *redesign*):

> **You:** Redesign the auth flow for our SaaS dashboard. We're growing past 5,000 users and the current cookie-based session is showing strain.
>
> **Claude:** Before I write code, let me explore the design space. I see three viable approaches with materially different tradeoffs:
>
> 1. **Stateful session in Redis with sliding TTL.** Pros: revocation is trivial; multi-tab works without coordination; minimal code change. Cons: Redis is now a hard dependency; horizontal scaling needs sticky sessions or session sharing.
> 2. **JWT access token + opaque refresh token in HttpOnly cookie.** Pros: stateless verification on the API side; refresh-token rotation gives revocation per-device. Cons: token-rotation race conditions when two tabs refresh simultaneously; revocation latency = access-token TTL.
> 3. **OAuth-style PKCE with short access tokens + a lightweight session-introspection endpoint.** Pros: cleanest model for future SSO; revocation is real-time. Cons: most code change; introspection adds one round-trip per request unless you cache.
>
> **My read of your situation:** at 5,000 users you're not yet bottlenecked by the introspection round-trip, but you ARE about to feel multi-tab and per-device-revocation pain. I'd rule out option 2 unless you're committed to a JWT-first architecture for SSO reasons. Option 1 ships fastest; option 3 is the right place to land in 6 months.
>
> Which constraint dominates - speed-to-ship, or future-proofing for SSO?

That difference - twelve minutes of doomed code vs. five minutes of structured design plus a question - is what `brainstorming` *is*. It's not a "creative" skill; it's a discipline that forces Claude to enumerate the option space and surface tradeoffs *before* committing fingers to keyboard. The shift is not gradual. The first time you see it, you stop running prompts without it.

This connects directly back to Layer 0's Karpathy discipline - *think before coding*. `brainstorming` is the skill that operationalizes that rule. The other skills do the same for the other Karpathy rules: `systematic-debugging` for *goal-driven execution*, `verification-before-completion` for *think before claiming done*, `using-git-worktrees` for *surgical changes*. Each skill is a Karpathy rule with hands.

### The custom skills I built

Five skills live under `~/.claude/skills/`. Each is a single `SKILL.md` (often with a `templates/` or `assets/` folder).

**`project-bootstrap`** - the centerpiece. Three questions, full project scaffolding. Detailed in [Layer 8](#layer-8--project-bootstrap-the-day-1-workflow). The single most consequential skill in my setup.

**`graphify`** - turns any folder of code/docs/papers into a navigable knowledge graph. Three outputs:

- `graph.html` - interactive force-directed visualization, open in a browser.
- `graph.json` - GraphRAG-ready JSON with nodes, edges, hyperedges, communities, cohesion scores.
- `GRAPH_REPORT.md` - plain-language audit with god nodes (most-connected concepts), surprising connections, suggested questions.

I wire it into git hooks so the graph auto-rebuilds on every Python commit. Cost: ~2 s warm cache, ~8 s cold. Benefit: the architecture map is always current, and on session start the project's `SessionStart` hook injects `GRAPH_REPORT.md` into Claude's context. Architecture questions get answered without a file-read round trip.

The auto-regen wiring (in `.githooks/post-commit`):

```bash
#!/usr/bin/env bash
# Auto-regenerate the graphify knowledge graph after Python commits.
# Scoped to binance_robust/ to keep the scan fast and avoid pulling in
# Research/ and other non-production dirs.
if git diff-tree --no-commit-id --name-only -r HEAD | grep -q '\.py$'; then
  cd binance_robust && graphify update . >/dev/null 2>&1 && cd ..
fi
```

Plus a `pre-push` hook that blocks pushes if the committed graph is stale relative to HEAD. Together: the graph in source control is always in sync with the code.

#### The morning graphify caught an architecture bug nobody else would have

Let me tell you about the four weeks where I almost shipped a god-node into production without realizing it.

The HFT codebase had a stretch where I was deep in feature work - Mission 6, Mission 7, Mission 8 - landing fixes faster than I was reviewing the architecture. Each mission was small. Each mission was reviewed. Each commit was clean. But over four weeks, a quiet drift was happening that none of the per-commit reviews could see, because none of them looked across commits.

Then I ran `graphify update binance_robust/`. The report came back with the usual stats - a few thousand nodes, a few hundred communities. But the "god nodes" section, which lists the most-connected concepts in the codebase, had a new entry near the top: **`risk-governance`**, with edges into 18 other subsystems. The original architecture isolated `risk-governance` to two upstream callers and one downstream alerting path. Three. Not 18.

I read the report a second time and realized what had happened. Each of the last six missions had added one or two `from risk_governance import ...` lines to a different subsystem - usually for something innocent like "let's emit a metric here too" or "let's check the kill-switch state from this guard." Each addition was justified in isolation. None had been tested against the architectural intent. The cumulative effect was that `risk-governance` had become the central nervous system of the entire codebase, with all the coupling, blast radius, and refactor cost that implies.

If I had shipped that to production, the next architecture mission would have been a two-week refactor instead of a two-day one. Maybe a four-week one if I had waited until the next quarter. **The graph caught it because the graph is the only artifact that reads across commits.** Code review catches per-commit issues. Tests catch per-call issues. The graph catches *cumulative drift* - the slow accretion of edges that no individual commit looks like a problem.

That's the moment graphify went from "nice viz" to "non-negotiable infrastructure" in my workflow. It runs on every Python commit. It's injected into the SessionStart hook for the HFT project, so every Claude session opens with a fresh architectural picture. And when one of the hft-team specialists has to make a decision about where to put new code, they have the current god-node list - they can ask "is this addition going to make `risk-governance` worse?" before they even propose it.

This is the cross-layer thread that ties graphify back to everything else. Layer 1's `session_start.sh` injects the graphify report into context. Layer 5's specialists read that injected report when reasoning about where new code belongs. **Graphify is the spine that the agents read.** Without it, every architectural reasoning step in a multi-agent mission would be flying blind. With it, every agent starts with a current, accurate map.

**`drawio-architect`** - generates production-quality `.drawio` diagrams using *real graph-layout algorithms*, not text instructions to Claude:

- Sugiyama topological layering (depth-based, no layer skipping).
- Barycenter sweep within layers (3 passes, minimizes edge crossings).
- Orthogonal A* edge routing (no diagonal overlaps).
- Pixel-level vision audit using Pillow + NumPy (catches overlapping nodes, clipped labels, missing arrowheads).

Output: `.drawio` XML (editable in app.diagrams.net) + 2× PNG render + `issues.json`. If the audit fails, the spec is auto-edited and re-rendered (max 4 iterations). Most diagrams converge in 1–2 passes.

**`manim-animator`** - generates 3Blue1Brown-quality math animations from natural-language prompts using Manim Community Edition. Two modes: "fast" (480p15 for iteration) and "superintelligence" (1080p60 final render with dual-AI vision review - Claude multimodal + Gemini adversarial). I use this for explaining trading concepts in video form.

**`karpathy-guidelines`** - installable form of the Karpathy four-rule discipline (think before coding, simplicity first, surgical changes, goal-driven execution). I invoke it at the start of complex code reviews.

### Skills I considered and didn't install

A skill is a permanent context-window cost - every session pays for it. Add only what compounds. Things I evaluated and rejected:

- **Auto-formatter wrapper skills** - Claude already knows how to call prettier/black; a skill adds nothing.
- **Logging-statement adders** - single-purpose, doesn't compound.
- **"Generate JSDoc" skills** - better as a code-writing convention in the project's CLAUDE.md.

The bar: would a skill make Claude meaningfully *better at a category of work*? If yes, install. If it's just another prompt template, don't.

---

## 7. Layer 5 - Agents: the specialists.

Skills are verbs. Agents are nouns. When the task fits a specialist's expertise better than a generalist's, you dispatch the specialist.

![Agent decision tree](/diagrams/06-agent-decision-tree.png)

The decision logic is simple:

- **Need broad codebase recon?** → `Explore` agent (read-only, fast, fan-out 3 in parallel for a survey).

For the multi-tier hierarchy specifically (the one I built for HFT, but the *pattern* is what matters), here is the full dispatch lifecycle - apex routes to chiefs, chiefs to leads, leads to specialists, specialists write handover blocks back into the workbook for synthesis:

![Agent dispatch lifecycle - apex to specialists, with CONSULT-REQUEST loopback](/diagrams/15-agent-dispatch.png)

Two things to notice. First, the **Single domain?** decision at the apex tier is a real branch - a one-line typo fix never goes through chiefs and leads; it routes directly to the right specialist and skips four levels. The hierarchy only kicks in when the mission *actually* spans multiple domains. Second, the **CONSULT REQUESTS** loopback at the specialist tier is the protocol that lets a specialist ask a peer ("→ god-agent: 'is this synchronization scheme race-safe?'") without leaving its lane - the apex receives the consult request, dispatches the peer in parallel, and feeds the answer back. This is how you get peer review *between* agents without flattening the hierarchy. The whole machine writes its working memory into the mission workbook so that any future Claude session - or you, six months from now - can read exactly how the team arrived at the final synthesis.
- **Single specialist can answer it?** → call the specialist directly.
- **Multi-domain mission?** → dispatch via an apex (`hft-cto` for HFT work; main session orchestrates otherwise).
- **Sub-tasks independent?** → fan out N agents in **one message** - they run concurrently.

### My generic agents

Twelve domain-agnostic specialists, useful in any project:

```
~/.claude/agents/
├── ai-engineer.md                      ← Opus. AI/ML/MLOps from math foundations to deployment
├── backend-specialist.md               ← Sonnet. APIs, DBs, queues, FastAPI/Express/Hono/NestJS
├── code-reviewer-generic.md            ← Sonnet. Domain-agnostic PR review with Karpathy discipline
├── config-compliance-enforcer.md       ← Sonnet. Single-canonical-path config pattern enforcement
├── devops-specialist.md                ← Sonnet. Docker/K8s/Terraform/GitHub Actions/IaC
├── frontend-specialist.md              ← Sonnet. React 19/Next 15/TS-strict/Tailwind 4/shadcn
├── god-agent.md                        ← Opus. Architecture validation against industry standards
├── hft-systems-architect.md            ← Opus. HFT/ULL theory, Citadel/Jane Street depth
├── mermaid-agent.md                    ← Sonnet. Mermaid diagram generation
├── scientific-blogger.md               ← Sonnet. Markdown research/blog writing with structure
├── security-auditor-generic.md         ← Opus. OWASP Top 10 + language footguns
└── test-writer-generic.md              ← Sonnet. TDD specialist, mock-first
```

Each agent is a single `.md` file with frontmatter:

```yaml
---
name: backend-specialist
description: REST/GraphQL APIs, databases (Postgres, SQLite, Redis), queues,
  background jobs, FastAPI / Express / Hono / NestJS. Use for API endpoint
  design, schema/migration questions, query optimization, queue and worker
  patterns. Read+Write.
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

You are a senior backend engineer. Defaults: FastAPI / Pydantic / SQLAlchemy /
Postgres for Python; Hono or Express / Drizzle or Prisma / Postgres for TS.
Override only when the project says otherwise.
```

The `description` field is what Claude pattern-matches on when deciding whether to dispatch this agent. **Write descriptions like a router would read them** - front-load the trigger words ("REST/GraphQL APIs, databases…") and end with explicit DO/DO-NOT scope.

### Built-in agents I rely on

- **`Explore`** - fast, read-only, no editing. Spawn three in parallel to map a codebase quickly.
- **`Plan`** - designs implementation plans without executing. Hand it the requirements + your exploration results; receive a step-by-step plan.
- **`general-purpose`** - full toolset. Use when no specialist fits and you need open-ended capability.

### Case study - how I built a 24-agent specialist team for HFT

This is the part of the post where my day-job creeps in, but stay with me - the *pattern* transfers even if the specifics don't. If you do not work on trading systems, mentally swap "HFT" for "ML training pipeline", "monorepo with 12 microservices", "game engine with five subsystems", or "any codebase where one generalist agent has started giving you confidently-wrong answers".

I work on a high-frequency trading system. The codebase calls itself, in its own README, "the federal-grade HFT crypto pipeline," and its preamble document opens with a line I think about every week:

> *"In the domain of High-Frequency Trading (HFT), data is not merely a stream of numbers; it is the fundamental reality upon which all financial decisions are based. A missing tick is not a statistic; it is a blind spot in the market view. A 100ms latency spike is not a glitch; it is an arbitrage opportunity lost to a competitor.*
>
> *The Binance Robust pipeline was engineered with a singular, uncompromising directive: **Zero Data Loss over a 5-Year Operational Horizon.**"*

That mandate is what dictates the agent architecture. Not "best practices." Not "scalability." A specific, testable promise - zero ticks lost, five years, no excuses - that any agent making a decision in this codebase has to weigh against. You cannot ask one generalist to hold that constraint while also reasoning about WAL durability, while also reasoning about lock-free SeqLock correctness, while also reasoning about Postgres COPY batch sizing, while also reasoning about kernel IRQ affinity. The cognitive load explodes; the hallucinations creep in; and a hallucination in this codebase is not a typo, it's a missing tick.

The codebase has subsystems with very different concerns: ingestion, WAL durability, shared-memory IPC, indicator math, trading-engine state machines, observability, risk governance, kernel tuning. A backend-specialist isn't qualified to reason about lock-free SeqLock correctness; an HFT specialist isn't qualified to design a Postgres COPY batch. I needed *real specialization*, with each specialist holding only the slice they're qualified to hold.

So I built a four-tier hierarchy as a Claude Code plugin:

```
hft-cto                        ← apex router, Opus, full mission orchestration
├── chief-systems-engineer     ← runs the "how it runs" branch
│   ├── lead-platform-engineer
│   │   ├── shared-memory-ipc-owner
│   │   ├── wal-durability-replay-owner
│   │   ├── database-persistence-owner
│   │   └── ingestion-messaging-owner
│   └── lead-perf-infra-engineer
│       ├── kernel-network-infra-owner
│       ├── latency-performance-owner
│       └── pipeline-orchestrator-owner
├── chief-quant-researcher     ← runs the "what it decides" branch
│   ├── lead-strategy-engineer
│   │   ├── indicators-engine-owner
│   │   ├── execution-microstructure-owner
│   │   └── trading-engine-risk-owner
│   └── lead-risk-compliance
│       ├── risk-governance-owner
│       ├── observability-sre-owner
│       └── devops-release-owner
├── architecture-review-board  ← arbiter for cross-domain disputes
└── advisory gods (3, Opus)    ← rust-systems-god, cpp-hotpath-god, cuda-gpu-god
```

**The pattern:**

- **Apex** (`hft-cto`) - entry point for missions. Decides whether the mission needs a chief or just a single specialist. Routes accordingly. Merges outputs. Applies final clearance.
- **Chiefs** - own a half of the system. Coordinate leads. Use when the mission spans multiple lead branches.
- **Leads** - own a vertical slice. Coordinate 2–3 specialists.
- **Specialists** - own a single subsystem. Cite `file:line` evidence in every claim.
- **Advisors** - language-level oracles (Rust, C++, CUDA). Today they're advisory because the codebase is Python; when Rust lands they expand to implementer+reviewer.
- **Arbiter** - when two specialists disagree, the arbiter (architecture-review-board) decides and emits a binding ADR.

**The consult protocol.** Any agent can emit a `CONSULT REQUESTS` block to ask peers for input. The caller dispatches the peers in parallel and feeds results back to the requesting agent. This emulates async-await across agents and prevents any single agent from pretending to expertise it doesn't have.

**The shared preamble.** Every agent in the team inherits a `~/.claude/plugins/hft-team/shared/preamble.md` that encodes the non-negotiable rules. Three of them in particular do most of the work:

```markdown
## 1. Ground-truth order (mandatory)

| Priority | Source                                                         | Status              |
|----------|----------------------------------------------------------------|---------------------|
| 1        | Python source files (*.py) under binance_robust/               | authoritative       |
| 2        | binance_robust/system-design/CODEBASE_KNOWLEDGE_README.md      | audited nav guide   |
| 3        | binance_robust/graphify/GRAPH_REPORT.md + graph.json           | god-nodes, communities |
| 4        | binance_robust/system-design/assets_drawio/DIAGRAM_MANIFEST.md | file:line evidence  |
| ❌       | Every other .md file in the repo                               | STALE - DO NOT CITE |

## 2. Evidence rule

Every non-trivial technical claim MUST cite file:path:line_number with a ≤5-line excerpt.
- No excerpt → no claim.
- No line number → no claim.
- If you cannot verify, say "unverified - need to read X" instead of guessing.

## 3. Investigate-then-implement protocol

Order of operations for EVERY non-trivial task:
1. Investigate - read relevant Python sources, map execution flow.
2. Report - summarize findings with file:line evidence, raise questions.
3. Wait - explicit "go ahead" from user.
4. Implement - only after approval.
```

That preamble is the closest thing this whole post has to a manifesto. It is what stops Claude from being plausibly wrong. Source code is truth. Docs are presumed stale. No claims without evidence. No edits without approval. Read those four paragraphs again - they're going to keep showing up, in different costumes, for the rest of this post.

**Shouldn't you just use one big agent?** I tried. The big agent hallucinated specialist knowledge. The specific moment that ended the experiment: I asked it about coordinating reads on the shared-memory tick buffer. It confidently proposed a single-writer-multi-reader pattern using *plain `volatile` reads* - the kind of pattern that "looks fine" in code review and produces silent corruption on x86-64 the moment two reader cores hit the same cache line. A specialist with a Python source-of-truth in its preamble and a god-agent on consult would never have proposed it. The generalist proposed it because it was synthesizing from C-language tutorials in its training data, not from the actual Python `SeqLock` implementation in `binance_robust/shared_memory/`. **The cure for hallucination is not a smarter generalist. The cure is structural - narrow each agent's scope to a slice it can actually verify, and force every claim to cite the source.**

#### What dispatching the team actually looks like - a real latency-regression mission

Let me show you a dispatch transcript. This is a generic version of a real mission from the archive - names of internal modules generic-ized, but the *shape* is exactly what happens when I type a multi-domain prompt and the team takes over. Three messages, three minutes of wall-clock, eight minutes of LLM compute, all four agents working in parallel.

> **You:** Tick-to-publish p99 doubled overnight on the SYMBOL_A feed - was 1.4 ms yesterday, 3.1 ms this morning. Find the regression. Be evidence-based, no guessing.
>
> **`hft-cto` (apex):** This spans perf-infra and platform. Decomposing into three parallel investigations:
>   1. `latency-performance-owner` - bisect the regression window, check Prometheus histograms for which stage of the tick pipeline absorbed the increase.
>   2. `kernel-network-infra-owner` - check IRQ affinity drift, NIC queue config, recent kernel updates that could have affected scheduling.
>   3. `pipeline-orchestrator-owner` - check if the asyncio supervisor's task counts changed; rule out a new task being scheduled on the hot loop.
>
> Dispatching all three in parallel. Each will return a handover block per the workbook convention. Workbook: `.claude/workbooks/2026-05-01-tick-p99-regression.md`.
>
> *[Three agents fire in parallel. ~90 seconds wall-clock.]*
>
> **Handover from `latency-performance-owner` (2026-05-01T07:14:22Z):**
> **Investigated:** Prometheus `tick_to_publish_seconds` histogram per-stage breakdown. `processing/conflation.py:118` shows the conflation stage absorbed +1.6 ms of the +1.7 ms total. Other stages flat within noise.
> **Concluded:** Regression is in the conflation stage. Not network. Not asyncio scheduling. Whatever changed, changed `processing/conflation.py` or its inputs.
> **Recommended next:** → `pipeline-orchestrator-owner`: "Did the conflation interval config change in the last 24h?"
>
> **Handover from `kernel-network-infra-owner` (2026-05-01T07:14:38Z):**
> **Investigated:** `/proc/interrupts` snapshot vs. yesterday's archived snapshot. NIC queue affinity unchanged. No kernel package updates in `apt log` for the last 7 days.
> **Concluded:** Kernel/network ruled out. Not the source.
>
> **Handover from `pipeline-orchestrator-owner` (2026-05-01T07:14:51Z):**
> **Investigated:** `git log --oneline -- config/config.yaml | head` shows commit `a3f2c19` from 2026-04-30 22:14 UTC changed `conflation_interval_ms: 5` → `conflation_interval_ms: 8`. Commit message: "tighten conflation per latency-perf advisory."
> **Concluded:** **Found the regression.** The "tighten" commit increased the interval, not decreased it - the commit message is inverted from the actual change. With an 8 ms interval, p99 will move from ~1.4 ms (mostly the 5 ms interval baseline) to ~3.1 ms (the 8 ms interval baseline + tail). This matches the observed regression to within noise.
> **Recommended next:** → user: "Revert `a3f2c19` or correct `conflation_interval_ms` to the intended value."
>
> **`hft-cto` synthesis:**
> Regression isolated to commit `a3f2c19` (2026-04-30 22:14 UTC). The commit message says "tighten" but the value moved from 5 ms → 8 ms, which is the opposite of tightening. Three independent specialists agree: not network, not scheduling, all in the conflation interval. Suggested action: revert and re-deploy. Estimated time-to-restore: <5 minutes once the revert is approved.

That is what specialization in action looks like. Three minutes from question to root-cause, with three independently-verified angles, every claim citing a `file:line` or a `git` artifact, and a final synthesis that's defensible. No agent hallucinated. No agent strayed outside its lane. The generalist couldn't have done this in three minutes - it would have spent forty minutes spelunking before finding the config diff, because no single generalist agent has the bandwidth to hold all three reasoning frames at once.

If your project has subsystems with genuinely different reasoning requirements, build a hierarchical team. Start with 3–5 specialists. Add an apex when you hit cross-domain missions. Add an arbiter when specialists start disagreeing. Don't build the full 24-agent thing on day one - I didn't either. Each specialist in mine was earned by an incident report. The lock-free SeqLock specialist exists because of the `volatile` reads incident. The risk-governance specialist exists because of the god-node drift I described in Layer 4. **You don't design a 24-agent team. You let one accrete, agent by agent, every time the generalist gets it wrong.**

---

## 8. Layer 6 - MCP servers: external minds.

The Model Context Protocol (MCP) is Anthropic's interface for plugging external systems into Claude as first-class tools. You write or install an MCP server; Claude can call its tools as naturally as `Read` or `Bash`.

![MCP fleet topology](/diagrams/07-mcp-fleet-topology.png)

#### What an MCP server actually is, in one paragraph

Before we get to the fleet I run, let me demystify the term, because "Model Context Protocol" sounds more abstract than it is. **An MCP server is a long-running subprocess on your machine that exposes a JSON-RPC interface.** Claude Code starts the subprocess when it launches, talks to it over stdio, and the subprocess advertises a list of tools - each tool has a name, a description, a JSON schema for its input, and a function on the other end that returns a result. Once registered, the tools show up in Claude's tool palette indistinguishable from `Read`, `Write`, or `Bash`. When Claude calls `gemini_ask("...")`, it's the same code path inside Claude Code as calling `Read(...)` - it's just dispatched to a different subprocess. That's the entire trick. The reason the protocol matters is that it gives you a uniform, language-agnostic way to plug *anything* into Claude - a database, a browser, another LLM, a vendor's API - without writing a custom plugin or modifying Claude Code itself. Twenty lines of Python and you've added a first-class tool.

I run five user-scope MCPs. Each is a deliberate choice - every MCP is context-window weight you pay on every session.

### Verifying what you've got

```bash
$ claude mcp list
Checking MCP server health…

claude.ai Excalidraw: https://mcp.excalidraw.com/mcp - ✓ Connected
gemini: /home/neo/miniconda3/bin/python3 /home/neo/.claude/mcp-servers/gemini/server.py - ✓ Connected
github: npx -y @modelcontextprotocol/server-github - ✓ Connected
context7: npx -y @upstash/context7-mcp - ✓ Connected
playwright: npx -y @playwright/mcp - ✓ Connected
ruflo: ruflo mcp start - ✓ Connected
```

Five user MCPs all green. (The `claude.ai Google …` MCPs above need OAuth and I don't use them.)

### Gemini - the second-opinion oracle

The big one. I built a custom MCP server that exposes Google Gemini 3.1 Pro as four tools to Claude. The full source is at `~/.claude/mcp-servers/gemini/server.py` (423 lines); here's the policy header that defines the contract:

```python
"""Gemini MCP server - exposes Google Gemini models as tools callable from Claude Code.

Hard policy (user-directed):
  - ONLY gemini-3.1-pro-preview is used. No fallbacks. No automatic
    substitution with 2.5-pro, flash, or any other model.
  - Thinking mode is ALWAYS ON (thinking_budget=-1, dynamic unbounded).
  - Strong default system prompt for deep reasoning and production-quality output.
  - If the API returns an error (429 RESOURCE_EXHAUSTED, thinking_config rejected,
    anything else) we surface it verbatim. The user wants to wait for quota
    reset rather than accept a lesser model's output.

Tools:
  - gemini_ask            : general single-turn query
  - gemini_long_context   : prompt + list of file paths; 1M-token context
  - gemini_second_opinion : adversarial challenge of another AI's reasoning
  - gemini_list_models    : list models the API key can see (diagnostic only)
"""
```

Three deliberate design choices:

**1. Hard-pin to one model.** `gemini-3.1-pro-preview` only. No automatic fallback to 2.5-pro or flash. If you ask for a second opinion you want the *strong* second opinion. Silent downgrades to a lesser model defeat the entire purpose.

**2. Thinking always on.** `thinking_budget=-1` - dynamic unbounded. The model decides how much to think. For an oracle whose value is depth, you never want to hobble that.

**3. No fallback on 429.** If the daily quota is exhausted, the server surfaces the quota error verbatim and you wait for it to reset. The wait is the right answer because you opted into 3.1-pro by calling this tool.

The default system prompt is itself a small artifact:

```
You are a senior principal software engineer with deep expertise across systems,
ML, low-latency trading infrastructure, and modern web/UI. You are invoked via
an MCP bridge from another AI's session, so the caller is typically another AI
or a developer who wants a substantive, rigorous answer - not a minimal stub.

Default posture for every response:
- Think carefully before writing. Use your full reasoning budget...
- Produce complete, working implementations - not minimal "hello world" stubs...
- Prefer long, substantive responses over short ones. If a question warrants
  600 lines of code, write 600 lines. Do not self-truncate to seem concise.
- Tradeoff: bias toward depth over speed. Latency is acceptable; shallow output
  is not.
```

When Claude calls `gemini_second_opinion(my_reasoning, question)`, what comes back is a thoughtful red-team of the proposed plan - not agreement, not summary, *challenge*. This is the most valuable thing I do with the Gemini MCP. Claude is genuinely good at finding holes in its own reasoning when prompted; pairing it with an independent model finds holes neither would catch alone.

#### The afternoon Gemini caught a race condition Claude was about to ship

Here's the canonical example of why I wired Gemini into the loop. The HFT codebase has a shared-memory ring buffer for tick handoff between the ingestion process and the trading process. I was reviewing a proposed refactor with Claude - multi-producer multi-reader, lock-free, the whole exercise. Claude read the implementation, walked through the SeqLock invariants, and concluded:

> "The pattern looks correct. The writer increments the sequence counter before and after the write; readers read the counter, read the data, re-read the counter, and retry if the counter changed or has the low bit set. This matches the canonical SeqLock pattern from Linux's kernel/seqlock.h. Approve."

Three approvals deep, I pasted the same code and Claude's analysis into `gemini_second_opinion`. Gemini came back, reasoning visibly, with this:

> "The pattern is correct in isolation, but you have a memory-ordering hazard at the producer-side that the SeqLock construction does NOT protect against on x86-64 under cache-line conflicts. Specifically: line 47 increments the sequence counter using a plain store, then writes the payload at lines 48–55, then increments the counter again at line 56. On x86-64 the store-buffer can reorder the payload writes with respect to the trailing counter increment as observed by another core that's contending on the same cache line - the *trailing* sequence write may become visible to a reader before some of the payload writes have flushed from the producer's store buffer. The SeqLock retry loop will then accept stale data because the trailing counter looks 'clean.' You need an explicit `__atomic_thread_fence(__ATOMIC_RELEASE)` between the payload writes and the trailing counter increment, OR the trailing increment itself must be `__atomic_store_n(..., __ATOMIC_RELEASE)`. Without one of those, the implementation is racy under realistic load. Sutter's 2012 atomic-weapons talk has the canonical example."

I read that, opened a tab, re-read Sutter's *atomic<> Weapons* slides, and lost forty-five minutes confirming the diagnosis. Gemini was right. Claude was wrong. Both were operating in good faith - Claude was matching against the canonical SeqLock pattern; Gemini was matching against the canonical *broken* SeqLock implementation that comes up in every multicore-correctness postmortem. Without the second-opinion call, that race would have shipped and produced exactly the kind of "mystery stale tick once an hour" bug that takes a quarter to diagnose in production.

That is what `gemini_second_opinion` *is*. Not a polite reviewer. Not a rubber stamp. An adversary, instructed to challenge - and pinned to a model strong enough to actually find the holes. Without the hard pin to `gemini-3.1-pro-preview`, a silent fallback to `gemini-2.5-flash` might have come back with "looks good" and the bug would have shipped anyway. The hard pin matters because the *value* of the second opinion is in the depth, not the response. **A weaker model agreeing with you is worse than no second opinion at all, because it gives you false confidence.**

This is the cross-layer thread for Layer 6: the Gemini MCP is invoked *inside* the missions you saw in Layer 5 and recorded *into* the workbooks you saw in Layer 3. When `hft-cto` is about to clear a non-trivial mission, it can call `gemini_second_opinion` as the final adversarial check, fold the response into the workbook as a `Round N - adversarial review` block, and only then let the mission close. The MCP isn't a separate tool you remember to use; it's a layer the agent hierarchy reaches for automatically when the cost of being wrong is high.

### GitHub - non-CLI flows

The `gh` CLI handles 90% of GitHub work. The GitHub MCP earns its keep on the other 10%: multi-step PR triage, complex issue filters, structurally fetching PR comments + reviews in one round trip instead of three. Install: `claude mcp add -s user github npx -- -y @modelcontextprotocol/server-github`.

### Context7 - current library docs

Claude's training data has a cutoff. When you ask about Next.js 15 features and Claude was trained on Next.js 14, you get plausible-but-wrong code. Context7 is an MCP that fetches **current docs** for any library on demand. Install: `claude mcp add -s user context7 npx -- -y @upstash/context7-mcp`. Use it whenever the answer depends on a library version Claude might not know.

### Playwright - browser automation

For end-to-end testing, scraping, screenshots, or anything else that needs a real browser. Install: `claude mcp add -s user playwright npx -- -y @playwright/mcp`. Then run `npx playwright install chromium` once to get the browser binary.

I used Playwright (via this MCP) to render the HTML mockups in this very blog post. Headless screenshot, deterministic, no manual capturing.

### Ruflo - persistent memory + embeddings (curated)

Ruflo is a sprawling toolkit (~200 MCP tools). My CLAUDE.md restricts what's actually used to a curated subset:

- **`memory_*`** - cross-session persistent KV memory beyond Claude Code's per-project auto-memory. Spans projects.
- **`agentdb_hierarchical-*`, `agentdb_pattern-*`** - tiered persistent memory (working / episodic / semantic).
- **`embeddings_init`, `embeddings_generate`, `embeddings_search`** - HNSW vector index. This is the Phase 2 backbone for the archive: when `~/claude-archive/` grows past the point where `grep` is fast enough, the embeddings layer goes on top without replacing it.

Everything else in Ruflo (swarm, hive-mind, neural training, browser automation, hooks-of-its-own) is **denylisted** in my CLAUDE.md - I either have a better in-tree primitive (Claude Code subagents for orchestration, native hooks for triggers) or it's experimental and unverified. Mixing Ruflo's swarm with Claude Code's subagents breaks dispatch routing; using Ruflo's hooks would conflict with my pre_tool_use safety hook. The lesson: a powerful tool, used selectively.

### Extending the setup - Gemini, Llama, OpenAI, or any model you can hit over an API

This is the part of Layer 6 that unlocks the rest of your post-Anthropic future.

Here is the topology you are extending - five MCPs in production today, plus the dotted-line slots where any model-as-MCP server you write next plugs into the same router with no changes to Claude Code itself:

![MCP fleet - production today, extension slots tomorrow](/diagrams/13-mcp-topology.png)

Notice the dashed boxes on the right. Each one is the same shape as the production servers on the left - a small Python (or TypeScript) process speaking JSON-RPC over stdio to Claude Code's tool router. The topology never has to change as you add models; you write a new server, run `claude mcp add`, and Claude can call its tools the next session. The router doesn't care whether the model behind a tool is Anthropic, Google, Meta, OpenAI, or your own fine-tune.

The Gemini MCP server I described above isn't special. It's a 423-line Python file using the official MCP SDK that exposes four tools backed by Google's API. The exact same pattern works for *any* LLM you can hit over HTTP - Llama running locally on Ollama or vLLM, OpenAI's frontier models, Mistral, DeepSeek, Cohere, anything. Once you've understood the Gemini server as a pattern, adding a second model is an afternoon. Adding a third is an hour.

**The shape of every model-MCP server.** Strip the Gemini server down to its essentials and you get:

```python
# ~/.claude/mcp-servers/<your-model>/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("<your-model>")

@mcp.tool()
def <model>_ask(prompt: str, system_instruction: str | None = None) -> str:
    """One-line description Claude will pattern-match on."""
    # Call your model's API here. Return the text response.
    return your_model_client.generate(prompt, system=system_instruction)

@mcp.tool()
def <model>_second_opinion(question: str, my_reasoning: str) -> str:
    """Adversarial red-team of another AI's reasoning."""
    # Same call, with a system prompt that instructs the model to challenge.
    ...

if __name__ == "__main__":
    mcp.run()
```

Twenty lines of structural code, plus whatever client library your model needs. Register it with `claude mcp add -s user <name> "$(which python3)" -- ~/.claude/mcp-servers/<name>/server.py` and Claude can call your tools as naturally as `Read` or `Bash`. There's nothing to compile, no plugin to install, no review from Anthropic - the MCP protocol is open.

**Wrapping a local Llama via Ollama.** If you want sovereignty over your second-opinion model - running it on your own machine, no API quotas, no per-token costs - point a server at a local Ollama endpoint:

```python
import requests

@mcp.tool()
def llama_ask(prompt: str, model: str = "llama3.3:70b") -> str:
    """Ask the locally-hosted Llama model. Use for offline second opinions."""
    resp = requests.post("http://localhost:11434/api/generate",
                          json={"model": model, "prompt": prompt, "stream": False},
                          timeout=300)
    resp.raise_for_status()
    return resp.json()["response"]
```

Same registration command. Same first-class tool experience. Now Claude has a *local* second opinion it can reach without a network round-trip - useful for when you're on a plane, when the API is rate-limited, or when the question genuinely shouldn't leave your machine.

**Wrapping OpenAI.** Identical pattern, different client library:

```python
from openai import OpenAI
client = OpenAI()  # reads OPENAI_API_KEY from env

@mcp.tool()
def gpt_second_opinion(question: str, my_reasoning: str) -> str:
    """Get GPT's adversarial review of Claude's reasoning."""
    resp = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are an adversarial reviewer..."},
            {"role": "user", "content": f"Question: {question}\n\nReasoning: {my_reasoning}"},
        ],
    )
    return resp.choices[0].message.content
```

**Three guardrails I learned the hard way when adding models:**

1. **Hard-pin the model.** Never let the server silently fall back to a cheaper version when quota runs out. The whole *point* of a second-opinion call is depth; a degraded model returning "looks good" is worse than no second opinion at all because it gives you false confidence. Surface the quota error verbatim. Wait for the reset.
2. **Make every tool's description specific.** Claude pattern-matches on description text to decide which tool to call. `gpt_ask` is too vague; `gpt_second_opinion` is precise enough that Claude won't accidentally invoke it for a casual question.
3. **One server, one model family.** Don't try to multiplex Gemini + GPT + Llama into one server with a `model=` parameter. Three small servers are easier to debug, version, and selectively disable than one large multiplexer.

The takeaway: **MCP is the unlock for model-agnostic AI workflows.** You're not betting your career on Anthropic remaining the frontier. You're using Claude Code as the orchestration layer, and you can add or swap external models behind it as the landscape shifts. Two years from now when something better than Claude exists, you keep the entire setup - the hooks, the memory, the agents, the skills, the workbooks - and you swap in a new MCP server. That's the architecture's hidden gift.

### Wiring all five at install time

```bash
claude mcp add -s user gemini "$(which python3)" -- ~/.claude/mcp-servers/gemini/server.py
claude mcp add -s user github npx -- -y @modelcontextprotocol/server-github
claude mcp add -s user context7 npx -- -y @upstash/context7-mcp
claude mcp add -s user playwright npx -- -y @playwright/mcp
# (ruflo MCP gets registered automatically by `ruflo init`)
npx playwright install chromium
```

Then:

```bash
claude mcp list   # confirm all 5 ✓ Connected
```

If any show `! Needs authentication` or `× Failed`, fix that one before moving on. A broken MCP is dead context-window weight.

---

## 9. Layer 7 - The plugin ecosystem.

Plugins are bundles. A plugin can ship skills, agents, slash commands, hooks, and MCP server configs together. The Claude Code plugin marketplace lets you install official + community bundles with one command.

My current install:

```json
"enabledPlugins": {
  "frontend-design@claude-plugins-official": true,
  "feature-dev@claude-plugins-official": true,
  "superpowers@claude-plugins-official": true,
  "code-review@claude-plugins-official": true,
  "typescript-lsp@claude-plugins-official": true,
  "claude-md-management@claude-plugins-official": true,
  "ralph-loop@claude-plugins-official": true,
  "figma@claude-plugins-official": true,
  "huggingface-skills@claude-plugins-official": true,
  "explanatory-output-style@claude-plugins-official": true
}
```

Ten enabled. Three of them carry most of the weight; the rest are situational.

**The three that change how I work every day:**

`superpowers` is the one to install first. Twelve lifecycle skills that fundamentally shift Claude from "code-now" to "think-then-code" - covered already in Layer 4. If you install nothing else from the plugin ecosystem, install this.

`feature-dev` adds three coordinated sub-agents (`code-architect`, `code-explorer`, `code-reviewer`) for non-trivial features. The architect designs, the explorer maps existing code, the reviewer audits the result. I use it whenever I'm about to write more than ~200 lines.

`frontend-design` adds a skill that produces UI biased *away* from generic AI aesthetics. When I want a UI that doesn't look like every ChatGPT-generated landing page on the internet, I invoke this.

#### What `frontend-design` actually does, with a real prompt

Let me show you the difference, because "biased away from generic AI aesthetics" is the kind of phrase that sounds nice and means nothing until you watch it work.

> **You (without `frontend-design`):** Build me a settings page with a theme toggle for my SaaS dashboard. Tailwind, shadcn, Next 15.
>
> **Claude:** *Generates a card with a centered title, a `Switch` component from shadcn, a description below, and a "Save changes" button. White background. Standard slate text. The theme toggle is the second item under "Appearance," nestled between an unused "Language" dropdown and a "Reduce motion" switch nobody asked for.*
>
> *[The output is competent and generic. You've seen this exact page on forty SaaS dashboards. It will work. It will also be invisible to anyone who's tired of generic SaaS dashboards.]*

> **You (with `frontend-design` loaded):** Build me a settings page with a theme toggle for my SaaS dashboard. Tailwind, shadcn, Next 15.
>
> **Claude (after invoking the skill):** Before I generate, let me commit to a few opinionated choices and tell you why so you can override.
>
> 1. **Layout:** Two-column on desktop (sticky nav with section labels on the left, settings panels on the right), single-column on mobile with a sticky section-header. Most settings pages use a single centered column; the two-column gives me room to make each section feel like a *room*, not a list item.
> 2. **The theme toggle as the hero of the "Appearance" section, not a row.** A 240×140 preview card showing the current theme rendered live (with mock content), and three preset chips below it (Light · Dark · Auto-by-time). Hover on a chip morphs the preview before commit. This makes the choice tactile, not abstract.
> 3. **No save button on toggle changes.** Settings auto-save on commit; the section header shows a 1.2s "Saved" affordance with a subtle horizontal sweep. Save buttons on settings pages are vestigial - they introduce a state where the UI lies about what's persisted.
> 4. **Color story:** rather than the default slate-50/slate-900, I'd use a single accent (your existing brand color) for the active state and one neutral with two warmth steps. The default Tailwind palette is the giveaway that something was AI-generated; one custom accent kills that signal instantly.
>
> Want me to override any of these before I generate the code? Otherwise I'll proceed with all four.

That's the skill working. It's not a different *codebase*; it's a different *posture*. The skill forces Claude to enumerate design decisions it would otherwise make silently, justify them in the language of UX rather than the language of components, and offer you the ability to override before code is committed. The output, after the four bullets, is a settings page you'd actually be proud to ship.

The skill's value isn't aesthetic - it's epistemic. It moves the design decisions out of "things Claude assumed" and into "things you and Claude agreed to," which is the only way a UI ever stops looking like a checklist.

**The other seven, briefly:**

| Plugin | When to use |
|---|---|
| `code-review` | Slash-command PR review when `gh pr view` isn't enough. |
| `claude-md-management` | Inheriting a repo with a bloated or stale CLAUDE.md. |
| `ralph-loop` | "Run this every 5 minutes" workflows (deploy watching, queue draining). |
| `huggingface-skills` | Training, eval, dataset, or paper-publishing work on HF. |
| `typescript-lsp` | TypeScript projects - type-aware refactor + autocomplete inside Claude. |
| `figma` | Design-to-code via Figma; collapses the handoff. |
| `explanatory-output-style` | Learning a new domain - Claude includes brief teaching asides. (Yes, this post was written in it.) |

### Installing plugins

Two-step:

```bash
# 1. Add the marketplace if not already present:
claude marketplace add claude-plugins-official  # one-time

# 2. Install:
claude plugin install superpowers@claude-plugins-official
claude plugin install feature-dev@claude-plugins-official
# ... etc
```

To disable without uninstalling:

```bash
# Edit ~/.claude/settings.json:
"enabledPlugins": {
  "superpowers@claude-plugins-official": false,   # disabled, still installed
  ...
}
```

Disabling is useful for experimenting with a smaller context. If you have 10 plugins enabled and you start hitting context limits, disable the ones least relevant to today's work.

### Things I tried and disabled

Two ex-installs, briefly: a documentation-writer plugin (output was generic and templatey; the `scientific-blogger` agent plus good prompts beats it) and an auto-PR-summarizer plugin (a CLAUDE.md rule plus `gh pr create` does the same job at zero context cost).

The bar to add a plugin is the same as the bar to add a skill: does it make Claude meaningfully better at a category of work? If the answer is "marginally," it's not worth the context-window weight.

---

## 10. Layer 8 - `project-bootstrap`: the day-1 workflow.

Layer 7 gave you the palette of plugins; Layer 8 is the mechanism that stamps those conventions onto every new project you start. Starting a fresh repo should not mean re-explaining your conventions to Claude every time. One command, three questions, a fully-conventioned scaffold.

### The three questions

When you say *"bootstrap this project"* in any directory (or `/project-bootstrap`), the skill asks:

1. **Domain** - HFT / quantitative trading · AI/ML training or research · Web full-stack · Automation / scripting · Other.
2. **Primary language(s)** - Python only · TypeScript / JavaScript only · Python + TypeScript · Other.
3. **Graphify auto-regeneration?** - Yes (wire `.githooks/post-commit` + `pre-push` to regen the knowledge graph on `.py` commits) or No (skip).

#### Live: thirty seconds from `mkdir` to "Claude knows this project"

Here's what running it on a brand-new directory actually looks like. Verbatim from a session I ran while drafting this post:

```
$ mkdir my-new-saas && cd my-new-saas
$ git init -q
$ claude
```

> **You:** /project-bootstrap
>
> **Claude:** Bootstrapping conventions for `my-new-saas`. Three questions:
>
> 1. **Domain?** (1) HFT / quantitative trading  (2) AI/ML training or research  (3) Web full-stack  (4) Automation / scripting  (5) Other
> 2. **Primary languages?** (1) Python only  (2) TypeScript/JavaScript only  (3) Python + TypeScript  (4) Other
> 3. **Wire graphify auto-regeneration on `.py` commits?** (yes/no)
>
> **You:** 3, 3, no
>
> **Claude:** Scaffolding now. *[28 seconds of file writes.]*
>
> ```
> ✓ CLAUDE.md (web full-stack + py/ts conventions, 78 lines)
> ✓ CLAUDE.local.md.template (rename to CLAUDE.local.md to use)
> ✓ .gitignore (extended with .claude/plans/, .claude/settings.local.json, etc.)
> ✓ .claude/settings.json (4 hooks pre-wired, py+ts allow patterns seeded)
> ✓ .claude/settings.local.json (gitignored personal allowlist)
> ✓ .claude/workbooks/INDEX.md
> ✓ .claude/plans/ (empty)
> ✓ docs/may_2026_onwards/ (5 templates: ADR, ADVISORY, MISSION_ISSUE, DEFERRED_ROADMAP, All_Issues)
> ✓ tests/ (placeholder)
> (no .githooks/ - graphify opted out)
>
> Bootstrap complete. Next steps:
> 1. Edit CLAUDE.md to add project-specific conventions you didn't get to mention here.
> 2. Rename CLAUDE.local.md.template → CLAUDE.local.md and add personal paths.
> 3. /exit and re-launch claude so the new .claude/settings.json hooks take effect.
> ```
>
> **You:** *[runs `tree -L 2`]*
>
> ```
> .
> ├── CLAUDE.md
> ├── CLAUDE.local.md.template
> ├── .claude
> │   ├── plans
> │   ├── settings.json
> │   ├── settings.local.json
> │   └── workbooks
> ├── docs
> │   └── may_2026_onwards
> └── tests
> ```

That's it. Twenty-eight seconds of scaffolding, three questions of input, and the new project inherits every convention I described in Layers 1 through 7. The next time I open Claude in this directory, the `session_start.sh` hook fires (workbook-hint runs because `.claude/workbooks/` exists), the project's `CLAUDE.md` loads (with the four-tier evidence-graded markers rule, the mission-workbook convention, the documentation standard), and the `.claude/settings.json` hooks are live.

Compare that to the alternative: spending five minutes the first time I open Claude here re-explaining "we use evidence-graded markers, not RESOLVED" and "mission workbooks go in `.claude/workbooks/`" and "always cite file:line." Five minutes × every new project × the rest of my career. The skill pays for itself the second time you use it. The third time, you wonder how you ever started a project without it.

### What it produces

```
<project root>/
├── CLAUDE.md                                   # project conventions (always)
├── CLAUDE.local.md.template                    # personal layer template (always)
├── .gitignore                                  # extended with Claude exclusions
├── .claude/
│   ├── settings.json                           # hooks + permissions for this project
│   ├── settings.local.json                     # personal allowlist (gitignored)
│   ├── workbooks/
│   │   └── INDEX.md                            # mission workbook index
│   └── plans/                                  # plan-mode artifacts (gitignored)
├── docs/
│   └── april_2026_onwards/
│       ├── ADR-001-<slug>.md.template
│       ├── ADVISORY-001-<slug>.md.template
│       ├── MISSION_X.X_ISSUE_<SLUG>.md.template
│       ├── DEFERRED_ISSUES_ROADMAP.md
│       └── All_Issues_Latest_April_2026.md
├── tests/
│   └── (placeholder)
└── .githooks/                                  # ONLY if graphify=yes
    ├── post-commit
    └── pre-push
```

The 14 templates live at `~/.claude/skills/project-bootstrap/templates/`:

```
ADR.template
ADVISORY.template
All_Issues.template
CLAUDE.local.md.template
CLAUDE.md.template
DEFERRED_ROADMAP.template
INDEX.md.template
MISSION_ISSUE.template
gitignore-additions.template
graphify-hook-block.template
post-commit.template
pre-push.template
settings.json.template
settings.local.json.template
```

**Substitution policy** (from the skill itself):

- `{{DATE_UTC}}` → `date -u '+%Y-%m-%d %H:%M:%SZ'`
- `{{MONTH_YEAR}}` → `date -u '+%B_%Y'` (e.g., `April_2026`)
- `{{PROJECT_NAME}}` → basename of cwd
- `{{LANGUAGES}}`, `{{DOMAIN}}` → user's answers
- `{{GRAPHIFY_BLOCK}}` → if yes, paste the graphify rules; else omit
- `{{LANGUAGE_ALLOWS}}` → seed allow patterns:
  - Python: `Bash(pytest:*)`, `Bash(python:*)`, `Bash(ruff:*)`, `Bash(mypy:*)`, `Bash(uv:*)`, `Bash(pip:*)`
  - TS/JS: `Bash(npm:*)`, `Bash(pnpm:*)`, `Bash(npx:*)`, `Bash(node:*)`, `Bash(eslint:*)`, `Bash(prettier:*)`, `Bash(tsc:*)`, `Bash(vitest:*)`
  - Always: `Bash(git:*)`, `Bash(gh:*)`, `Bash(make:*)`, `Bash(just:*)`, `Bash(rg:*)`, `Bash(jq:*)`

After scaffolding, the skill runs verification:

```bash
[[ -f CLAUDE.md ]] && echo "✓ CLAUDE.md"
[[ -f .claude/settings.json ]] && echo "✓ .claude/settings.json"
jq -e '.hooks // empty' .claude/settings.json >/dev/null && echo "✓ settings.json valid JSON"
[[ -d .claude/workbooks ]] && echo "✓ .claude/workbooks/"
[[ -d docs ]] && echo "✓ docs/"
ls .githooks/ 2>/dev/null && echo "✓ .githooks/" || echo "(no .githooks/ - graphify opted out)"
```

### What it deliberately doesn't do

From the skill source:

> - Does **not** install language toolchains (uv, pnpm, etc.). Assume they're already installed.
> - Does **not** create source code, application entry points, or framework scaffolds (use `create-next-app`, `cookiecutter`, `cargo new`, etc. for those).
> - Does **not** register MCP servers - those are user-scoped and registered once globally.
> - Does **not** modify `~/.claude/` - operates only on the current project.
> - Does **not** clobber existing files without asking (hard rule).

This is Karpathy "do exactly what was asked, nothing more" applied at skill design time. The skill's job is to scaffold conventions; not to be a project generator.

### One mission's lifecycle, end to end

![One mission's lifecycle](/diagrams/08-mission-lifecycle.png)

A typical multi-step mission, with all the layers acting in concert:

1. You: *"Implement feature X across the auth and billing modules."*
2. Claude opens `<repo>/.claude/workbooks/2026-04-26-feature-x.md` - this becomes the episodic memory for the entire mission.
3. Claude dispatches **two `Explore` agents in parallel**: one maps existing patterns for X, one maps tests covering X-adjacent code. Recon arrives in a single round trip.
4. Claude dispatches a **`Plan` agent**: "Design implementation given this recon." Receives a step-by-step plan with verification gates per step.
5. Plan written to `~/.claude/plans/<slug>.md`. Claude calls `ExitPlanMode` for your approval.
6. You approve.
7. **Per plan step:** Claude dispatches the appropriate **specialist agent**, the specialist edits files, returns a handover block (file:line evidence), Claude appends the handover to the workbook.
8. Optional: Claude calls **`gemini_second_opinion`** with the drafted plan and Claude's reasoning. Gemini red-teams. Claude folds the feedback in.
9. Claude runs tests / verifier. `PASS: 38 / REGRESSIONS: 0`.
10. Claude writes the workbook's `Final synthesis`, marks `Status: closed`.
11. You `/exit`.
12. The **Stop hook** archives the transcript + workbook + plans to `~/claude-archive/2026/04/<project>/<session-id>/`.

You now have:
- The code change shipped.
- A workbook documenting *why*, with file:line evidence at every step.
- A plan in `~/.claude/plans/`.
- An archived transcript that's `grep`-able forever.

If you come back tomorrow and ask "what did we do for feature X?", Claude finds the workbook by name, reads the handover blocks, and you're back in context in seconds - not minutes.

---

## 11. Layer 9 - Backup, replication, and the portable kit.

Let me tell you about the Friday my laptop died.

It was 6:47 PM. I was wrapping up a soak-test review and had just typed `git push` when the screen flickered, the fans went silent, and the machine refused to boot. SSD-controller failure, as I learned the next day. Not a thing I could troubleshoot remotely. The drive was bricked, the data was bricked, and the next morning's all-hands was in eleven hours.

If this had been six months earlier, that Saturday would have been a twelve-hour reinstall - re-registering MCPs, hunting `chmod +x` flags I had forgotten, regenerating OAuth tokens, fishing API keys out of password-manager attachments, re-discovering which environment variables lived in which `~/.bashrc` line, then spending Sunday afternoon learning what I had forgotten to back up. I had done that exact Saturday once already. I knew exactly how it ended.

Instead, I dragged the spare laptop out from under the desk, rsync'd the kit tarball off the home NAS, ran the recipe you're about to read, ran the verifier, watched it print `PASS: 38 / REGRESSIONS: 0`, and was back inside the same project - same memory, same workbooks, same conventions, same statusline showing the same cache-hit ratio I had walked away from - in **one hour and forty-three minutes**. The Monday all-hands ran on time. Nobody noticed the laptop had changed.

That is the story I want you to keep in your head while you read the rest of this layer. Portability is not a "nice to have." Portability is what turns a dead laptop on a Friday from a weekend-killer into a coffee-break. You should build this kit even if you never plan to migrate, because:

- **Disk failure happens.** A new laptop should be 90 minutes away, not 6 months.
- **The kit is also backup.** If you nuke `~/.claude/` by accident (and you will, eventually - every advanced user does), the kit restores it.
- **Sharing is high-leverage.** Teammates can adopt your setup in an afternoon. The kit is the artifact you ship them.

### What's in my kit

```
~/Desktop/Claude_Total_Replication/
├── README.md                                   ← manifest + reading order
├── Developer_Read.txt                          ← TL;DR for non-engineers
├── claude-cli-documentation.md      (185 KB)   ← 3,799-line full system reference
├── claude-cli-replication-recipe.md ( 15 KB)   ← 12-step replication recipe (Path A Ubuntu / Path B WSL2)
├── claude-config-bundle.tgz         ( 64 MB)   ← curated tarball of ~/.claude/ (excludes caches/secrets/transcripts)
├── claude-archive-bundle.tgz        (872 KB)   ← tarball of ~/claude-archive/
├── SECRETS_TEMPLATE.txt             (  1 KB)   ← placeholder for the 2 API keys (paste from password manager)
└── Blog/                                       ← THIS BLOG (markdown + diagrams + sources)
```

The two tarballs are the active payload. The two markdown files are the human-readable instructions. The secrets template is the only thing you fill in by hand on the new machine.

### Building the kit on your machine (one-time + on demand)

```bash
mkdir -p ~/Desktop/Claude_Total_Replication
cd ~

# 1. Bundle ~/.claude/ minus the noise
tar czf ~/Desktop/Claude_Total_Replication/claude-config-bundle.tgz \
    --exclude='.claude/cache' \
    --exclude='.claude/file-history' \
    --exclude='.claude/paste-cache' \
    --exclude='.claude/telemetry' \
    --exclude='.claude/session-env' \
    --exclude='.claude/sessions' \
    --exclude='.claude/shell-snapshots' \
    --exclude='.claude/todos' \
    --exclude='.claude/tasks' \
    --exclude='.claude/statsig' \
    --exclude='.claude/debug' \
    --exclude='.claude/downloads' \
    --exclude='.claude/ide' \
    --exclude='.claude/backups' \
    --exclude='.claude/projects' \
    --exclude='.claude/.session-clock' \
    --exclude='.claude/.credentials.json' \
    --exclude='.claude/history.jsonl' \
    --exclude='.claude/stats-cache.json' \
    --exclude='.claude/mcp-needs-auth-cache.json' \
    --exclude='.claude/settings.local.json' \
    .claude/

# IMPORTANT: settings.local.json is excluded above because it contains your
# personal Bash allowlist - likely sudo/chmod/apt-install patterns specific to
# your machine. Shipping it would auto-grant those privileges on the recipient's
# machine. The replication recipe walks readers through generating a fresh
# settings.local.json with their own allowlist on the new machine.

# 2. Bundle the archive
tar czf ~/Desktop/Claude_Total_Replication/claude-archive-bundle.tgz claude-archive/

# 3. Capture secret names (NOT values)
grep -E '^export (GEMINI_API_KEY|GITHUB_TOKEN)' ~/.bashrc \
  | sed 's/=.*/=<paste from password manager>/' \
  > ~/Desktop/Claude_Total_Replication/SECRETS_TEMPLATE.txt
```

Re-run any time you've added a hook, agent, skill, or plugin and want to refresh the kit.

### What's deliberately excluded

| Path | Why excluded | What to do on the new machine |
|---|---|---|
| `~/.claude/.credentials.json` | OAuth tokens - machine-specific. | Run `claude` once, log in interactively → file regenerates. |
| `~/.claude/projects/` (159 MB) | Per-session JSONL transcripts. Already in `claude-archive-bundle.tgz`. | Skip - Claude Code creates new transcripts as you work. |
| `~/.claude/cache/`, `file-history/`, `paste-cache/`, `telemetry/`, `session-env/`, `sessions/`, `shell-snapshots/`, `todos/`, `tasks/`, `statsig/`, `debug/`, `downloads/`, `ide/`, `backups/` | Auto-managed by Claude Code. | Regenerated on first use. |
| `.session-clock/` | Transient per-session state. | Cleaned by Stop hook. |
| `history.jsonl` (2.1 MB) | Claude Code interaction history. Machine-specific. | Skip. |
| `~/.claude.json` (top-level config DB) | MCP registrations + project metadata. | Don't migrate; recreated by `claude mcp add` commands in step 10 of the recipe. |
| `GEMINI_API_KEY`, `GITHUB_TOKEN` | Secrets. | Re-export in `~/.bashrc` from your password manager. |

### Replication on a new machine - Path A (Ubuntu native)

Time: ~90 minutes.

```bash
# 1. OS prerequisites
sudo apt update && sudo apt install -y \
  curl jq git build-essential ripgrep \
  python3-pip nodejs npm notify-osd libnotify-bin pulseaudio-utils

# Node 20+ (install via nvm if system version is older)
node --version | grep -E '^v(20|21|22|23|24)' >/dev/null || {
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  source ~/.bashrc; nvm install 22 && nvm use 22
}

# uv (Python pkg mgr) and pnpm (Node pkg mgr)
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://get.pnpm.io/install.sh | sh -

# GitHub CLI - see your distro's gh install instructions

# 2. Install Claude Code
curl -fsSL https://claude.ai/install.sh | bash || npm install -g @anthropic-ai/claude-code
claude --version    # confirm ≥ 2.1.119

# 3. Install Ruflo (for the Ruflo MCP)
npm install -g ruflo

# 4. Transfer the kit, extract
cd ~
# (place claude-config-bundle.tgz + claude-archive-bundle.tgz in $HOME)
tar xzf claude-config-bundle.tgz
tar xzf claude-archive-bundle.tgz

# 5. Re-export your two API keys (from your password manager)
echo 'export GEMINI_API_KEY="<paste-from-password-manager>"' >> ~/.bashrc
echo 'export GITHUB_TOKEN="<paste-from-password-manager>"' >> ~/.bashrc
source ~/.bashrc

# 6. Make scripts executable (tar may have lost +x)
chmod +x ~/.claude/hooks/*.sh ~/.claude/statusline.sh ~/.claude/scripts/*.sh

# 7. Initialize Ruflo runtime (creates ~/.claude-flow/)
cd ~ && ruflo init --skip-claude --with-embeddings --minimal --force

# 8. Register the MCP servers
claude mcp add -s user gemini "$(which python3)" -- ~/.claude/mcp-servers/gemini/server.py
claude mcp add -s user github npx -- -y @modelcontextprotocol/server-github
claude mcp add -s user context7 npx -- -y @upstash/context7-mcp
claude mcp add -s user playwright npx -- -y @playwright/mcp
# (ruflo MCP gets registered automatically by `ruflo init` in step 7)

# 9. Install Playwright's chromium
npx playwright install chromium

# 10. Verify everything
~/.claude/scripts/verify-top-1-setup.sh --quiet
# Expected: All checks passed (PASS: 38, REGRESSIONS: 0)

claude mcp list
# Expected: gemini, github, context7, playwright, ruflo - all ✓ Connected
# (you'll also see `claude.ai Excalidraw ✓ Connected` and four `! Needs authentication`
#  entries for the claude.ai-managed Google MCPs - those are normal)
```

### Replication on Windows - Path B (WSL2 wrapper)

Claude Code itself runs natively on Windows via PowerShell - *but this particular setup doesn't*. The hooks are bash, the statusline is bash, and the verifier is bash. PowerShell doesn't run bash, `jq` behaves differently, and the Unicode glyphs (♻ ⏱ ⚡) don't render in cmd.exe. So for **this** setup specifically, you need WSL2.

```powershell
# 1. Enable WSL2 + install Ubuntu (one-time, in PowerShell as Admin)
wsl --install -d Ubuntu-24.04
# Reboot when prompted.

# 2. Inside the WSL Ubuntu shell that opens - set up your username + password
sudo apt update && sudo apt upgrade -y
```

Then **inside the WSL shell**, follow Path A *exactly* - every command, every path. WSL2 gives you a real Linux filesystem under the hood.

**Windows-specific gotchas:**

| Issue | Fix |
|---|---|
| `\r\n` line endings break bash scripts when files transfer from Windows | `dos2unix ~/.claude/hooks/*.sh ~/.claude/statusline.sh ~/.claude/scripts/*.sh` after extracting |
| WSL CWD vs Windows path mismatch | Always launch `claude` from inside WSL. Project files at `/mnt/c/Users/...` are accessible but slow - prefer `~/projects/...` (native Linux fs). |
| `notify-send` doesn't work in WSL by default | Install `wsl-notify-send` or ignore. The archive still happens - just no popup. |
| Corporate Windows + Zscaler/proxy | Configure `https_proxy`, `http_proxy` env vars before `npm install` and `apt install`. Ask IT for the proxy URL. |
| Secrets | Export in `~/.bashrc` *inside* WSL. Not Windows env vars. |

Use **Windows Terminal** (free, Microsoft Store) for the colors. cmd.exe and default PowerShell don't render the gradient.

### macOS

Path A applies, with `brew` instead of `apt` for prerequisites:

```bash
brew install jq ripgrep node@22 gh
```

Everything else is identical.

### The verifier

After replication, run:

```bash
$ ~/.claude/scripts/verify-top-1-setup.sh
```

It produces a per-section audit:

```
─── 4. User-global hooks - integrity ───
  [OK]  4.x pre_tool_use.sh (executable, 2568B)
  [OK]  4.x session_start.sh (executable, 1307B)
  [OK]  4.x user_prompt_submit.sh (executable, 693B)
  [OK]  4.x session_stop_archive.sh (executable, 3238B)

─── 5. settings.json - structural integrity ───
  [OK]  5.0 settings.json valid JSON
  [OK]  5.1 deny rules (17 entries)
  [OK]  5.2 hook SessionStart wired to ~/.claude/hooks/
  ...
─── 6. MCP servers - health ───
  [OK]  6.x gemini ✓ Connected
  [OK]  6.x github ✓ Connected
  [OK]  6.x context7 ✓ Connected
  [OK]  6.x playwright ✓ Connected
  [OK]  6.x ruflo ✓ Connected
  ...
===================================================================
 SUMMARY  -  PASS: 38   REGRESSIONS: 0
===================================================================
  All checks passed. Setup is healthy.
```

`PASS: 38 / REGRESSIONS: 0` is the success signal (the verifier's check count grows over time as I add new validation rules - `0 REGRESSIONS` is the part that matters). Run it every two weeks. Catches regressions from plugin auto-updates, accidental clobbers, and `ruflo init` overwriting your settings (a known issue documented in the recipe).

### Privacy: what NOT to bundle

- **API keys.** They're in your shell rc file, not in `~/.claude/`. Confirm with `grep -E '^export (GEMINI_API_KEY|GITHUB_TOKEN)' ~/.bashrc` before tarring.
- **`.credentials.json`.** OAuth tokens. Always re-acquire on the new machine via `claude` interactive login.
- **`settings.local.json`.** Your personal Bash allowlist - usually contains `sudo`-prefixed and `chmod` patterns specific to your machine. Sharing it auto-grants those privileges on the recipient's machine. Excluded by the tar command above; double-check it's not in the bundle.
- **Anything in `~/.claude/projects/<slug>/`** if your transcripts contain sensitive info. The bundle excludes these by default; confirm.

When in doubt, `tar tzf claude-config-bundle.tgz | grep -iE 'env|token|key|cred|secret|local'` and audit the result before sending the tarball anywhere.

### A safety footnote on my settings.json

My bundled `settings.json` sets `"skipDangerousModePermissionPrompt": true` and `"skipAutoPermissionPrompt": true`. **These bypass two of Claude Code's built-in approval prompts.** I run with them on because (a) my deny rules + `pre_tool_use.sh` hook + curated `settings.local.json` allowlist are stricter than the default prompts, and (b) the constant prompting otherwise destroys flow. If you adopt my bundle wholesale, **review these two flags and decide whether to flip them back to `false`**. The safe default is `false` - keep them off until you've audited your own deny rules + hooks and convinced yourself you're not regressing safety. There's no shame in keeping the prompts; I just got tired of them after six months of consistent setup.

---

## 12. Layer 10 - A day in the life.

![A day in the life](/diagrams/09-weekly-composition.png)

Let me walk you through a real Tuesday end-to-end, because the inventory of layers above doesn't tell you what it *feels* like to use them all at once. Four prompts. One ship. Six hours. Closed by 5:30 PM.

#### 09:12 - open the laptop

```
$ claude
```

The statusline appears: `[opus-4.7] binance_robust (dev-test-main) ctx:[░░░░░░░░░░░░░░░] 4% ... ♻ - %`. Cache is cold; the ratio is dashed because no requests have fired. The session_start hook prints a quiet workbook hint: *"Recent mission workbooks: 2026-04-30-mission-9-phase-a.md, 2026-04-29-mission-8.md, 2026-04-27-mission-3-closure.md"*. The `MEMORY.md` index has loaded silently.

> **Prompt 1:** continue

That's the whole prompt. Claude reads `project_mission_9_phase_a_complete.md` from the auto-memory ("Operator restart-ready: new Claude session can resume from this entry"), reads the queued next steps (24h soak gates, paper-soak comparison, Phase B), and responds: *"Picking up where Mission 9 Phase A left off. Phase B is queued - three audit-deferred MEDIUM items: H-22 pool singleton, H-12 chaos test, H-4 perf benchmark. Want to start with H-22, or kick off the 24h soak first?"* Total ramp time: zero seconds. The Layer 3 memory ladder did its job.

#### 10:34 - a tick-latency regression report comes in

> **Prompt 2:** Tick-to-publish p99 doubled overnight on the SYMBOL_A feed. Find the regression. Be evidence-based.

This is the dispatch you saw in Layer 5. `hft-cto` fans out three specialists in parallel. Three handover blocks return inside 90 seconds. Root cause isolated: a config commit from the night before that inverted the conflation interval. Ship a one-line revert, validated by the latency-performance-owner against the Prometheus histogram, ready for review by 10:43.

#### 13:15 - a frontend side project I owe a friend

I `cd` into a different repo. The project's own SessionStart hook fires; the project's CLAUDE.md loads. A different statusline (different branch, different cache state, different rate-limit footprint). Different auto-memory: this project's `feedback_*` and `project_*` files load instead of the HFT ones. **Same setup, different project, zero context bleed.**

> **Prompt 3:** Build me a settings page with a theme toggle. Tailwind, shadcn, Next 15.

`frontend-design` skill matches. The opinionated four-bullet design rationale you saw in Layer 7 fires. Twelve minutes of code. A real PR-ready component, not a generic SaaS card.

#### 16:50 - close out for the day

I write a one-paragraph mission-workbook close-out for the latency revert (file:line evidence for the revert, links to the latency-performance-owner's handover block, gates for the next 24h soak). I `/exit`.

The Stop hook fires async. Twelve seconds later, the transcript JSONL, the workbook, and the project's CLAUDE.md snapshot are sitting at `~/claude-archive/2026/05/binance_robust/<session-id>/`. Three years from now I'll be able to `grep` *"conflation_interval"* across the archive and find this exact afternoon.

#### The pattern, explicit

- **Hooks fire constantly** but invisibly. Each one is a few ms of shell. They make the rest possible.
- **Skills get invoked semi-automatically.** "Redesign the WAL writer" → brainstorming auto-loads. "Build me a settings page" → frontend-design auto-loads. I rarely think about which skill - Claude routes to the right one based on description match.
- **Subagents fan out aggressively.** Three Explore agents in parallel beats one running serially every time. The ceiling is "how many independent things am I asking for at once" - when the answer is 3+, fan out.
- **Gemini gets pulled in for adversarial reviews** before implementation lands. About 1 in 3 missions; not every mission justifies a second opinion, but anything non-trivial does.
- **The Stop hook closes the loop.** When I `/exit`, the session is preserved. Tomorrow morning Claude knows where we left off.

A cheat-sheet for what fires when:

| Event | Trigger | Frequency |
|---|---|---|
| `session_start.sh` | `claude` launched | Once per session |
| `user_prompt_submit.sh` | You hit Enter | Every prompt |
| `pre_tool_use.sh` | Bash/Edit/Write/MultiEdit call | Every tool invocation |
| `session_stop_archive.sh` | Session ends | Once per session, async |
| `post-commit` (graphify) | `.py` files in commit | Every Python commit |
| `pre-push` (graphify staleness) | `git push` | Every push |
| Statusline render | Claude is idle for >300 ms | ~Continuously, throttled |
| MEMORY.md load | Session start | Once per session |
| Workbook hint | Project has `.claude/workbooks/` | Once per session |

Total invisible overhead: ~30 ms wall time on a typical prompt. Negligible. The value: massive.

---

### The whole stack, in one diagram

![Full setup architecture](/diagrams/10-setup-architecture.png)

The complete architecture: Claude Code at the center, seven supporting subsystems orbiting - safety net, memory ladder, skills, agents, MCPs, UI layer, hooks. Hooks archive to the memory ladder. project-bootstrap scaffolds CLAUDE.md and workbooks. superpowers orchestrates the agents.

And here is the same picture drawn at a different angle - a wiring diagram showing every layer in this post and how each one connects back to the Claude Code core. If you're a visual thinker, this is the single image to keep open in another tab while you read the rest:

![Top-1% Claude Code setup - overall architecture](/diagrams/11-overall-architecture.png)

Three things to notice in this diagram. First, the **Claude Code core** sits at the centre with arrows in and out of every other layer - every layer is *in service of* the core, none of them replace it. Second, the **safety net (Layer 1)** is the only layer that *guards* the core rather than being called by it; it sits on the outside, intercepting every tool call before it lands. Third, the **portable kit (Layer 9)** has a dotted line to the core because it doesn't talk to the core at runtime - it *replicates the entire setup* onto a new machine where a fresh core then comes online. Once you can read this single diagram, you can navigate the rest of the post by name.

The layers stack: the safety net protects you, the statusline informs you, the memory ladder gives you continuity, and the rest is leverage on top.

---

## 13. Live demo: watch the system build a real app in under an hour.

The post above describes the *infrastructure*. This section shows the *workflow* — what happens when that infrastructure is pointed at a brand-new project.

The prompt below — `PROJECT_BRIEF.md` — is what I paste into a fresh Claude Code session to build a photographer's portfolio app from scratch: backend (FastAPI + Pydantic + SQLModel + Pillow), frontend (Vite + React + TS + Tailwind + Framer Motion), tests (pytest + Playwright + Lighthouse), CI/CD (GitHub Actions, pinned action versions), GitHub repo (auto-created), local deploy (background uvicorn + vite preview), URL handoff. **One prompt, ~58 minutes wall clock, zero clicks beyond plan approval.**

![Photography Dashboard build flow](/diagrams/16-photography-dashboard-flow.png)

### How Claude actually executes the brief

The flow above maps every event to the system layer that produced it.

- **Phase A — Plan mode (~12 min).** Pure deliberation. Pre-flight reads cwd / git status / port availability / pypi+npm+github reachability. Then `superpowers:brainstorming`, then `superpowers:writing-plans`, then a Gemini MCP red-team on the plan. *Zero* files written, *zero* GitHub repo, *zero* code yet.
- **Phase B — Bootstrap (~5 min).** The moment after I click "Yes, proceed", the `project-bootstrap` skill scaffolds the project files (project-level `CLAUDE.md`, `.claude/workbooks/`, `.githooks/post-commit` for graphify auto-regen). Then `git init` → `gh repo create --private --push`. The GitHub repo materializes around T+13:30. A fresh `.venv/` is created — pip never touches system Python. Vite scaffolds `web/`. Two commits land.
- **Phase C — Parallel implementation (~28 min).** `superpowers:dispatching-parallel-agents` fans out three Tasks in one Claude turn: `backend-specialist` (FastAPI + 8 endpoints + EXIF + thumbs + comments + pytest), `frontend-specialist` (gallery + lightbox-with-focus-trap + stats + comments + vitest), `devops-specialist` (`.github/workflows/ci.yml` + scripts + README). After each slice → `code-reviewer-generic` → commit → push. Every push triggers GitHub Actions CI on the workflow file written earlier in the same phase.
- **Phase D — Verification (~12 min, sequential).** Servers boot in the background (`nohup`, logs in `.logs/`), thumb warmup generates 55 PNGs, Playwright MCP runs the smoke + regression suites with `document.fonts.ready` waits and 2% pixel-diff tolerance, Lighthouse runs ×3 (median), `gh run list` polls CI.
- **Phase E — URL handoff (~1 min).** All 23 quality gates printed green, then the `🟢 LIVE` block with frontend / API docs / repo / CI URLs.

### The full prompt

The full `PROJECT_BRIEF.md` lives in the open-source repo: **[`examples/photography-dashboard/PROJECT_BRIEF.md`](https://github.com/saugatapaul1010/claude-code-top1-setup/blob/main/examples/photography-dashboard/PROJECT_BRIEF.md)** — read it on GitHub or paste the raw file directly into a new Claude Code session.

> ```bash
> # Quick fetch
> curl -L https://raw.githubusercontent.com/saugatapaul1010/claude-code-top1-setup/main/examples/photography-dashboard/PROJECT_BRIEF.md > PROJECT_BRIEF.md
> ```


## 14. Best practices - the do's, the don'ts, and how the mechanism actually works.

Before the closing, a working developer's reference card. These are the patterns I keep coming back to, distilled from two-plus years of watching the setup do well and watching it do badly. Use this section as the lookup table you'd staple to your monitor.

### The mechanism, in one paragraph

Every layer in this post is a different way of **keeping Claude's context window stable, focused, and useful**. The safety net (Layer 1) keeps Claude from doing irreversible things while it's working in your context. The statusline (Layer 2) keeps *you* honest about what's in the context - how full it is, how warm the cache is, what it's costing. The memory ladder (Layer 3) keeps the context *continuous* across sessions: what was loaded yesterday is reachable today without re-explanation. Skills (Layer 4) keep the context *procedural* - invoking a skill is loading a recipe Claude executes verbatim. Agents (Layer 5) keep the context *narrow*: each specialist holds only the slice it can verify. MCPs (Layer 6) extend the context *outward* - to other models, other tools, external state. Plugins (Layer 7) bundle the above. The bootstrap (Layer 8) makes a new project inherit the whole machine on day one. The kit (Layer 9) makes a new machine inherit the whole setup in 90 minutes. Once you see every layer as a different lever on the same context window, the design choices below stop being arbitrary and start being obvious.

### Do - twelve patterns that compound

1. **Do put the unstable stuff in auto-memory, not in CLAUDE.md.** CLAUDE.md is loaded into the system prompt every session; every byte that mutates between calls invalidates the prompt cache. Big rule: if a piece of guidance might evolve, it belongs in `~/.claude/projects/<slug>/memory/feedback_*.md`, not in CLAUDE.md.
2. **Do write `Why:` and `How to apply:` on every memory entry.** A rule without a *why* is a weird taboo; with a *why* Claude can reason about edge cases instead of blindly following.
3. **Do open a mission workbook the moment a task spans ≥2 sub-agents or ≥2 user turns.** The cost of opening one is twenty seconds; the benefit is that next week you (or a new Claude session) can resume from exactly where you left off.
4. **Do dispatch independent sub-tasks in parallel, in one message.** Three Explore agents fired together arrive in one round-trip; three fired sequentially arrive in three. The ceiling is "how many independent things am I asking for" - when the answer is 3+, fan out.
5. **Do call `gemini_second_opinion` on anything non-trivial before you ship.** One in three missions justifies it. The wins, when they happen, are catastrophic-bug-sized.
6. **Do invoke `brainstorming` before any redesign or new-feature prompt.** The output is categorically better. The first time you watch this side-by-side you stop running redesigns without it.
7. **Do run the verifier every two weeks.** `~/.claude/scripts/verify-top-1-setup.sh`. Catches plugin auto-updates that clobbered your settings, accidental deletions, corrupted hooks. `0 REGRESSIONS` is the one number you care about.
8. **Do refresh the kit any time you add a hook, agent, skill, or plugin.** The tarball is the rollback path; if you don't keep it current, your next disaster recovery is a worse weekend than it has to be.
9. **Do let the statusline be intrusive.** If ♻ drops below 70%, stop and ask what changed. If `ctx:` goes red, `/clear` and restart. The number on screen is your live debugger; act on it.
10. **Do pin every external model to a specific version.** Silent fallbacks are how you ship false-confidence outputs. A degraded second opinion is worse than no second opinion.
11. **Do scope graphify to your production-code subdirectory, not the repo root.** Pulling `Research/`, `node_modules/`, `vendor/` into the graph inflates run time 10× and pollutes the god-node analysis with junk.
12. **Do make agent descriptions read like a router would read them.** Front-load trigger words, end with explicit DO/DO-NOT scope. Claude pattern-matches on description text; vague descriptions get vague routing.

### Don't - twelve traps to avoid

1. **Don't pile every preference into CLAUDE.md.** I see 800-line CLAUDE.mds in the wild. Cache hit ratio collapses; cost goes up 10×; nobody notices because the default statusline doesn't show ♻.
2. **Don't skip the backup before editing the live blog/CLAUDE.md/settings.json.** `cp foo foo.backup.md` is one keystroke; rolling back from a corrupted settings.json without one is an hour.
3. **Don't run `ruflo init` without diff'ing settings.json afterward.** The `--skip-claude` flag is unreliable in v3.5.80; it has clobbered my settings before. Diff. Restore. Move on.
4. **Don't enable every plugin "just in case."** Each plugin pays a context-window tax on every session. Ten plugins enabled is fine; twenty is not.
5. **Don't write skills that wrap things Claude already knows how to do.** A "format with prettier" skill adds zero value over `Bash(npx prettier ...)`. Skills exist to encode procedure, not to be aliases.
6. **Don't try to multiplex multiple model families into one MCP server.** Three small servers - `gemini`, `gpt`, `llama` - are easier to debug, version, and selectively disable than one large multiplexer with a `model=` parameter.
7. **Don't let `defaultMode: "auto"` substitute for explicit deny rules on secrets.** Auto-approve lets Claude work without prompting; deny rules keep it from touching things that should be untouchable. They're orthogonal. Use both.
8. **Don't store API keys in `~/.claude/`.** Keys live in your shell rc file (`~/.bashrc`, `~/.zshrc`), exported as env vars. The kit explicitly excludes credential files; the recipe re-creates them on the new machine from your password manager.
9. **Don't claim "fixed" without a behavioral test.** Adopt the evidence-graded markers (✅ VERIFIED / 🟡 PATCHED / 🟠 AUDIT-ONLY / 🔒 LATENT) and use them on every issue ledger. A commit SHA is not evidence of correctness.
10. **Don't poll an agent's status after dispatching it.** Spawn it (in the background if needed), trust it to return, and review the result when it lands. Polling spams the model and wastes your context window.
11. **Don't commit `.claude/settings.local.json`.** It contains your machine-specific Bash allowlist (likely with `sudo`/`apt` patterns). Sharing it would auto-grant those privileges to a teammate who pulls your repo.
12. **Don't try to build the 24-agent hierarchy on day one.** Start with three specialists. Add an apex when you hit cross-domain missions. Add an arbiter when specialists disagree. The team accretes; it isn't designed.

### How the five-year retrieval actually works (because this surprised me too)

This is the property of the setup that I still marvel at, and it works because of a deliberate design choice in Layer 3 that I want to make explicit. Here is the data flow, end to end, from today's `/exit` to a question you might type in 2031:

![5-year retrieval - today's session, archive, scale, future query](/diagrams/14-five-year-retrieval.png)

Read the diagram left to right. **Today's session** flows into the **Stop hook**, which idempotently `cp -n`s every artifact (transcript, MANIFEST, workbooks, plan files, and a snapshot of the CLAUDE.md as it was at the time) into the deterministic `~/claude-archive/YYYY/MM/<project>/<session>/` layout. That's Phase 1. As the archive grows, you periodically check whether `grep` is still fast enough; for most users, the answer stays *yes* for years. When it eventually doesn't, Phase 2 - an HNSW vector overlay built nightly from Ruflo's `embeddings_*` tools - sits on top of the archive without replacing it. **Crucially, the source of truth never moves.** The archive is always plain files; the embeddings layer is always an accelerator, not a substitute. So a future Claude session asking *"why did we decide X in 2026?"* can use either the grep path or the semantic path - and either one returns the exact workbook, the exact handover block, the exact `file:line` citation that was recorded the day the decision was made.

1. **The Phase-1 archive at `~/claude-archive/` is plain files in a deterministic layout.** `YYYY/MM/<project-slug>/<session-id>/` with `transcript.jsonl`, `MANIFEST.json`, a snapshot of CLAUDE.md from that session, the workbooks active during the session, the plan-mode artifacts. No database. No proprietary format. No vendor lock-in.
2. **`grep -r` will work in 2031.** The whole archive is searchable with `grep`, `rg`, `awk`, or any Unix tool you'll still have in five years. The session-id naming is deterministic; the MANIFEST.json gives you the cwd, the source transcript path, the timestamp.
3. **When you come back five years from now and ask Claude *"why did we decide X?"*, the path is concrete:** Claude opens `~/claude-archive/`, searches for the keyword, finds the relevant `transcript.jsonl` and the workbook from that day, reads the handover blocks, surfaces the rationale with the original `file:line` citations. The auto-memory index doesn't need to know about old projects; the archive is a `grep` away.
4. **When `~/claude-archive/` outgrows `grep` (somewhere past 10–20 GB),** the Phase-2 plan is to put a semantic index *on top of* the archive without replacing it. Ruflo's HNSW embeddings tools are wired in for exactly this. The archive itself stays plain files forever. The embedding layer is an accelerator, not a substitute.

This is why the archive uses `cp -n` (no overwrite) and `set -uo pipefail` deliberately *without* `-e`: every step has `|| true`, so a failure on one file does not corrupt the rest. The Stop hook is async, fault-tolerant, and idempotent. Re-running it on the same session is a no-op. Three years from now when you've upgraded Claude Code through six versions, your archive from today is still readable, still `grep`-able, still complete.

---

## 15. Key takeaways - what to remember if you only remember nine things.

If you remember only nine things from this entire post, let it be these:

1. **The bottleneck stops being how fast Claude codes; it becomes how well you set Claude up to do its job.** Every layer in this post is a different lever on that one bottleneck.
2. **The safety net is non-negotiable.** Hooks + deny rules together. Once installed, you can finally let Claude work unsupervised without watching every keystroke.
3. **Memory is split across four tiers for a reason.** Hot tier (CLAUDE.md, always loaded - keep it small), warm tier (auto-memory + workbooks, loaded on relevance), and cold tier (`~/claude-archive/`, plain files, `grep`-able forever). Each tier has a different cache cost and a different lifetime.
4. **Skills encode procedure; agents carry identity.** A skill loaded into context tells Claude *how* to do something; an agent dispatched in parallel tells Claude *who* should do it. Don't conflate them.
5. **Specialization is the cure for hallucination.** A narrow agent with a tight preamble and a `file:line` evidence rule will not invent broken synchronization schemes. A generalist will.
6. **MCP makes the setup model-agnostic.** Twenty lines of Python wraps any LLM as a first-class Claude tool. You're not betting your career on Anthropic; you're using Claude Code as the orchestration layer and swapping models behind it as the landscape shifts.
7. **The project-bootstrap skill is the highest-leverage compounding investment in the entire setup.** Three questions, thirty seconds, every new project inherits every convention you've earned. Five minutes saved × every new project × the rest of your career.
8. **Portability is what turns a dead laptop on a Friday into a coffee break.** The kit is not optional. Ninety minutes from new-machine to back-in-flow. Build it even if you never plan to migrate.
9. **Encode discipline once, inherit it always.** This is the principle that runs underneath every layer. Karpathy rules in CLAUDE.md, evidence-graded markers in auto-memory, investigate-then-implement in the agent preamble, mission-workbook format as a convention, safety as hooks, portability as a tarball. Each layer is one act of encoding that pays for itself for the rest of your career.

---

## 16. Appendix A - Full file index.

Every file the kit drops on your machine, with a one-line purpose. Use this as a "what is this file again?" reference.

### `~/.claude/` (user-global)

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Global rules - Karpathy, MCP server docs, mission-workbook convention, markdown documentation standard. ~250 lines. |
| `settings.json` | Master config. 17 deny rules + 4 hooks + statusline command + 10 enabled plugins + env vars + theme. 112 lines. |
| `settings.local.json` | Personal allowlist (gitignored). Project-specific Bash whitelists. |
| `statusline.sh` | 223-line statusline with gradient bar, dual clocks, cache-hit %, rate-limit bars. |
| `hooks/pre_tool_use.sh` | PreToolUse safety net - blocks .env / rm -rf / curl\|bash / fork bombs. 48 lines. |
| `hooks/session_start.sh` | SessionStart workbook hint. 32 lines, defers to project hook if present. |
| `hooks/user_prompt_submit.sh` | Per-prompt context injection (timestamp + cwd + branch + git status). 24 lines. |
| `hooks/session_stop_archive.sh` | Phase-1 lossless archive on Stop. 89 lines, async, idempotent. |
| `scripts/verify-top-1-setup.sh` | Auditor. Returns `0 REGRESSIONS` when healthy. Run every 2 weeks. |
| `agents/*.md` | 12 generic agents (ai-engineer, backend-specialist, frontend-specialist, devops-specialist, etc.). |
| `skills/project-bootstrap/SKILL.md` + `templates/` (14 files) | The day-1 scaffold skill. |
| `skills/graphify/SKILL.md` | Code-to-knowledge-graph skill. |
| `skills/drawio-architect/SKILL.md` | Production-grade .drawio diagrams (Sugiyama + A* routing). |
| `skills/manim-animator/SKILL.md` | 3B1B-quality math animations. |
| `skills/karpathy-guidelines/SKILL.md` | Karpathy 4-rule discipline. |
| `mcp-servers/gemini/server.py` | Custom Gemini MCP server. 423 lines. |
| `plugins/hft-team/agents/*.md` | 24 hft-team specialist agents. |
| `plans/*.md` | Plan-mode artifacts. Persisted across sessions. |
| `projects/<slug>/memory/MEMORY.md` + topical files | Per-project auto-memory. |

### `~/claude-archive/` (user-global)

| Path | Purpose |
|---|---|
| `YYYY/MM/<project-slug>/<session-id>/transcript.jsonl` | Full session transcript. |
| `YYYY/MM/<project-slug>/<session-id>/MANIFEST.json` | Archive metadata (timestamp, session_id, cwd, source_transcript). |
| `YYYY/MM/<project-slug>/<session-id>/CLAUDE.md` | Snapshot of project CLAUDE.md at archive time. |
| `YYYY/MM/<project-slug>/<session-id>/workbooks/` | Mission workbook snapshots. |
| `YYYY/MM/<project-slug>/<session-id>/plans/` | Plan-mode artifact snapshots. |
| `.archive.log` | Audit trail - one line per session archived. |

### Per-project (created by `project-bootstrap`)

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Project rules (committed). |
| `CLAUDE.local.md.template` | Personal layer template (rename to `CLAUDE.local.md` for use; gitignored). |
| `.claude/settings.json` | Project hooks + permissions. |
| `.claude/settings.local.json` | Personal allowlist (gitignored). |
| `.claude/workbooks/INDEX.md` | Mission workbook index. |
| `.claude/plans/` | Plan-mode artifacts (gitignored). |
| `docs/<MONTH>_onwards/ADR-001-*.md.template` | Architecture Decision Record template. |
| `docs/<MONTH>_onwards/ADVISORY-001-*.md.template` | Advisory (living strategic doc) template. |
| `docs/<MONTH>_onwards/MISSION_X.X_ISSUE_*.md.template` | GitHub-issue-ready mission template. |
| `docs/<MONTH>_onwards/All_Issues_Latest_<MONTH>_<YEAR>.md` | Regression ledger. |
| `docs/<MONTH>_onwards/DEFERRED_ISSUES_ROADMAP.md` | Deferred-issues roadmap. |
| `.githooks/post-commit` | Graphify auto-regen (only if opted in). |
| `.githooks/pre-push` | Graphify staleness check (only if opted in). |

---

## 17. Appendix B - Troubleshooting.

**Hooks aren't firing.**
Check three things: (1) `chmod +x ~/.claude/hooks/*.sh` - tar can lose the executable bit; (2) the path in `settings.json` uses `~` (Claude Code expands it) not `$HOME` (which it doesn't); (3) `claude` is being launched from the right shell - your hook depends on `jq` and `git` being on PATH.

**Statusline is missing or showing garbage.**
Check `chmod +x ~/.claude/statusline.sh`. Test it standalone:
```bash
echo '{"model":{"display_name":"opus-4.7"},"workspace":{"current_dir":"'$PWD'"},"context_window":{"used_percentage":25}}' | bash ~/.claude/statusline.sh
```
If you see `[opus-4.7] <basename> ctx:[██░░░░░░░░░░░░░] 25%`, the script works - Claude Code's wiring is the problem (check `settings.json` `statusLine` section). If you see literal escape codes (`\033[…`), your terminal isn't rendering true-color - switch to Windows Terminal / Alacritty / kitty / iTerm2.

**`claude mcp list` shows MCP as `× Failed` or `! Needs authentication`.**
For Gemini: `echo $GEMINI_API_KEY` - empty? Re-export. Wrong? Check the key in your password manager.
For GitHub: `echo $GITHUB_TOKEN`. Same drill.
For Playwright: `npx playwright install chromium`.
For Context7: usually network; check `npx @upstash/context7-mcp --help` runs at all.

**`ruflo init` clobbered my settings.**
Known issue in v3.5.80 - the `--skip-claude` flag is unreliable. After `ruflo init`, diff `~/.claude/settings.json` against the version from your kit and restore manually if needed. Also clean up Ruflo's swarm/sparc skills:
```bash
rm -rf ~/.claude/skills/{hooks-automation,pair-programming,skill-builder,sparc-methodology,stream-chain,swarm-advanced,swarm-orchestration,verification-quality} 2>/dev/null
```

**Verifier fails on `5.1 deny rules (17 entries)` - "expected 17, got X".**
Your `settings.json` deny list has been edited. Re-merge from the bundle's settings.json or update the verifier's expected count.

**Auto-memory isn't loading.**
Per-project memory lives at `~/.claude/projects/<sanitized-cwd-path>/memory/MEMORY.md`. The slug is the absolute path with `/` → `-`. If you're not seeing memory loaded, check that directory exists and has a `MEMORY.md`. If it doesn't, Claude Code creates it on first save - but only if you (or Claude) actually save a memory in that project.

**Graphify is slow.**
First run is always slow - it builds the cache. Subsequent runs are 2–8 s. If yours is 40+ s consistently, you're scanning the wrong directory (running from repo root pulled in `Research/` and `node_modules/`). Scope to your production-code subdirectory, e.g., `cd src && graphify update .`.

**WSL: bash scripts complain about `^M` characters.**
Line endings problem from Windows transfer. Fix:
```bash
sudo apt install dos2unix
dos2unix ~/.claude/hooks/*.sh ~/.claude/statusline.sh ~/.claude/scripts/*.sh
```

**Context-window keeps blowing up.**
Three culprits in order of likelihood: (1) CLAUDE.md is too big - split into auto-memory; (2) you have too many plugins enabled - disable the irrelevant ones; (3) you're not using `/clear` between unrelated tasks. The statusline's `ctx:` bar tells you when to clear.

**The ♻ cache-hit % is consistently below 70%.**
Something in your stable prefix (system prompt, CLAUDE.md, auto-memory index, skill descriptions, hook output) is changing between calls and invalidating the cache. Common culprits: (1) a `user_prompt_submit.sh` hook that injects content with a constantly-changing field - like a high-precision timestamp or a sequence number - into the `<context>` block; (2) a CLAUDE.md you edited mid-session (the cache invalidates immediately); (3) skill descriptions that include dynamic content (e.g., a date). Diagnosis: open one session, send three trivial prompts, watch the ratio. If it's below 90% on the third turn, your prefix is mutating. Re-read the Layer 2 prompt-cache aside; the fix is almost always to move the dynamic content out of the prefix or to batch related calls in one turn instead of three.

---

## 18. Appendix C - Extending with your own custom agent / skill / MCP.

### Adding your own custom agent

Drop a markdown file at `~/.claude/agents/<your-agent>.md`:

```yaml
---
name: my-rust-specialist
description: Rust 1.85 with tokio, axum, sqlx. Use for Rust code in any project. Read+Write.
tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

You are a senior Rust engineer. Defaults: tokio for async, axum for HTTP,
sqlx for DB. Cite line numbers in every code reference. Apply Karpathy
discipline.
```

Restart `claude` to pick up the new agent. Test by asking a Rust question and watching whether Claude dispatches your agent (its name should appear in the agent's response).

### Adding your own custom skill

Drop a directory at `~/.claude/skills/<skill-name>/`:

```
~/.claude/skills/my-skill/
├── SKILL.md           ← the skill prompt
├── templates/         ← optional templates
└── assets/            ← optional helper files
```

`SKILL.md` frontmatter:

```yaml
---
name: my-skill
description: Use when the user asks to do X. [Pattern-matched against prompts.]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# my-skill

[Body of the skill - what to do, in what order, with what verification gates.]
```

Test by either typing `/my-skill` (user-invocable) or by phrasing a prompt that matches the description (model-invocable).

### Adding your own custom MCP server

The Gemini MCP server at `~/.claude/mcp-servers/gemini/server.py` is a reference - you can copy its structure for any external service:

```python
from fastmcp import FastMCP
mcp = FastMCP("my-service")

@mcp.tool()
def my_tool(arg: str) -> str:
    """One-line description for Claude."""
    return do_something(arg)

if __name__ == "__main__":
    mcp.run()
```

Register:

```bash
claude mcp add -s user my-service "$(which python3)" -- /path/to/your/server.py
claude mcp list   # confirm ✓ Connected
```

That's it. Your tools are now first-class in Claude Code.

---

*If this post helped you, tell another developer. The whole field is figuring this out at the same time, and good setups should be public.*

---

---

## 19. Closing.

### What does this stack cost?

Tokens: a typical session uses ~30K tokens for the always-loaded layer (CLAUDE.md + auto-memory index + skill descriptions). At Opus 4.7 prices that's ~$0.45/session of "fixed cost" before any work happens. Cache hit ratio of >90% (which the statusline keeps you honest about) brings effective cost to about $0.05/session.

Time: 60–90 minutes to set up from scratch using the recipe. Two hours of refinement after using it for a week (everyone's preferences differ slightly). Then ~5 minutes per month maintaining it (running the verifier, refreshing the kit when something interesting changes).

### What does it not cost?

It does *not* cost you the ability to debug it. Every layer is a shell script or markdown file. If a hook misbehaves, you read 48 lines of bash. If a skill produces wrong output, you read 164 lines of markdown. There's no opaque binary or vendor SDK between you and the behavior. This is by design - the alternative (a heavyweight orchestration framework) hides too much when you need to fix something at 2 AM.

### What this is not

This isn't magic. It's an amplifier, not an autopilot. Karpathy's "think before coding" is a rule the setup tries to make Claude follow - but if you skip thinking, the setup doesn't think for you. Every plan still needs your judgment. Every PR still needs your review.

It is not finished. I expect to add a Phase 2 semantic layer over the archive when `grep` stops being fast enough. I expect to refactor the agent hierarchy when the codebase migrates Python → Rust. I expect new MCPs to land that are worth installing. The kit is versioned; expect v2 in 6 months.

It is not the only way. There are other top-1% setups out there - Loop+ralph for autopiloting, fancier statusline themes, different skill libraries. Take this as a *baseline* and ride past it.

### What to do next

1. **Clone the kit.** `git clone <your fork> ~/Desktop/Claude_Total_Replication` or rebuild it from the recipe in this post.
2. **Run the recipe.** Path A (Ubuntu/Mac) or Path B (Windows/WSL2). 60–90 minutes.
3. **Run the verifier.** `~/.claude/scripts/verify-top-1-setup.sh`. Expect `0 REGRESSIONS`.
4. **Open a real project.** Run `/project-bootstrap`. Answer three questions. Watch the scaffolding land.
5. **Use it for a week.** Pay attention to what bugs you. Modify the parts that do.
6. **Share back.** If you build something better - a smarter hook, a sharper agent, a more useful skill - open a PR or write your own post. The whole field is figuring this out at the same time.

The full kit is at `~/Desktop/Claude_Total_Replication/` on my machine; if you'd like me to ship a public Git repo with these artifacts, [reach out](mailto:saugata.paul1010@gmail.com) - happy to maintain it.

### One last thing - the philosophy that ties it all together

If you only remember one paragraph from this entire post, let it be this one.

**Encode discipline once, inherit it always.** That is the principle that runs underneath every layer above. The Karpathy rules are encoded in a global CLAUDE.md so every project inherits them without re-typing. The evidence-graded markers are encoded in an auto-memory file so every agent in every mission inherits them without being lectured. The "Investigate then implement" protocol is encoded in the hft-team preamble so every specialist inherits it without me having to remind them. The mission-workbook handover format is encoded in a convention so every dispatched agent inherits the format without coordination. The safety net is encoded in hooks so every Bash call inherits the guardrail without me watching. The portability is encoded in a tarball + a verifier so every machine I ever own inherits the setup without ceremony. **Each layer is one act of encoding that pays for itself for the rest of your career.**

Most tools ask you to learn them. This setup asks you to encode what you already know - your conventions, your evidence standards, your safety practices, your taste - once, and then inherit it automatically on every new project, in every new session, on every new machine. After you've built this, using Claude Code without it will feel the way it feels to write code without tests. Possible. But the risk creeps up on you until you notice you're debugging at 2 AM instead of shipping at 5 PM.

The bottleneck stops being "how fast does Claude code." The bottleneck becomes "how well do I set Claude up to do its job." The setup's worth compounds: better memory means fewer explanations, fewer explanations mean longer uninterrupted sessions, longer sessions mean better code, better code means more trust, more trust means more delegation, more delegation means more output. The whole post you just read is one principle in twelve costumes.

If you have made it this far, you are either building this or deciding whether to build this. **Both are the right answer.** And if you build it, change the parts I got wrong and tell me what you changed. The whole field is figuring this out at the same time, and good setups should be public.

### Thank you, and a few names

If you have made it this far, thank you. I know it was long. The whole thing took me six months to build and one weekend to write up - and honestly the writeup was the harder part.

If you build on this, please tell me. If you build something *better* than this, please tell me louder. My email is in the byline below. I read every message and I would much rather hear "your hook script broke on my Mac, here's the fix" than another LinkedIn DM. The whole field is figuring this out at the same time, and good setups should be public.

Build something good with it.

- Saugata Paul · April 2026 · Bangalore, India

---

## 20. Get the setup.

The infrastructure half of this post is open-source. Two install paths:

```bash
# Path A: clone + install (recommended — read what you're installing first)
git clone https://github.com/saugatapaul1010/claude-code-top1-setup
cd claude-code-top1-setup
./install.sh        # backs up your existing ~/.claude/ first

# Path B: one-shot tarball install
curl -L https://github.com/saugatapaul1010/claude-code-top1-setup/releases/latest/download/claude-code-top1-setup.tar.gz | tar -xz
cd claude-code-top1-setup && ./install.sh
```

**What's in the tarball (under 1 MB):**

- 4 lifecycle hooks · 223-line statusline · sanitized `CLAUDE.md` + `settings.json`
- 11 generic specialist agents (backend, frontend, devops, security, code-review, ai-engineer, test-writer, etc.)
- 5 skills (`project-bootstrap`, `graphify`, `drawio-architect`, `manim-animator`, `karpathy-guidelines`)
- A 4-tier **team-plugin scaffold** (24 agent stubs, 4 skill stubs, 8 shared docs) — *structure preserved, bodies blank for you to fill in with your own domain*

**What's NOT in the tarball:** the actual hft-team agent content (24 specialist agents tied to a real trading codebase) — that's proprietary IP. You inherit the *shape* of the four-tier hierarchy; you write the *content* for whatever domain you work in.

The installer auto-backs up your existing `~/.claude/` to `~/.claude.backup-<timestamp>/` before touching anything, so rolling back is one `mv` away.

Repo: [github.com/saugatapaul1010/claude-code-top1-setup](https://github.com/saugatapaul1010/claude-code-top1-setup)

---

## 21. Thank you, and a few names.

If you have made it this far, thank you. I know it was long.

Massive thanks to the people whose work I have stood on top of: **Andrej Karpathy**, whose four discipline rules (think before coding · simplicity first · surgical changes · goal-driven execution) run through every layer of this post; and **Anthropic's engineering team**, who built Claude Code itself plus the plugin marketplace and the skills system that made all of this possible.

---

## 22. Got a better idea? Tell me.

This post is one engineer's working setup, frozen on a particular Sunday afternoon. **It will be wrong about something.** It will be missing something obvious that you've already solved. It will quietly assume something that doesn't hold for your stack.

If you've read this far, you're probably the kind of engineer who has opinions - and your opinions are exactly what would make this better.

**Three asks:**

1. **If anything here is incorrect, outdated, or just *worse* than what you do** - tell me. I'd rather be corrected on a Tuesday than keep being wrong about it for a year.
2. **If you've built a layer I'm missing** - a hook, a skill, a memory pattern, an MCP integration, a statusline trick, an agent dispatch idiom - tell me. I'll try it, credit you, and update the post.
3. **If you found this useful** - pass it to one other engineer who's still using Claude Code "the way it ships." That's how setups stop being secret and start being standard.

**Reach me anywhere:**

- 📧 **Email** - [saugata.paul2020@gmail.com](mailto:saugata.paul2020@gmail.com)
- 💼 **LinkedIn** - [linkedin.com/in/saugata-paul-06413b126](https://www.linkedin.com/in/saugata-paul-06413b126/)
- 🐙 **GitHub** - [github.com/saugatapaul1010](https://github.com/saugatapaul1010)

If you have a fantastic suggestion, please don't keep it to yourself - drop it in any of the channels above and I'll fold it back into a future revision so the whole community benefits. Good setups belong in the open.
