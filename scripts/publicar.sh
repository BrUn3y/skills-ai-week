#!/usr/bin/env bash
# Create the requested personal repository and deploy the reviewed static site.
set -euo pipefail
cd "$(dirname "$0")/.."

github_login=$(gh api user --jq .login)
repository="$github_login/skills-ai-week"

if [ -n "$(git status --porcelain)" ]; then
  printf '%s\n' 'Hay cambios sin guardar. Revisa y crea un commit antes de publicar.' >&2
  exit 1
fi

if git remote get-url origin >/dev/null 2>&1; then
  printf '%s\n' 'Ya existe un remoto origin. Revisa su destino antes de crear otro repositorio.' >&2
  exit 1
fi

gh repo create "$repository" --public \
  --description 'Guía visual en español sobre skills de Claude Code, Codex e IBM Bob, creada con Archify.' \
  --source . --remote origin --push
gh api --method POST "repos/$repository/pages" -f build_type=workflow >/dev/null
gh workflow run pages.yml --repo "$repository"
printf 'Repositorio: https://github.com/%s\n' "$repository"
printf 'Pages se está desplegando. Consulta: gh run list --repo %s\n' "$repository"
