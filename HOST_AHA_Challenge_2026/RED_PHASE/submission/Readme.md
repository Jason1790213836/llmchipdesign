

# AHA (Adaptive Hardware Attack) Pipeline Report

This document details the methodology, tools, and strategic frameworks used to architect the **AHA (Adaptive Hardware Attack) Pipeline**[cite: 83, 84]. [cite_start]The core objective was to move beyond manual code editing and instead use AI as an **Automated Hardware Security Architect** capable of identifying injection points, justifying attack stealth, and generating synthesis-ready hardware Trojans[cite: 85].

## AI Methodology & Framework

### 1. Interaction Method: Direct API Integration
[cite_start]Unlike a standard chat interface (Web UI), this project utilized a **headless Python-driven pipeline** interacting directly with the **OpenAI API**[cite: 88].
* [cite_start]**Model Used**: `gpt-4o` (Omni)[cite: 89].
* [cite_start]**Reasoning**: `gpt-4o` was chosen for its high reasoning capabilities in Verilog RTL syntax and its ability to understand complex Abstract Syntax Trees (AST)[cite: 90].
* [cite_start]**Execution**: The AI acted as a "Stealth Consultant" within an automated loop[cite: 91]. [cite_start]The Python script fed code structures to the AI, which returned technical justifications and optimized logic strings[cite: 92].

### 2. Supporting Framework: The AST Hybrid Approach
[cite_start]To ensure modifications were precise, we wrapped the AI around a **Static Analysis Framework**[cite: 94]:
* [cite_start]**PyVerilog (AST Parsing)**: We used PyVerilog to convert the `aes_core.v` file into an Abstract Syntax Tree[cite: 95].
* [cite_start]**Signal Discovery**: A recursive search algorithm walked the AST to find specific hardware targets like the `ready` signal or internal registers[cite: 96].
* [cite_start]**Context Injection**: Instead of sending the entire codebase, we sent only the **relevant AST nodes**[cite: 97]. [cite_start]This provided the AI with a "map" of the hardware to choose the most stealthy injection point[cite: 98].

---

## Trojan Evolution & AI Creative Logic

[cite_start]The AI progressed through three distinct "generations" of Trojan design to optimize the **PPA (Power, Performance, Area)** profile and stealth[cite: 99, 100].

### Generation 1: 32-Bit Logic Leakage Trigger
* [cite_start]**AI Strategy**: Implement a basic logic hijack on the output bus[cite: 102].
* [cite_start]**Trigger Mechanism**: The AI chose a 32-bit partial-match trigger: `block[31:0] == 32'hDEADBEEF`[cite: 103].
* [cite_start]**Payload**: When triggered, the ciphertext is XORed with the secret key[cite: 104].
* [cite_start]**Result**: The output appears as valid high-entropy noise to a casual observer, but the attacker can extract the key by simply XORing the "garbage" ciphertext with the known trigger word[cite: 105].

### Generation 2: Stealth DFA (Differential Fault Analysis)
* [cite_start]**AI Strategy**: Transition from data leakage to **Differential Fault Analysis**[cite: 107].
* [cite_start]**Creative Twist**: Instead of leaking the whole key, the AI identified critical AES rounds (e.g., Round 9) to inject a single-bit fault[cite: 108].
* [cite_start]**Stealth Factor**: This requires significantly less area than a full XOR mask[cite: 109]. [cite_start]The attack is only visible when the specific trigger word and the specific clock cycle align, making it nearly impossible to find using standard NIST test vectors[cite: 110].

### Generation 3: "Hardware Ghost" (Probability Side-Channel)
* [cite_start]**AI Strategy**: For ultimate stealth, the AI proposed a **Probability-based Side-Channel Power Leakage Trojan**[cite: 112].
* [cite_start]**The Logic**: The AI injected a "Dummy Load" toggling signal that does not hijack the `result` bus[cite: 113].
* **Stealth Factor**: 
    * **Functional**: 0% change in output; [cite_start]100% NIST test pass rate[cite: 114].
    * [cite_start]**PPA**: Area overhead is negligible (approx. 0.001%), appearing as noise in PPA reports[cite: 115].
    * [cite_start]**Detection**: Since the key bits are leaked via **Power Analysis (DPA)** or EM emissions based on switching probabilities, the Trojan is invisible to digital formal verification tools[cite: 116].

---

## Execution Workflow

1.  [cite_start]**Step 1: Deep Analysis**: The script uses PyVerilog to extract every signal name from the AES core[cite: 118].
2.  [cite_start]**Step 2: AI Strategic Prompting**: The AI selects a target from the signals (e.g., choosing `ready` over `clk` for lower switching visibility)[cite: 119].
3.  [cite_start]**Step 3: Synthesis-Friendly Injection**: The Python script uses an AI-guided replacement to insert the Trojan logic before the `endmodule` statement[cite: 120].
4.  [cite_start]**Step 4: Automated Verification**: The AI generates a custom Testbench (`tb_stealth_trigger.v`) that verifies the key leakage through XOR math[cite: 121].

---

## Summary of AI "Creativity" Points
* [cite_start]**Dynamic Adaptation**: The AI adapted the attack based on whether the AST revealed a "round counter" or a "state machine"[cite: 123].
* [cite_start]**PPA Awareness**: The AI actively minimized the gate count to stay below the 0.5% detection threshold[cite: 124].
* [cite_start]**Multi-Domain Attack**: Shifting the attack from the **Digital Domain** (logic corruption) to the **Physical Domain** (power leakage)[cite: 125].

> [cite_start]**Note on Security**: All API interactions were performed using environment variables, and all generated code was sandboxed in a separate build directory to prevent contamination of the source RTL[cite: 126].