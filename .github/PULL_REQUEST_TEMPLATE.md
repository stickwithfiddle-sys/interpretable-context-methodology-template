## Summary

What changed?

## Type

- [ ] Feature
- [ ] Fix
- [ ] Documentation
- [ ] Example
- [ ] Release

## Checklist

- [ ] README or docs updated if behavior changed
- [ ] Example workspace updated if useful for beginners
- [ ] `CHANGELOG.md` updated
- [ ] Version updated if this is a release PR
- [ ] `python -m pytest`
- [ ] `python tools/check_packaged_assets.py`
- [ ] `python tools/check_docs_site.py`
- [ ] `python -m icm validate templates/icm-workspace --strict`
- [ ] `python -m icm validate examples/completed-content-plan --strict`
- [ ] `python -m icm validate examples/completed-research-brief --strict`
- [ ] `python -m icm init /tmp/icm-existing-smoke --name "Existing Smoke"`
- [ ] `python -m icm status examples/completed-content-plan`
- [ ] `python -m icm review stages/01_discovery --workspace examples/completed-content-plan`
- [ ] `python -m icm review stages/01_discovery --workspace examples/completed-research-brief`
- [ ] `python -m icm doctor examples/completed-content-plan --strict`
- [ ] `python -m icm doctor examples/completed-research-brief --strict`

## Notes For Reviewers

Anything risky, unresolved, or worth checking closely?
