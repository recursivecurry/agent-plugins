import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import build
from test_build import GitCase, commit_all, git, write

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "plugins/hermes/curry"


class HermesDistributionTest(unittest.TestCase):
    def test_readme_installation_targets_the_selected_profile(self):
        for readme in ("README.md", "README.ko.md"):
            text = (ROOT / readme).read_text()
            section = text.split("### ")[3]
            snippet = section.split("```bash\n", 1)[1].split("```", 1)[0]
            self.assertIn('hermes --profile "$profile" config path', snippet)
            self.assertIn('hermes --profile "$profile" plugins enable curry', snippet)
            for profile in ("default", "review-test"):
                with self.subTest(readme=readme, profile=profile), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    home = root if profile == "default" else root / "profiles" / profile
                    script = '''
set -eu
python3() { :; }
hermes() {
    test "$1" = --profile
    test "$2" = "$EXPECTED_PROFILE"
    shift 2
    case "$*" in
        "config path") printf '%s/config.yaml\\n' "$EXPECTED_HOME" ;;
        "plugins validate plugins/hermes/curry") ;;
        "plugins enable curry") test -f "$EXPECTED_HOME/plugins/curry/plugin.yaml" ;;
        *) return 1 ;;
    esac
}
''' + snippet.replace("profile=default", f"profile={profile}")
                    result = subprocess.run(
                        ["bash", "-c", script], cwd=ROOT, capture_output=True, text=True,
                        env={**os.environ, "HERMES_HOME": str(root / "wrong-profile"),
                             "EXPECTED_PROFILE": profile, "EXPECTED_HOME": str(home)},
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue((home / "plugins/curry/plugin.yaml").is_file())
                    self.assertFalse((root / "wrong-profile/plugins").exists())

    def test_rendered_hermes_skills_have_no_foreign_target_leaks(self):
        for path, output in build.expected_outputs(ROOT).items():
            if path.startswith(PACKAGE + "/skills/") and path.endswith(".md"):
                text = output.content.decode()
                for term in (*build.FOREIGN_IN_HERMES, "<!-- target:", "{{model:", "fork_turns"):
                    with self.subTest(path=path, term=term):
                        self.assertNotIn(term, text)

    def test_target_conversion_preserves_families_without_inventing_ids(self):
        source = "{{model:GPT-Astra}} / {{model:GPT-Sol}}\n<!-- target:claude -->\nClaude call\n<!-- /target -->\n<!-- target:codex -->\nCodex call\n<!-- /target -->\n<!-- target:hermes -->\nHermes call\n<!-- /target -->\n"
        rendered = build.render_template(source, "hermes", "test.tmpl", notice=False).decode()
        self.assertEqual(rendered, "GPT-Astra / GPT-Sol\nHermes call\n")

    def test_lint_rejects_unresolved_template_syntax(self):
        for syntax in ("{{model:}}", "<!-- target: hermes -->"):
            with self.subTest(syntax=syntax):
                self.assertTrue(list(build.lint_template("test.tmpl", syntax + "\n", None)))

    def test_hermes_rejects_foreign_harness_syntax(self):
        for syntax in ("${CLAUDE_PLUGIN_ROOT}", "${PLUGIN_ROOT}", "collaboration.spawn_agent", "agents/openai.yaml", "disable-model-invocation: true"):
            with self.subTest(syntax=syntax):
                violations = list(build.lint_template("test.tmpl", syntax + "\n", None))
                self.assertTrue(any("Hermes" in str(error) for error in violations), syntax)

    def test_native_package_bundles_skills_and_shared_context(self):
        outputs = build.expected_outputs(ROOT)
        manifest = json.loads(outputs[f"{PACKAGE}/plugin.yaml"].content)
        claude = json.loads(outputs[build.CLAUDE.manifest].content)
        self.assertEqual(manifest["name"], "curry")
        self.assertEqual(manifest["version"], claude["version"])
        self.assertIn(f"{PACKAGE}/__init__.py", outputs)
        context = outputs[f"{PACKAGE}/hooks/session-context.md"].content
        self.assertEqual(context, (ROOT / "src/plugin/hooks/session-context.md").read_bytes())
        self.assertNotIn(f"{PACKAGE}/hooks/session-start.sh", outputs)
        for skill in build.skill_dirs(ROOT):
            self.assertIn(f"{PACKAGE}/skills/{skill.name}/SKILL.md", outputs)
        ship = outputs[f"{PACKAGE}/skills/ship-until-done/SKILL.md"].content.decode()
        self.assertIn("inactive on Hermes", ship)

    def test_registers_static_context_and_only_safe_skills(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for path, output in build.expected_outputs(ROOT).items():
            if path.startswith(PACKAGE + "/"):
                file = root / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_bytes(output.content)
        spec = importlib.util.spec_from_file_location("curry_plugin", root / PACKAGE / "__init__.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        class Context:
            def __init__(self):
                self.skills = {}
                self.sections = {}

            def register_skill(self, name, path, description="", frontmatter=None):
                self.skills[name] = (path, description)

            def register_system_prompt_section(self, id, content, **kwargs):
                self.sections[id] = content

        context = Context()
        module.register(context)
        self.assertEqual(set(context.skills), {"minimal-code", "git-hygiene", "natural-clear-writing"})
        self.assertEqual(set(context.sections), {"curry.session-context"})
        self.assertIsInstance(context.sections["curry.session-context"], str)
        self.assertIn("curry:minimal-code", context.sections["curry.session-context"])
        for path, description in context.skills.values():
            self.assertTrue(path.is_file())
            self.assertTrue(description)


class HermesVersionTest(GitCase):
    def test_hermes_only_change_requires_shared_version_bump(self):
        self.build()
        commit_all(self.root, "base")
        git(self.root, "tag", "base")
        write(self.root, "src/hermes/__init__.py", "def register(ctx): pass\n")
        self.build()
        commit_all(self.root, "Hermes only")
        with self.assertRaisesRegex(build.BuildError, "shared plugin version"):
            build.version_check(self.root, "base")
        self.set_version("0.3.0")
        self.build()
        commit_all(self.root, "bump")
        self.assertEqual(build.version_check(self.root, "base"), 0)


if __name__ == "__main__":
    unittest.main()
