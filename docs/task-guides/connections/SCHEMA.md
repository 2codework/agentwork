# Frontend contract — task-first-connections/1.2

Input: `connections.json` (UTF-8). r1/r2 preserved; r3 is the editorial replacement candidate.

Top-level: `schema_version`, `id`, `title`, `checked_on`, `verification_scope`, `license_status`, `routes[]`, `chooser`, `sources[]`, `known_gaps[]`.

Route IDs (unchanged): `no-extra-tool`, `official-docs-mcp`, `repeatable-office-skill`.

All routes: `id`, `title`, `audience`, `outcome`, `level`, `product`, `connection`, `accounts_cost`, `minimum_access`, `start_url`, `start_label`, `onboarding_steps[]`, `steps[]`, `prompt`, `config` (string or null), `test_input`, `reference_output`, `expected_observations[]`, `recovery[{symptom,action}]`, `disconnect`, `platform_notes[]`, `source_ids[]`.

Conditional fields: no-extra-tool has `followup_prompt`, `followup_prompt_label`, `file_prompt`, `file_correction_prompt`; official-docs-mcp has `commands`, `onboarding_commands`; repeatable-office-skill has `creator_prompt`, `config_filename`, `disable_config`, `disable_path_note`, `windows_disable_config`, `onboarding_commands`.

`chooser`: `title`, `cards[{question,answer,example,route_id|null}]`, `before_connect[]`, `plugin_note`, `not_promises[]`, `source_ids[]`.

`sources[]`: `id`, `title`, `url`, `checked_on`, `authority`, `supports`, `verification`.

Render order: outcome → product/start link → first-time onboarding → accounts/cost/privacy/access → steps → copyable prompt/config → expected observations + reference answer → recovery/disconnect. Keep full configuration and prompts copyable. Show source audit and `verification_scope` in secondary expandable metadata, not the learner opening. Use one quiet label: “自编虚构样例；验收结果供对照，不代表已替你实跑。”
