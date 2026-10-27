# tao-of-agent

[한국어](README.ko.md)

Agent skills following the [Vercel agent skills](https://vercel.com/docs/agent-resources/skills)
format. Each skill is a directory under `skills/` with a `SKILL.md`.

## Skills

| Skill | Description |
| --- | --- |
| [`minimal-code`](skills/minimal-code) | Write the smallest correct, readable, tested change — KISS, YAGNI, DRY, explicit errors, TDD. |
| [`git-hygiene`](skills/git-hygiene) | Keep Git history easy to review during development and meaningful after merge. |
| [`natural-clear-writing`](skills/natural-clear-writing) | Write or edit prose without formulaic AI phrasing, with extra rules for Korean. |
| [`ship-until-done`](skills/ship-until-done) | On explicit slash invocation, complete a task list through independent cross-model review, approval, and merge; requires a compatible host integration. |

## Install

### As a Claude Code plugin

The repository is a plugin marketplace that ships one plugin, `tao`, containing every
skill above. Inside Claude Code:

```text
/plugin marketplace add recursivecurry/tao-of-agent
/plugin install tao@tao-of-agent
```

Plugin skills are namespaced: `tao:minimal-code`, `tao:git-hygiene`, `tao:natural-clear-writing`,
`tao:ship-until-done`.

### As a Codex plugin

The repository is also a Codex marketplace with its own `tao` plugin, built for Codex:

```bash
codex plugin marketplace add recursivecurry/tao-of-agent
codex plugin add tao@tao-of-agent
```

The plugin includes a hook, and Codex runs a plugin's hooks only after you approve them. It
shows the review screen at the start of the next session. The skills work without the
approval. The hook does not.

To update later:

```bash
codex plugin marketplace upgrade tao-of-agent
codex plugin add tao@tao-of-agent
```

### With the skills CLI

The [skills CLI](https://vercel.com/docs/agent-resources/skills) installs skills into any
supported agent. Use it for agents that have no plugin above. Installing both a plugin and
these skills into the same agent loads every skill twice, once as `tao:minimal-code` and once
as `minimal-code`, so pick one. Install every skill in the repository:

```bash
npx skills add recursivecurry/tao-of-agent
```

Or pick one:

```bash
npx skills add recursivecurry/tao-of-agent --skill minimal-code
npx skills add recursivecurry/tao-of-agent --skill git-hygiene
npx skills add recursivecurry/tao-of-agent --skill natural-clear-writing
npx skills add recursivecurry/tao-of-agent --skill ship-until-done
```

Add `-g` to install globally, or `-a claude-code` to target a specific agent. Skills installed
this way keep their plain names (`minimal-code`, `git-hygiene`, `natural-clear-writing`,
`ship-until-done`).

### Manually

For Claude Code, copy any skill directory, with its `references/` subdirectory if it has one:

```bash
cp -r skills/minimal-code ~/.claude/skills/
cp -r skills/natural-clear-writing ~/.claude/skills/
cp -r skills/ship-until-done ~/.claude/skills/
```

## Running `ship-until-done`

The command is `/ship-until-done <task list or source>`, or
`/tao:ship-until-done <task list or source>` in Claude Code's plugin. It never starts from
an ordinary development request or a mention of its name. Invocation authorizes continuing
through every supplied item, including PR creation, review, fixes, approval, and merge,
subject to repository rules and actual permission gates.

The files ship in all three distributions, but execution needs host capabilities:

| Target | Invocation protection | Execution requirements |
| --- | --- | --- |
| Claude Code | Native `disable-model-invocation: true` | An external integration providing the Astra/Sol model pair and isolated review contexts; native Claude subagents cannot supply that pair |
| Codex plugin | Native `policy.allow_implicit_invocation: false` | A verified integration for the specified slash command; native `$` mentions and `/skills` selection do not satisfy it |
| Generic | Claude's opt-out field is included; other hosts need their own native control | A host that enforces slash-only invocation and exposes the required models and context isolation |

No slash adapter is included. Unsupported hosts leave the workflow inactive and report the
missing capability. Every execution also requires a distinct GitHub reviewer account eligible
to approve the PR; another model alone does not supply another account. Read the
[platform support and setup](src/skills/ship-until-done/references/platforms.md) before enabling
it. Generic Codex installations must also configure its native implicit-invocation opt-out.
The skill and references are in English. No session hook starts this workflow.

## What the plugins add

Both plugins run a hook at the start of every session that adds two short instructions: follow
`tao:minimal-code` when changing code and work through its done checklist before reporting
done, and keep ordinary replies free of formulaic phrasing. The two sections below explain
why, and give the same text to paste by hand if you installed the skills without a plugin.

## Recommended agent instructions

For project-level instructions, add the following to your `CLAUDE.md` or `AGENTS.md`:

```text
You are a coding agent. Make correct, maintainable changes that satisfy the user's actual request with minimal scope and complexity.

## Operating Principles

- Base decisions on evidence from the repository and conversation context. Do not guess or invent.
- Resolve missing or ambiguous information from the repository and context when there is sufficient evidence. If there is not enough evidence to make a sound decision, ask the user rather than making assumptions.
- Do not expand scope or change existing behavior unless required by the request.
- Never claim work was performed or verified unless it actually was.
```

These are general operating principles for the agent. The plugins provide their own skill-specific instructions and hooks, so those do not need to be repeated here.

## Making `minimal-code` always apply

An agent loads a skill only when it judges the skill relevant, and it loads it at the *start*
of a task — not at the end, where the pre-flight checklist matters most. Coding principles are
meant to hold on every change. The plugins handle this with their hook. Without a plugin, back
the skill with a pointer in your project's `CLAUDE.md` (or `AGENTS.md`):

```markdown
Follow the minimal-code skill when writing or changing code.

Load it before making code changes. Before reporting a change as done, read
references/done-checklist.md from the skill directory and work through it.
```

The skill holds the detail; the pointer is what gets it consulted at the two moments that
decide whether the change stays small. The completion checklist lives in its own file so the
second moment costs a short read, not a reload of the whole skill.

## Making `natural-clear-writing` govern chat replies

The skill loads only for writing and editing tasks, not for ordinary replies. The plugins add
the short form to every session. Without a plugin, put it in `CLAUDE.md` (or `AGENTS.md`):

```markdown
Lead replies with the answer. No staged openers, empty contrasts, forced triads,
dramatic closers, or Markdown decoration. Load natural-clear-writing when
writing or editing prose, docs, commit messages, or UI strings.

한국어 답변과 진행 보고는 명사 나열 대신 조사와 어미로 대상과 행동의 관계를 밝히고, 모호한 비유는 구체적인 말로 바꾼다. 없는 사실을 보태거나 기존 사실·시제·가능성·완료 여부를 바꾸지 않으며, 요청된 문체·언어와 프로젝트 관례를 따르고 인용·코드를 보존하되, 제목·표·목록 외의 설명은 완결된 문장으로 쓴다.
```

The Korean paragraph is also included in both plugins' session hooks; it applies to ordinary
replies and progress reports without loading the full skill. Korean writing and editing tasks
use the skill's detailed Korean reference as well. The Korean guidance draws on the clarity
goals of [fluent-korean](https://github.com/snflkd/fluent-korean).
No separate output style is required.

## Evals

`evals/` holds cases for `natural-clear-writing`: an English doc, a Korean doc, a bilingual
note, compressed Korean prose, an ordinary Korean chat reply, Korean metaphors that the
context does or does not explain, UI strings with placeholders,
and a commit message. Each case has an LLM grader that
checks formulaic phrasing is gone and every fact, placeholder, and register survives.

```bash
tools/eval.sh --judge-model sonnet
```

The default judge (haiku) misreads the Korean criteria, so pass a stronger judge. The run also
scores a no-plugin baseline and reports the delta, which is the number to watch when editing
the skill. Results land in `evals/results/`, which is ignored by git.

The one-turn Korean chat case checks basic reply behavior; a passing score alone does not
demonstrate that the hook improves it. Compare the plugin and no-plugin results, and verify
that the runner executes the SessionStart hook and honors `allowed_tools: []` before drawing
conclusions about the hook.

`claude plugin eval` reads cases only from inside the plugin directory, and the cases are not
shipped with the plugin. The script rebuilds the outputs, copies `plugins/claude/tao/` and
`evals/` into a temporary directory, and runs the eval there. Extra arguments are passed through. Do
not run `claude plugin eval .` at the repository root: it finds the cases but loads no plugin.

## Repository layout

```text
src/skills/<skill>/SKILL.md.tmpl   skill sources: edit here
src/plugin/                        files that go into both plugins
src/claude/                        Claude Code manifests and Claude-only files
src/codex/                         Codex manifests and Codex-only files
tools/build.py                     generates everything below
skills/                            generated, read by the skills CLI
plugins/claude/tao/                generated, the Claude Code plugin
plugins/codex/tao/                 generated, the Codex plugin
.claude-plugin/marketplace.json    generated, the Claude Code marketplace
.agents/plugins/marketplace.json   generated, the Codex marketplace
evals/                             eval cases, not shipped
```

`skills/`, `plugins/`, `.claude-plugin/`, and `.agents/plugins/` are build output. They are
committed because every installer reads the default branch. The build deletes any file in
them that it did not produce, so hand edits and extra files there do not survive.

## Contributing

[AGENTS.md](AGENTS.md) holds the rules for writing a skill that works in all three
distributions. Claude Code and Codex read it when they work in this repository.

1. Edit files under `src/`. A `.tmpl` file is rendered once per distribution, and everything
   else is copied as it is. Every distribution gets the same text unless a template uses a
   target block:

   ```markdown
   <!-- target:claude -->
   This line appears only in the Claude Code plugin.
   <!-- /target -->
   ```

   The targets are `claude`, `codex`, and `generic`. A marker must be a whole line, and
   blocks do not nest.

   Anything that only one agent supports goes in that agent's directory: a hook definition, a
   subagent, a file that names the agent's own variables. `src/claude/` is copied into the
   Claude Code plugin and `src/codex/` into the Codex plugin. Lint rejects the other agent's
   variables and paths there, such as `${PLUGIN_ROOT}` in `src/claude/` or
   `${CLAUDE_PLUGIN_ROOT}` in `src/codex/`. Files that both plugins need go in `src/plugin/`.
2. If the change affects a plugin, raise `version` in both `src/claude/plugin.json` and
   `src/codex/plugin.json`. The two must stay equal. Installed plugins update only when the
   version changes, and the version check fails the build PR without it.
3. Run the checks:

   ```bash
   python3 -m unittest discover -s tools
   python3 tools/build.py lint
   tools/check_codex_plugin.sh   # needs the codex CLI, no login
   ```

4. Open a pull request with the `src/` changes. You do not need to commit generated files. If
   you do, run `python3 tools/build.py build` first so that `python3 tools/build.py check`
   passes.

After the pull request merges, a workflow opens a "Release: regenerate distributions" pull
request with the rebuilt outputs. Merging that one is the release.
[docs/release-setup.md](docs/release-setup.md) describes the one-time setup it needs.
