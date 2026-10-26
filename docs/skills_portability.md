# Skill portability by capability

Checked on 2026-10-26. This is a bounded compatibility assessment of the five Python testing skills, not a market catalog or a certification.

## Canonical source and evidence levels

The only maintained source is `.agents/skills/<name>/SKILL.md`. Each entry contains its essential workflow and example; the [project profile](testing.md#project-profile) supplies this API's contracts, fixtures, paths and limits. A different repository supplies its own profile. The examples target Python/Pytest; another programming stack needs a reviewed adaptation rather than an assumed compatibility claim.

**Documented** means a current official source describes a format or loader. **Inspected** means these local files were checked structurally. **Executed** means a named task actually read and applied a version here. Loading a file alone establishes neither test quality nor another client's compatibility.

The local evaluation used explicit file reads in this Codex desktop workflow. The three read-only evaluators reported their requested local skills absent from preexisting catalogs; mutation and HTTP used explicit path reads too. Native discovery, implicit matching and other clients were not executed.

## What is being reused

A model family supplies inference; a harness supplies the agent loop, context, tools and approvals. A framework/SDK helps build that loop. Agent Skills defines a bundle format; the client decides discovery and invocation. A protocol or orchestration framework is not automatically a skill loader.

The common frontmatter here uses `name`, `description`, `license` and string-valued `metadata.version`. The [Agent Skills specification](https://agentskills.io/specification) defines the format; the consistent headings are a repository convention. We omit client-specific macros, tool allowlists and UI metadata from the common source. Common name, description, license and version metadata does not grant execution permissions; client-specific tool policies require separate review.

## Client matrix

All rows are **documented / execution not tested**, except the explicit local reads described above. Sources were consulted on 2026-10-26; documentation can change independently of an installed version.

| Product/client | Documented source/discovery and invocation | Adaptation or uncertainty | Official source |
| --- | --- | --- | --- |
| Codex CLI / IDE extension | Repo `.agents/skills`; `$` mention or skill selector; progressive reading | Same canonical root. This desktop evaluation used file paths, not a CLI/IDE discovery test. Optional UI metadata is client-specific. | [Codex skills](https://developers.openai.com/codex/skills/) |
| Claude Code | `.claude/skills/<name>`; `/name` | Needs authorized exposure at its supported root. Do not presume this client's discovery of `.agents` or copy its dynamic/context fields into the core. | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Antigravity IDE | Workspace `.agents/skills`; name mention and Customizations | Same source root documented; verify IDE catalog and tools rather than borrowing App/CLI commands. | [IDE skills](https://www.antigravity.google/docs/skills?tab=ide) |
| Antigravity App | Workspace `.agents/skills`; `/name` | Separate surface and global roots from the IDE. No installation/configuration tested. | [Skills, App tab](https://www.antigravity.google/docs/skills?tab=app) |
| Antigravity CLI | Workspace `.agents/skills`; skill commands `/name` | Verify the installed CLI and permissions independently of the IDE/App. | [Skills, CLI tab](https://www.antigravity.google/docs/skills?tab=cli) |
| ZCode Agent | Settings -> Skills; `$name`; project/global import by link or copy | Exact local project destination was not established by the consulted page. Refresh/import is a future authorized action; do not invent a path. | [ZCode Skill](https://zcode.z.ai/en/docs/skill) |
| OpenCode | `.opencode/skills`, `.claude/skills`, `.agents/skills`; `skill({name})` | Existing source root documented. Loading permission and test-execution permission are separate. | [OpenCode skills](https://opencode.ai/docs/skills/) |
| GitHub Copilot in VS Code | `.github/skills`, `.claude/skills`, `.agents/skills`; `/name` | Scope is this editor client, not every Copilot product or SDK. | [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills) |
| Kimi Code CLI | `.kimi-code/skills`, `.agents/skills`; `/skill:name` | Distinct from Kimi models. Current and older Kimi CLI documentation differ; check the installed version rather than mixing commands. | [Current Kimi Code](https://moonshotai.github.io/kimi-code/en/customization/skills), [older Kimi CLI](https://moonshotai.github.io/kimi-cli/en/customization/skills.html) |
| Qwen Code (Alibaba/Qwen) | `.qwen/skills`, `.agents/skills`; `/name`; `/skills` manages the panel | Distinct from Qwen models/API. Check name precedence and extension prefixes. | [Qwen Code skills](https://qwenlm.github.io/qwen-code-docs/en/users/features/skills/) |
| Gemini CLI | `.gemini/skills` and `.agents/skills`; `/skills` manages skills | Verify actual activation mechanism, precedence and tool approval in the installed CLI; not every Gemini surface. | [Gemini CLI skills](https://geminicli.com/docs/cli/using-agent-skills/) |
| Hermes Agent | `~/.hermes/skills`; `/name`, `skill_view` | Direct discovery of this checkout's `.agents` was not established. Future exposure must include the complete bundle without divergent copies. | [Hermes skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills) |
| MiMoCode (Xiaomi) | `.mimocode/skills`, `.agents/skills`; `/name` | A concrete harness, distinct from MiMo models. Verify precedence, available tools and execution policy. | [MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code#builtin-skills) |
| DeepSeek Harness (`dsh`) | `.dsh/skills` before `.agents/skills`; `skill({name})` | Concrete harness/SDK, not the model API. Developer preview with breaking changes: no stable compatibility claim. | [Skills subsystem](https://deepseek-harness.github.io/deepseek-harness/en/reference/subsystems/skills), [project README](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.md) |

Meta/Llama's [model repository](https://github.com/meta-llama/llama-models) does not itself establish a specific client loader for these skills. The same distinction applies to an arbitrary model API from Kimi, Google, Xiaomi, DeepSeek or Alibaba, even where a separately named harness above supports the format. Manual provision of instructions or an SDK loader is a possible adaptation, not native discovery demonstrated here.

The name **SpaceXAI** was not resolved to a specific product by the consulted sources. It is not silently mapped to xAI, Grok or SpaceX. Compatibility remains unknown until the intended product is identified.

## Capability checklist before reuse

| Capability | Functional / structural / oracle | Mutation / HTTP lifecycle |
| --- | --- | --- |
| Files and context | Read the actual skill, project profile, contracts, fixtures and current tests; supply measured coverage for structural selection | Also obtain the exact snapshot/operator or launcher/health contract |
| Execution | Optional for design-only reviews; installed Python/Pytest and project dependencies for execution | Required bounded subprocess execution, owned handles and cleanup |
| Additional dependency | Structural measurement uses installed Coverage.py; oracle review needs no specialized analyzer | Supplied mutation needs no engine; HTTP example uses the project's installed Uvicorn/HTTPX/SQLAlchemy |
| Writes | Only authorized test/evidence destinations | Exclusive disposable copies or synthetic storage; never the user's application database |
| Shell and paths | Adapt interpreter, environment-variable syntax and quoting to CMD/PowerShell/POSIX | Verify loopback, process stop and file/port release semantics on that OS |
| Authority | Instructions and metadata do not grant access | The service/executor must enforce permissions and limits independently of the model |

For a new client, first verify format support, installed version and loader policy; then explicitly load the same version and perform one bounded task with the required tools. Record actual read, commands, results and cleanup. Keep source and distributed hashes aligned. A future authorized link/import/package can expose the canonical bundle; this change creates none and does not install other clients or alter global directories.

When distributing a skill independently, retain its license and method attribution and the relevant project licensing material. External URLs are attribution/optional reading; essential instructions remain local. Locally stored skills do not make remote model inference offline. Written guardrails do not demonstrate sandbox enforcement.

## Source limitations

The Codex source URL redirects to ChatGPT Learn. The canonical Claude Platform [best-practices page](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) timed out during direct retrieval; an officially indexed variant was readable. No configuration workaround was applied. These recommendations favor concise instructions, relative resources and evaluation by use; they are not additional format requirements or authorization for wider experiments.

No additional client, SDK adapter, account, credential, tool or service was installed. The [testing guide](testing.md) distinguishes the current evaluation from historical results and records the limits of the local checks.
