# Contributing to MimicTTS

Maintained by **[Rajjit Laishram](https://rajjitlaishram.netlify.app)**.

Thank you for your interest in contributing. All contributions are welcome — bug fixes, new features, documentation improvements, and more.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Code Style](#code-style)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/your-username/MimicTTS.git
   cd MimicTTS
   ```

3. **Add the upstream remote** so you can pull in future changes:

   ```bash
   git remote add upstream https://github.com/rajjitlai/MimicTTS.git
   ```

---

## Development Setup

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env config
copy .env.example .env   # Windows
cp .env.example .env     # Linux / macOS
```

Configure `.env` with your `HF_TOKEN` before running any inference scripts.

---

## Branching Strategy

| Branch type | Naming convention | Example |
|---|---|---|
| Bug fix | `fix/<short-description>` | `fix/cuda-device-detection` |
| New feature | `feat/<short-description>` | `feat/batch-processing` |
| Documentation | `docs/<short-description>` | `docs/update-readme` |
| Refactor | `refactor/<short-description>` | `refactor/model-loader` |

Always branch off `main`:

```bash
git checkout main
git pull upstream main
git checkout -b feat/your-feature-name
```

---

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>(<scope>): <short summary>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `chore`, `test`

**Examples:**

```
feat(runner): add multi-output support
fix(model): handle missing CUDA gracefully
docs(readme): update model options table
```

- Keep the summary under 72 characters.
- Use present tense ("add feature" not "added feature").
- Reference issues where applicable: `fix(model): handle OOM error (#42)`.

---

## Pull Request Process

1. Ensure your branch is up to date with `upstream/main`.
2. Open a Pull Request against `main` using the provided PR template.
3. Fill in all sections of the template — do not leave them blank.
4. A maintainer will review within a few days. Please be patient and responsive to feedback.
5. Once approved and all checks pass, your PR will be merged.

---

## Code Style

- Formatted with [black](https://github.com/psf/black). Run `black .` before committing.
- Imports sorted with [isort](https://pycqa.github.io/isort/). Run `isort .` before committing.
- Style checked with [flake8](https://flake8.pycqa.org/). Max line length is 88 (black-compatible).
- Type hints are encouraged but not mandatory.
- All new functions should have a docstring.

Install the tools:

```bash
pip install black isort flake8
```

---

## Reporting Bugs

Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) issue template. Include:

- A clear, descriptive title.
- Steps to reproduce the issue.
- What you expected vs. what actually happened.
- Your environment (OS, Python version, GPU/CPU, CUDA version).

---

## Requesting Features

Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) issue template. Include:

- The problem you are trying to solve.
- Your proposed solution.
- Any alternatives you considered.
