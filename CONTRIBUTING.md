# Contributing to Memory Demo Harness

Thanks for your interest in contributing!

## How to Contribute

### Reporting Issues
- Check existing issues first
- Provide clear reproduction steps
- Include error messages and screenshots
- Specify your environment (OS, Python version, etc.)

### Suggesting Features
- Describe the use case
- Explain the expected behavior
- Consider backward compatibility

### Submitting Pull Requests

1. **Fork and clone**
   ```bash
   git clone https://github.com/your-username/memory-demo-harness
   cd memory-demo-harness
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Make changes**
   - Write clear, documented code
   - Add tests for new features
   - Update documentation

4. **Test**
   ```bash
   python tests/test_basic.py
   python tests/test_judge.py
   python tests/test_highlighting.py
   ```

5. **Commit**
   ```bash
   git commit -m "feat: Add support for X"
   ```

   Use conventional commits:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `test:` - Tests
   - `refactor:` - Code refactoring

6. **Push and create PR**
   ```bash
   git push origin feature/my-feature
   ```

## Areas for Contribution

### High Priority
- **Memory backend integrations**
  - mem0 support
  - Zep integration
  - LangChain memory adapters
  
- **Agent backend support**
  - LangChain LLM wrapper
  - LlamaIndex integration
  - Local model support (Ollama, etc.)

### Medium Priority
- **UI improvements**
  - Export to markdown/CSV
  - Conversation replay mode
  - Token cost calculator
  - Multi-persona comparison

### Documentation
- More example configurations
- Video walkthroughs
- Blog posts/tutorials
- Translation to other languages

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set API key
cp .env.example .env
# Edit .env with your API key

# Run tests
python tests/test_basic.py

# Run app
streamlit run app.py
```

## Code Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small
- Add comments for non-obvious logic

## Testing

- All new features need tests
- Tests should be fast and isolated
- Use descriptive test names
- Mock external API calls

## Documentation

- Update README.md for new features
- Add docstrings to new functions
- Create docs in `docs/` for complex features
- Update examples in `examples/`

## Adding a Memory Backend

1. **Implement the protocol** in `memory_backends.py`:
   ```python
   class MyBackend(MemoryBackend):
       def recall(self, query, history) -> str:
           ...
       def store(self, user_msg, assistant_msg, history):
           ...
       def clear_session(self):
           ...
   ```

2. **Register in factory**:
   ```python
   def create_memory_backend(config, ...):
       if config["type"] == "my_backend":
           return MyBackend(config)
   ```

3. **Add example config** in `examples/my_backend.yaml`

4. **Update README** with integration details

5. **Add tests** in `tests/test_my_backend.py`

## Questions?

- Open a [discussion](https://github.com/your-org/memory-demo-harness/discussions)
- Join our community chat (TBD)
- Email maintainers (TBD)

## Code of Conduct

Be respectful, inclusive, and collaborative. We're all here to learn and build together.
