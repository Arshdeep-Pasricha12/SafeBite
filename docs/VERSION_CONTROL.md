# SafeBite — Version Control & Git Strategy

**Version:** 1.0.0  
**Repository Branching Standard:** GitFlow / GitHub Flow Variant  

---

## 1. Branching Strategy

SafeBite uses a structured branching taxonomy to ensure that production stability is protected while allowing rapid feature iteration and verified defect remediation.

```
main (Production Ready / Release Baseline)
  │
  ├── feature/assessment-engine (Scoring logic & explainability)
  ├── feature/data-provenance    (FSSAI / NYC OpenData ingestion)
  ├── feature/browser-extension  (Chrome Manifest V3)
  ├── fix/bcrypt-auth-mismatch   (Resolved AUD-001)
  └── fix/database-path-fallback (Resolved AUD-002)
```

### Branch Definitions:
- **`main`:** The protected production baseline. Every commit on `main` must pass all 23 automated tests and build cleanly without compiler or linter errors.
- **`feature/<name>`:** Dedicated branches for developing discrete user capabilities (e.g. `feature/extension-matching`). Merged via pull requests after code review.
- **`fix/<defect-id>`:** Targeted branches addressing audited defects or regressions (e.g. `fix/auth-passwords`).
- **`docs/<topic>`:** Documentation and evidence updates.

---

## 2. Commit Message Conventions

SafeBite enforces the **Conventional Commits** standard (`type(scope): description`):

| Type | Purpose | Example |
|---|---|---|
| `feat` | Introduces a new system feature or endpoint | `feat(assessment): implement repeat violation 1.5x multiplier` |
| `fix` | Resolves a software defect or bug | `fix(security): resolve bcrypt password hash verification failure` |
| `docs` | Documentation and specification updates | `docs(readme): add consolidated evidence dossier links` |
| `test` | Adding or updating unit, integration, or regression tests | `test(matching): add fuzzy search integration test cases` |
| `refactor` | Code restructuring without changing external behavior | `refactor(config): replace hardcoded D drive path with dynamic resolution` |
| `chore` | Dependency maintenance, build tooling, or config updates | `chore(deps): upgrade reportlab and selenium for verification` |

---

## 3. Pull Request & Review Workflow

1. **Branch Creation:** Create a branch from `main` with a descriptive name.
2. **Local Pre-Commit Verification:** Run `pytest -v` and `npm run build` locally. Never push code that breaks tests.
3. **Pull Request Submission:** Open a PR targeting `main` containing a clear description of changes, affected components, and test evidence.
4. **Mandatory Review Gates:**
   - 100% automated test pass (no test regressions).
   - Zero committed secrets (`.env`, private keys).
   - Clean linting and build validation.
5. **Merge Policy:** Squash and merge to maintain a clean linear commit history on `main`.

---

## 4. Rollback & Disaster Recovery Procedures

If a critical defect bypasses staging into `main`:
1. **Immediate Revert:**
   ```bash
   git revert -m 1 <commit-hash>
   git push origin main
   ```
2. **Database Schema Rollback:**
   - If a migration caused database corruption, restore the pre-migration snapshot from `database/safebite.db.backup`.
3. **Hotfix Branch:** Create a `fix/hotfix-<issue>` branch to isolate and correct the issue before re-deploying.

---

## 5. Excluded Files (`.gitignore` Rules)

To prevent repository bloat and credential leaks, the following patterns are strictly excluded:

```gitignore
# Python & Virtual Environments
__pycache__/
*.py[cod]
*$py.class
venv/
.pytest_cache/

# Node & Frontend Build
frontend/node_modules/
frontend/dist/
*.log

# Environment Secrets & Local Config
.env
.env.local
*.pem
*.key

# Temporary Test Artifacts & OS Files
.DS_Store
Thumbs.db
```
