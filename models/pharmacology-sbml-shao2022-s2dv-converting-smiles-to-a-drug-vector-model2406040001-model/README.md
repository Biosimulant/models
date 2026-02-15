# Shao2022 - S2DV: converting SMILES to a drug vector for predicting the activity of anti-HBV small molecules

**Source**: [biomodels_ebi](https://www.ebi.ac.uk/biomodels/MODEL2406040001)
**Standard**: sbml
**Authors**: Jinsong Shao; Qineng Gong; Zeyu Yin; Wenjie Pan; Sanjeevi Pandiyan

## Description

The model uses Word2Vec, a natural language processing technique to represent SMILES strings. The model was trained on over 4000 small molecules with associated experimental HBV inhibition data (IC50)


## Usage

This model was auto-generated from the biomodels_ebi repository.

```yaml
# In a space.yaml wiring file:
models:
  - repo: Biosimulant/models
    alias: model
    manifest_path: models/pharmacology-sbml-shao2022-s2dv-converting-smiles-to-a-drug-vector-model2406040001-model/model.yaml
```

## Tags

systemsbiology, sbml, biomodels_ebi, auto-generated, biomodels-ebi, non_curated
