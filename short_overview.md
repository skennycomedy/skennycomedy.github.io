## What is OwlONE

- nebulaONE Gen AI platform built MS Azure--FAU's instance (OWLS!)
- FAU SSO--login before event so we have you in system
- Data stays within FAU's secure Azure environment

## UI/basics

- **ONEchat** — default, general-purpose immediate chat
  - Image gen, Web Search, Data & File Tools
  - CAN ASK IT ABT THE PLATFORM--[[QUICK PROMPT]]
  - "+": file uploads, M365, canvas, Skills (later)
  - BOTTOM OF CHAT: Execution Details, Regen (for model switch), playback

- **Left Nav Panel** -- akin to copilot, chatgpt...
  - **Explore Agents** — Official green check, useful defaults
  - **Chats tab** — searchable, exportable history
  - **agents tab** PINNED & RECENT
  
## AGENTS: official vs personal agents (we'll focus mostly official)

**personal: you can do right now, create & share with link
  - knowledge sources: files, websistes, API calls

**official: created by admins -- prefab for promptathon -- more configs avail

## WALKTHRU: show rather than tell...

[[[ OPEN BUILDER TAB & SHELL TAB ]]]
  - review what builder gives...AI makes mistakes :)
  - COVER BELOW WHILE BUILDER BUILDING

### KNOWLEDGE--core of **RAG (Retrieval-Augmented Generation)** — the agent retrieves relevant info from your sources and uses it to ground its responses. (model's on the RAG)

  #### file libs
      - File Libs indexed vectorized, super fast (max = ranked for relevancy then drills down)
      - If agent has both a File Lib and website, use system instructions to tell the agent which to prefer in which scenario.

  #### web
      - [demo] add fau website <=5 pg max speed/tokens
      - specific subdomains = targeted responses.

  #### model selection
      - try builder suggestion, experiment, all have diff strengths
      - max response, creativity, verbosity....defaults reasonable, tweak/test playground

  #### connection to external APIs as knowledge sources also availble

### WHEN SEE MULTI AGENT--GO RIGHT INTO SKILLS
    - acts as 'subagent' invoke for specific tasks
    - so its instructions don't need to be loaded for all interactions (like sys prompt)
    - performance analysis example -- before skills multiple agents to do this kind of optimization
    - add a skill: bottom-left initial->settings
    - better than multi-agent when the task only requires additional instructions—not a separate permission set or model.

#### CAPABILITIES
  - Data & File Tool: analyze data, create spreadsheets, etc
  - Add Files & Images: chat during convo
  - Generate Artifacts: html mockups
  - Internet search
  - Image Creation
  - Personal Microsoft 365

#### Appearance Tab--not much wiggle room
  - Guidelines — Attach a guidelines document

#### Publishing/Access -- preconfigured for event
  - only be visible, configurable by yr group until ready to release
  - Activate Agent: toggle ON when the agent is ready for user
  - Once activated, agent appears in the Explore Agents catalog for the designated audience.--we're still sorting out groups

#### test in the Chat Playground
  - live testing environment — changes made here are real-time but only visible to you; chat history NOT saved
  - **Show Execution Details** inspect (similar to front end except available in excruciating detail)
  - chat starters useful as quick prompts but also public facing can be used to inspire your users

