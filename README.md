# Mantella Living World - All in One

Mantella Living World is a set of mods for [Mantella](https://www.nexusmods.com/skyrimspecialedition/mods/98631) 0.14 on Skyrim Special Edition. It tells Mantella NPCs what fits their life and what is going on around them: relationships, your deeds and fame, what each NPC plausibly knows, how you are getting by, and more. The Integration Hub is the shared base, Direct AI Connect is the patched Mantella.exe that everything runs inside, and each of the eight modules works on its own.

This repository holds the source of every Living World mod in one place and replaces the separate per-mod repositories.

## What is inside

| Folder | What it adds | Version |
|---|---|---|
| [Integration Hub](Integration%20Hub/) | The base every module needs: the Living World tab in Mantella's settings page, memory, action gates and the debug menu | 1.2.3 |
| [Direct AI Connect](Direct%20AI%20Connect/) | The patched Mantella.exe that Living World runs inside, with more LLM services and Dual Input built in | 1.5.0 |
| [Relationships](Relationships/) | Marriage, affection, family ties and shared history | 1.2.1 |
| [World](World/) | What NPCs know about you: fame, bounty, titles, quest outcomes, what you did to them, recognition, party banter | 1.2.1 |
| [Knowledge](Knowledge/) | Each NPC knows what fits their life: home, hold, job, quest secrets, lore lookups and map marks | 1.1.1 |
| [Survival](Survival/) | NPCs notice hunger, cold, rest, food, beds, wounds and vampirism | 1.0.1 |
| [Followers](Followers/) | Party orders by talking, through Nether's Follower Framework | 1.2.1 |
| [Missives](Missives/) | Job posters who know their own jobs | 1.1.1 |
| [Arousal](Arousal/) | Arousal, appetite and temperament from OSL Aroused (adult) | 1.1.1 |
| [OStim Expansion](OStim%20Expansion/) | OStim scenes and affection run by conversation (adult) | 1.2.1 |

Each folder has the mod's own README, CHANGELOG and LICENSE.

`tools/build_aio.py` builds the All in One installer from the separate release archives.

## Install

Download the All in One installer from the [Nexus page](https://www.nexusmods.com/skyrimspecialedition/mods/198897) or from the [Releases](https://github.com/Abhisek571/Mantella-Living-World-AIO/releases) tab and install it with your mod manager. The installer asks which modules you want. The readme inside the archive has the full steps and requirements.

## License

- Living World mods: GNU AGPL-3.0 (see [LICENSE](LICENSE) and each mod's own LICENSE).
- The SKSE plugins of World and Survival: GPL-3.0.
- Direct AI Connect: GNU AGPL-3.0-or-later. It bundles no Mantella executable.

Unofficial, not endorsed by the Mantella authors.

Author: itsPigeon2000
