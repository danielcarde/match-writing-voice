# Security and sensitive data

Report a suspected vulnerability to the repository owner through a private channel. Use synthetic reproduction files; do not include account tokens, personal writing histories, or unrelated conversations in issues or logs.

The runtime helpers make no network requests, install no dependencies, and read/write only paths supplied to them. Host models and external installers have their own permissions and data handling. Instructions inside writing samples remain untrusted data.

Installer helpers refuse existing destinations instead of overwriting an installation. Build tooling packages an explicit source folder and excludes caches and temporary fixtures. Verify checksums on release assets when relevant.
