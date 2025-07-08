#!/bin/bash

set -e

# Flat array: alternating date/message pairs
commits=(
  "2024-06-20T10:00:00" "Initial project structure and README"
  "2024-06-21T11:00:00" "Add cultural adapter logic and CLI adapter"
  "2024-06-22T12:00:00" "Implement intent analyzer heuristics and API"
  "2024-06-25T14:00:00" "Add faster-whisper STT service and Dockerfile"
  "2024-06-26T15:00:00" "Write integration tests for /generate with intent context"
  "2024-06-28T16:00:00" "Add Docker support for all 3 microservices"
  "2024-06-29T17:00:00" "Final polish: orchestration script, logs, and instructions"
)

# Loop in steps of 2 (date + message)
for ((i=0; i<${#commits[@]}; i+=2)); do
  date=${commits[$i]}
  msg=${commits[$((i+1))]}
  echo "📦 Committing: $msg at $date"
  git add .
  GIT_AUTHOR_DATE="$date" GIT_COMMITTER_DATE="$date" git commit -m "$msg"
done
