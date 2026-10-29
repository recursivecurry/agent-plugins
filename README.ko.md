# agent-skills

[English](README.md)

[Vercel agent skills](https://vercel.com/docs/agent-resources/skills) 형식을 따르는 에이전트
스킬 모음입니다. 스킬 하나는 `skills/` 아래의 디렉터리 하나이고, 그 안에 `SKILL.md`가 있습니다.

## 스킬

| 스킬 | 설명 |
| --- | --- |
| [`minimal-code`](skills/minimal-code) | 정확하고 읽기 쉬우며 테스트된 변경을 가장 작게 만듭니다. KISS, YAGNI, DRY, 명시적인 오류 처리, TDD를 따릅니다. |
| [`git-hygiene`](skills/git-hygiene) | 개발 중에는 리뷰하기 쉽고 병합 후에는 의미가 남는 Git 이력을 유지합니다. |
| [`natural-clear-writing`](skills/natural-clear-writing) | 상투적인 AI 문체 없이 글을 쓰거나 고칩니다. 한국어에는 추가 규칙을 적용합니다. |
| [`ship-until-done`](skills/ship-until-done) | 명시적인 슬래시 명령으로 작업 목록을 독립적인 교차 모델 리뷰·승인·머지까지 완수합니다. 호환되는 호스트 연동이 필요합니다. |

## 설치

### Claude Code 플러그인으로 설치

이 저장소는 플러그인 마켓플레이스이며, 위의 모든 스킬을 담은 플러그인 `curry` 하나를 제공합니다.
Claude Code 안에서 다음을 실행합니다.

```text
/plugin marketplace add recursivecurry/agent-skills
/plugin install curry@agent-skills
```

플러그인의 스킬에는 네임스페이스가 붙습니다: `curry:minimal-code`, `curry:git-hygiene`,
`curry:natural-clear-writing`, `curry:ship-until-done`.

### Codex 플러그인으로 설치

이 저장소는 Codex 마켓플레이스이기도 하며, Codex에 맞춰 만든 별도의 `curry` 플러그인을 제공합니다.

```bash
codex plugin marketplace add recursivecurry/agent-skills
codex plugin add curry@agent-skills
```

플러그인에는 hook이 들어 있고, Codex는 사용자가 승인한 뒤에만 플러그인의 hook을 실행합니다.
승인 화면은 다음 세션을 시작할 때 나타납니다. 스킬은 승인하지 않아도 동작하지만 hook은
동작하지 않습니다.

나중에 업데이트하려면 다음을 실행합니다.

```bash
codex plugin marketplace upgrade agent-skills
codex plugin add curry@agent-skills
```

### 기존 `tao` 설치에서 이전

`tao@tao-of-agent`를 설치했다면 에이전트에서 해당 플러그인과 `tao-of-agent` 마켓플레이스를
제거하세요. 그런 다음 위의 설치 명령으로 `curry@agent-skills`를 추가하고 에이전트를 다시
시작하세요. 저장해 둔 `tao:<skill>` 참조도 `curry:<skill>`로 바꾸세요.

### skills CLI로 설치

[skills CLI](https://vercel.com/docs/agent-resources/skills)는 지원하는 모든 에이전트에 스킬을
설치합니다. 위에 플러그인이 없는 에이전트에 사용하세요. 한 에이전트에 플러그인과 이 스킬을
함께 설치하면 모든 스킬이 `curry:minimal-code`와 `minimal-code`로 두 번 로드되므로 둘 중 하나만
고르세요. 저장소의 모든 스킬을 설치하려면 다음을 실행합니다.

```bash
npx skills add recursivecurry/agent-skills
```

하나만 골라 설치할 수도 있습니다.

```bash
npx skills add recursivecurry/agent-skills --skill minimal-code
npx skills add recursivecurry/agent-skills --skill git-hygiene
npx skills add recursivecurry/agent-skills --skill natural-clear-writing
npx skills add recursivecurry/agent-skills --skill ship-until-done
```

전역으로 설치하려면 `-g`를, 특정 에이전트를 지정하려면 `-a claude-code`를 붙입니다. 이렇게
설치한 스킬은 접두사 없는 이름(`minimal-code`, `git-hygiene`, `natural-clear-writing`, `ship-until-done`)을
그대로 씁니다.

### 수동 설치

Claude Code에서는 스킬 디렉터리를 복사합니다. `references/` 하위 디렉터리가 있으면 함께
복사합니다.

```bash
cp -r skills/minimal-code ~/.claude/skills/
cp -r skills/natural-clear-writing ~/.claude/skills/
cp -r skills/ship-until-done ~/.claude/skills/
```

## `ship-until-done` 실행하기

명령은 `/ship-until-done <작업 목록 또는 출처>`이며, Claude Code 플러그인에서는
`/curry:ship-until-done <작업 목록 또는 출처>`로 실행합니다. 일반적인 개발 요청이나 스킬 이름의
언급만으로는 시작하지 않습니다. 실행하면 저장소 규칙과 실제 권한 제한을 지키면서 주어진 모든
항목의 PR 생성, 리뷰, 수정, 승인, 머지까지 이어서 진행합니다.

파일은 세 배포판 모두에 포함되지만, 실행하려면 호스트가 필요한 기능을 제공해야 합니다.

| 대상 | 자동 실행 방지 | 실행에 필요한 기능 |
| --- | --- | --- |
| Claude Code | 기본 설정인 `disable-model-invocation: true`를 적용합니다. | 검증된 Fable/Opus 모델 선택 기능과 독립된 리뷰 컨텍스트가 필요합니다. 기본 서브 에이전트가 조건을 충족하면 사용할 수 있습니다. |
| Codex 플러그인 | 기본 설정인 `policy.allow_implicit_invocation: false`를 적용합니다. | 지정된 슬래시 명령을 검증할 수 있는 연동이 필요합니다. 기본 `$` 호출과 `/skills` 선택은 이 조건을 충족하지 않습니다. |
| Generic | Claude의 자동 호출 차단 필드를 포함합니다. 다른 호스트에는 해당 호스트의 기본 차단 설정이 필요합니다. | 슬래시 명령으로만 실행하도록 제한하고, 필요한 모델과 독립 컨텍스트를 제공하는 호스트가 필요합니다. |

슬래시 명령 어댑터는 포함하지 않습니다. 지원하지 않는 호스트에서는 워크플로를 실행하지 않고
부족한 기능을 알립니다. 실행하려면 PR 작성자와 별개로 유효한 승인을 제출할 수 있는 GitHub
리뷰어 계정도 필요합니다. 모델을 바꾸는 것만으로 계정이 바뀌지는 않습니다. 사용하기 전에
[플랫폼 지원 및 설정 안내](src/skills/ship-until-done/references/platforms.md.tmpl)를 읽으세요.
Generic 스킬을 Codex에 설치했다면 Codex의 기본 자동 호출 차단 설정도 적용해야 합니다.
참조 문서는 단계별로 읽습니다. 작업 전에는 플랫폼 사전 점검과 실행 지침, 첫 리뷰에는
리뷰 패킷, 매 머지 전에는 머지 조건, 차단 또는 재개 시에는 복구 지침을 읽습니다.
재리뷰에서는 변경 SHA·발견 사항·증거를 전달하고 전체 발견 사항 기록은 조회 가능한 위치에
보존합니다. Codex는 GPT-Astra와 GPT-Sol, Claude Code는 Fable과 Opus를 짝지으며,
실제 모델 ID는 호스트에서 검증해야 합니다. 스킬과 참조 문서는 영어로 작성되어 있습니다.
세션 hook은 이 워크플로를 시작하지 않습니다.

## 플러그인이 추가하는 것

두 플러그인은 세션을 시작할 때마다 hook을 실행해 짧은 지침 두 가지를 넣습니다. 하나는 코드를
바꿀 때 `curry:minimal-code`를 따르고 완료를 보고하기 전에 그 스킬의 완료 체크리스트를 점검하라는
지침이고, 다른 하나는 일반 답변에서 상투적인 표현을 쓰지 말라는 지침입니다. 아래 두 절은 그
이유를 설명하고, 플러그인 없이 스킬만 설치한 경우 직접 붙여 넣을 같은 문구를 제공합니다.

## `minimal-code`를 항상 적용하기

에이전트는 스킬이 관련 있다고 판단할 때만 스킬을 로드하고, 그것도 작업을 *시작*할 때
로드합니다. 완료 전 체크리스트가 가장 필요한 작업의 끝에서는 로드하지 않습니다. 코딩 원칙은
모든 변경에 적용되어야 합니다. 플러그인은 hook으로 이 문제를 해결합니다. 플러그인이 없다면
프로젝트의 `CLAUDE.md`(또는 `AGENTS.md`)에 스킬을 가리키는 문구를 넣어 보완하세요.

```markdown
Follow the minimal-code skill when writing or changing code.

Load it before making code changes. Before reporting a change as done, read
references/done-checklist.md from the skill directory and work through it.
```

세부 내용은 스킬에 있습니다. 이 문구는 변경이 작게 유지될지를 좌우하는 두 시점에 에이전트가
스킬을 참조하게 합니다. 완료 체크리스트를 별도 파일로 둔 것은 두 번째 시점에 스킬 전체를 다시
로드하지 않고 짧은 파일 하나만 읽게 하기 위해서입니다.

## `natural-clear-writing`을 일반 답변에도 적용하기

이 스킬은 글을 쓰거나 고치는 작업에서만 로드되고 일반 답변에서는 로드되지 않습니다.
플러그인은 요약한 규칙을 모든 세션에 넣습니다. 플러그인이 없다면 `CLAUDE.md`(또는
`AGENTS.md`)에 다음을 넣으세요.

```markdown
Lead replies with the answer. No staged openers, empty contrasts, forced triads,
dramatic closers, or Markdown decoration. Load natural-clear-writing when
writing or editing prose, docs, commit messages, or UI strings.

한국어 답변과 진행 보고는 명사 나열 대신 조사와 어미로 대상과 행동의 관계를 밝히고, 모호한 비유는 구체적인 말로 바꾼다. 없는 사실을 보태거나 기존 사실·시제·가능성·완료 여부를 바꾸지 않으며, 요청된 문체·언어와 프로젝트 관례를 따르고 인용·코드를 보존하되, 제목·표·목록 외의 설명은 완결된 문장으로 쓴다.
```

위 한국어 문단은 두 플러그인의 세션 hook에도 포함됩니다. 전체 스킬을 로드하지 않아도 일반
답변과 진행 보고에 적용되며, 한국어 글을 쓰거나 고칠 때는 스킬의 상세 한국어 규칙도 적용됩니다.
한국어 지침은 [fluent-korean](https://github.com/snflkd/fluent-korean)의 명확한 한국어 작성 원칙을 참고했습니다.
별도 output-style을 설치할 필요는 없습니다.

## 평가

`evals/`에는 `natural-clear-writing`의 평가 케이스가 있습니다. 영어 문서, 한국어 문서, 두
언어가 섞인 메모, 압축된 한국어 문장, 일반 한국어 채팅 답변, 문맥으로 풀 수 있거나 없는
한국어 비유, 플레이스홀더가 있는 UI 문자열,
커밋 메시지입니다. 각 케이스에는 LLM 채점기가
있어 상투적인 표현이 사라졌는지, 모든 사실과 플레이스홀더와 어조가 보존되었는지 확인합니다.

```bash
tools/eval.sh --judge-model sonnet
```

기본 채점 모델(haiku)은 한국어 채점 기준을 잘못 읽으므로 더 강한 모델을 지정하세요. 실행하면
플러그인이 없는 기준선도 함께 채점해 차이를 보고합니다. 스킬을 수정할 때 살펴볼 숫자가 이
차이입니다. 결과는 `evals/results/`에 저장되며, 이 디렉터리는 git이 무시합니다.

한 턴짜리 한국어 채팅 사례는 기본 답변 동작을 확인합니다. 통과 점수만으로 hook의 개선 효과를
입증할 수는 없습니다. 플러그인 적용 결과와 기준선을 비교하고, 실행기가 SessionStart hook을
실행하며 `allowed_tools: []`를 준수하는지 확인해야 합니다.

`claude plugin eval`은 플러그인 디렉터리 안의 케이스만 읽는데, 평가 케이스는 플러그인에
포함되어 배포되지 않습니다. 그래서 이 스크립트는 출력을 다시 빌드하고 `plugins/claude/curry/`와
`evals/`를 임시 디렉터리에 복사한 뒤 거기서 평가를 실행합니다. 추가 인자는 그대로 전달됩니다.
저장소 루트에서 `claude plugin eval .`을 실행하지 마세요. 케이스는 찾지만 플러그인을 로드하지
않습니다.

## 저장소 구조

```text
src/skills/<skill>/SKILL.md.tmpl   스킬 소스: 여기를 수정합니다
src/plugin/                        두 플러그인에 모두 들어가는 파일
src/claude/                        Claude Code 매니페스트와 Claude 전용 파일
src/codex/                         Codex 매니페스트와 Codex 전용 파일
tools/build.py                     아래의 모든 것을 생성합니다
skills/                            생성됨, skills CLI가 읽습니다
plugins/claude/curry/              생성됨, Claude Code 플러그인
plugins/codex/curry/               생성됨, Codex 플러그인
.claude-plugin/marketplace.json    생성됨, Claude Code 마켓플레이스
.agents/plugins/marketplace.json   생성됨, Codex 마켓플레이스
evals/                             평가 케이스, 배포되지 않습니다
```

`skills/`, `plugins/`, `.claude-plugin/`, `.agents/plugins/`는 빌드 출력입니다. 모든 설치
도구가 기본 브랜치를 읽기 때문에 이 디렉터리들을 커밋해 둡니다. 빌드는 이 디렉터리에서 자신이
만들지 않은 파일을 삭제하므로, 직접 수정한 내용이나 추가한 파일은 남지 않습니다.

## 기여하기

세 배포판 모두에서 동작하는 스킬을 쓰기 위한 규칙은 [AGENTS.md](AGENTS.md)에 있습니다. Claude
Code와 Codex는 이 저장소에서 작업할 때 이 파일을 읽습니다.

1. `src/` 아래의 파일을 수정합니다. `.tmpl` 파일은 배포판마다 한 번씩 렌더링되고, 나머지
   파일은 그대로 복사됩니다. 템플릿은 target block으로 배포판별 내용을 선택할 수 있습니다.

   ```markdown
   <!-- target:claude -->
   이 줄은 Claude Code 플러그인에만 들어갑니다.
   <!-- /target -->
   ```

   타깃은 `claude`, `codex`, `generic`입니다. 마커는 한 줄 전체를 차지해야 하고, 블록은
   중첩할 수 없습니다.

   배포 대상에 맞춰 모델명을 바꾸려면 템플릿에 `{{model:GPT-Astra}}`,
   `{{model:GPT-Sol}}`, `{{model:GPT-Terra}}`, `{{model:GPT-Luna}}`를 사용합니다.
   배포판 재생성 시 다음과 같이 매칭합니다.

   | Codex | Claude Code |
   | --- | --- |
   | GPT-Astra | Fable |
   | GPT-Sol | Opus |
   | GPT-Terra | Sonnet |
   | GPT-Luna | Haiku |

   Generic 출력은 Codex 이름을 유지합니다. 일반 텍스트의 모델명과 템플릿이 아닌 파일은
   바꾸지 않습니다. 이 이름들은 모델 계열을 나타내며, 실행 모델 ID는 호스트에서 확인해야 합니다.

   한 에이전트만 지원하는 것은 그 에이전트의 디렉터리에 둡니다. hook 정의, subagent, 그
   에이전트의 변수 이름을 쓰는 파일이 여기에 해당합니다. `src/claude/`는 Claude Code
   플러그인으로, `src/codex/`는 Codex 플러그인으로 복사됩니다. lint는 이 디렉터리에 다른
   에이전트의 변수와 경로가 있으면 거부합니다. 예를 들어 `src/claude/`의 `${PLUGIN_ROOT}`나
   `src/codex/`의 `${CLAUDE_PLUGIN_ROOT}`입니다. 두 플러그인에 모두 필요한 파일은
   `src/plugin/`에 둡니다.
2. 변경이 플러그인에 영향을 주면 `src/claude/plugin.json`과 `src/codex/plugin.json`의
   `version`을 함께 올립니다. 두 값은 같아야 합니다. 설치된 플러그인은 버전이 바뀔 때만
   업데이트되고, 버전을 올리지 않으면 빌드 PR의 버전 검사가 실패합니다.
3. 검사를 실행합니다.

   ```bash
   python3 -m unittest discover -s tools
   python3 tools/build.py lint
   tools/check_codex_plugin.sh   # codex CLI가 필요하고, 로그인은 필요 없습니다
   ```

4. `src/` 변경으로 pull request를 엽니다. 생성된 파일은 커밋하지 않아도 됩니다. 커밋한다면
   먼저 `python3 tools/build.py build`를 실행해 `python3 tools/build.py check`가 통과하게
   하세요.

pull request가 병합되면 워크플로가 다시 빌드한 출력으로 "Release: regenerate distributions"
pull request를 엽니다. 이 pull request를 병합하는 것이 릴리스입니다. 여기에 필요한 1회성 설정은
[docs/release-setup.md](docs/release-setup.md)에 있습니다.
