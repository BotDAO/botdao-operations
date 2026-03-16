# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, **do not open a public GitHub Issue**. Instead, please report it privately:

1. Use [GitHub's private vulnerability reporting](https://github.com/BotDAO/botdao-operations/security/advisories/new)
2. Or email: **security@botdao.ai**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge reports within 48 hours and aim to resolve critical issues within 7 days.

## Scope

The following are in scope:
- This repository (`botdao-operations`)
- GitHub Actions workflows and their configurations
- Agent configurations and operational logic
- Smart contract interactions (when live)

## Out of Scope

- Third-party services (Bybit, Twitter/X, DeFiLlama)
- Social engineering attacks against team members
- Denial of service attacks

## Security Practices

- **Secrets**: All API keys and tokens are stored in GitHub Actions Secrets, never committed to the repository
- **Workflow inputs**: User-provided inputs are passed via environment variables, not interpolated directly into shell commands
- **Human review**: All content passes through a PR review gate before publishing
- **Treasury**: On-chain spending limits are enforced at the smart contract level, independent of agent code
