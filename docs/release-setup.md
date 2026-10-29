# Release setup

Generated files are committed, and a workflow keeps them current. When changes to `src/` or
`tools/` land on `main`, `.github/workflows/build-pr.yml` rebuilds the outputs and opens one
pull request from the `bot/build` branch. Merging that pull request is the release.

The workflow needs a GitHub App. A pull request opened with the default `GITHUB_TOKEN` does
not trigger `check.yml`, so its required checks would never report. Until the setup below is
done, the workflow fails with a message that points to this file.

## One-time setup

1. Create a GitHub App owned by the repository owner, with no webhook and these repository
   permissions:

   | Permission | Access |
   | --- | --- |
   | Contents | Read and write |
   | Pull requests | Read and write |

2. Install the App on this repository only.
3. Generate a private key for the App.
4. In the repository's Actions settings, add:

   | Kind | Name | Value |
   | --- | --- | --- |
   | Variable | `BUILD_APP_ID` | The App ID |
   | Secret | `BUILD_APP_KEY` | The contents of the private key file |

5. In the repository's Actions settings, allow GitHub Actions to create pull requests.
6. Protect `main` and require these status checks from `check.yml`:

   - `test`
   - `lint`
   - `generated`
   - `version`

   Leave `skills-cli` and `codex-cli` optional. They read the text output of the skills CLI
   and the Codex CLI, which may change between CLI versions.

## Verify installation after the rename

1. If `tao@tao-of-agent` is installed, uninstall the old plugin and remove the old
   marketplace before installing `curry@agent-plugins`. See the README's migration section.
2. Install the Claude Code plugin from GitHub:

   ```bash
   claude plugin marketplace add recursivecurry/agent-plugins
   claude plugin install curry@agent-plugins
   ```

   After a restart, verify that `curry:minimal-code`, `curry:git-hygiene`, and
   `curry:natural-clear-writing` are available.
3. Install the Codex plugin from GitHub:

   ```bash
   codex plugin marketplace add recursivecurry/agent-plugins
   codex plugin add curry@agent-plugins
   ```

   Start a Codex session, approve the hook on the review screen, and ask which skill it was
   told to follow when changing code. The answer should name `curry:minimal-code`.
4. At the next release, check how a Codex install picks up the new version: run
   `codex plugin marketplace upgrade agent-plugins`, start a session, and see whether
   `codex plugin list` shows the new version. If it does not, `codex plugin add curry@agent-plugins`
   is needed as well, which is what the README tells users to run.

## Each release after that

1. Merge a pull request that changes `src/` and raises `version` in both
   `src/claude/plugin.json` and `src/codex/plugin.json`.
2. Review the "Release: regenerate distributions" pull request. Its body lists the version
   change and which skills changed in each distribution.
3. Merge it.

If the build pull request fails the `version` check, the source change did not raise the
version. Raise it in both manifests in a new pull request. The build pull request updates
itself once that merges.
