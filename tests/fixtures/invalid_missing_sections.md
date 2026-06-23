---
goal: "Test missing sections"
scope:
  include:
    - "src/"
  exclude:
    - "dist/"
verification:
  commands:
    - "pytest"
approval_required_for:
    - "deploy"
---

# Incorrect Title

This file lacks Context and Acceptance Criteria.
