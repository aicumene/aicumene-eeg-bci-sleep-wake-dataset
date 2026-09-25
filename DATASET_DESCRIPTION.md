# AiCumene EEG-BCI Sleep–Wake Dataset — Dataset Description

**Dataset creators:** Alexandra Bernadotte and Ivan Menshikov  
**Project / data source:** AiCumene  
**Version:** 1.0  
**Dataset DOI:** `10.5281/zenodo.22923070`

## 1. Overview

The **AiCumene EEG-BCI Sleep–Wake Dataset** has two components:

1. **A public synthetic sleep-EEG benchmark** — **45 synthetic** whole-night polysomnography (PSG) recordings, each paired with a time-synchronised sleep-stage hypnogram, **produced by per-recording oscillator resynthesis of the Sleep-EDF Expanded (Sleep Cassette) corpus** (PhysioNet): oscillatory modes are refitted per 30-s epoch and re-rendered with randomised phase and small frequency jitter. They are therefore **phase-randomised surrogates derived from Sleep-EDF** and preserve each source recording's oscillatory structure. **All 45 synthetic recordings are released publicly** (they contain no real-subject identities to protect).

2. **Real AiCumene wearable-EEG recordings** — **40 de-identified human recordings** acquired with AiCumene neurointerface devices. These are **not part of this public archive**; de-identified data may be made available to qualified researchers under controlled access (see §6).

The dataset accompanies research on **Brain Oscillator Intrinsic Dimension (BOID)**:

https://research.aicumene.com/papers/boid-coma/
DOI: 10.13140/RG.2.2.31610.25288

The **45 synthetic** recordings are stored in the **European Data Format (EDF / EDF+)**, carry neutral identifiers `S0001`–`S0045`, and each spans approximately **21–23 h** (a full day–night cycle). Each recording consists of two files:

| File | Content | Format |
|---|---|---|
| `S00xx-PSG.edf` | Multi-channel PSG signals | EDF |
| `S00xx-Hypnogram.edf` | 30-s sleep-stage annotations | EDF+ (annotations only) |

---

## Source data and attribution

The synthetic recordings are derived from the **Sleep-EDF Database Expanded
(Sleep Cassette)**, distributed by PhysioNet under the **Open Data Commons
Attribution License v1.0 (ODC-BY)**. In accordance with that license, this
derived dataset attributes the source:

- Kemp, B., Zwinderman, A. H., Tuk, B., Kamphuisen, H. A. C., & Oberyé, J. J. L.
  (2000). *Analysis of a sleep-dependent neuronal feedback loop: the slow-wave
  microcontinuity of the EEG.* IEEE Transactions on Biomedical Engineering,
  47(9), 1185–1194.
- Goldberger, A. L., Amaral, L. A. N., Glass, L., et al. (2000). *PhysioBank,
  PhysioToolkit, and PhysioNet.* Circulation, 101(23), e215–e220.
- Sleep-EDF Database Expanded, PhysioNet. https://physionet.org/content/sleep-edfx/

The oscillator-resynthesis procedure that produced these surrogates is documented
and released in the companion repository.

---

## 2. Signal montage (PSG)

Every PSG file uses the **same 7-channel montage** with identical header conventions across all recordings:

| # | Label | Modality | Sampling | Unit | Pre-filtering |
|---:|---|---|---:|---|---|
| 0 | `EEG 1` | EEG | 100 Hz | µV | 0.5–100 Hz |
| 1 | `EEG 2` | EEG | 100 Hz | µV | 0.5–100 Hz |
| 2 | `EOG` | Electro-oculogram | 100 Hz | µV | 0.5–100 Hz |
| 3 | `Resp` | Respiration | 1 Hz | — | 0.03–0.9 Hz |
| 4 | `EMG` | Electromyogram | 1 Hz | µV | HP 16 Hz / LP 0.7 Hz |
| 5 | `Temp` | Body temperature | 1 Hz | °C | — |
| 6 | `Marker` | Event marker | 1 Hz | — | — |

Samples are stored as **16-bit integers** with per-channel physical calibration (physical min/max ↔ digital min/max) in the EDF header, in accordance with the EDF specification.

Each EDF **data record spans 30 s**, so one data record corresponds to one scoring epoch.

The two EEG derivations and the EOG are the high-rate channels sampled at **100 Hz**. Respiration, EMG, temperature, and the event-marker channel are low-rate auxiliary channels sampled at **1 Hz**.

The pre-filter strings in the montage table reproduce the EDF header metadata inherited from the source recordings; they describe the original acquisition chain and should **not** be interpreted as digital filtering applied to the 1-Hz auxiliary channels after downsampling. In particular, the 1-Hz `EMG` channel carries a rectified muscle-tone **envelope** rather than the raw electromyogram waveform.

---

## 3. Sleep staging (Hypnogram)

Hypnograms are **EDF+ annotation files**.

Stages are annotated on a fixed **30-second epoch** grid using the standard EDF+ stage vocabulary:

| Annotation | Stage |
|---|---|
| `Sleep stage W` | Wake |
| `Sleep stage 1` | N1 |
| `Sleep stage 2` | N2 |
| `Sleep stage 3` | N3 (slow-wave sleep) |
| `Sleep stage R` | REM |
| `Sleep stage ?` | Unscored / indeterminate |
| `Movement time` | Movement (rare) |

Source Sleep-EDF annotations were originally scored according to the
Rechtschaffen–Kales system. For this synthetic release, stages 3 and 4 were merged
into a single N3 class to obtain the five-state Wake/N1/N2/N3/REM convention used
in the present analysis.

### Aggregate stage composition (epochs covered by the PSG signal, all 45 recordings)

| Stage | Share | Epochs |
|---|---:|---:|
| Wake | 70.6% | 87,028 |
| N1 | 3.1% | 3,826 |
| N2 | 16.0% | 19,683 |
| N3 | 4.6% | 5,693 |
| REM | 5.6% | 6,953 |
| Unscored (`?`) | 0.1% | 95 |

Total: **123,278** scored epochs (≈ **1,027 h**), consistent with the per-recording
durations in `METADATA.csv`. (Hypnogram annotations that extend beyond the end of
the PSG signal are excluded from this tabulation.)

Recordings span a **full day–night cycle** of approximately **21.4–23.5 hours**, and therefore include long waking periods around the sleep episode.

Wake consequently dominates the total epoch count, while the sleep period constitutes a subset of each recording.

---

## 4. Durations

| Statistic | Value |
|---|---|
| Recordings | 45 |
| Epoch length | 30 s |
| Data records per recording | 2,570–2,820 |
| Duration per recording | 21.4–23.5 h |
| Median duration | 23.4 h |
| Total signal duration | ≈ 1,027 h |

---

## 5. Metadata and anonymisation

The public recordings are **Sleep-EDF-derived surrogates**; Sleep-EDF Expanded is already de-identified and the headers here are neutralised, so no participant-identifying information is present. For completeness:

- Header identity fields contain no names or personal identifiers.
- Recording **start dates are surrogate dates** and do not correspond to real calendar dates or acquisition order.
- **No demographic or clinical metadata** are distributed with this release.
- Signal headers use a **uniform template** across all 45 recordings, including identical channel labels, units, transducer fields, and pre-filter fields.
- Recordings are therefore not distinguishable by participant identity through header metadata.


Public metadata for all 45 synthetic recordings are provided in the repository root as `METADATA.csv`.

The public metadata fields are:

| Field | Description |
|---|---|
| `record_id` | Neutral record identifier |
| `state` | Broad state coverage (`wake+sleep`) |
| `sleep_stage` | Aggregate record-level stage descriptor (`mixed`) |
| `recording_duration_seconds` | Total recording duration in seconds |
| `sampling_rate_hz` | Sampling rate of the EEG channels |
| `n_eeg_channels` | Number of EEG derivations (2) |
| `file_name` | PSG filename |
| `dataset_version` | Dataset release version |
| `notes` | Record-level notes, including paired hypnogram filename |

The value `n_eeg_channels = 2` refers to the two EEG derivations (`EEG 1` and `EEG 2`) and does not count the auxiliary PSG channels (EOG, respiration, EMG, temperature, and marker).

Public dataset identifiers are neutral research identifiers:

```text
S0001
S0002
...
S0045
```

The identifiers do not encode names, email addresses, medical-record numbers, customer identifiers, dates of birth, or other direct identifiers.

---

## 6. Access model

The dataset uses a two-part access model.

### Public subset — synthetic

**All 45 synthetic recordings** are distributed publicly (via Zenodo, with documentation in the companion repository):

https://github.com/aicumene/aicumene-eeg-bci-sleep-wake-dataset

The original public synthetic outputs and associated metadata are licensed under **CC BY-NC 4.0** to the extent the creators are entitled to license them; rights in the underlying Sleep-EDF source database remain governed by **ODC-BY 1.0** (Kemp et al., 2000; PhysioNet, Goldberger et al., 2000).

### Controlled subset — real recordings

The **40 real AiCumene wearable-EEG recordings** are not stored in the public repository.

De-identified data may be made available to qualified researchers for non-commercial scientific research under a data-use agreement provided as part of the controlled-access process, subject to applicable participant-consent, ethical, privacy, data-protection, and legal requirements.

Data-access requests should be sent to:

**bernadotte@aicumene.com**

---

## 7. Dataset creators

**Alexandra Bernadotte**  
**Ivan Menshikov**

Project / data source:

**AiCumene**

---

## 8. Example BOID visualisations

The repository contains author-generated BOID visualisations for selected public recordings:

- `S0003`
- `S0006`
- `S0011`
- `S0014`

Files:

- `figures/S0003_boid_sleep_profile.png`
- `figures/S0006_boid_sleep_profile.png`
- `figures/S0011_boid_sleep_profile.png`
- `figures/S0014_boid_sleep_profile.png`

These figures show BOID values across time together with sleep-stage background bands and stage-wise summaries. They are provided as visual illustrations of the associated BOID analysis and do not replace access to the underlying EDF / EDF+ recordings.

Associated BOID preprint:  
https://research.aicumene.com/papers/boid-coma/  
DOI: 10.13140/RG.2.2.31610.25288

---


### Multimodal PSG example

A multimodal example from public record `S0003` is provided as:

`figures/S0003_auxiliary_psg_channels.png`
- `figures/S0006_auxiliary_psg_channels.png`
- `figures/S0011_auxiliary_psg_channels.png`
- `figures/S0014_auxiliary_psg_channels.png`

The figure aligns the sleep-stage hypnogram with EMG, EOG, respiration, and body-temperature channels. Reduced EMG activity during several REM intervals provides an illustrative physiological correlate of REM-related muscle atonia in this recording.

Figure: **© 2026 Alexandra Bernadotte · AiCumene · CC BY-NC 4.0**  
Dataset DOI: **10.5281/zenodo.22923070**


## Analysis and reproducibility code

The canonical BOID implementation and article-level analysis code are maintained at:

https://github.com/aicumene/BOID

This dataset repository does not duplicate the BOID estimator. It contains a thin public-record wrapper at:

`analysis/reproduce_public_record.py`

The wrapper reads a paired public EDF / EDF+ record and calls the installed `boid` package to generate the 4-s BOID table and a derived 30-s sleep-stage table.

Associated BOID preprint:  
https://research.aicumene.com/papers/boid-coma/  
**DOI: 10.13140/RG.2.2.31610.25288**


## 9. Associated BOID research

### BOID preprint

**Bernadotte, A. & Menshikov, I.**  
*Brain Oscillator Intrinsic Dimension marks consciousness, recovery mode, and failed downshifting in coma.*  
2026.  
https://research.aicumene.com/papers/boid-coma/  
DOI: **10.13140/RG.2.2.31610.25288**

### Methodologically related prior work

**Bernadotte, A.**  
*Estimating the Number of Sources in EEG with Hankel Embedding for Brain-Computer Interface.*  
2026 12th International Conference on Automation, Robotics and Applications (ICARA), pp. 621–626, 2026.  
DOI: **10.1109/ICARA69401.2026.11480398**

https://doi.org/10.1109/ICARA69401.2026.11480398

**Menshikov, I., Elfimov, N. & Bernadotte, A.**  
*A Lightweight Hankel-Embedded Pipeline for Real-Time EEG Filtering and Classification.*  
2026 12th International Conference on Automation, Robotics and Applications (ICARA), pp. 589–593, 2026.  
DOI: **10.1109/ICARA69401.2026.11480292**

https://doi.org/10.1109/ICARA69401.2026.11480292

---

## 10. Citation

Suggested dataset citation:

> **Bernadotte, A. & Menshikov, I. (2026). AiCumene EEG-BCI Sleep–Wake Dataset (Version 1.0). AiCumene. DOI: 10.5281/zenodo.22923070.**

Please also cite the associated BOID publication / preprint.


If a peer-reviewed version of the associated BOID study is published, the final article citation and DOI should be added to this document.

---

## 11. Licensing

This release uses a **layered licence**.

- **Source data.** The recordings are derived from the Sleep-EDF Database Expanded
  (Sleep Cassette), PhysioNet, distributed under the **Open Data Commons
  Attribution License v1.0 (ODC-BY)**. Rights in the underlying Sleep-EDF database
  remain governed by ODC-BY, and its attribution requirements are retained (see
  *Source data and attribution*, above).
- **Synthetic outputs and documentation.** The original synthetic outputs of the
  resynthesis procedure, the associated metadata, and this documentation are
  licensed under **Creative Commons Attribution–NonCommercial 4.0 International
  (CC BY-NC 4.0)**, to the extent the creators are entitled to license them.

See `LICENSE` and `PATENT_NOTICE.md`. The controlled real-recording subset is
governed separately by a data-use agreement provided to approved researchers as
part of the controlled-access process.

---

## 12. Patent notice

The dataset license grants **no patent rights**.

In particular, access to the recordings does not grant a patent license to BOID or to related methods, algorithms, biomarkers, systems, implementations, or applications for estimating oscillatory or intrinsic dimensionality of brain activity.

See `PATENT_NOTICE.md`.

---

## 13. Research-use limitations

The dataset is provided for scientific research.

It is not provided as a clinically validated medical device or as a substitute for clinical diagnosis, treatment, or individual medical decision-making.

Users accessing the controlled real recordings must comply with applicable ethical, privacy, institutional, and legal requirements concerning human neurophysiological data. The public synthetic recordings contain no original participant recordings, direct identifiers, or real acquisition metadata; they are synthetic surrogates derived from de-identified Sleep-EDF recordings.
