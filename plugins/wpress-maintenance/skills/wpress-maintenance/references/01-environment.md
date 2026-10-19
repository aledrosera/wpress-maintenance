# Phase: environment

## Objective
A local WordPress in containers that matches the production versions and is ready for the import.

## Determine
- Container images available for the WordPress, PHP and database versions read from the archive, for this machine's CPU architecture.
- A free local port.
- The path inside the WordPress container from which the import tool reads archives.

## Decide
- Use the exact production versions when available; otherwise the nearest compatible ones (same PHP minor line, same database family and major line) and record the deviation.
- PHP limits large enough for the import and for later media processing: upload size, request size, memory, execution time.
- Three services: web (WordPress), database, command line (sharing the WordPress files volume and the network).
- Mount the original archive read-only at the path the import tool reads from; never copy it.
- Environment files live in the working folder; site files and database live in named volumes.
- Local-only database credentials.

## Risks to check
- The command-line container has its own PHP memory limit; plugins loaded on the command line can exhaust it.
- Database commands run from the command-line container can fail on TLS negotiation against a local database without TLS: query the database container directly or configure the client for local use.
- Names of containers, volumes and networks must not collide with other projects on the same machine.

## Exit criteria
WordPress answers on the local port and the command line reaches the database.

## Report
Environment: images and versions used, deviations from production, local URL.
