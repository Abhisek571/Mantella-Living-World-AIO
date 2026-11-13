# Mantella Living World - All in One

Version {VERSION}

Every Mantella Living World mod in one download: the Integration Hub, Mantella - Direct AI Connect and all eight modules. The installer asks which modules you want; each module works on its own, so take only the ones you need.

## What is inside

{INCLUDED}

| Mod | What it adds | Needs (besides the Hub) |
|---|---|---|
| Integration Hub | The base: the Living World tab in Mantella's settings page, memory, action gates and the debug menu. Always installed | |
| Mantella - Direct AI Connect | The patched Mantella.exe that everything in Living World runs inside | Mantella 0.14, Python 3.11 once |
| Relationships | Marriage, affection, family ties and shared history | M.A.R.A.S, Relations Finder and Lover's Ledger, each only for its own part |
| World | What NPCs know about you, recognition, what you did to them, settling a bounty, party banter | Address Library for SKSE Plugins |
| Knowledge | What each NPC plausibly knows, quest secrets, lore lookups and map marks | |
| Survival | Hunger, cold, rest, food, beds, wounds and vampirism noticed by NPCs | Address Library for SKSE Plugins; Survival Mode for hunger, Survival Mode Improved for cold and tiredness |
| Followers | Party orders by talking | Nether's Follower Framework |
| Missives | Job posters who know their own jobs | Missives |
| Arousal (adult) | Arousal, appetite and temperament | OSL Aroused, powerofthree's Papyrus Extender |
| OStim Expansion (adult) | OStim scenes and affection (dances, kisses, hugs) run by conversation | OStim Standalone and an animation pack, OSL Aroused, Actions For Mantella - Expanded Sex Actions |

The installer recommends Followers, Missives, Arousal and OStim Expansion only when their required mod is active in your load order.

## Requirements

- Mantella 0.14, with a normal conversation working first
- SKSE, PapyrusUtil, Papyrus MessageBox - SKSE NG, powerofthree's Papyrus Extender, MCM Helper, SkyUI
- Python 3.11 from python.org, once, for Direct AI Connect's setup (3.12 and newer cannot build the patch)
- Mantella's Advanced Actions turned on, with a model that supports tool calling, for the actions that need it
- The requirements of each module you pick (table above)

Built and tested on Skyrim Special Edition with Mod Organizer 2.

## Install (Mod Organizer 2)

1. Close Skyrim and Mantella.
2. Install this archive as one mod and pick the modules you want.
3. In MO2's left pane, place it below Mantella. With OStim Expansion, also place it below Actions For Mantella - Expanded Sex Actions.
4. Enable the mod and the Living World plugins it adds.
5. Right-click the mod, Open in Explorer, and run Setup Backend.cmd once. It finds Mantella 0.14's own Mantella.exe in your other mods and builds the patched copy here.
6. With OStim Expansion: close the game and run tools\Mantella Living World - OStim Expansion\Build Flows.cmd from the same folder, then enable the new mod "Mantella Living World - OStim Expansion - Flows". Run it again whenever you add or remove animation packs.
7. In game, run the setup when the reminder box asks, or press the Living World hotkey (Home) while aiming at nobody. Save afterwards.
8. Open Mantella's settings page (http://localhost:4999/ui while Mantella is running), turn on Advanced Actions in the Actions tab, and check the Living World tab's Status page. It lists anything that is missing.

Your LLM service and its key keep working as before.

## Coming from the separate downloads

Disable or remove the separate Living World mods and the separate Mantella - Direct AI Connect before enabling this one, so no file is installed twice. Your memories, overrides and settings live outside the mod folders and stay as they are. Keep your OStim Expansion Flows mod.

## Adding or removing a module later

Reinstall this archive over the same mod and change the ticks. Removing the Integration Hub mid-playthrough is not supported.

## After an update

Run Setup Backend.cmd again, and Build Flows.cmd if you use OStim Expansion.

## Documentation

Each mod's own readme and license are in the Docs folder of the installed mod. The module pages on Nexus have the full feature lists and questions and answers.

## License

The Living World mods are GNU AGPL-3.0; the SKSE plugins of World and Survival are GPL-3.0. Mantella - Direct AI Connect is GNU AGPL-3.0-or-later and bundles no Mantella executable. Unofficial, not endorsed by the Mantella authors.

Author: itsPigeon2000
