#!/bin/sh

main() {
  echo "Saving CSS file..." >&2

  __css_path="./sql/2_query/explain.css"
  curl --fail --silent --show-error https://explain.tensor.ru/css/explain.css > "${__css_path}" || return "$?"

  # Remove borders under links (they are not links anymore anyway)
  sed -Ei 's/^( *border-bottom *:).*$/\1 0px\;/' "${__css_path}" || return "$?"

  # Change Font
  sed -Ei "s/^( *font-family *:).*\$/\\1 'Fira Code', 'Ubuntu Mono', 'Lucida Console', monospace\\;/" "${__css_path}" || return "$?"

  # Fix errors
  sed -Ei 's/nowrap\;nodes_ids$/nowrap\;/g' "${__css_path}" || return "$?"
  sed -Ei 's/align-items:top\;$/align-items:start\;/g' "${__css_path}" || return "$?"

  # Fix warnings
  sed -Ei 's/([ :]0)px/\1/g' "${__css_path}" || return "$?"
  sed -Ei '/font-size: inherit\;/d' "${__css_path}" || return "$?"
  sed -Ei '/font-size: 14px\;/d' "${__css_path}" || return "$?"

  echo "Saving CSS file: success!" >&2
}

main "${@}" || exit "$?"
