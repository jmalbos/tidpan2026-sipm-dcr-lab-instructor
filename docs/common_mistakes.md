# Common Student Mistakes

## Setup Problems

- Running `pytest` before activating the virtual environment.
- Opening the notebook from a different directory and losing track of relative
  paths.
- Editing the notebook only, instead of editing `student/analysis.py`.
- Changing function names or argument names, which breaks the tests.

## Data Loading

- Forgetting that column 0 is the timestamp and treating it as a waveform sample.
- Returning the full array instead of `(timestamps, waveforms)`.
- Accidentally using only the first event instead of all events.

## Timing

- Treating timestamp ticks as seconds.
- Using `16e-9` incorrectly as `16e9` or `1/16e-9`.
- Assuming the acquisition lasted exactly 10 minutes.
- Computing live time as `last_time` instead of `last_time - first_time`.
- Computing inter-arrival times from raw ticks after converting other quantities
  to seconds.

## Rate And Uncertainty

- Reporting the rate in counts per tick rather than Hz.
- Forgetting to convert Hz to mHz/mm^2 using the 36 mm^2 SiPM area.
- Using `sqrt(rate)` instead of `sqrt(N) / T` for the rate uncertainty.
- Forgetting that the uncertainty is statistical only.
- Removing burst events from the live time instead of only from the event count
  in this simplified exercise.
- Computing final amplitude, crosstalk-like, and afterpulse-like summaries on
  the full dataset after burst tagging has already been introduced.

## Waveforms

- Treating the pulses as positive-going.
- Computing `max - baseline` instead of `baseline - min`.
- Estimating the baseline from the full waveform, including the pulse.
- Using one global baseline for all waveforms without checking whether it is
  appropriate.

## Candidate Tags

- Confusing burst tagging with afterpulse tagging. Bursts require at least five
  consecutive events with short separations; afterpulse candidates use a much
  shorter delay window.
- Tagging only the intervals in a burst rather than all events in the burst.
- Returning an afterpulse mask with length `n_events - 1` instead of `n_events`.
- Forgetting that the first event has no previous inter-arrival time.
- Treating simple threshold tags as definitive physical labels.
- Changing thresholds without explaining how the candidate counts change.

## Interpretation

- Saying that a small p-value or visible short-delay excess means the analysis
  failed. It means the simple Poisson model is incomplete.
- Forgetting that correlated noise, electronics dead time, threshold choice, and
  acquisition settings can bias the apparent dark count rate.
- Over-interpreting one file as a full sensor characterization.
