# AI Agent Guidelines

This file contains instructions and guidelines for AI agents working on this repository.

## 🔒 Security Best Practices

**Never commit sensitive information to this repository:**

- API keys, tokens, or credentials
- Personal access tokens (PATs)
- Database connection strings with passwords
- Environment-specific configuration values

**For MCP configuration files (`mcp.json`):**

- Use placeholder values like `"YOUR_API_KEY_HERE"` or `"${API_KEY}"`
- Reference environment variables for sensitive data
- Include documentation about required environment variables

## 📋 Repository Guidelines

### Purpose

This repository is one of several for Microsoft Ignite 2025 sessions and should:

- Provide a consistent structure for all Ignite content repositories
- Include proper documentation for the customer
- Support MkDocs documentation generation
- Enable Learn MCP (Model Context Protocol) server integration

### Consistent Experience

- Maintain the existing folder structure (`docs/`, `src/`, `lab/`, etc.)
- Don't remove placeholder folders unless explicitly instructed
- Keep the banner image and branding consistent
- Ensure all links use proper campaign codes when referencing Learn content
- SUPPORT.md should be updated with support information.
- All readme files in the repo should have updates
- All subfolder names under /docs should be reviewed for mkdocs compatibility
- Unused subfolders (e.g. that only have a README file in them) should be cleaned up before the repo is released.
- No large binary files like powerpoints or videos should be added to the repo.

### What NOT to modify without permission

- License files (`LICENSE`, `CODE_OF_CONDUCT.md`)
- Security files (`SECURITY.md`)
- GitHub workflow files in `.github/` directory

## 🔧 Troubleshooting

### `Azure CLI not found on path` in notebooks

The `AzureCliCredential` in the Part 5 notebook may fail with `CredentialUnavailableError: Azure CLI not found on path` if the Jupyter kernel can't find the `az` binary.

**Cause:** On Apple Silicon Macs, Homebrew typically installs `az` to `/opt/homebrew/bin/az`. `AzureCliCredential` resolves `az` via the process `PATH`, so this error usually means the Jupyter/VS Code kernel's `PATH` does not include the directory where `az` is installed (for example, `/opt/homebrew/bin`), even though `az` works in your interactive terminal.

**Fix:** Ensure `az` is on the kernel `PATH`:

1. In a regular terminal, verify that `az` is installed and note its location:

   ```bash
   which az
   ```

2. In the notebook (or the integrated terminal inside VS Code using the same environment as the kernel), check the `PATH`:

   ```bash
   echo $PATH
   # or in a Python cell:
   import os
   os.environ["PATH"]
   ```

3. Make sure the directory from `which az` (for example, `/opt/homebrew/bin`) appears in the kernel `PATH`. Common ways to fix this include:

   - Starting VS Code from a terminal session where `which az` succeeds:

     ```bash
     code .
     ```

   - Updating your shell profile (e.g., `~/.zshrc` or `~/.bash_profile`) so that `/opt/homebrew/bin` is added to `PATH` for login and GUI sessions.

**Alternative (advanced):** If you've migrated from Intel Homebrew, you might still have `/usr/local/bin/az` as a stale symlink from an old installation. You can inspect and, if necessary, repair it:

```bash
ls -l /usr/local/bin/az
```

If this shows a symlink pointing to a non‑existent location (for example, a missing Cellar directory), you can recreate it to point to the current Homebrew install:

```bash
sudo rm /usr/local/bin/az
sudo ln -s /opt/homebrew/bin/az /usr/local/bin/az
```
