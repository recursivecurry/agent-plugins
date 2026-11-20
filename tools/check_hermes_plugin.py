"""Run with Hermes' Python environment; no model calls or live-profile changes."""

import json
import os
import shutil
import tempfile
from pathlib import Path


def main():
    package = Path(__file__).resolve().parents[1] / "plugins/hermes/curry"
    with tempfile.TemporaryDirectory(prefix="curry-hermes-") as directory:
        home = Path(directory)
        os.environ["HERMES_HOME"] = str(home)
        installed = home / "plugins/curry"
        shutil.copytree(package, installed)
        (home / "config.yaml").write_text("plugins:\n  enabled: [curry]\n", encoding="utf-8")

        from hermes_cli.plugins import get_plugin_manager
        from tools.skills_tool import skill_view, skills_list

        manager = get_plugin_manager()
        manager.discover_and_load()
        names = {
            skill["name"] for skill in json.loads(skills_list())["skills"]
            if skill["name"].startswith("curry:")
        }
        assert names == {"curry:minimal-code", "curry:git-hygiene", "curry:natural-clear-writing"}, names
        viewed = json.loads(skill_view("curry:minimal-code"))
        assert viewed["success"], viewed
        checklist = json.loads(skill_view("curry:minimal-code", file_path="references/done-checklist.md"))
        assert checklist["success"] and "Before Reporting Done" in checklist["content"], checklist
        assert manager.find_plugin_skill("curry:ship-until-done") is None
        sections = manager.render_system_prompt_sections({"session_id": "curry-test"})
        section = next(item for item in sections if item.id == "curry.session-context")
        original = (installed / "hooks/session-context.md").read_text(encoding="utf-8").strip()
        assert section.content == original
        (installed / "hooks/session-context.md").write_text("changed after registration", encoding="utf-8")
        again = manager.render_system_prompt_sections({"session_id": "curry-test"})
        assert next(item for item in again if item.id == section.id).content == original
        print("Hermes discovery, three namespaced skills, reference loading, static prompt, and fail-closed workflow: OK")


if __name__ == "__main__":
    main()
