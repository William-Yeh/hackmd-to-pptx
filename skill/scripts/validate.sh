#!/usr/bin/env bash
#
# Validate HackMD to PowerPoint AgentSkills.io Skill
#
# Checks:
# - SKILL.md exists with valid frontmatter
# - Required frontmatter fields are present and valid
# - Directory structure follows agentskills.io format
# - Python dependencies are installed
# - Documentation files exist
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==================================="
echo "AgentSkills.io Validator"
echo "hackmd-to-pptx skill"
echo "==================================="
echo

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

errors=0
warnings=0

# Check SKILL.md existence
echo "Checking skill file..."

if [[ -f "SKILL.md" ]]; then
    echo -e "  ${GREEN}✓${NC} SKILL.md exists"
else
    echo -e "  ${RED}✗${NC} SKILL.md missing (required for agentskills.io)"
    ((errors++))
    exit 1
fi

echo

# Validate SKILL.md frontmatter
echo "Validating SKILL.md frontmatter..."

# Extract frontmatter (between --- markers)
if command -v python3 &> /dev/null; then
    frontmatter=$(python3 << 'EOF'
import sys
import re

with open('SKILL.md', 'r') as f:
    content = f.read()

# Extract YAML frontmatter
match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if match:
    print(match.group(1))
else:
    sys.exit(1)
EOF
)

    if [[ $? -eq 0 ]]; then
        echo -e "  ${GREEN}✓${NC} Valid frontmatter structure"

        # Check required fields
        if echo "$frontmatter" | grep -q "^name: "; then
            name=$(echo "$frontmatter" | grep "^name: " | cut -d' ' -f2- | tr -d '\r')
            echo -e "  ${GREEN}✓${NC} name: $name"

            # Validate name format (alphanumeric, hyphens, underscores)
            if [[ ! "$name" =~ ^[a-z0-9][a-z0-9_-]+[a-z0-9]$ ]]; then
                echo -e "  ${YELLOW}⚠${NC}  name format should be lowercase with hyphens/underscores"
                ((warnings++))
            fi

            # Check name matches directory name
            dir_name=$(basename "$PROJECT_ROOT")
            if [[ "$name" != "$dir_name" ]]; then
                echo -e "  ${YELLOW}⚠${NC}  name ($name) doesn't match directory ($dir_name)"
                ((warnings++))
            fi
        else
            echo -e "  ${RED}✗${NC} name field missing (required)"
            ((errors++))
        fi

        if echo "$frontmatter" | grep -q "^description: "; then
            description=$(echo "$frontmatter" | grep "^description: " | cut -d' ' -f2-)
            desc_length=${#description}

            if [[ $desc_length -ge 1 && $desc_length -le 1024 ]]; then
                echo -e "  ${GREEN}✓${NC} description: ${desc_length} chars"
            elif [[ $desc_length -gt 1024 ]]; then
                echo -e "  ${YELLOW}⚠${NC}  description too long (${desc_length} > 1024 chars)"
                ((warnings++))
            else
                echo -e "  ${RED}✗${NC} description too short (${desc_length} chars)"
                ((errors++))
            fi
        else
            echo -e "  ${RED}✗${NC} description field missing (required)"
            ((errors++))
        fi

        # Check optional but recommended fields
        if echo "$frontmatter" | grep -q "^license: "; then
            license=$(echo "$frontmatter" | grep "^license: " | cut -d' ' -f2- | tr -d '\r')
            echo -e "  ${GREEN}✓${NC} license: $license"
        else
            echo -e "  ${YELLOW}⚠${NC}  license field missing (recommended)"
            ((warnings++))
        fi

        if echo "$frontmatter" | grep -q "^compatibility: "; then
            echo -e "  ${GREEN}✓${NC} compatibility field present"
        else
            echo -e "  ${YELLOW}⚠${NC}  compatibility field missing (recommended)"
            ((warnings++))
        fi

        if echo "$frontmatter" | grep -q "^metadata:"; then
            echo -e "  ${GREEN}✓${NC} metadata section present"
        else
            echo -e "  ${YELLOW}⚠${NC}  metadata section missing (optional)"
        fi
    else
        echo -e "  ${RED}✗${NC} Failed to extract frontmatter"
        ((errors++))
    fi
else
    echo -e "  ${YELLOW}⚠${NC}  python3 not available, skipping frontmatter validation"
    ((warnings++))
fi

echo

# Check directory structure
echo "Checking directory structure..."

# Required files
if [[ -f "scripts/convert.py" ]]; then
    echo -e "  ${GREEN}✓${NC} scripts/convert.py (core converter)"
else
    echo -e "  ${RED}✗${NC} scripts/convert.py missing"
    ((errors++))
fi

if [[ -f "requirements.txt" ]]; then
    echo -e "  ${GREEN}✓${NC} requirements.txt"
else
    echo -e "  ${RED}✗${NC} requirements.txt missing"
    ((errors++))
fi

if [[ -f "README.md" ]]; then
    echo -e "  ${GREEN}✓${NC} README.md"
else
    echo -e "  ${YELLOW}⚠${NC}  README.md missing (recommended)"
    ((warnings++))
fi

if [[ -f "LICENSE" ]]; then
    echo -e "  ${GREEN}✓${NC} LICENSE"
else
    echo -e "  ${YELLOW}⚠${NC}  LICENSE missing (recommended)"
    ((warnings++))
fi

# Recommended directories
if [[ -d "examples" ]]; then
    example_count=$(find examples -type f | wc -l | tr -d ' ')
    echo -e "  ${GREEN}✓${NC} examples/ ($example_count files)"
else
    echo -e "  ${YELLOW}⚠${NC}  examples/ missing (recommended)"
    ((warnings++))
fi

if [[ -d "references" ]]; then
    ref_count=$(find references -type f -name "*.md" | wc -l | tr -d ' ')
    echo -e "  ${GREEN}✓${NC} references/ ($ref_count docs)"
else
    echo -e "  ${YELLOW}⚠${NC}  references/ missing (recommended for detailed docs)"
    ((warnings++))
fi

if [[ -d "scripts" ]]; then
    echo -e "  ${GREEN}✓${NC} scripts/ (validation and tools)"
else
    echo -e "  ${YELLOW}⚠${NC}  scripts/ missing (optional)"
fi

# Check for plugin-specific files that shouldn't exist
if [[ -f "plugin.json" ]]; then
    echo -e "  ${YELLOW}⚠${NC}  plugin.json found (Claude Code plugin format, should be removed for agentskills.io)"
    ((warnings++))
fi

if [[ -d "agents" ]]; then
    echo -e "  ${YELLOW}⚠${NC}  agents/ found (Claude Code plugin format, should be removed for agentskills.io)"
    ((warnings++))
fi

if [[ -d "skills" ]]; then
    echo -e "  ${YELLOW}⚠${NC}  skills/ found (Claude Code plugin format, should be removed for agentskills.io)"
    ((warnings++))
fi

echo

# Check Python dependencies
echo "Checking Python dependencies..."

if command -v python3 &> /dev/null; then
    echo -e "  ${GREEN}✓${NC} Python $(python3 --version | cut -d' ' -f2)"

    # Check version is 3.8+
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
        echo -e "  ${GREEN}✓${NC} Python version $python_version >= 3.8"
    else
        echo -e "  ${RED}✗${NC} Python version $python_version < 3.8 (required: 3.8+)"
        ((errors++))
    fi

    # Check each requirement
    if [[ -f "requirements.txt" ]]; then
        # Map package names to import names
        declare -A import_map=(
            ["python-pptx"]="pptx"
            ["PyYAML"]="yaml"
        )

        while IFS= read -r package; do
            # Skip empty lines and comments
            [[ -z "$package" || "$package" =~ ^# ]] && continue

            pkg_name=$(echo "$package" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | tr -d ' ')
            import_name="${import_map[$pkg_name]:-$pkg_name}"

            if python3 -c "import $import_name" 2>/dev/null; then
                echo -e "  ${GREEN}✓${NC} $pkg_name"
            else
                echo -e "  ${YELLOW}⚠${NC}  $pkg_name (not installed)"
                ((warnings++))
            fi
        done < requirements.txt

        if [[ $warnings -gt 0 ]]; then
            echo
            echo -e "  ${YELLOW}ℹ${NC}  Install dependencies with:"
            echo "     pip install -r requirements.txt"
        fi
    fi
else
    echo -e "  ${RED}✗${NC} Python 3 not found"
    ((errors++))
fi

echo

# Check documentation references
echo "Checking documentation..."

if [[ -f "SKILL.md" ]]; then
    # Check for broken internal links
    if grep -q "references/" SKILL.md; then
        echo -e "  ${GREEN}✓${NC} References to references/ directory found"

        # Extract referenced files and check they exist
        ref_files=$(grep -o "references/[A-Z_-]*\.md" SKILL.md | sort -u)
        missing_refs=0

        for ref in $ref_files; do
            if [[ -f "$ref" ]]; then
                echo -e "    ${GREEN}✓${NC} $ref exists"
            else
                echo -e "    ${YELLOW}⚠${NC}  $ref referenced but missing"
                ((warnings++))
                ((missing_refs++))
            fi
        done

        if [[ $missing_refs -eq 0 ]]; then
            echo -e "  ${GREEN}✓${NC} All referenced docs exist"
        fi
    fi

    # Check SKILL.md length
    line_count=$(wc -l < SKILL.md)
    if [[ $line_count -gt 500 ]]; then
        echo -e "  ${YELLOW}⚠${NC}  SKILL.md is $line_count lines (recommended: < 500)"
        echo "     Consider moving detailed content to references/"
        ((warnings++))
    else
        echo -e "  ${GREEN}✓${NC} SKILL.md length: $line_count lines"
    fi
fi

echo

echo "==================================="
echo "Validation Summary"
echo "==================================="

if [[ $errors -eq 0 && $warnings -eq 0 ]]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo
    echo "Your hackmd-to-pptx skill follows agentskills.io format."
    echo
    echo "Next steps:"
    echo "  1. Test conversion: python scripts/convert.py examples/demo.md test.pptx"
    echo "  2. Share your skill at https://agentskills.io"
    exit 0
else
    if [[ $errors -gt 0 ]]; then
        echo -e "${RED}✗ $errors error(s) found${NC}"
    fi
    if [[ $warnings -gt 0 ]]; then
        echo -e "${YELLOW}⚠ $warnings warning(s) found${NC}"
    fi
    echo

    if [[ $errors -gt 0 ]]; then
        echo "Please fix the errors above before using the skill."
        exit 1
    else
        echo "Warnings are non-critical but recommended to address."
        exit 0
    fi
fi
