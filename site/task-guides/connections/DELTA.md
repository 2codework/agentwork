# r2 → r3 minimal editorial changes

- Added `followup_prompt_label`: the old example-specific correction is explicitly only for fictional L1–L5.
- Added `file_correction_prompt`: generic real-attachment correction with source checking; no assumed example facts.
- Added `disable_path_note` and `windows_disable_config`: valid TOML forward-slash Windows absolute-path example and instruction to replace with actual path.
- Schema 1.2 adds only those four route fields. Source ledger, source facts, account/permission scope, prompts/configuration already present in r2 otherwise preserved.
- No product runtime performed. r1/r2 unchanged.
