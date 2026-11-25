# StudioNet proofs

[Contract on StudioNet](https://explorer-studio.genlayer.com/address/0x88ea342BEb8E05F5C186582e0B3636222B5D6D52) ·
[Pinned source](https://github.com/ehsandto/cadence-intersection/blob/9ed573e3810a3bcb0b5fa3f60c99b95ef3e46290/contracts/CadenceIntersection.py) ·
[Machine-readable receipts and readbacks](PROOFS.json)

| Transaction | Finalized consensus | Verified outcome |
| --- | --- | --- |
| [Deploy](https://explorer-studio.genlayer.com/tx/0x22efd2e5cfeb158fd1c8025351e560b91df65b4ef6d7f036e013199e75ac2c62) | Majority agree | Deployed source matches the pinned GitHub source after line-ending normalization. |
| [Index aligned fixture](https://explorer-studio.genlayer.com/tx/0xe131eeaa3a388e4670b0ec1f7c8357df72ed081d07be38223a692911a72e5809) | Majority agree | Active cycles `[6,2]`, `[8,4]`. Common ticks are 20 modulo 24. |
| [First conflict attempt](https://explorer-studio.genlayer.com/tx/0x6bd8c41cfa2b738a7628fb33ed9c43026d3c399605f1e2d7c659e063dfbdbda8) | Majority disagree | Acquisition or interpretation error. A contract read confirmed the index was absent. |
| [Retry identical conflict fixture](https://explorer-studio.genlayer.com/tx/0x69bcbbe1f42c79a69428b42d73f99ff42340979d176ee6f959569f96f12c4ad9) | Majority agree | Active cycles `[6,2]`, `[8,3]`. Conflict witness gives residues 0 and 1 modulo 2. |

The aligned fixture returned two shared ticks, 68 and 92, in `[0,100)` after excluding two blackout ticks. The window `[45,92)` returned only 68. The conflict fixture returned zero shared ticks. Both successful registrations had recorded validator executions, and the stored source text matched the pinned fixture bytes.

The first conflict attempt reported the combined acquisition-or-interpretation error. That receipt cannot distinguish an HTTP problem from an invalid model response. The published journal retains the rejected receipt and the absence check.

`npm ci` followed by `node scripts/live.mjs --verify-only` rechecks the receipts, source, exact evidence, progression, and query results.
