# Setup Guide

Complete installation and environment setup instructions for the HackMD to PowerPoint converter.

## Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Dependencies:** python-pptx, lxml, PyYAML

## Installation Methods

### Option 1: User Installation (Recommended)

Install dependencies to your user directory without requiring admin/sudo:

```bash
pip install --user python-pptx lxml PyYAML
```

**Advantages:**
- No admin/sudo required
- Won't affect system Python
- Works on restricted systems

**Note:** Ensure `~/.local/bin` (Linux/macOS) or `%APPDATA%\Python\Scripts` (Windows) is in your PATH.

### Option 2: Virtual Environment

Create an isolated Python environment for this project:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# When done, deactivate
deactivate
```

**Advantages:**
- Complete isolation from system Python
- Easy to delete and recreate
- Recommended for development

**Disadvantage:**
- Must activate environment before each use

### Option 3: System-Wide Installation

Install dependencies globally (requires admin/sudo):

```bash
# Linux/macOS
sudo pip3 install python-pptx lxml PyYAML

# Windows (as Administrator)
pip install python-pptx lxml PyYAML
```

**Advantages:**
- Available system-wide
- No activation needed

**Disadvantages:**
- Requires admin privileges
- May conflict with other Python packages
- Not recommended for shared systems

### Option 4: Using uv (Fast)

If you have [uv](https://github.com/astral-sh/uv) installed:

```bash
uv pip install python-pptx lxml PyYAML
```

**Advantages:**
- Much faster than pip
- Modern package resolver
- Good for development

### Option 5: Using pipx (For Tools)

If using pipx (for tools, not libraries):

```bash
# Create environment
pipx install --editable .
```

Note: This is less common for converter tools.

## Verification

After installation, verify everything works:

```bash
# Check Python version
python3 --version
# Should show 3.8.x or higher

# Check dependencies
python3 -c "import pptx; print('python-pptx:', pptx.__version__)"
python3 -c "import lxml; print('lxml:', lxml.__version__)"
python3 -c "import yaml; print('PyYAML: OK')"

# Test basic conversion
python scripts/convert.py examples/demo.md test-output.pptx

# Verify output file exists
ls -lh test-output.pptx
```

If all commands succeed, installation is complete.

## Environment-Specific Setup

### macOS

```bash
# Install Python 3 if needed (via Homebrew)
brew install python3

# Install dependencies
pip3 install --user python-pptx lxml PyYAML

# Add user bin to PATH if not already
echo 'export PATH="$HOME/Library/Python/3.x/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3 and pip if needed
sudo apt update
sudo apt install python3 python3-pip

# Install dependencies
pip3 install --user python-pptx lxml PyYAML

# Add user bin to PATH if not already
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Linux (Fedora/RHEL/CentOS)

```bash
# Install Python 3 and pip if needed
sudo dnf install python3 python3-pip

# Install dependencies
pip3 install --user python-pptx lxml PyYAML

# Add user bin to PATH if not already
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Windows

```powershell
# Install Python 3 from python.org if needed
# https://www.python.org/downloads/

# Install dependencies
pip install python-pptx lxml PyYAML

# Verify installation
python --version
python -c "import pptx; print('python-pptx OK')"
```

## Configuration Setup

### Creating Configuration Files

Place configuration files in the same directory as your markdown files:

```bash
# Create config.json
cat > config.json << 'EOF'
{
  "colors": {
    "accent": "0891B2",
    "codeBlock": "F1F5F9"
  },
  "fonts": {
    "header": "Arial",
    "body": "Calibri",
    "code": "Consolas"
  }
}
EOF
```

Or copy from examples:

```bash
cp examples/config.json .
# Edit as needed
```

### Configuration File Location

The converter looks for config files in this order:

1. `config.json` in markdown file directory
2. `config.yaml` in markdown file directory
3. `config.yml` in markdown file directory
4. Default values (built into convert.py)

### Testing Configuration

```bash
# Create test markdown with config
echo '## Test Slide

- This is a test
- With `inline code`' > test.md

# Create custom config
echo '{
  "colors": {
    "accent": "FF0000"
  }
}' > config.json

# Convert
python scripts/convert.py test.md

# Open and verify accent color is red
open test.pptx  # macOS
```

## Common Issues

### "No module named 'pptx'"

**Cause:** python-pptx not installed

**Solution:**
```bash
pip install --user python-pptx
```

### "No module named 'lxml'"

**Cause:** lxml not installed

**Solution:**
```bash
pip install --user lxml
```

### "No module named 'yaml'"

**Cause:** PyYAML not installed (only needed for YAML configs)

**Solution:**
```bash
pip install --user PyYAML
```

Or use JSON config files instead.

### "pip: command not found"

**Cause:** pip not in PATH or not installed

**Solution:**
```bash
# macOS/Linux
python3 -m pip install --user python-pptx lxml PyYAML

# Windows
python -m pip install python-pptx lxml PyYAML
```

### "Permission denied"

**Cause:** Trying to install system-wide without permissions

**Solution:** Use `--user` flag:
```bash
pip install --user python-pptx lxml PyYAML
```

### Virtual environment not activating

**Cause:** Wrong activation command for your shell

**Solutions:**
```bash
# bash/zsh (most Linux/macOS)
source venv/bin/activate

# fish shell
source venv/bin/activate.fish

# csh/tcsh
source venv/bin/activate.csh

# Windows Command Prompt
venv\Scripts\activate.bat

# Windows PowerShell
venv\Scripts\Activate.ps1
```

### Python 2 vs Python 3

If `python` points to Python 2:

```bash
# Always use python3 explicitly
python3 convert.py input.md output.pptx

# Or create alias
alias python=python3
```

## Advanced Setup

### Pre-commit Hooks

Automatically validate markdown before committing:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: validate-markdown
        name: Validate Markdown Syntax
        entry: python
        language: system
        args: [scripts/validate-markdown.py]
        files: \.md$
EOF

# Install hooks
pre-commit install
```

### Editor Integration

#### VS Code

Install extensions:
- **Markdown All in One** - Markdown preview
- **markdownlint** - Syntax checking
- **Python** - Python support

#### Vim/Neovim

```vim
" Add to .vimrc
autocmd FileType markdown setlocal spell
autocmd FileType markdown setlocal textwidth=80
```

### Batch Processing Script

Create a script to convert multiple files:

```bash
#!/bin/bash
# convert-all.sh

for md_file in *.md; do
    output_file="${md_file%.md}.pptx"
    echo "Converting $md_file -> $output_file"
    python scripts/convert.py "$md_file" "$output_file"
done
```

Make executable:
```bash
chmod +x convert-all.sh
./convert-all.sh
```

## Updating

To update dependencies:

```bash
# Update all packages
pip install --upgrade python-pptx lxml PyYAML

# Or using requirements.txt
pip install --upgrade -r requirements.txt
```

To update the converter itself:

```bash
# If installed from git
git pull origin main

# Then test
python scripts/convert.py examples/demo.md test.pptx
```

## Uninstallation

### Remove Dependencies

```bash
pip uninstall python-pptx lxml PyYAML
```

### Remove Virtual Environment

```bash
rm -rf venv/
```

### Remove Converter

```bash
# If installed locally
rm -rf /path/to/hackmd-to-pptx/

# If linked in PATH
rm ~/.local/bin/convert.py  # or wherever symlinked
```

## Next Steps

After successful setup:

1. **Read SKILL.md** - Learn markdown syntax and features
2. **Try examples** - Convert `examples/demo.md`
3. **Create your slides** - Start with example as template
4. **Customize themes** - Create config.json for branding

See **TROUBLESHOOTING.md** for common issues and **SYNTAX.md** for complete markdown reference.
