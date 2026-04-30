import os
import json
import anthropic
import time
from dotenv import load_dotenv

# ==========================================
# 1. INITIALIZATION & CONFIG
# ==========================================
load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Pathing based on your folder structure
BASE_CHALLENGE_DIR = "./blue-team_release/aes/"
# 2026 Flagship Model (Balanced for high context and lower cost)
CURRENT_MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """
You are a top-tier Hardware Security Expert. Audit the provided AES-128 Verilog code for stealthy hardware Trojans. 

### Audit Strategy:
1. Look for 'magic number' triggers (e.g., specific inputs like 0xDEADBEEF).
2. Look for 'leakage' logic (XORing keys with data, routing to extra pins).
3. Look for 'round skipping' or 'counter manipulation'.

### Output Constraints:
Return findings STRICTLY as a JSON object. If no Trojans are found, return an empty array for "trojans_detected".
Format for lines: Use hyphens for ranges (123-234) and commas for individual lines (123, 234).

{
  "trojans_detected": [
    {
      "confidence_score": 1-100,
      "files": "filename.v",
      "lines": "(line_range)",
      "vulnerability_type": "String",
      "explanation": "String"
    }
  ]
}
"""

# ==========================================
# 2. FILE HANDLING & AUDIT LOGIC
# ==========================================

def ingest_project_files(folder_path):
    """Recursively finds all RTL files (including src/rtl)."""
    combined_code = ""
    files_found = False
    for root, _, files in os.walk(folder_path):
        for filename in sorted(files):
            if filename.endswith(".v") or filename.endswith(".sv"):
                files_found = True
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, folder_path)
                combined_code += f"\n\n### FILE: {rel_path} ###\n"
                with open(filepath, 'r', encoding='utf-8') as f:
                    for idx, line in enumerate(f, start=1):
                        combined_code += f"{idx:04d} | {line}"
    return combined_code if files_found else None

def audit_instance_with_retry(instance_name, code_blob):
    """Executes audit with Exponential Backoff for Rate Limits (429)."""
    print(f"[*] Analyzing {instance_name}...")
    
    max_retries = 5
    wait_time = 30  # Start with 30s wait for 30k TPM limit

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=CURRENT_MODEL,
                max_tokens=4096,
                temperature=0.1,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": f"Audit {instance_name}:\n\n{code_blob}"}]
            )
            
            # Parse JSON safely
            raw_text = response.content[0].text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            return json.loads(raw_text)

        except anthropic.RateLimitError:
            print(f"  [!] Rate limit hit (429). Waiting {wait_time}s (Attempt {attempt+1}/{max_retries})...")
            time.sleep(wait_time)
            wait_time *= 2  # Double wait time for next retry
            
        except Exception as e:
            print(f"  [!] Permanent Error on {instance_name}: {e}")
            return None
            
    print(f"  [!] Failed {instance_name} after {max_retries} retries.")
    return None

# ==========================================
# 3. MAIN RUNNER
# ==========================================

def main():
    if not os.path.exists(BASE_CHALLENGE_DIR):
        print(f"[!] Path not found: {BASE_CHALLENGE_DIR}")
        return

    folders = sorted([d for d in os.listdir(BASE_CHALLENGE_DIR) 
                     if os.path.isdir(os.path.join(BASE_CHALLENGE_DIR, d))])

    # TESTING LIMIT: First 3 folders. Change to [:] to run all 44.
    test_set = folders[3:]
    results_log = []

    print(f"Starting audit on: {test_set}\n")

    for folder_name in test_set:
        full_path = os.path.join(BASE_CHALLENGE_DIR, folder_name)
        code_blob = ingest_project_files(full_path)
        
        if not code_blob:
            continue

        result = audit_instance_with_retry(folder_name, code_blob)
        
        if result:
            result['instance'] = folder_name
            results_log.append(result)
            
            if result.get("trojans_detected"):
                print(f"\n[🚨 ALERT] {folder_name} flagged!")
                for t in result["trojans_detected"]:
                    print(f"   - {t['vulnerability_type']} in {t['files']} at {t['lines']}")
            else:
                print(f"  [✓] {folder_name} passed.")

        # Delay between separate folder requests to stay under 30k TPM
        time.sleep(15)

    # Save results to a file for later review
    with open("audit_results.json", "w") as f:
        json.dump(results_log, f, indent=4)
    print(f"\nAudit complete. Results saved to audit_results.json")

if __name__ == "__main__":
    main()
