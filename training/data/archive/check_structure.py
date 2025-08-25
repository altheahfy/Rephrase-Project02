import json

print("=== JSON構造確認 ===")

with open('official_test_results.json', 'r', encoding='utf-8') as f:
    current = json.load(f)
print('Current type:', type(current))
print('Current length:', len(current) if hasattr(current, '__len__') else 'N/A')

with open('backup_100_percent_baseline.json', 'r', encoding='utf-8') as f:
    baseline = json.load(f)
print('Baseline type:', type(baseline))
print('Baseline length:', len(baseline) if hasattr(baseline, '__len__') else 'N/A')

print("\n=== Current structure sample ===")
if isinstance(current, list) and len(current) > 0:
    print("List structure - First item:", type(current[0]))
    print("Sample keys:", list(current[0].keys()) if isinstance(current[0], dict) else "Not dict")
elif isinstance(current, dict):
    print("Dict structure - Keys:", list(current.keys()))
else:
    print("Unknown structure")
