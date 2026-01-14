# toolbox security

Security and privacy tools.

## Subcommands

- [toolbox security audit](Command-security-audit) — Audit a file or directory for PII (Personally Identifiable Information).
- [toolbox security hardware-setup](Command-security-hardware-setup) — Register a FIDO2/YubiKey for hardware-backed security.
- [toolbox security mount](Command-security-mount) — Mount an encrypted vault as a temporary virtual drive.
- [toolbox security quantum-decrypt](Command-security-quantum-decrypt) — Decrypt a .qvault file using hardware-bound keys.
- [toolbox security quantum-encrypt](Command-security-quantum-encrypt) — Encrypt a file using Quantum-Resistant Hybrid AES-256-GCM.
- [toolbox security steg-extract](Command-security-steg-extract) — Extract hidden data from an image.
- [toolbox security steg-hide](Command-security-steg-hide) — Hide a file inside an image using LSB steganography (optionally encrypted).
- [toolbox security vault-announce](Command-security-vault-announce) — Announce a vault to the local network for discovery.
- [toolbox security vault-decrypt](Command-security-vault-decrypt) — Decrypt a .vault file.
- [toolbox security vault-discover](Command-security-vault-discover) — Discover shared vaults on the local network.
- [toolbox security vault-encrypt](Command-security-vault-encrypt) — Encrypt a file into a secure vault (.vault).
- [toolbox security verify](Command-security-verify) — Hardened Security Audit: Verify integrity of all security subsystems.

## Help

```text
Usage: toolbox security [OPTIONS] COMMAND [ARGS]...

  Security and privacy tools.

Options:
  --help  Show this message and exit.

Commands:
  audit            Audit a file or directory...
  hardware-setup   Register a FIDO2/YubiKey for...
  mount            Mount an encrypted vault as...
  quantum-decrypt  Decrypt a .qvault file using...
  quantum-encrypt  Encrypt a file using...
  steg-extract     Extract hidden data from an...
  steg-hide        Hide a file inside an image...
  vault-announce   Announce a vault to the...
  vault-decrypt    Decrypt a .vault file.
  vault-discover   Discover shared vaults on...
  vault-encrypt    Encrypt a file into a secure...
  verify           Hardened Security Audit:...
```

Back: [Command Index](Command-Index)
