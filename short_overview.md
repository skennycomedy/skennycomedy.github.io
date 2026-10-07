## What is OwlONE

- nebulaONE Gen AI platform built MS Azure--FAU's instance (OWLS!)
- FAU SSO--login before event so we have you in system
- Data stays within FAU's secure Azure environment

## UI/basics

- **ONEchat** — default, general-purpose immediate chat
  - Image gen, Web Search, and Data & File Tools are available.
  - CAN ASK IT ABT THE PLATFORM--[[QUICK PROMPT]] (doc bot) -- don't mention api?
  - "+": file uploads, Microsoft 365 sources, canvas, Skills (cover more detail later)
  --- bottom of chat icons/interaction ---
  - Execution Details — performance metrics, errs
  - Regenerate — resends prompt (for model switch)
  - start playback: if you like being read to

- **Left Nav Panel: -- akin to copilot, chatgpt...
  - **Explore Agents** — Official green check, useful defaults on homepage
  - **New Chat** — fresh ONEchat session.
  - **Chats tab** — searchable, exportable history
  - **agents tab** PINNED & RECENT
  
## AGENTS: official vs personal agents (we'll focus mostly official)

- **official: created by admins -- prefab for promptathon
  - all authorized users (based on groups and roles) can see
  - knowledge sources: File Libraries, APIs, MCPs, Connections, M365, websites
  - skills available

**personal: you can do right now, only creator sees and then shares with link
  - knowledge sources: files, websistes, API calls

#### WALKTHRU: creating official agent--builder

[[[ OPEN BUILDER TAB & SHELL TAB ]]]

  - agent instructions: System-level default applies broadly across the platform, shouldn't need to touch
    review--if contradict how you want yr agent, ok to delete them (meant as initial template)
  - review what builder gives...AI makes mistakes :)

////// KNOWLEDGE--agent access info beyond model trained on. core of **RAG (Retrieval-Augmented Generation)** — the agent retrieves relevant info from your sources and uses it to ground its responses. (model's on the RAG)

  /// web
      - [demo] add fau website <=5 pg max speed/tokens
      - The **When to Use** field important---NO JOKES & not for you (as i once thought) their for model! clearer = better
      - specific subdomains = targeted responses.
  /// file libs
      - File Libs best, indexed vectorized, super fast -- WE WILL HAVE ALREADY CREATED YOUR LIB (for demo) most file types ok (no code)
      - max docs -- finds ranks most relevant pics top <max docs>
      - again, meaningful lib description** — this is how the agent decides when to use it
      - If agent has both a File Lib and website, use system instructions to tell the agent which to prefer in which scenario.

  /// model selection
      - try builder suggestion, experiment, all have diff strengths...see which is giving you what you want (playground)
      - max response, creativity, verbosity....the defaults reasonable, tweak/test as you go--what the playground is for!

 /// connection to external APIs as knowledge sources also availble

....WHEN SEE MULTI AGENT--GO RIGHT INTO SKILLS

/////// CAPABILITIES -- Toggle on/off depending on whats needed -- can always check info bubble as well as doc bot
  - Data & File Tool: analyze data, create charts, spreadsheets, and documents.
  - Add Files & Images: users can attach files in chat during convo
  - Generate Artifacts: interactive outputs (quick HTML mockups, easily shared) users can view in a side panel
  - Internet search: MUST BE ON FOR URL IN KNOWLEDGE SRC
  - Image Creation: users can generate images in chat
  - Personal Microsoft 365: users search their own OneDrive/Outlook/Teams/calendar within the agent (users not agents ks)
  - only use knowledge sources: limits responses to only info from knowledge sources--e.g. instructors curated content

/////// Appearance Tab--not much wiggle room
- **Guidelines** — Attach a guidelines document (a set of content rules the agent must follow, managed separately).

/////// Publishing/Access -- preconfigured for event in shell -- don't worry too much about the access/sharing configs
  - only be visible, configurable by yr group until ready to release
  - Activate Agent: toggle ON when the agent is ready for users. (can still keep only w/in yr group at this point)
  - Once activated, agent appears in the Explore Agents catalog for the designated audience.--show home screen again

////// After Creation:
  - Use **Update** to save changes, **Reset** to discard unsaved changes, **Clone** to create a copy, or **Delete** to remove the agent.

////// test in the Chat Playground
  - live testing environment — changes made here are real-time but only visible to you; chat history NOT saved
  - **Show Execution Details** inspect (similar to front end except available in excruciating detail)
  - chat starters useful as quick prompts but also public facing can be used to inspire your users

////// SKILLS -- reusable instruction sets — Markdown files with two components:
  - **When-to-Use Description** — short trigger statement (when to be used)
  - **Instructions Body** — The full set of directives loaded on demand when triggered
  - example: faculty (stored all course  wanted modes: course logistics mode (e.g. syllabus), flashcard mode, quiz mode
  - consider our unruly agent instructions--could possibly make a skill for each type of marketing--e.g. 'brand voice', by making a skill we're kinda making a 'subagent' in a way only invoke that set of instructions when the user is prompting about 'brand voice'
  - entire sys prompt sent to model that's how skills came about...reduce context/make more managable
  - before skills would've needed multiple agents to do this kind of optimization
[[[ add a skill: bottom-left initial->settings ]]]
  - efficiency by progressive disclosure: OwlONE injects only the Skill’s compact name and description into the system prompt, then loads the full instructions only when the user’s request matches.
  - keeps base context smaller, reduces repeated instructions, same specialized behavior reused across multiple agents.
  - better than multi-agent when the task only requires additional instructions—not a separate permission set or model.
       - avoids routing overhead and multi-agent complexity while keeping the core agent focused
  -Two Types--personal, instance-wide. only personal available to you (other is meant for skills that admin can make available to all agents/users).
- great for long, specialized instruction sets that only apply some of the time.
- add in-chat, use same way just adding explicityly instead of implicitly. other selector only for admins so can make some skills avail platform-wide


>>>>>>>>>>>>>>>>>>>> ADD SKILL QUICK PROMPT ON OSTUDENT:

i'd like to break out one of the main capabilities of this agent into a separate skill. suggest what it should be and give me the separate skill instructions to use. 
