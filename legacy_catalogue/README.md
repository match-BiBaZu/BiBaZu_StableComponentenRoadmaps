# Historical roadmap catalogue

`originals/` contains the nine previously bundled Big Boi roadmap sets, with their
original bytes, IDs and hashes. They are separate from this repository's current grouped
component folders and are not substituted for grouped targets.

`path_migrations.json` records exact former file paths, relative destinations and SHA-256
hashes. Both GUIs resolve only exact entries with matching hashes. Existing external paths
are left as selected; numerical pose IDs are never used to guess a replacement.

The additive `.consumer.json` sidecars are generated offline by this repository and bound
to each original JSON/YAML file's hash. They supply legacy calibration choices and routes
without altering saved roadmap hashes. Regenerate with the documented
`upgrade_consumer_exports --legacy-root` command after a deliberate source change.
