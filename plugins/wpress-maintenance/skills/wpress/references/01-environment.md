# Phase: environment

## Objective
A local WordPress in containers that matches production, is cut off from the outside world, and is ready for the import.

## Determine
- Container images available for the WordPress, PHP and database versions read from the archive, for this machine's CPU architecture.
- What the site's code expects beyond versions: PHP extensions and loaders for encoded code, services used by drop-ins (object cache, database), the production web server family (from the live response headers). A drop-in whose service cannot be provided is disabled locally and reported, not deleted.
- A free local port.
- The path inside the WordPress container from which the import tool reads archives.

## Decide
- Exact production versions when available; otherwise the nearest compatible ones (same PHP minor line, same database family and major line), recorded as a deviation.
- PHP limits large enough for the import and for media processing: upload size, request size, memory, execution time.
- Three services: web (WordPress), database, command line (sharing the WordPress files volume and the network). Environment files in the working folder; site files and database in named volumes; local-only database credentials; names that do not collide with other projects on the machine.
- Mount the original archive read-only at the path the import tool reads from; never copy it.
- Cut-off from the outside world at environment level (principle 3): mail disabled or captured for every transport, scheduled tasks not self-triggered, outbound requests from the site's code blocked except to the official sources the flow itself needs; verify the cut before the first request to the restored site.

## Risks to check
- The command-line container has its own PHP memory limit; plugins loaded on the command line can exhaust it.
- Database commands from the command-line container can fail on TLS negotiation against a local database without TLS: query the database container directly or configure the client for local use.
- A network export needs the matching environment kind and local domain mapping (preflight).

## Exit criteria
WordPress answers on the local port; the command line reaches the database; the cut-off is verified.

## Report
Environment: images and versions used, deviations from production, extensions and services provided, cut-off in place, local URL.
