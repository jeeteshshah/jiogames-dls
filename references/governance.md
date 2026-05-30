# JioGames DLS Governance

> The DLS is a product, not a shared folder. It has owners, a version, a change process, and a deprecation policy. Changes that skip this process create the drift the DLS exists to prevent.

**Structure**

1. Ownership Model
2. Change Classification
3. RFC Process
4. Versioning
5. CHANGELOG Format
6. Deprecation Policy
7. Release Checklist

---

# 1. Ownership Model

### Roles

| Role | Responsibilities | Approvals required |
|---|---|---|
| **DLS Owner** (2 people) | Final authority on breaking changes, new governance rules, deprecation, releases | 2 owners must approve breaking changes and RFC acceptance |
| **Component Owner** (1 per component) | Owns the contract for their component — states, tokens, radius, sizing, a11y | Approves changes to their component's contract |
| **Platform Lead** (Mobile / Web / TV) | Reviews platform-specific behaviour, breakpoints, focus rules | Approves platform section changes affecting their platform |
| **Contributor** | Anyone proposing a change | Follows RFC process; cannot self-merge breaking changes |

### Assignment

Every contracted component (component-contracts.md) has a named Component Owner. Every governance document has a named DLS Owner responsible for keeping it current. Ownership is recorded in the component contract and updated at each release.

### Quorum for breaking changes

A breaking change (see §2) requires:
- Both DLS Owners approving
- Relevant Component Owner approving (if a contract changes)
- Relevant Platform Lead approving (if platform behaviour changes)

---

# 2. Change Classification

Every change to the DLS is one of three types. The type determines what process is required.

### Breaking (Major)

Requires RFC + full owner approval. Blocked from shipping until approved.

Examples:
- Token renamed or removed (`--jio` → `--brand-primary`)
- Token value changed (`--bg` from `#06080F` to anything else)
- Component contract changed (radius, sizing, or state recipe altered)
- New rule added to a forbidden list
- Governance doc structure changed in a way that invalidates existing implementations
- `validate.sh` check upgraded from WARN → ERR

### Additive (Minor)

Requires RFC if it introduces a new reusable pattern. Small additions (new token, new component, new doc section) can go through lightweight review.

Examples:
- New token added to `tokens.json`
- New component contracted in component-contracts.md
- New section added to a governance doc
- New `validate.sh` check added (as WARN)
- New stack utility added to `tokens.css`

### Patch

No RFC required. One owner review sufficient.

Examples:
- Typo or wording fix in any doc
- `$description` update in `tokens.json`
- Non-breaking addition to a QA checklist
- Build script bug fix that doesn't change output
- Doc cross-reference updated

---

# 3. RFC Process

RFC = Request for Change. Required for all breaking changes and significant additive changes.

### When an RFC is required

| Change | RFC required |
|---|---|
| Any breaking change (§2) | Yes — always |
| New token (colour, size, spacing, radius) | Yes |
| New contracted component | Yes |
| New governance rule or forbidden pattern | Yes |
| Existing token value change | Yes |
| Component contract update (any field) | Yes |
| New `validate.sh` check at ERR level | Yes |
| Doc section addition | Lightweight (1 owner approval) |
| Patch fix | No |

### RFC template

File as a document or ticket with:

```
## RFC: [short title]

**Type:** Breaking / Additive
**Affects:** [list of files/components/tokens]
**Author:** [name]
**Date:** [YYYY-MM-DD]

### Problem
What is wrong or missing with the current system?

### Proposal
What specifically changes? Include:
- Token names (before → after)
- Contract fields affected
- Validate.sh impact
- Migration path for existing implementations

### Alternatives considered
What else was tried or rejected and why?

### Impact
- Screens affected: [list or "all"]
- Platforms affected: [Mobile / Web / TV]
- Breaking for existing implementations: [Yes / No]

### Approvals needed
- [ ] DLS Owner 1
- [ ] DLS Owner 2 (required for breaking)
- [ ] Component Owner: [name] (if contract changes)
- [ ] Platform Lead: [name] (if platform behaviour changes)
```

### RFC lifecycle

1. **Draft** — author writes RFC, shares with owners
2. **Review** — owners and affected leads comment, propose changes
3. **Approved** — required approvals collected; author may implement
4. **Implemented** — change merged, CHANGELOG updated, version bumped
5. **Rejected** — documented with reason; can be re-raised with new proposal

---

# 4. Versioning

The DLS uses **semantic versioning**: `MAJOR.MINOR.PATCH`

| Version bump | When |
|---|---|
| **MAJOR** (`2.0.0`) | Any breaking change — token removed/renamed, contract changed, forbidden rule added |
| **MINOR** (`1.1.0`) | Additive change — new token, new component, new governance section |
| **PATCH** (`1.0.1`) | Fix — typo, description, non-breaking build fix |

### Version lives in

- `tokens/tokens.json` → `"$version"` field
- `CHANGELOG.md` → top entry
- Git tag (`v1.0.0`) at each release

### Rules

- Never skip MAJOR for a breaking change to avoid team friction. A skipped MAJOR means teams won't know their implementations may be broken.
- MINOR bumps do not require migration. MAJOR bumps require a migration note in CHANGELOG.
- A release candidate is tagged `v1.1.0-rc.1` before finalising.
- `tokens.json "$version"` must match the git tag at release. `build.py --check` does not verify this — it is a manual release step.

---

# 5. CHANGELOG Format

`CHANGELOG.md` lives at the DLS root. Follow [Keep a Changelog](https://keepachangelog.com/) format.

```markdown
# Changelog

## [Unreleased]

## [1.1.0] — YYYY-MM-DD
### Added
- `--mint` token for secondary brand accent (colour-governance.md §3)
- Tab Bar component contract (component-contracts.md)

### Changed
- `tokens-and-components.md` renamed to "Component Patterns & Token Index"; defers typography/spacing authority to dedicated docs

### Deprecated
- `--cyan` — prefer `--mint` for brand-approved secondary accent usage

### Removed
- (nothing)

### Fixed
- Genre tile radius corrected from `--r8` to `--r5` (matched actual CSS and component-contracts)

### Security
- (nothing)
```

### Change type definitions

| Type | What belongs here |
|---|---|
| **Added** | New tokens, new components, new doc sections, new CI checks |
| **Changed** | Existing token values, contract updates, doc restructures, check level changes |
| **Deprecated** | Tokens or patterns marked for removal in a future MAJOR |
| **Removed** | Tokens, patterns, or doc sections deleted |
| **Fixed** | Bugs, incorrect values, broken cross-references, stale docs |
| **Security** | (Rare for a DLS — would cover auth-related component patterns) |

### Rules

- Every RFC-level change gets a CHANGELOG entry before it ships.
- Patch fixes may be batched into a single entry.
- Entries are written for the **implementer audience** — what do they need to know to update their screens?

---

# 6. Deprecation Policy

Deprecation is a two-phase process. Nothing is removed without a grace period.

### Phase 1 — Deprecated (MINOR bump)

1. Mark the token or pattern as deprecated in `tokens.json` `$description` and in the relevant governance doc.
2. Add a CHANGELOG `Deprecated` entry.
3. `validate.sh` may add a WARN for use of the deprecated item (optional at this phase).
4. The item still works — implementations are not broken.

Example in `tokens.json`:
```json
"cyan": {
  "$value": "#26D6C9",
  "$type": "color",
  "$description": "DEPRECATED — use --mint for brand-approved secondary accent. Will be removed in v2.0.0."
}
```

### Phase 2 — Removed (MAJOR bump)

1. RFC required (breaking change).
2. Remove from `tokens.json` and `build.py`.
3. Regenerate `tokens.css`.
4. Add CHANGELOG `Removed` entry with migration note.
5. `validate.sh` adds an ERR check for any remaining usage of the old token name or value.

### Grace period

Minimum **one MINOR release** between Deprecated and Removed. Teams must have time to migrate before the MAJOR lands.

### What can be deprecated

- Individual tokens (`--cyan`, raw values)
- Component variants (`cta-sm` if TV-safe variant is introduced)
- Gradient recipes (if a new approved recipe replaces an old one)
- Governance rules (if a rule is relaxed or replaced)

### What cannot be deprecated without RFC

- Core brand tokens (`--jio`, `--bg`, `--text`)
- Any token used in more than 3 contracted components
- Any `validate.sh` ERR-level check

---

# 7. Release Checklist

Run before tagging a release:

### Token pipeline
- [ ] `tokens/tokens.json "$version"` updated to new version
- [ ] `python3 tokens/build.py` run — `tokens.css` regenerated
- [ ] `python3 tokens/build.py --check` passes
- [ ] `bash tools/ci.sh` passes with exit 0

### Docs
- [ ] `CHANGELOG.md` updated — `[Unreleased]` section moved to versioned entry with date
- [ ] All affected governance docs updated and cross-references verified
- [ ] Any deprecated items marked in `tokens.json` and relevant doc
- [ ] Component contracts updated for any contract changes

### Approvals
- [ ] All RFC approvals collected for breaking/additive changes in this release
- [ ] Component Owner sign-off for any contract changes
- [ ] Platform Lead sign-off for platform behaviour changes

### Git
- [ ] All changes committed to main/master
- [ ] Git tag created: `git tag v{MAJOR}.{MINOR}.{PATCH}`
- [ ] Tag pushed: `git push origin v{MAJOR}.{MINOR}.{PATCH}`

### Comms
- [ ] Release note shared with implementation teams (CHANGELOG entry is the content)
- [ ] Migration notes called out separately for any MAJOR version bump
