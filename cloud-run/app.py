from pathlib import Path

print("=" * 80)
print("REGISTRY FILES")
print("=" * 80)

registry_path = Path(__file__).resolve().parent / "registry" / "gcp"

print(registry_path)

if registry_path.exists():
    for f in registry_path.glob("*.yaml"):
        print(f.name)
else:
    print("Registry folder not found")