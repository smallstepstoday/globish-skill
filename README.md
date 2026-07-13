# Globish — a Claude Agent Skill and Plugin

A [Claude Agent Skill](https://github.com/anthropics/skills) that makes Claude write every document in **Globish**: Jean-Paul Nerrière's ~1,500-word, simplified international English, plus a plain-writing style (short sentences, active voice, no idioms, no cultural references). Point it at Claude in [Cowork](https://claude.ai), Claude Code, or the Claude API, and it becomes the default language for everything Claude writes — reports, emails, memos, docs — so the output is readable by anyone working in English as a second or third language.

> Built by [@smallstepstoday](https://github.com/smallstepstoday).

## Why

Most writing aimed at a "general audience" still assumes native-level English: idioms, phrasal verbs, 40-word sentences, cultural references. That's a real barrier for the majority of English readers worldwide, who learned it as an additional language. Globish (coined by Jean-Paul Nerrière, a former IBM VP of international marketing, after watching how non-native speakers actually communicated at international conferences) is a deliberately constrained subset of English built to solve exactly that problem. This skill operationalizes it: instead of "write clearly" as a vague instruction, Claude gets an approved vocabulary, a style guide, and a script that checks a draft against both before it ships.

## How this repo is organized

This repo is set up to do three jobs from one source of truth, so there's no duplicated copy of the skill sitting around:

```
.claude-plugin/plugin.json       — plugin manifest (defines the "globish" plugin's contents)
.claude-plugin/marketplace.json  — marketplace catalog (lets people add this repo with /plugin marketplace add)
skills/globish/                   — the skill itself — the only copy, used by all install paths below
hooks/                             — PostToolUse hook: auto-checks prose files as Claude writes them
examples/before_after.md          — a worked example
CASE_STUDY.md                     — the project write-up
```

`plugin.json` alone only describes a single plugin's contents — it isn't something `/plugin marketplace add` can browse. `marketplace.json` is the actual catalog file that command reads; here it just points back at this same repo (`source: "./"`), so the repo does double duty as both the plugin and a one-plugin marketplace for it — the same pattern [anthropics/skills](https://github.com/anthropics/skills) uses for itself, just at a smaller scale.

## What's inside `skills/globish/`

```
skills/globish/
├── SKILL.md                    — triggers the skill, defines the workflow
├── LICENSE.txt                 — per-skill license (Apache-2.0)
├── references/
│   ├── wordlist.md              — ~1,500 approved root words, A–Z, human-readable
│   └── style-guide.md           — the plain-writing rules, with before/after examples
└── scripts/
    ├── check_globish.py         — compliance checker (vocabulary, sentence length,
    │                               forbidden tenses, idioms)
    ├── wordlist.txt              — the approved word list, one per line (used by the script)
    └── idioms.txt                — ~70 common business idioms/clichés to flag
```

## How it works

1. **Draft normally.** Claude writes the content the way it naturally would.
2. **Rewrite to Globish.** Vocabulary and sentences get brought in line with `references/style-guide.md`.
3. **Run the checker.** `scripts/check_globish.py` scans the draft for:
   - words not on the approved list (after stripping normal inflections and checking ~100 irregular verb forms — "sent" resolves to "send," "wrote" resolves to "write," etc.)
   - sentences over 15 words
   - the two tenses Globish drops (past perfect continuous, future perfect continuous)
   - idioms and business clichés
4. **Fix what's flagged.** Proper nouns, numbers, and technical terms with no plain-English substitute are always allowed, as long as they're defined on first use — the checker skips capitalized non-sentence-initial words automatically so it doesn't flag names and places.
5. **Deliver**, noting any terms kept outside the word list and why.

See [`examples/before_after.md`](examples/before_after.md) for a full worked example (explaining quantum physics, with and without the skill).

## Automatic check on every write

When installed as a plugin, `hooks/check_globish_on_write.py` runs as a `PostToolUse` hook after every `Write` or `Edit` tool call. If the file is prose (`.md`, `.markdown`, `.txt`, `.mdx`) and isn't part of the plugin's own bundled reference material, it runs the same compliance check automatically and prints a short summary — off-list word count, long-sentence count, forbidden-tense hits, idiom hits — so Claude sees it in the same turn and can offer to fix what's flagged. Clean files produce no output. Like the checker itself, the hook only reports; it never blocks the write.

## Try it

```bash
python3 skills/globish/scripts/check_globish.py path/to/draft.txt
```

or pipe text directly:

```bash
echo "Your draft text here." | python3 skills/globish/scripts/check_globish.py -
```

## Install

**As a plugin (Claude Code / Cowork):**
```
/plugin marketplace add smallstepstoday/globish-skill
/plugin install globish@globish
```
(`smallstepstoday/globish-skill` is the repo to fetch the catalog from; `globish@globish` is `<plugin-name>@<marketplace-name>` — both happen to be called `globish`, but they're separate names defined in `plugin.json` and `marketplace.json` respectively.)

**As a standalone skill (Claude Code / Cowork):** copy `skills/globish/` into your skills directory.

**Claude.ai:** upload the `skills/globish` folder as a custom skill — see [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

**Claude API:** upload via the [Skills API](https://docs.claude.com/en/api/skills-guide#creating-a-skill).

## Design notes

- **The word list** is reconstructed from Nerrière's official published Globish vocabulary, supplemented with core conjugated forms of *be*, *have*, and *do* (is, am, are, was, were, been, had, did, would, could) and the article *an* — several published copies of the list omit these as "assumed" grammar, but a working checker needs them.
- **The checker is a report, not a gate.** It's deterministic where determinism helps (vocabulary, sentence length, tense patterns) and leaves judgment calls — is this technical term unavoidable? does this sentence actually read fine at 16 words? — to Claude and the user.
- **Irregular verbs** are handled with an explicit lookup table rather than a stemmer/lemmatizer dependency, keeping the script to the Python standard library.
- **The hook mirrors the checker's own philosophy.** `hooks/check_globish_on_write.py` always exits `0` and never modifies or blocks a write — it only prints a summary Claude can act on. Enforcement stayed a design non-goal throughout this project; the goal is visibility at the moment a draft is written, not a lint error that stops work.

## Limitations

- The approved-word check is a heuristic (suffix stripping + an irregular-verb table), not a full lemmatizer — it will occasionally flag a valid inflection or miss an invalid one.
- The idiom list (`skills/globish/scripts/idioms.txt`) is a starter set of common offenders, not exhaustive. Contributions welcome.
- The sentence splitter can be thrown off by punctuation directly inside quotation marks (e.g., a sentence ending `word."` rather than `word.` followed by a space) — a known quirk, tracked for a future fix.

## License

Apache License 2.0 — see [LICENSE](LICENSE). The Globish vocabulary itself is Jean-Paul Nerrière's work (2004); this repository packages an independent reconstruction of the word list plus original tooling and documentation around it, and claims no rights over "Globish" as a term or method.

## Credits

- Jean-Paul Nerrière, creator of Globish (2004)
- Built with [Claude](https://claude.ai) using the [Agent Skills](https://github.com/anthropics/skills) framework
