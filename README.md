# The World in One Day — Thursday 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b169-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b169-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026**: 50 stories across 10 regions.

## Layout V165

Masthead, then a full-width hero banner (Macy's 100th Thanksgiving parade postponed — the first ever over weather), twin heroes below it (IRGC claims two tankers hit by mines in Hormuz; Trump tariffs and the global market rebound), 10 cards in two rows of five, a 12-pin world map beside 37 more stories, a DATE CHECK strip listing seven events deliberately left out because they happened on 22–25 November, and a sources footer.

## The three heroes

1. **Macy's 100th Thanksgiving Parade postponed** — first weather postponement in the parade's history; an East Coast storm brings heavy rain and gusts to 60 mph.
2. **Hormuz: IRGC claims two tankers hit by mines** — one a supertanker carrying over 2 million barrels; the claim is unverified, marked [CL].
3. **Trump tariffs: world markets rebound** — Europe and Asia rise as the new tariff salvo is judged milder than feared.

## DATE CHECK — deliberately left out

COP31 failed (22 Nov) · Shenzhou-24 launched (25 Nov) · Cairo tanker blast, 31 dead (25 Nov) · Cartagena hostages freed (25 Nov) · Australia–Solomon pact (25 Nov) · UK energy prices +26% (25 Nov) · Huawei convicted (24 Nov). None of these is 26 November news, so none is a story in the image — they are listed only in the DATE CHECK strip.

## How it is built

`gen.py` (Pillow, build-time only) renders `entry.png` at 1024×1024 with in-code assertions: exactly 37 ALSO items, the exact 7-item DATE CHECK, 12 map pins all on land with a legend listing every pin, card decks of at most two lines, and no text overlapping artwork. `main.py` is standard-library only and copies `entry.png` to `MAKEFUN_OUTPUT_DIR`.

## Verification

- `entry.png` sha256: `48bbe326c43ad93e6058a55ffd44c838fcee354ef67612f4d7db7458252a8eb1` (161,662 bytes, 1024×1024, all in-code asserts pass).
- Stdlib-venv sim passed: venv without Pillow, different cwd, empty out dir, read-only repo copy — `main.py` wrote an identical-digest `entry.png`.
- Revisions vs V165: hero 2 deck drops "north of Khasab" (assert: "khasab" absent from hero 2; corpus ban on "Khasab"); UKMTO 222-26 tagged `[CL]` with "25 Nov"; two ALSO storm sub-facts replaced by "NBC airs 2025 parade rerun Thu 08:30 [C]" and "Steelers release Aaron Rodgers [C]" (ALSO still 37).

## License

MIT — see `LICENSE`.
