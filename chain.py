from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from typing import List
import os

class BallooniverseChain:
    def __init__(self, api_key=None, llm='gemini'):
        self.llm_provider = llm
        if llm == 'gemini':
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro-exp-03-25",
                google_api_key=api_key or os.getenv("GOOGLE_API_KEY"), 
                temperature=0
            )
        elif llm == 'ollama':
            self.llm = OllamaLLM(
                model="deepseek-r1:14b",
                temperature=0,
                num_ctx=32768,
                num_predict=32768
            )
        elif llm == 'openai':
            self.llm = ChatOpenAI(
                model="o4-mini",
                api_key=api_key or os.getenv("OPENAI_API_KEY"),
                temperature=0
            )
        elif llm == 'deepseek':
            self.llm = ChatDeepSeek(
                model="deepseek-reasoner",
                api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
                temperature=0,
                max_tokens=None
            )
        
        self.system_prompt = """You are a helpful **AI Coding Assistant**, specializing in building interactive experiences using **JavaScript**, **HTML**, and **CSS**.

Your task is to assist the user in **developing a complete web-based game** by writing **full**, well-structured, clean, and modular code that runs entirely in the browser.

You will receive the user's requests incrementally. Each request will either:
1. Describe a new **feature or enhancement** to be implemented in the game.
2. Provide an existing **code snippet** for refinement or integration.

For every response:
- You must always **output the entire, complete HTML, CSS, and JavaScript code** in a **single `.html` code block**.
- **Do not output partial code, patches, or comments like "the rest remains the same"**. Always regenerate the full working project at its current stage.
- Ensure the code is **fully runnable in a browser**, without requiring external libraries or frameworks.
- Use **clear comments** to explain key logic and help with future refinement.
- Ensure the gameplay runs smoothly and the user interface is visually understandable.
- Maintain consistency and integration with previous features already built.

Do not include any AI-generated text outside the `<script>`, `<style>`, and `<body>` blocks unless specifically requested.

Your role is to **collaborate with the user through full code delivery** — write, refine, and optimize browser-based games in a progressive, human-guided development process."""
        
        self.human_messages = [
            """Hi AI! I’d like your help building a web-based game called **Ballooniverse**, using only **HTML, CSS, and JavaScript**. Please provide all code in a single `.html` file that runs entirely in the browser without external libraries.

This first version should establish the **core rules, basic mechanics, and visual layout**. Focus only on implementing the gameplay loop — we’ll expand on features in later prompts.

---

### 🎮 **Game Overview:**
In **Ballooniverse**, the player controls a floating balloon trying to ascend as high as possible through the sky. The balloon must avoid sharp obstacles that can pop it. The game ends when the balloon collides with any obstacle.

---

### 🧠 **Rules and Mechanics:**

1. **Player Control:**
   - The balloon should float continuously upward on its own.
   - The player can **move the balloon left or right** using the arrow keys (`←` and `→`) or `A` and `D`.

2. **Obstacles:**
   - Obstacles (such as spikes or darts) should appear from the top or sides of the screen and move toward the balloon.
   - Obstacles must be generated randomly over time.
   - If the balloon **collides with any obstacle**, the balloon "pops" and the game ends.

3. **Game Loop:**
   - The game starts automatically or with a simple click-to-start.
   - The player should be able to control the balloon immediately.
   - When the balloon pops, the game should clearly stop and display a basic message like “Game Over”.

---

### 📐 **Visual Requirements:**

- Use a simple background representing the sky (e.g., gradient or sky blue).
- Represent the balloon using a simple shape or image (e.g., circle or SVG).
- Obstacles can be rectangles or basic shapes for now — no need for detailed images yet.

---

### ⚙️ **What to Implement Now:**

✅ A balloon that moves upward automatically.  
✅ Left and right keyboard control.  
✅ Random obstacle spawning and movement.  
✅ Collision detection between balloon and obstacles.  
✅ End game when a collision happens.  
✅ Basic CSS styling (colors, layout) to differentiate elements.  
✅ Clearly separated and commented HTML, CSS, and JavaScript sections.
✅ A score that is displayed at the top of the screen and counts how many obstacles the balloon has avoided.

⚠️ Important: Please provide the full updated `.html` file, including all HTML, CSS, and JavaScript, in every response, not just code snippets or notes.""",

            """Great job setting up the initial version of **Ballooniverse**! Now I’d like to enhance the game by adding **Beginner and Intermediate-level features** based on a game development rubric. This is the next step in an ongoing development process, so please **build on the existing structure**, and **keep the code clean and modular**, written entirely in a single `.html` file.

---

### 🎯 **Goal of this Update:**
You will now add scoring, UI screens, pause/resume logic, physics-like motion, and difficulty progression.

---

### ✅ **Beginner-Level Features (Required):**

1. **Scoring System:**
   - Introduce a score based on how many obstacles the balloon has avoided.
   - The score should be updated **in real-time** and displayed at the **top of the screen** during gameplay.

2. **Start/Restart/Score Board Screens:**
   - Implement a **Start Screen** with a “Play” button that begins the game.
   - Implement a **Game Over Screen**:
     - Display a **final score** when the balloon pops.
     - Provide a **“Restart” button** that resets the game to the Start Screen.
   - The UI should smoothly transition between screens (Start → Game → Game Over → Restart).

---

### ⚙️ **Intermediate-Level Features (Required):**

3. **Pause and Resume Functionality:**
   - Allow the player to **pause/resume the game** by pressing the `P` key.
   - When paused, gameplay should freeze (balloon stops moving, obstacles stop spawning/moving).
   - Visually indicate when the game is paused (e.g., show “Paused” text overlay).

4. **Simple Physics-Like Movement:**
   - Improve the realism of the balloon's motion:
     - Simulate **slight gravity** pulling the balloon downward.
     - Add **horizontal wind forces** that occasionally push the balloon left or right.
   - These should create gentle, believable drift, not extreme or random movement.

5. **Multiple Levels or Increasing Difficulty:**
   - As the player reaches **higher altitudes**:
     - Gradually increase the **speed** of incoming obstacles.
     - Increase the **frequency** and **variety** of obstacle types.
   - This simulates a **leveling system**, with the sky getting more dangerous as you climb.

---

### 📘 **Instructions for Implementation:**
- Maintain all previously implemented functionality (Prompt 1).
- Keep all code (HTML, CSS, JavaScript) in a single `.html` file.
- Use helpful comments throughout to explain new logic.
- Write clean, modular code that’s easy to build on in the next phase.
- Make sure that the character will not leave the screen. Make the camera follow the character.

⚠️ Important: Please provide the full updated `.html` file, including all HTML, CSS, and JavaScript, in every response, not just code snippets or notes.""",

            """Excellent progress so far — *Ballooniverse* is shaping up to be a polished and enjoyable game. Now, I’d like to expand it with **advanced features**, which will add intelligence and atmosphere to the gameplay. Please build upon the existing code from the previous steps, maintaining everything already implemented.

All code should remain in a **single `.html` file**, structured with **clean HTML, CSS, and JavaScript** sections. Prioritize smooth performance and clear documentation.

---

### 🧠 **1. Basic Enemy AI: Smart Birds**

Introduce a new obstacle type: **birds**.

- These birds should **intelligently track the balloon’s horizontal position**.
- Birds should **spawn periodically from above**, and move down the screen while **adjusting their horizontal movement** to follow the player’s balloon.
- The tracking behavior should feel:
  - **Noticeable and intentional** (not random).
  - **Balanced**, so it's challenging but not impossible to avoid.
- They should **stop tracking** once they move off-screen or pass the balloon.

🛠️ Implementation tips:
- Use smooth interpolation or simple tracking logic (e.g., follow the balloon’s x position over time).
- Introduce bird obstacles in a way that complements existing random obstacles.

---

### 🔊 **2. Sound and Music:**

Add audio to bring the world of *Ballooniverse* to life:

- **Ambient Wind Sound:**
  - Loop a soft, subtle wind sound in the background throughout gameplay.
  - It should start when the game begins and stop on game over or pause.

- **Balloon Pop Sound:**
  - Play a satisfying popping sound effect **immediately** when the balloon collides with any obstacle (including birds).
  - This should sync tightly with the balloon's disappearance or game-over animation.

🛠️ Implementation tips:
- Use `<audio>` tags in HTML or JavaScript's `Audio` API.
- Preload sounds to avoid latency.
- Add user-friendly volume levels.

---

### 📘 **Integration Notes:**

- Maintain all features from the earlier prompts (core mechanics, scoring, screens, pause, physics, difficulty scaling).
- Comment your code clearly, especially where you integrate the enemy AI and sound logic.
- Ensure audio is not intrusive or repetitive.
- Make sure performance remains smooth across obstacle types.

⚠️ Important: Please provide the full updated `.html` file, including all HTML, CSS, and JavaScript, in every response, not just code snippets or notes.""",

            """Amazing work so far! The game is nearly complete. Let’s now elevate *Ballooniverse* to its full polished form by implementing two **master-level features**: balloon theme selection and persistent game state saving. These features will enhance personalization and create a seamless experience for returning players.

As always, keep all code in a **single `.html` file**, written with **HTML, CSS, and JavaScript**. Please maintain the current code structure and functionality, and ensure everything works together smoothly.

---

### 🎨 **1. Theme / Character Selection:**

Allow players to **customize their balloon** before playing:

- Add a **Balloon Selection Screen** that appears before gameplay begins.
- Provide **at least 3 distinct balloon styles**, which may differ in:
  - **Color**
  - **Shape** (optional, e.g., round, heart, long)
  - **Design** (e.g., plain, polka dot, striped)

💡 Implementation Guidelines:
- Show the player a **preview** of each balloon option.
- Let the player **click or press a button** to choose a style before starting the game.
- After selection, the balloon in the game should use the chosen style.
- Style changes can be implemented via different CSS classes, image assets, or canvas drawing styles.

---

### 💾 **2. Save and Load Game State (Using Local Storage):**

Implement **persistent data storage** using the browser’s `localStorage`:

- **Automatically save** the following after each game:
  - The player's **highest altitude score**
  - The **selected balloon theme**
  - (Optional) Whether sound/music was toggled, if applicable

- When the game is opened again:
  - Automatically **load and apply** the last selected balloon style.
  - Display the **highest score** on the Start or Score screen.

💡 Implementation Guidelines:
- Use `localStorage.setItem()` and `localStorage.getItem()` for saving and retrieving values.
- Ensure this functionality **does not interfere** with the current game logic.
- Provide fallbacks or defaults in case no saved data exists.

---

### 📘 **Integration Notes:**

- Continue to **preserve all features** from previous stages: core gameplay, scoring, UI screens, pause/resume, physics, difficulty progression, enemy AI, and sound.
- Make the **character selection and save/load system feel native** to the flow of the game (e.g., it should not disrupt the experience).
- **Comment the new code** thoroughly and maintain clean structure for further iteration or debugging.

⚠️ Important: Please provide the full updated `.html` file, including all HTML, CSS, and JavaScript, in every response, not just code snippets or notes."""]
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ])
        
        self.chat_map = {}
        
        self.pipeline = self.prompt_template | self.llm | StrOutputParser()
        
        self.pipeline_with_history = RunnableWithMessageHistory(
            self.pipeline,
            get_session_history=self.get_chat_history,
            input_messages_key="input",
            history_messages_key="history"
        )
    
    def get_chat_history(self, session_id: str) -> InMemoryChatMessageHistory:
        if session_id not in self.chat_map:
            self.chat_map[session_id] = InMemoryChatMessageHistory()
        return self.chat_map[session_id]
    
    def get_game_code(self, human_messages: List[str] = None) -> str:
        if human_messages is None:
            human_messages = self.human_messages
            
        for human_message in human_messages:
            result = self.pipeline_with_history.invoke({"input": human_message}, config={"session_id": "1"})
        
        return result
    