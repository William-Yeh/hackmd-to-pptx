# Troubleshooting Guide

Common issues and solutions when using the HackMD to PowerPoint converter.

## Formatting Issues

### Bullets Not Showing

**Problem:** Text appears without bullet points in the generated slides

**Cause:** Only lines starting with `-`, `*`, or `1.` get bullets. This is intentional design.

**Solution:**

Lines **with** bullets:
```markdown
## My Slide

- This gets a bullet ✓
* This also gets a bullet ✓
1. This gets numbered ✓
```

Lines **without** bullets:
```markdown
## My Slide

This is plain text (no bullet) ✓
Just regular paragraph text ✓
```

**Key Point:** If you want bullets, add `-` or `*` prefix. If you want plain text, don't use any prefix.

### Code Not Highlighted

**Problem:** Code blocks appear in monochrome without syntax highlighting

**Common Causes:**

1. **No language specified**

   ❌ Wrong:
   ````markdown
   ```
   def hello():
       return "world"
   ```
   ````

   ✅ Correct:
   ````markdown
   ```python
   def hello():
       return "world"
   ```
   ````

2. **Language not supported**

   Check if your language is in the supported list:
   - Python, JavaScript, TypeScript, Java, Kotlin, Scala, Haskell
   - Go, Rust, Ruby, Perl, PHP, SQL, Bash/Shell
   - YAML, JSON, HTML, C++, diff

   If not supported, see SYNTAX.md for how to add language support.

3. **Incorrect language name**

   Language names must be lowercase:

   ❌ Wrong: ` ```Python `, ` ```PYTHON `

   ✅ Correct: ` ```python `

**Solution:** Always specify the language in lowercase after the opening fence.

### Wrong Slide Layout Used

**Problem:** Section slide has bullet placeholder, or content slide uses title layout

**Cause:** Layout is chosen based on slide content structure

**Section Slide Rules:**
- Must have `# Title` (single #)
- Can have `### Subtitle` (triple ###)
- Should NOT have bullet points
- Plain text only

✅ Correct section slide:
```markdown
---
# Introduction
### Welcome to Our Presentation

This is a section slide with no bullets.
Just plain descriptive text.
```

❌ Wrong (will create content slide):
```markdown
---
# Introduction

- This has bullets
- So it becomes a content slide
```

**Content Slide Rules:**
- Use `## Title` (double ##)
- Can have bullets, code, lists
- Standard slide layout

✅ Correct content slide:
```markdown
----
## Key Features

- Feature one
- Feature two
- Feature three
```

### Inline Formatting Not Working

**Problem:** `**bold**`, `_italic_`, or `` `code` `` not rendering

**Common Causes:**

1. **Spaces around markers**

   ❌ Wrong: `** bold **`, `_ italic _`

   ✅ Correct: `**bold**`, `_italic_`

2. **Nested formatting conflicts**

   ❌ Complex: `**_bold italic_**` (may not work in all cases)

   ✅ Simple: `**bold**` or `_italic_` separately

3. **Code backticks with spaces**

   ❌ Wrong: `` ` code ` ``

   ✅ Correct: `` `code` ``

**Solution:** Ensure no spaces between markers and text.

### Checkboxes Not Rendering

**Problem:** `[ ]` and `[x]` appearing as literal text instead of ☐ and ☑

**Cause:** Incorrect spacing or format

✅ Correct:
```markdown
- [ ] Unchecked task
- [x] Completed task
```

❌ Wrong:
```markdown
- [] No space
- [X] Capital X
- [ x ] Spaces inside brackets
```

**Requirements:**
- Must be part of a bullet list (line starts with `-` or `*`)
- Exactly one space between brackets: `[ ]`
- Lowercase x for checked: `[x]`

### Hyperlinks Not Clickable

**Problem:** Links appear as plain text instead of clickable hyperlinks

**Cause:** Incorrect markdown link syntax

✅ Correct:
```markdown
[Click here](https://example.com)
[Link text](https://google.com)
```

❌ Wrong:
```markdown
(Click here)[https://example.com]  # Reversed
https://example.com  # Plain URL (not a markdown link)
[Click here] (https://example.com)  # Space between
```

**Note:** Plain URLs (without `[text](url)` syntax) are not auto-converted to links.

## Configuration Issues

### Configuration Not Applied

**Problem:** Custom colors or fonts not showing in output

**Common Causes:**

1. **Wrong file location**

   Config must be in the **same directory** as the markdown file:

   ✅ Correct:
   ```
   my-slides/
   ├── presentation.md
   └── config.json
   ```

   ❌ Wrong:
   ```
   project/
   ├── my-slides/
   │   └── presentation.md
   └── config.json  # Too far up
   ```

2. **Wrong filename**

   Must be exactly: `config.json`, `config.yaml`, or `config.yml`

   ❌ Wrong: `configuration.json`, `settings.json`, `theme.json`

3. **Invalid JSON/YAML syntax**

   Test with:
   ```bash
   # JSON
   python3 -m json.tool config.json

   # YAML
   python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

4. **Hex colors with # prefix**

   ❌ Wrong:
   ```json
   {
     "colors": {
       "accent": "#0891B2"
     }
   }
   ```

   ✅ Correct:
   ```json
   {
     "colors": {
       "accent": "0891B2"
     }
   }
   ```

   **Always omit the `#` prefix!**

5. **Invalid font names**

   Fonts must exist on the system. Test with:
   ```bash
   # List available fonts (macOS)
   fc-list : family | sort -u

   # Windows: Check C:\Windows\Fonts
   ```

   Common safe fonts:
   - **Cross-platform:** Arial, Courier New, Times New Roman
   - **Windows:** Calibri, Consolas, Trebuchet MS
   - **macOS:** Helvetica, Monaco, Menlo

### Colors Not Showing as Expected

**Problem:** Colors in slides don't match config values

**Debugging Steps:**

1. **Verify hex format**

   Must be 6-digit hex (RGB):
   - `RRGGBB` format
   - Valid chars: `0-9`, `A-F` (case insensitive)
   - No `#` prefix

   ✅ Valid: `0891B2`, `FF0000`, `1a2b3c`

   ❌ Invalid: `#0891B2`, `0891B`, `blue`

2. **Check if key names are correct**

   Valid color keys:
   ```json
   {
     "colors": {
       "accent": "0891B2",
       "codeBlock": "F1F5F9",
       "syntaxKeyword": "7C3AED",
       "syntaxString": "059669",
       "syntaxComment": "6B7280",
       "syntaxNumber": "DC2626",
       "syntaxFunction": "2563EB",
       "syntaxType": "D97706"
     }
   }
   ```

   ❌ Wrong key names: `accentColor`, `code-block`, `keyword_color`

3. **Verify config is being loaded**

   Add debug output:
   ```bash
   python convert.py input.md output.pptx --verbose  # if supported
   # Or check converter source to ensure config loading works
   ```

## Conversion Errors

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'pptx'`

**Cause:** python-pptx not installed

**Solution:**
```bash
pip install --user python-pptx lxml PyYAML
```

See SETUP.md for detailed installation instructions.

### "No such file or directory"

**Problem:** `FileNotFoundError: [Errno 2] No such file or directory: 'input.md'`

**Cause:** File path is incorrect or file doesn't exist

**Solutions:**

1. **Use absolute path:**
   ```bash
   python convert.py /full/path/to/slides.md /full/path/to/output.pptx
   ```

2. **Navigate to file directory:**
   ```bash
   cd /path/to/markdown/files
   python /path/to/convert.py slides.md output.pptx
   ```

3. **Verify file exists:**
   ```bash
   ls -la slides.md
   ```

### "Permission denied" When Saving PPTX

**Problem:** Cannot write output file

**Causes:**

1. **Output file is open in PowerPoint**

   Solution: Close PowerPoint and try again

2. **No write permissions in directory**

   Solution:
   ```bash
   # Check permissions
   ls -la output.pptx

   # Write to home directory instead
   python convert.py input.md ~/output.pptx
   ```

3. **Directory doesn't exist**

   Solution:
   ```bash
   mkdir -p output/
   python convert.py input.md output/slides.pptx
   ```

### Empty Output File

**Problem:** PPTX file is created but has 0 bytes or is corrupted

**Causes:**

1. **Conversion crashed mid-process**

   Check for error messages in terminal output

2. **Markdown file is empty or invalid**

   Verify markdown has content:
   ```bash
   cat input.md
   ```

3. **Disk full**

   Check disk space:
   ```bash
   df -h .
   ```

### Slides Missing from Output

**Problem:** Some slides don't appear in the generated PPTX

**Common Causes:**

1. **Incorrect separator usage**

   Use `---` for sections, `----` for slides:
   ```markdown
   ---
   # Section 1

   ----
   ## Slide 1

   ----
   ## Slide 2
   ```

2. **Empty slides**

   Slides with no title or content are skipped:

   ❌ Will be skipped:
   ```markdown
   ----


   ----
   ```

   ✅ Will be included:
   ```markdown
   ----
   ## Title Required

   Content optional but title required.
   ```

3. **YAML frontmatter not stripped**

   If markdown starts with `---` frontmatter, it might be incorrectly parsed:

   Solution: Remove frontmatter or use `----` instead:
   ```markdown
   ---
   title: My Presentation
   ---

   # First Slide  # This might be skipped
   ```

## Slide Master Issues

### Changes to Slide Master Not Applying

**Problem:** Edited slide master but slides don't update

**Cause:** Not all content uses placeholders, or layout was changed

**Solutions:**

1. **Verify placeholder usage**
   - Title: Uses placeholder
   - Body text: Uses placeholder
   - Code blocks: NOT placeholder (direct shapes)

2. **Reapply layout**
   - Right-click slide → Layout → Reapply current layout

3. **Regenerate from markdown**
   - If major changes needed, reconvert markdown

### Slide Master Shows Different Fonts

**Problem:** Slide master font doesn't match what's in slides

**Cause:** Fonts are set programmatically during conversion, not via slide master

**Solution:**

1. **Option A:** Edit slide master for NEW content
   - Slide master affects content added in PowerPoint later
   - But not content generated during conversion

2. **Option B:** Change config and reconvert
   - Modify `config.json` fonts
   - Reconvert markdown to PPTX

## Performance Issues

### Slow Conversion

**Problem:** Conversion takes a long time for large presentations

**Causes:**

1. **Many code blocks**
   - Syntax highlighting is computationally intensive
   - Each code block creates multiple text runs

2. **Large markdown file**
   - 100+ slides can take 10-30 seconds

**Solutions:**

1. **Split large presentations:**
   ```bash
   # Convert chapters separately
   python convert.py chapter1.md ch1.pptx
   python convert.py chapter2.md ch2.pptx
   # Merge in PowerPoint
   ```

2. **Disable syntax highlighting temporarily:**
   - Use plain code fences (no language)
   - Add language only for final version

3. **Use faster hardware:**
   - SSD vs HDD makes a difference
   - More RAM helps with large files

## Platform-Specific Issues

### macOS: "Operation not permitted"

**Cause:** Gatekeeper or SIP restrictions

**Solution:**
```bash
# Use user install
pip install --user python-pptx lxml PyYAML

# Or allow Terminal in Security & Privacy settings
```

### Windows: "Python not found"

**Cause:** Python not in PATH

**Solution:**
1. Reinstall Python with "Add to PATH" checked
2. Or use full path:
   ```powershell
   C:\Python38\python.exe convert.py input.md output.pptx
   ```

### Linux: "lxml install fails"

**Cause:** Missing system dependencies for lxml

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install python3-dev libxml2-dev libxslt1-dev

# Fedora/RHEL
sudo dnf install python3-devel libxml2-devel libxslt-devel

# Then retry
pip install --user lxml
```

## Still Having Issues?

1. **Check the examples:**
   ```bash
   python convert.py examples/demo.md test.pptx
   ```
   If this works, the issue is in your markdown.

2. **Validate your markdown:**
   - Check syntax against examples/demo.md
   - Ensure proper separator usage
   - Verify code block language names

3. **Enable debugging:**
   - Run with verbose output (if available)
   - Check terminal for error messages
   - Examine generated PPTX in PowerPoint

4. **Report an issue:**
   - Include markdown file (or minimal reproduction)
   - Include config file (if used)
   - Include error messages from terminal
   - Include Python version: `python3 --version`
   - Include OS: macOS/Windows/Linux version

See SETUP.md for installation help and SYNTAX.md for markdown reference.
