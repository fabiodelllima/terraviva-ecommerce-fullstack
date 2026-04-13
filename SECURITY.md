# Security Policy

## Supported Versions

This project is in active development. Security updates are applied only to the latest release on the `main` branch.

| Version  | Supported |
| -------- | --------- |
| `main`   | Yes       |
| < latest | No        |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it privately. **Do not open public GitHub issues for security vulnerabilities.**

### Preferred channel: GitHub Private Vulnerability Reporting

Use the [Report a vulnerability](https://github.com/fabiodelllima/terraviva-ecommerce-fullstack/security/advisories/new) button on the repository's Security tab. This creates a private advisory visible only to maintainers.

### Alternative channel

If you cannot use GitHub's private reporting, contact the maintainer directly via the email listed on the [maintainer's GitHub profile](https://github.com/fabiodelllima).

## What to Expect

- **Acknowledgment**: within 72 hours of report
- **Initial assessment**: within 7 days, including severity classification (CVSS v3.1)
- **Resolution timeline**: communicated after assessment, based on severity
  - Critical (CVSS 9.0+): patch within 7 days
  - High (CVSS 7.0-8.9): patch within 30 days
  - Medium/Low: patch in next scheduled release
- **Disclosure**: coordinated with reporter; credit given in advisory unless anonymity is requested

## Scope

In scope:
- Source code under `terraviva/frontend/` and `terraviva/backend/`
- CI/CD configuration under `.github/workflows/`
- Dependency management configuration

Out of scope:
- Third-party services (Vercel, hosted databases) — report to respective providers
- Vulnerabilities in dependencies already tracked by Dependabot
- Issues requiring physical access or social engineering

## Security Practices

This project employs:
- Automated dependency scanning via Dependabot (configured in `.github/dependabot.yml`)
- Mandatory CI checks (lint, test, build) on all pull requests
