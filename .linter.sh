#!/bin/bash
cd /tmp/kavia/workspace/code-generation/fastusermanage-552733-deb22aa4/fastuser_manage
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

