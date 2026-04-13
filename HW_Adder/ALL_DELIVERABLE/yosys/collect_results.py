import csv

# Manually enter your best final results from each run
results = [
    {
        "Starting Architecture": "CLA8",
        "Optimization Mode": "Delay",
        "Final Cells": 42,
        "Final Logic Delay": 168.33,
        "Final Area (um²)": 73.948,
        "Architecture Identified": "CLA"
    },
    {
        "Starting Architecture": "RCA8",
        "Optimization Mode": "Balanced",
        "Final Cells": 44,
        "Final Logic Delay": 216.09,
        "Final Area (um²)": 57.722,
        "Architecture Identified": "RCA"
    }
]

# Print markdown table
headers = [
    "Starting Architecture",
    "Optimization Mode",
    "Final Cells",
    "Final Logic Delay",
    "Final Area (um²)",
    "Architecture Identified"
]

print("| " + " | ".join(headers) + " |")
print("|" + "|".join(["---"] * len(headers)) + "|")

for row in results:
    print("| " + " | ".join(str(row[h]) for h in headers) + " |")

# Save CSV file
with open("final_summary_table.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(results)

print("\nSaved to final_summary_table.csv")