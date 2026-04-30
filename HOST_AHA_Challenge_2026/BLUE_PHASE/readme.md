# README: Automated Semantic Auditing for Hardware Trojan Detection

## IEEE HOST 2026 AI Hardware Attack (AHA!) Challenge — Blue Team Submission

---

## 1. Architectural Philosophy: Zero-Knowledge Semantic Auditing

Our submission utilizes a **Zero-Knowledge Semantic Auditing Pipeline**, a framework designed to identify hardware Trojans within RTL (Register Transfer Level) designs without reliance on a "Golden Model" or forbidden `diff`-based methodologies.

Traditional detection often relies on structural comparisons; however, our approach leverages the high-order reasoning of 2026-era Large Language Models (LLMs) to perform **Functional Verification**. By treating the RTL as a mathematical realization of the AES-128 algorithm, the framework identifies logic that deviates from the cryptographic specification (NIST FIPS 197) or exhibits suspicious behavioral patterns inconsistent with standard encryption workflows.

## 2. Interaction Methodology & API Integration

To maintain strict adherence to the "No Manual Analysis" rule and ensure results are reproducible and scalable across 44 instances, we bypassed web-based UI interactions in favor of a **Programmatic Verification Layer**.

- **SDK/Interface:** Anthropic Python SDK.

- **Systematic Batch Processing:** The framework automatically iterates through the challenge directory, ingests the source code, and manages the auditing lifecycle without human intervention.

- **Audit Traceability:** Every detection is accompanied by an automated log of the exact prompt-response pair, ensuring a verifiable chain of evidence for the identified vulnerabilities.

## 3. Model Configuration: Claude Sonnet 4.6

For the primary auditing engine, we selected **claude-sonnet-4-6 (Release 2026)**.

- **Contextual Depth:** The model’s **1M-token context window** is critical for hardware security. It allows the entire AES core (including sub-modules like S-Boxes, Key Expansion, and State Machines) to be analyzed as a single unified entity. This enables the AI to correlate triggers located in the **Control Path** with malicious payloads hidden in the **Data Path**.

- **HDL Reasoning:** Sonnet 4.6 demonstrates superior understanding of non-blocking assignments, signal sensitivity lists, and combinatorial loops—frequent areas where stealthy Trojans are implanted to avoid detection by standard linting tools.

## 4. Automation Infrastructure & Resilience

The detection pipeline is built on a robust software engineering foundation to ensure deterministic output:

### A. Pre-processing & Source Annotation

Prior to ingestion, the RTL files are automatically parsed and **line-numbered**. This metadata allows the AI to provide high-precision localization, meeting the competition’s requirement for specific line-range reporting.

### B. Deterministic Schema Enforcement

The AI is constrained by a **Strict JSON Schema**. By enforcing a machine-readable output format, we eliminate "hallucinations" and conversational filler, ensuring the extraction of:

- `vulnerability_type`

- `confidence_score`

- `precise_line_localization`

- `technical_rationale`

### C. Throughput Resilience (Error 429 Management)

To manage the high token volume required for 44 AES instances, the framework implements an **Exponential Backoff Algorithm**. This ensures that the pipeline handles Rate Limit errors (429) gracefully, maintaining maximum throughput and preventing script termination during large-scale audits.

## 5. Detection Heuristics (Algorithmic Verification)

Following the "No-Diff" mandate, the AI performs **Semantic Anomaly Detection** by evaluating the code against three primary security pillars:

- **Trigger Heuristics:** Identifying non-standard comparators, redundant counters, or "magic number" sequence detectors (e.g., `0xDEADBEEF`) that exist outside the legitimate AES state machine transitions.

- **Payload Analysis:** Detecting unauthorized multiplexers or signal redirections that XOR secret key material with plaintext or route internal state bits to primary output ports.

- **Cryptographic Compliance:** Validating the mathematical integrity of the S-Box transformations and Round Key generation against **NIST SP 800-38A**. Any logic that provides a "bypass" or "short-circuit" to the standard 10-round requirement is flagged as a high-severity vulnerability.

## 6. Conclusion

The methodology presented herein demonstrates that AI-driven semantic analysis is a viable, scalable alternative to traditional hardware verification. By automating the auditing of 44 complex instances, we prove that a well-architected AI framework can achieve a level of coverage and "Engineering Rigor" that is impossible through manual human review alone, while strictly respecting the constraints of the HOST 2026 AHA! Challenge.
