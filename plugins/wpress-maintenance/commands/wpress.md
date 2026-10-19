---
description: Restore, secure, clean, optimize and verify a WordPress site from a .wpress backup in the current folder
argument-hint: "[phase|resume]"
---

Use the `wpress-maintenance` skill on the current working folder.

Arguments: `$ARGUMENTS`
- Empty: run the full flow from the `preflight` phase.
- `resume`: read the report in the working folder and the running local environment, then continue from the first phase without a section in the report.
- A phase id (`preflight`, `environment`, `import`, `baseline`, `audit`, `remediation`, `cleanup`, `media`, `seo`, `accessibility`, `performance`, `verification`, `delivery`): run only that phase, with the environment and report already present.

Talk to the user and write the report in the user's language.
