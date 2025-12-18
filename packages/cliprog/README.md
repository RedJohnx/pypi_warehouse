# cliprog 📊

Lightweight CLI progress bars for Python.

## Installation

```bash
pip install cliprog
```

## Usage

### Simple Iterator Wrapper

```python
from cliprog import progress

for item in progress(items, desc="Processing"):
    process(item)

# Works with range
for i in progress(range(100)):
    do_work(i)
```

### Manual Progress Bar

```python
from cliprog import ProgressBar

bar = ProgressBar(total=100, desc="Downloading")
for chunk in download():
    save(chunk)
    bar.update(1)
bar.close()
```

### Spinner

```python
from cliprog import spinner

spin = spinner("Loading data")
for _ in range(10):
    spin.update()
    time.sleep(0.1)
spin.done("Data loaded!")
```

## Output Examples

```
Processing [████████████████░░░░░░░░░░░░░░░░░░░░░░░░]  42.0% 42/100 ETA: 12s
```

## Customization

```python
bar = ProgressBar(
    total=100,
    desc="Custom",
    width=30,          # Bar width
    fill="▓",          # Filled character
    empty="░",         # Empty character
    show_percent=True, # Show percentage
    show_count=True,   # Show current/total
    show_eta=True,     # Show time remaining
)
```

## License

MIT
