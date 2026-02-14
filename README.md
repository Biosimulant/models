# biomodels

Public curated monorepo for `bsim` model packs and composed spaces.

## Layout
- `models/<model-slug>/`: one model package per folder, each with `model.yaml`.
- `spaces/<space-slug>/`: composed spaces with `space.yaml`.
- `libs/`: shared helper code for curated models.
- `templates/model-pack/`: starter template for new model packs.
- `scripts/`: manifest and entrypoint validation scripts.

## Linking in bsim-platform
- Root manifests can be linked with `manifest_path=model.yaml` or `space.yaml`.
- Subdirectory manifests must be linked with explicit `manifest_path`, for example:
  - `models/hodgkin-huxley/model.yaml`
  - `spaces/ecosystem/space.yaml`

## External Repos
External authors can keep models in independent repositories and link them directly in `bsim-platform`.
This monorepo is curated, not exclusive.

## bsim Install
Model authors should install `bsim` from GitHub:

```bash
pip install "bsim @ git+https://github.com/<org>/bsim.git@<ref>"
```
