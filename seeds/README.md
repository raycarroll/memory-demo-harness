# Persona Seed Files

Pre-populated memory files for different user personas.

## Format

```
# Comments start with #
User is a Senior Data Scientist named Alex Chen
User prefers Python over R
User works in ML Ops on Kubernetes
...
```

- One fact per line
- Lines starting with `#` are ignored
- Empty lines are ignored
- Facts are loaded when persona is selected

## Available Personas

### Data Scientist (`data-scientist.txt`)
- Name: Alex Chen
- Role: Senior Data Scientist
- Focus: ML Ops, Python, Kubernetes
- 13 pre-populated facts

### SRE On-call Engineer (`oncall-engineer.txt`)
- Name: Jordan Lee
- Role: Site Reliability Engineer
- Focus: Incident response, CLI tools, Kubernetes
- 14 pre-populated facts

### Full-stack Developer (`developer.txt`)
- Name: Sam Rodriguez
- Role: Full-stack Developer
- Focus: Python/TypeScript, React, FastAPI
- 14 pre-populated facts

## Usage in UI

1. Select a persona from the "User Persona" dropdown
2. Click "🔄 New Session" to load the seed file
3. The left agent (with memory) will have access to all pre-loaded facts
4. Start asking questions immediately

## Creating New Personas

```bash
# Create a new seed file
cat > seeds/my-persona.txt << 'EOF'
# My Custom Persona
User is a <role> named <name>
User prefers <preference>
...
EOF
```

Then add to `config.yaml`:

```yaml
personas:
  my-persona:
    name: "<Name> - <Role>"
    description: "Brief description"
    seed_file: ./seeds/my-persona.txt
```

## Tips

- Keep facts concise and specific
- Start with identity facts (name, role)
- Add preferences and constraints
- Include relevant tools/technologies
- Add context about current projects
- 10-15 facts is a good starting point
