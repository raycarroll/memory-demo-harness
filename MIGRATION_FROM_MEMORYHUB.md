# Migration from MemoryHub Repo

This tool was originally developed as a demo within the [MemoryHub](https://github.com/redhat-et/memory-hub) project and has been extracted as a standalone repository.

## What Changed

### Repository Structure
**Before:** `memory-hub/demos/memory-comparison/`  
**After:** Standalone `memory-demo-harness/` repo

### Scope
**Before:** MemoryHub-specific demo  
**After:** General-purpose memory comparison tool supporting any backend

### MemoryHub Integration
**Before:** Tightly coupled  
**After:** MemoryHub is one of many supported backends (see `examples/memoryhub.yaml`)

## For MemoryHub Users

### Using This Tool with MemoryHub

1. **Clone this repo**
   ```bash
   git clone https://github.com/your-org/memory-demo-harness
   cd memory-demo-harness
   ```

2. **Configure MemoryHub backend**
   ```bash
   cp examples/memoryhub.yaml config.yaml
   ```

3. **Set MemoryHub credentials**
   ```bash
   export MEMORYHUB_API_KEY="mh-..."
   export MEMORYHUB_URL="http://localhost:8080/mcp/"
   ```

4. **Run**
   ```bash
   streamlit run app.py
   ```

### Example Configuration

```yaml
# config.yaml
memory:
  memoryhub:
    type: memoryhub
    url: ${MEMORYHUB_URL}
    api_key: ${MEMORYHUB_API_KEY}
    user_id: demo-user
```

## For Contributors

### History Preserved
The original development history is in the MemoryHub repo under `demos/memory-comparison/`.

### Attribution
This tool was created as part of the MemoryHub project. See:
- Original: https://github.com/redhat-et/memory-hub/tree/main/demos/memory-comparison
- Planning: https://github.com/redhat-et/memory-hub/blob/main/planning/memory-demo-harness.md

### License
Same MIT license as original MemoryHub project.

## Cross-References

### In MemoryHub Docs
```markdown
## Demos
See [memory-demo-harness](https://github.com/your-org/memory-demo-harness)
for interactive side-by-side comparison demos.
```

### In This Repo
```markdown
## MemoryHub Integration
Example configuration: [examples/memoryhub.yaml](examples/memoryhub.yaml)
Learn more: [MemoryHub](https://github.com/redhat-et/memory-hub)
```
