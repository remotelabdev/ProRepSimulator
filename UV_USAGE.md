# Using UV with ProRepSimulator

## Quick Start with UV

`uv` is a fast Python package installer and environment manager. Here's how to use it with this project:

### Method 1: Using `uv run` (Simplest - Recommended)

```bash
# Run visualization directly (uv handles everything automatically)
uv run visualize_openlist.py

# Run demo
uv run demo_openlist.py

# Run Jupyter notebook
uv run jupyter notebook openlist_demo.ipynb
```

**What `uv run` does:**
- Automatically creates a virtual environment if needed
- Installs dependencies from `requirements.txt`
- Runs your script
- All in one command!

### Method 2: Manual Environment Setup

```bash
# 1. Create virtual environment
uv venv

# 2. Activate it
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Run scripts
python visualize_openlist.py
python demo_openlist.py
```

### Method 3: System-wide Installation (Not Recommended)

```bash
# Install dependencies system-wide
uv pip install --system matplotlib numpy jupyter

# Run scripts
python3 visualize_openlist.py
```

## UV vs PIP Comparison

| Task | PIP | UV |
|------|-----|-----|
| Create venv | `python -m venv .venv` | `uv venv` |
| Install package | `pip install matplotlib` | `uv pip install matplotlib` |
| Install from file | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Run script | Need manual activation + install | `uv run script.py` |
| Speed | Normal | **10-100x faster!** |

## Common UV Commands

```bash
# Create virtual environment
uv venv

# Install single package
uv pip install matplotlib

# Install from requirements.txt
uv pip install -r requirements.txt

# Run script with auto-install
uv run visualize_openlist.py

# Run Python REPL with dependencies
uv run python
```

## Troubleshooting

### "No virtual environment found"

**Solution**: Either create one with `uv venv` or use `uv run`:

```bash
# Option A: Create venv first
uv venv
uv pip install matplotlib numpy

# Option B: Just use uv run (easier)
uv run visualize_openlist.py
```

### "Network timeout" during installation

**Solution**: Increase timeout:

```bash
UV_HTTP_TIMEOUT=120 uv pip install matplotlib numpy
```

### Dependencies not found when running script

**Solution**: Make sure virtual environment is activated:

```bash
source .venv/bin/activate
python visualize_openlist.py
```

Or use `uv run`:

```bash
uv run visualize_openlist.py
```

## Why Use UV?

1. **Speed**: 10-100x faster than pip
2. **Simplicity**: `uv run` handles everything automatically
3. **Reliability**: Better dependency resolution
4. **Modern**: Built in Rust, actively maintained

## Example: Running Visualizations

```bash
# Fastest way (one command, auto-install):
uv run visualize_openlist.py

# Alternative (manual setup):
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python visualize_openlist.py
```

## Project Dependencies

This project requires:
- `matplotlib` - For creating charts
- `numpy` - For numerical calculations
- `jupyter` - For interactive notebooks (optional)

All listed in `requirements.txt`.

## Next Steps

Try running the demo:

```bash
uv run demo_openlist.py
```

Then generate visualizations:

```bash
uv run visualize_openlist.py
```

---

**TIP**: Use `uv run` for the simplest experience - it handles virtual environments and dependencies automatically!
