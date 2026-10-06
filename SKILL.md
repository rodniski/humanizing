---
name: humanizing
description: Fix the structural tells of AI writing that word lists miss — the explained moral at the end, discovery-order narration, tidy closure, vague allusions, symmetric sections, emotions shown through the body but never named. Use when drafting or reviewing prose longer than a few sentences (docs, READMEs, PR descriptions, posts, emails, fiction), when the user says text "sounds like AI", "feels generated", "too tidy", "too neat", asks to "humanize" or "make it read like a person wrote it", or when a surface pass (unslop, Humanizer) already removed the buzzwords and the text still reads machine-made.
license: MIT
user-invocable: true
argument-hint: "[review · rewrite · draft] [text or file]"
metadata:
  author: rodniski
  version: "0.1.0"
---

# Humanizing

Word-level tells ("delve", "tapestry", em-dash floods) are easy to strip and newer models already avoid them. What keeps giving AI text away is structure: the decisions about order, emphasis, closure and reference that happen before any sentence is written. StoryScope (Russell et al., COLM 2026) separated human from AI fiction at 93.2% macro-F1 using those decisions alone, with every style feature removed.

This skill works on that layer. Pair it with a surface pass; it does not replace one.

## Modes

| Mode | What it does |
|------|--------------|
| `review` (default for pasted text) | Flag structural tells with the quoted span, the rule it breaks and a one-line fix. Change nothing. |
| `rewrite` | Restructure the text under the rules below. Keep every fact, number, name and claim. |
| `draft` | Write new prose with the rules applied from the first line. |

When writing anything long on your own initiative, apply the rules silently. Do not announce that you are doing it.

## The rules

Each rule names the default to break and the evidence behind it (AI vs human rates from StoryScope, fiction corpus). For non-fiction the rules are extrapolations of the same defaults, not measured results.

### 1. Don't end on the moral

AI closes by telling the reader what it all meant (narrators state the theme in 77% of AI stories vs 52% of human ones). End on the last fact, the decision, or the next action. If the point needs stating, state it once, early.

Cut: "Ultimately, this shows…", "In the end, what matters is…", "This highlights the importance of…", a final paragraph that restates the first.

### 2. Name, don't allude

AI gestures at things (72% vague allusions vs 50%) and rarely names real works, people, places or brands (24% vs 47%). Replace every gesture with the specific thing: file and line, PR number, the measured value, the author and title, the street.

If you cannot name it, ask whether the sentence needs to exist.

### 3. Say it plainly

AI dresses statements in imagery. In fiction it renders emotion through the body (81% vs 38%) and almost never labels it (8% vs 29%). In technical prose the same habit shows as metaphor, "journey", "landscape", a bug that "lurks". Use the direct word when the direct word is accurate: "this is broken", "she was afraid", "we got it wrong".

Imagery stays when it carries information the plain word cannot.

### 4. Order by importance, not by discovery

AI narrates in the order things happened to it: first I checked X, then Y, finally Z. Humans jump: they open with the result and go back only as far as the reader needs (human stories show more flashbacks, time jumps and delayed disclosure). Lead with the conclusion. Put the trail after it, or drop it.

### 5. Leave open what is open

AI resolves everything: internal acceptance over unresolved endings (47% vs 27%), clear-cut protagonists over morally mixed ones (38% mixed vs 59%). Real work has loose ends. Say what you did not check, what is a guess, what is still disputed. One honest "not verified" beats a tidy wrap.

### 6. Let parts be uneven

AI builds symmetric structures: three bullets per section, every section the same length, every aside tied back to the thesis (79% of AI stories have no subplot vs 57%). Size each part by its weight. A one-line section is fine. An aside can stay an aside.

### 7. Write to someone

AI writes as if no one is reading (direct reader address in 7% of AI stories vs 28%). Know who the reader is and talk to them: "you" when it fits, their vocabulary, the question they actually asked.

## Process

1. **Find the point.** One sentence. If you cannot write it, the text is not ready to restructure.
2. **Reorder** (rule 4): point first, then what the reader needs, in falling order of importance.
3. **Sweep the edges:** the last paragraph (rule 1) and every vague noun phrase (rule 2).
4. **Check shape** (rule 6): does any section exist only for symmetry? Merge or cut it.
5. **Add the open ends** (rule 5) if there are any. Do not invent doubt.
6. **Read it as the reader** (rule 7). Then stop.

For `review`, report in this shape:

```markdown
- "<quoted span>" — rule N (<name>): <one-line fix>
```

Sort by impact. Skip anything that is a judgment call unless the user asked for everything.

## Don't trade one tell for another

Over-correcting produces its own fingerprint. Avoid:

- **Forced abruptness.** Ending without a conclusion is not the goal; ending without a *redundant* one is.
- **Fake casualness.** Slang, "honestly", "look," and sentence fragments sprinkled in to sound human.
- **Manufactured doubt.** Hedging facts you verified to satisfy rule 5.
- **Token references.** Dropping a famous name to satisfy rule 2 when it adds nothing.
- **Gratuitous nonlinearity.** In fiction, a flashback because the rules said so.

If a rule makes a specific text worse, break the rule.

## Fiction

The rules above hold, plus the narrative defaults StoryScope found most diagnostic:

- Keep the theme implicit. No closing paragraph where the character understands the lesson.
- Let a subplot run that does not mirror the main theme.
- Use time: open late, jump, delay a disclosure, recontextualize an earlier scene.
- Let the protagonist be wrong, mixed, or unresolved. Let the ending be external, or open.
- Name emotions sometimes. Not every feeling needs a tightening chest.
- Reference real books, places and people by name.
- Vary escalation. Not every story needs a quiet epilogue; not every story needs a climax.

When asked to *generate* fiction from a brief, don't let the brief dictate structure: a one-paragraph premise invites a linear, single-track, theme-stated story.

## Scope

This is a writing-quality tool. It does not promise to beat AI detectors and should not be framed as one. In StoryScope, a fine-tuned classifier on raw text still separated human from AI at 99.9%; structure is one layer of many.

See [references/examples.md](references/examples.md) for before/after pairs per rule and context.
