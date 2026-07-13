# Case study: building a Globish writing skill for Claude

**Author:** Dave, [@smallstepstoday](https://github.com/smallstepstoday)
**Tools:** Claude (Cowork), Python, Claude's Agent Skills framework
**Repo:** [github.com/smallstepstoday/globish-skill](https://github.com/smallstepstoday/globish-skill)

## The problem

I wanted every document Claude produces for me — reports, memos, emails — to default to language a non-native English speaker could read comfortably on the first pass. "Write in plain English" as a standing instruction is too vague to hold up over a long session; it drifts. I wanted something closer to a spec: an actual approved vocabulary and a set of testable style rules, enforced the same way every time.

That's a well-defined existing idea — Globish, coined in 2004 by Jean-Paul Nerrière, a former IBM VP of international marketing, who noticed that non-native speakers at international conferences converged on a shared, simplified subset of English regardless of their first language. He formalized it as a ~1,500-word vocabulary plus a set of grammar constraints. The task was to turn that into something Claude could actually apply and check itself against, not just imitate loosely.

## Research: finding the actual word list

Nerrière's original word list turned out to be harder to pin down than expected. Several secondary sources reference "the 1,500-word Globish list" without reproducing it, and at least one site hosts a _modified, personal_ variant with 195 words swapped in and out — not the canonical list. I traced it back to the official source (`jpn-globish.com`), which hosts the original vocabulary as a PDF.

PDF text extraction from a multi-column layout is messy — words get pulled out of column order, and short high-frequency words like "an," "is," "was," and "were" turned out to be missing from the extracted list entirely (whether because the PDF extraction dropped them, or because the original list treats conjugated forms of "be" as assumed grammar rather than vocabulary, isn't fully clear). I wrote a script to parse the raw extraction, dedupe, and reconstruct a clean, alphabetized word list — landing on 1,499 unique root words, then adding back 14 core grammar words (articles and "be"/"have"/"do" conjugations) that any working checker needs regardless of whether the original list included them explicitly.

## Design decisions

**A deterministic checker, not just an instruction.** The easy version of this skill would just say "use simple words and short sentences" in the prompt and hope. Instead, I built `check_globish.py`: a Python script that tokenizes a draft, checks every word against the approved list (with suffix-stripping for regular inflections and a ~100-entry irregular verb table so "sent" resolves to "send" and "wrote" resolves to "write"), flags sentences over 15 words, regex-matches the two tenses Globish excludes, and checks against a curated list of ~70 business idioms and clichés. This turns "did I follow the rules" from a vibe into a report Claude reads before delivering.

**Exceptions are policy, not exceptions to the rule.** Proper nouns, numbers, and necessary technical terms would make a naive word-list filter useless — you can't write about quantum physics in a 1,500-word vocabulary without the word "atom." Rather than treat these as edge cases the checker fights against, I built them into the skill's actual policy: capitalized non-sentence-initial words are auto-skipped as likely proper nouns, and technical terms are explicitly allowed as long as they're defined in plain words on first use.

**Progressive disclosure.** Following Claude's skill-authoring conventions, the SKILL.md stays short (the workflow and the rules of thumb); the full word list and the detailed style guide with before/after examples live in `references/`, loaded only when needed. The script is bundled rather than described in prose, because "check 1,500 words against a draft" is a job for deterministic code, not a language model re-deriving the list from memory each time.

## Testing

I validated the checker against two hand-written samples: a deliberately bad paragraph full of business jargon ("let's circle back once we've had a chance to dig into the numbers... don't you think we should synergize our efforts to leverage the low-hanging fruit") and a clean rewrite. The checker correctly flagged every idiom, every passive construction, the one instance of a forbidden tense ("had been anticipating"), and every off-list word in the first pass — and returned a clean report on the second.

I then ran the finished skill against a real prompt — "explain quantum physics in plain English" — through three drafting passes, using the checker's output after each pass to guide revisions (dropping unnecessary jargon like "wave-particle duality" and "uncertainty principle" as _named_ concepts while keeping the underlying explanation; fixing a sentence-splitter edge case around quotation marks by rephrasing rather than patching the script mid-task). The final version reads clean except for five topic-essential technical terms, each defined on first use. See [`examples/before_after.md`](examples/before_after.md) for the full comparison.

## What this demonstrates

- **Primary-source research discipline** — tracing a commonly-cited-but-rarely-linked artifact (the actual Globish word list) back to its origin rather than working from secondhand summaries, and being explicit about the gaps and judgment calls in that source (missing grammar words, a competing unofficial variant).
- **Turning fuzzy instructions into checkable specs** — converting "write simply" into a vocabulary list, a style guide with rules and examples, and a script that verifies compliance, rather than relying on a language model to self-assess against a vague standard.
- **Practical NLP without heavyweight dependencies** — inflection handling and irregular-verb resolution built with the Python standard library, keeping the tool portable and dependency-free.
- **Iterative, test-driven prompt/skill engineering** — building the skill, testing it against adversarial and real examples, reading the actual tool output, and revising based on what the checker caught rather than eyeballing the result.
- **Skill design following Claude's own authoring conventions** — progressive disclosure (SKILL.md → references/ → scripts/), a description written to trigger reliably, and a workflow that treats the checker as a report the model uses judgment against, not an unquestionable gate.

## What I'd do next

- Fix the sentence-splitter's quotation-mark edge case in the script itself, rather than working around it in the prose.
- Expand the idiom list and open it to community contributions.
- Add a small test suite (`pytest`) covering the irregular-verb table and the suffix-stripping logic, so future edits to the wordlist or script are regression-tested rather than eyeballed.
