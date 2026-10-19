# Phase: preflight

## Objective
Complete, valid inputs and a machine able to run the whole flow.

## Determine
- Archive: the `.wpress` files in the working folder.
  - None: ask the user for a reachable URL, download it into the working folder in a resumable way, then validate it with the reader (`info` must exit 0).
  - More than one: ask which one to use.
- Archive metadata from the reader `info`: site URL, WordPress, PHP and database versions, table prefix, theme, active plugins, encryption, entry count, content size.
- Encryption: when `info` reports it, ask the user for the All-in-One WP Migration password.
- Unlimited Extension: a zip in the working folder whose plugin folder is `all-in-one-wp-migration-unlimited-extension`.
  - Missing: download it into the working folder from
    `https://nextcloud.joinindots.com/index.php/s/PJxrSyW2gSwqDxZ/download/all-in-one-wp-migration-unlimited-extension.zip`
    and check that it is a zip containing that plugin folder.
  - Download failed or wrong content: ask the user for the zip or for its location.
- Machine: container runtime installed, running and reachable from the session's shell (a command sandbox can block it); Python 3 on the shell path; free space where the container runtime stores its volumes ≥ archive content size + database size + margin for media processing; a free local port.
- Live site: whether the site URL from the metadata answers.

## Decide
- A missing requirement stops the flow with a precise message: what is missing and how to provide it.
- Container commands blocked by a command sandbox: stop and tell the user which container commands must be allowed to run outside the sandbox.
- A cloud or remote session without a local container runtime cannot run the flow: say so and stop.
- More archives than one: the user chooses; never pick one yourself.
- Live site unreachable: continue, and record that every comparison will use the local baseline only.
- Inputs downloaded by the flow are temporary unless the user wants to keep them; inputs provided by the user stay where they are.

## Risks to check
- A partially downloaded archive can have a plausible size and still be truncated: validation is the reader, not the size.
- The container runtime may store volumes on a different disk or virtual disk than the working folder: measure free space there.
- The archive content size reported by `info` is the space the import needs, before the database grows.

## Exit criteria
Reader `info` succeeds on the chosen archive; a valid add-on zip is available; the container runtime runs; space and port are available.

## Report
Create the report file in the working folder, in the user's language, named after the site. First section: source archive (name, size, date), site URL, production versions, inputs obtained by the flow, requirements met.
