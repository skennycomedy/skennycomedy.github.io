## What is OwlONE

- nebulaONE Gen AI platform built MS Azure--FAU's instance (OWLS!)
- FAU SSO--login before event so we have you in system
- Data stays within FAU's secure Azure environment

## UI/basics -- ONEchat

- **ONEchat** — default, general-purpose immediate chat
  - Image gen, Web Search, Data & File Tools
  - CAN ASK IT ABT THE PLATFORM--[[QUICK PROMPT]]
  - "+": file uploads, M365, canvas, Skills (later)
  - BOTTOM OF CHAT: Execution Details, Regen (for model switch), playback

- **Left Nav Panel**  (akin to copilot, chatgpt, etc)
  - **Explore Agents** — Official green check
  - **Chats tab** — searchable, exportable
  - **agents tab** PINNED & RECENT
  
## AGENTS: official vs personal agents (we'll focus official)

**personal: you can do right now, create & share with link
  - knowledge sources: files, websistes, API calls

**official: created by admins -- prefab for promptathon -- more configs avail

## WALKTHRU: show rather than tell...

[[[ OPEN BUILDER TAB & SHELL TABS ]]]
  - review what builder gives...AI makes mistakes :)
[[[ COVER BELOW WHILE BUILDER BUILDING ]]]

### KNOWLEDGE--core of **RAG (Retrieval-Augmented Generation)** — the agent retrieves relevant info from sources and uses to ground responses

 #### file libs [[ show prefab ]]
 - indexed vectorized, super fast (max = ranked for relevancy then drills down)

 #### web
 - <=5 pg max speed/tokens
 - specific subdomains = targeted responses (e.g. fau.edu/oit)

 #### model selection
 - try builder suggestion, experiment, all have diff strengths
 - max response, creativity, verbosity....defaults reasonable, tweak/test playground

 #### connection to external APIs as knowledge sources also availble

### WHEN SEE MULTI AGENT--GO RIGHT INTO SKILLS
- now do what previously might've required a 'subagent' to be invoked
- so instructions for skill don't have to get loaded each time with the full sys prompt only when needed
- [[ performance analysis example ]]  -- before skills multiple agents to do this kind of optimization
- add a skill: bottom-left initial->settings
- multi-agent only needed when task requires a separate permission set or model.

#### CAPABILITIES
- Data & File Tool: analyze data, create spreadsheets, etc
- Add Files & Images: chat during convo
- Generate Artifacts: html mockups
- Internet search
- Image Creation
- Personal M365

#### Appearance Tab--not much wiggle room
- Guidelines — Attach a guidelines document

#### Publishing/Access -- preconfigured
- only accessible by yr team initially
- Activate Agent: toggle ON when the agent is ready for user this shared with all logged in
- Once activated, agent appears in the Explore Agents (we'll create groups for promptathon)

#### test in the Chat Playground
  - chat history NOT saved
  - **Show Execution Details** inspect (similar to front end except available in excruciating detail)
  - chat starters -- public facing inspire your users

