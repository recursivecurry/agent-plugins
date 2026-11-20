from pathlib import Path


def register(ctx):
    root = Path(__file__).resolve().parent
    context = (root / "hooks/session-context.md").read_text(encoding="utf-8")
    ctx.register_system_prompt_section("curry.session-context", context)
    for name in ("minimal-code", "git-hygiene", "natural-clear-writing"):
        path = root / "skills" / name / "SKILL.md"
        description = next(
            line.removeprefix("description: ")
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.startswith("description: ")
        )
        ctx.register_skill(name, path, description=description)