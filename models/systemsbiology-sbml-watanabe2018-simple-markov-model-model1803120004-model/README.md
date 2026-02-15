# Watanabe2018_Simple markov model

**Source**: [biomodels_ebi](https://www.ebi.ac.uk/biomodels/MODEL1803120004)
**Standard**: sbml
**Authors**: Leandro Watanabe; Jacob Barhak; Chris Myers

## Description

Simple Markov model.There are 3 disease states: Healthy, Sick, and Dead, where the Dead state is terminal.The yearly transition probabilities are:Healthy to Dead: 0.01; Healthy to Sick: 0.2 for Male a


## Usage

This model was auto-generated from the biomodels_ebi repository.

```yaml
# In a space.yaml wiring file:
models:
  - repo: Biosimulant/models
    alias: model
    manifest_path: models/systemsbiology-sbml-watanabe2018-simple-markov-model-model1803120004-model/model.yaml
```

## Tags

systemsbiology, sbml, biomodels_ebi, auto-generated, biomodels-ebi, non_curated
