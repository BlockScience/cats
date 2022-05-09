# Usage: Basic CAT Chain
**Steps:**
1. Open 2 terminal sessions
2. **CAT0: terminal session A** Content-Address Dataset and create initial BOM given s3 URIs
```bash
python apps/cat0/execute.py
```
3. **CAT1: terminal session B** Content-Address Transform Dataset given CAT0 BOM
```bash
python apps/cat1/execute.py
```