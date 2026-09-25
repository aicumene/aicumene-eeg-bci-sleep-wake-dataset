# AiCumene EEG-BCI Sleep–Wake Dataset

**Alexandra Bernadotte · Ivan Menshikov**  
**AiCumene · 2026**  
**Version:** 1.0  
**Dataset DOI:** `10.5281/zenodo.22923070`

## Overview

The **AiCumene EEG-BCI Sleep–Wake Dataset** has two components: a **public synthetic sleep-EEG benchmark** of **45 synthetic recordings** — produced by per-recording oscillator resynthesis of Sleep-EDF Expanded (Sleep Cassette; PhysioNet) — phase-randomised surrogates preserving each source recording's oscillatory structure — and **40 real AiCumene wearable-EEG recordings** held under controlled access.

Each recording is paired with a synchronized sleep-stage hypnogram.

This Zenodo record is the **canonical public archive** for **all 45 synthetic recordings** (`S0001`–`S0045`).

The **40 real recordings** are not included in the public Zenodo deposit and are available to qualified researchers under controlled access, as described in `DATA_AVAILABILITY.md`.

## Public files

Each public record consists of two files:

```text
S00xx-PSG.edf
S00xx-Hypnogram.edf
```

The expected public filenames are listed in `PUBLIC_DATA_MANIFEST.csv`.

The public EDF / EDF+ files are intentionally **not duplicated in the companion GitHub repository**. Zenodo is the canonical archive for the public signal data.

## Dataset characteristics

- Synthetic benchmark: **45 synthetic recordings**, all released publicly
- Real AiCumene wearable-EEG recordings (controlled access): **40**
- Total signal duration: approximately **1,027 hours**
- Typical recording duration: approximately **21.4–23.5 h**
- Sleep scoring epoch: **30 s**
- File formats: **EDF** (PSG) and **EDF+** (hypnogram)
- Licence: **CC BY-NC 4.0** (synthetic outputs) + **ODC-BY 1.0** (underlying Sleep-EDF source)

The public metadata table is provided as `METADATA.csv`.

## Licensing

The original synthetic outputs, metadata, and documentation are licensed under **CC BY-NC 4.0** to the extent the creators are entitled to license them. Rights in the underlying Sleep-EDF source database remain governed by **ODC-BY 1.0**.

See `LICENSE`.

Controlled-access recordings are governed separately by the Data Use Agreement in the companion dataset repository.

No patent license is granted by access to this dataset.

## Dataset citation

**Bernadotte, A. & Menshikov, I. (2026). AiCumene EEG-BCI Sleep–Wake Dataset (Version 1.0). AiCumene. DOI: 10.5281/zenodo.22923070.**

## Companion dataset repository

Documentation, figures, reproducibility instructions, citation metadata, the controlled-access Data Use Agreement, and patent notice are maintained at:

https://github.com/aicumene/aicumene-eeg-bci-sleep-wake-dataset

## Canonical analysis code

The BOID repository contains the BOID-specific analysis layer, including TLS-ESPRIT pole processing, BOID estimation, oscillator descriptors, topology-based analyses, and article-level statistical workflows:

https://github.com/aicumene/BOID

The upstream MSSA signal-subspace implementation accompanies a separate methodological preprint and repository. The BOID estimator is not duplicated in this dataset repository.

## Reproducibility

The companion GitHub repository provides auxiliary-channel regeneration code in [`resynthesis/`](resynthesis/) (`aux_channels.py`, licensed under PolyForm Noncommercial 1.0.0). The oscillator-resynthesis script that generates the EEG surrogate is released together with the separate MSSA methodological preprint (https://github.com/aicumene/MSSA).

## Associated BOID preprint

**Alexandra Bernadotte, Ivan Menshikov.**  
*Brain Oscillator Intrinsic Dimension marks consciousness, recovery mode, and failed downshifting in coma.*  
2026.

https://research.aicumene.com/papers/boid-coma/

**DOI:** `10.13140/RG.2.2.31610.25288`

## Future peer-reviewed publication

**Alexandra Bernadotte, Ivan Menshikov.**  
*Brain states are organized by regulated oscillator dimensionality.*

A peer-reviewed journal publication describing the regulated-oscillator-dimensionality analysis is in preparation / submission.

**Its final journal citation and DOI should be added to this Zenodo record immediately after publication.**

The full list of associated preprints and peer-reviewed methodological works is provided in [`RELATED_WORKS.md`](RELATED_WORKS.md).

## Key methodological references

**Bernadotte, A.**  
*Topology-driven classification of time series.* bioRxiv (2026).  
**DOI:** `10.64898/2026.04.25.720787`


**Bernadotte, A.**  
*Estimating the Number of Sources in EEG with Hankel Embedding for Brain-Computer Interface.* ICARA 2026, pp. 621–626.  
**DOI:** `10.1109/ICARA69401.2026.11480398`

**Menshikov, I., Elfimov, N. & Bernadotte, A.**  
*A Lightweight Hankel-Embedded Pipeline for Real-Time EEG Filtering and Classification.* ICARA 2026, pp. 589–593.  
**DOI:** `10.1109/ICARA69401.2026.11480292`



## Representative figures

Representative BOID and auxiliary PSG figures derived from the public synthetic recordings are included in [`figures/`](figures/). These are supplementary visual documentation; the canonical raw public data remain the EDF / EDF+ files in `public_data/`.

For full figure captions, see:

[`figures/README.md`](figures/README.md)

## Controlled access

The 40 real AiCumene wearable-EEG recordings are available to qualified researchers for legitimate non-commercial scientific research under controlled access.

Contact:

**bernadotte@aicumene.com**

The controlled-access Data Use Agreement is maintained in the companion dataset repository.

## Contents of this Zenodo deposit

```text
AiCumene-EEG-BCI-Sleep-Wake-Dataset/
├── README.md
├── DATASET_DESCRIPTION.md
├── DATA_AVAILABILITY.md
├── METADATA.csv
├── PUBLIC_DATA_MANIFEST.csv
├── CITATION.cff
├── LICENSE
├── PATENT_NOTICE.md
├── RELATED_WORKS.md
├── figures/
│   ├── README.md
│   └── *.png                    (representative BOID + auxiliary-channel figures)
└── public_data/
    ├── README.md
    ├── S0001-PSG.edf … S0045-PSG.edf
    └── S0001-Hypnogram.edf … S0045-Hypnogram.edf
```
