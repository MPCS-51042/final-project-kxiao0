# Final Project Proposal
**My ideas for my final project are...**

1. An api that helps identify potential comps in League of legends - TeamFight Tactics. The project will (1) need web scraping (maybe using Beautiful Soup?) on a few TFT data pages (e.g. https://www.leagueofgraphs.com/tft/comps and https://www.leagueofgraphs.com/tft/items) to get best comps and suitable items for those champions; (2) take inputs of base items from user to give recommendations on (a) potential comps and its relevant data in order of relevance level and win rate (b) recommended combined items for champions (c) additional base items and champions that need to be obtained


**To Do (Suggested by Chelsea)**

1. Proof of concept on the integrations with LoL TeamFight data pages and any other APIs
2. Figure out your UI: both the input (how will a user trigger recommendations) and the output (list of champions and items)
3. Implement the logic to get from a user’s inputs to the output list from the data you’re collecting thanks to step 1
4. Implement screens in some kind of UI Framework (Flask would be good for a little web app, or you could do something local)

**Project plan**

1. By end of week 4 (Feb 5): POC on the integration with LoL TeamFight Tactics game data pages and other APIs (Note: data not pulled by Web scrap yet, hard code numbers if needed; overall logic clear - with details to be refined, i.e. detailed code to be used)
2. By end of week 5 (Feb 12): Web scrap done, data preliminary processed; UI identified (input and output)
3. By end of week 6 (Feb 19): Web scrap data fully processed, logic implementation started (the program should be able to take input, extract data and give recommendations based on PoC, with some limitations in algorithm)
4. By end of week 7 (Feb 26): Fine-tuning recommendation logic, test with extreme cases / updates in data etc, UI Framework implementation starts
5. By end of week 8 (Mar 5): Adjust logic and UI for user-friendly purpose (e.g. add descriptions)
6. Final touch: Finalize UI, code walk-through video recording

