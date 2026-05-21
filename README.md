# Antimicrobial activity prediction against Helicobacter pylori from public ChEMBL data

Bioactivity prediction of growth inhibition in Helicobacter pylori, trained as binary (active/inactive) classifiers from publicly available data in ChEMBL. Independent models are trained on multiple bioactivity datasets, corresponding to dose-response (MIC) assays, among others. A ranking score is provided for each model alongside a combined consensus score.

This model was incorporated on 2026-05-19.


## Information
### Identifiers
- **Ersilia Identifier:** `eos9eyo`
- **Slug:** `antimicrobial-activity-hpylori`

### Domain
- **Task:** `Annotation`
- **Subtask:** `Activity prediction`
- **Biomedical Area:** `Peptic ulcer disease`
- **Target Organism:** `Helicobacter pylori`
- **Tags:** `Gram-negative bacteria`, `Antimicrobial activity`, `ChEMBL`

### Input
- **Input:** `Compound`
- **Input Dimension:** `1`

### Output
- **Output Dimension:** `4`
- **Output Consistency:** `Fixed`
- **Interpretation:** Probability of antimicrobial activity against Helicobacter pylori from 3 ChEMBL-trained sub-models, plus a quality-weighted consensus score.

Below are the **Output Columns** of the model:
| Name | Type | Direction | Description |
|------|------|-----------|-------------|
| consensus_score | float | high | Tanh-transformed quality-weighted consensus probability across the 3 sub-models. Recommended threshold: 0.775. |
| merged_mic_decoys | float | high | Probability from sub-model trained on MIC measurements merged across 4 ChEMBL assays (cutoff 10 uM; n=1070 incl. decoys). Recommended threshold: 0.874. |
| general_mic | float | high | Probability from sub-model trained on MIC measurements aggregated across 311 ChEMBL assays (cutoff 10 uM; n=792). Recommended threshold: 0.505. |
| general_iz | float | high | Probability from sub-model trained on inhibition zone diameter measurements aggregated across 67 ChEMBL assays (cutoff 20 mm; n=120). Recommended threshold: 0.636. |


### Source and Deployment
- **Source:** `Local`
- **Source Type:** `Internal`
- **S3 Storage**: [https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9eyo.zip](https://ersilia-models-zipped.s3.eu-central-1.amazonaws.com/eos9eyo.zip)

### Resource Consumption
- **Model Size (Mb):** `18`
- **Environment Size (Mb):** `1888`


### References
- **Source Code**: [https://github.com/ersilia-os/chembl-antimicrobial-models](https://github.com/ersilia-os/chembl-antimicrobial-models)
- **Publication**: [https://github.com/ersilia-os/chembl-antimicrobial-models](https://github.com/ersilia-os/chembl-antimicrobial-models)
- **Publication Type:** `Other`
- **Publication Year:** `2026`
- **Ersilia Contributor:** [arnaucoma24](https://github.com/arnaucoma24)

### License
This package is licensed under a [GPL-3.0](https://github.com/ersilia-os/ersilia/blob/master/LICENSE) license. The model contained within this package is licensed under a [GPL-3.0-or-later](LICENSE) license.

**Notice**: Ersilia grants access to models _as is_, directly from the original authors, please refer to the original code repository and/or publication if you use the model in your research.


## Use
To use this model locally, you need to have the [Ersilia CLI](https://github.com/ersilia-os/ersilia) installed.
The model can be **fetched** using the following command:
```bash
# fetch model from the Ersilia Model Hub
ersilia fetch eos9eyo
```
Then, you can **serve**, **run** and **close** the model as follows:
```bash
# serve the model
ersilia serve eos9eyo
# generate an example file
ersilia example -n 3 -f my_input.csv
# run the model
ersilia run -i my_input.csv -o my_output.csv
# close the model
ersilia close
```

## About Ersilia
The [Ersilia Open Source Initiative](https://ersilia.io) is a tech non-profit organization fueling sustainable research in the Global South.
Please [cite](https://github.com/ersilia-os/ersilia/blob/master/CITATION.cff) the Ersilia Model Hub if you've found this model to be useful. Always [let us know](https://github.com/ersilia-os/ersilia/issues) if you experience any issues while trying to run it.
If you want to contribute to our mission, consider [donating](https://www.ersilia.io/donate) to Ersilia!
