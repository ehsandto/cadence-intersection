# CadenceIntersection — Shared Ticks from Published Schedules

**Contribution type** Builder → Intelligent Contracts

CadenceIntersection finds shared ticks across independently interpreted recurring schedules. It combines compatible phases into an arithmetic progression. Any reader can query a half-open time window for its first and last shared ticks, count, and the number excluded by blackouts.

The leader and validators independently fetch the complete commit-pinned manifest and verify the SHA-256. Each uses an LLM to extract the operative period and phase from every description, including distinguishing active settings from rejected proposals. Consensus compares the full fetched text and every extracted cycle exactly. The resulting phases determine whether the shared progression exists.

In the fictional demonstration, periods six and eight with phases two and four align at phase 20 every 24 ticks. After the blackouts remove ticks 20 and 44, only ticks 68 and 92 remain in the first 100 ticks. With operative phase three for the eight-tick schedule, the phases disagree modulo two. The contract returns the two incompatible residues as a checkable conflict witness.

GenVM lint and six tests passed. Tests compare 1,225 pairs of short cycles and 496 blackout windows with direct enumeration.

StudioNet verified the deployment, aligned schedule, blackout boundary, and conflict witness. The first conflict attempt returned an acquisition or interpretation error. A direct read confirmed it committed no index. The identical pinned fixture succeeded on retry.

[GitHub repository](https://github.com/ehsandto/cadence-intersection) ·
[StudioNet deployment](https://explorer-studio.genlayer.com/address/0x88ea342BEb8E05F5C186582e0B3636222B5D6D52) ·
[Proofs and receipts](https://github.com/ehsandto/cadence-intersection/blob/main/LIVE_PROOFS.md)
