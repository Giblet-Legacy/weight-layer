# Forge Stack Context — P10 Weight

CLAUDE.md — Context briefing for AI assistants working in this repository.

## The Immutable Rule
Never rewrite a primitive. Add a layer.

## Dual-Device Workflow
We build on an S24 (Termux) and a laptop (VS Code). State is confirmed, never assumed. Always use LF line endings. Commit messages must be clear. We use the Good/Bad/Ugly CHANGELOG format (latest at top).

## Header Discipline
Every file MUST have a top header paragraph explaining its function.
Every function MUST have a numbered header.

## P10 Architecture Specifics
- Pure math layer. No file I/O, no database, no crypto.
- Implements the Leighton Weight decay formula exactly.
- Neutral attractor: lambda drifts to 1.00, never zero.
- k is the decay constant. It is never called lambda.
- The tooling MUST refuse to run without an explicit k.
