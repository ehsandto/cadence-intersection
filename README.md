# CadenceIntersection

CadenceIntersection finds shared ticks across periodic schedules written in prose. It combines compatible schedules into a single arithmetic progression and measures it over query windows with blackout intervals.

`index_schedule(coordinate, commitment)` accepts a GitHub raw path pinned to a full commit and the manifest's exact SHA-256. The manifest has two to five schedule descriptions and up to ten half-open blackout intervals. Leader and validators independently fetch the whole manifest, check the digest, and use an LLM to extract each operative period and phase. Agreement requires the exact canonical observation, including the full text and every interpreted cycle. The document hash keys the immutable index.

`get_schedule(commitment)` returns the evidence, cycles, merged blackouts and the shared progression. When residues disagree modulo the greatest common divisor of two periods, it returns their indices and residues as a conflict witness. An unresolved cycle yields `UNKNOWN` unless the known cycles already prove a conflict.

`query(commitment, start, end)` returns the first and last shared ticks, the count, and the number removed by blackouts within `[start,end)`. It uses modular arithmetic and merged intervals, with no iteration over ticks. Tick bounds are integers from 0 through 10^15.

The fixtures describe fictional schedules. Phases two and four on periods six and eight align at phase 20 every 24 ticks. After blackouts remove ticks 20 and 44, the window `[0,100)` contains ticks 68 and 92. Replacing the operative phase four with phase three produces an even/odd conflict and zero shared ticks.

Install `requirements-dev.txt`, run `python -m pytest tests -q`, and run `genvm-lint check contracts/CadenceIntersection.py`.

[Submission](SUBMISSION.md) · [StudioNet proofs](LIVE_PROOFS.md)
