# Resynthesis pipeline

Auxiliary code for the synthetic component of the AiCumene EEG-BCI Sleep–Wake
Dataset, released for transparency and reproducibility.

## `aux_channels.py`

Regenerates the auxiliary polysomnography channels (EOG, EMG, respiration,
temperature) as stage-conditioned physiological surrogates (e.g. EMG muscle
atonia in REM). The EEG derivations are not touched, so the Brain Oscillator
Intrinsic Dimension (BOID) is unaffected. Requires `numpy` and `mne`.

```bash
python aux_channels.py <output_dir>          # stage-conditioned auxiliary channels
```

## Oscillator resynthesis (released with the MSSA preprint)

The script that resynthesises the EEG derivations themselves depends on the
AiCumene **MSSA** signal-subspace estimator and is released together with the
separate MSSA methodological preprint and repository:

> https://github.com/aicumene/MSSA

It re-renders each 30-s epoch from its oscillator modes as phase-randomised
damped sinusoids — preserving each recording's oscillatory / spectral structure,
and therefore its BOID, while decorrelating the sample-level waveform.

## Provenance and attribution

The synthetic recordings are **phase-randomised surrogates derived from Sleep-EDF
Expanded (Sleep Cassette)**, PhysioNet, distributed under the Open Data Commons
Attribution License v1.0 (ODC-BY). Each synthetic recording corresponds to a
Sleep-EDF source recording and preserves its oscillatory content; no independent
human recording is claimed. Attribution:

- Kemp, B., Zwinderman, A. H., Tuk, B., Kamphuisen, H. A. C., & Oberyé, J. J. L.
  (2000). *Analysis of a sleep-dependent neuronal feedback loop: the slow-wave
  microcontinuity of the EEG.* IEEE Transactions on Biomedical Engineering,
  47(9), 1185–1194.
- Goldberger, A. L., Amaral, L. A. N., Glass, L., et al. (2000). *PhysioBank,
  PhysioToolkit, and PhysioNet.* Circulation, 101(23), e215–e220.
- Sleep-EDF Database Expanded, PhysioNet. https://physionet.org/content/sleep-edfx/

## Licensing

Software license: **PolyForm Noncommercial License 1.0.0** (`PolyForm-Noncommercial-1.0.0`).

This license applies only to the software in this directory. Dataset files,
metadata, and documentation are licensed separately as described in the
repository-level `LICENSE`.
