# Pre-Push Checklist

Before pushing to GitHub, please verify the following:

## 📋 Code Quality

- [ ] All Python files follow PEP 8 style guidelines
- [ ] No syntax errors or warnings
- [ ] All functions have docstrings
- [ ] Code is properly commented
- [ ] No hardcoded credentials or sensitive data
- [ ] All print statements use proper logging where applicable

## 🧪 Testing

- [ ] Demo mode works: `python3 demo_mode.py`
- [ ] All scripts are executable: `chmod +x scripts/*.sh`
- [ ] No broken imports
- [ ] Example scripts run without errors
- [ ] Documentation examples are accurate

## 📚 Documentation

- [ ] README.md is up to date
- [ ] All new features are documented
- [ ] CHANGELOG.md is updated
- [ ] Code comments are clear and helpful
- [ ] No broken links in documentation
- [ ] All markdown files render correctly

## 🔒 Security

- [ ] No credentials in code or config files
- [ ] `.env` file is in `.gitignore`
- [ ] No API keys or tokens committed
- [ ] Sensitive data is properly excluded
- [ ] Security warnings are addressed

## 📁 Files & Structure

- [ ] `.gitignore` is properly configured
- [ ] No unnecessary files included
- [ ] Large files (models, datasets) are excluded
- [ ] File permissions are correct
- [ ] Directory structure is clean

## 🔧 Configuration

- [ ] `.env.example` is updated with new variables
- [ ] `config.py` has sensible defaults
- [ ] All paths use proper path joining
- [ ] Configuration is well-documented

## 🎯 Git Hygiene

- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts
- [ ] Branch is up to date with main
- [ ] Commits are logically organized
- [ ] No debug/test commits

## ✅ Final Checks

- [ ] Run: `git status` - verify all changes are intentional
- [ ] Run: `git diff` - review all changes
- [ ] Check for TODO/FIXME comments
- [ ] Verify version numbers are updated (if applicable)
- [ ] Test installation from scratch (if possible)

## 🚀 Ready to Push

Once all items are checked:

```bash
# Review changes
git status
git diff

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: descriptive message about changes"

# Push to GitHub
git push origin main
```

## 📝 Commit Message Format

Use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example:
```
feat: add real-time SMS alerting via Twilio

- Implemented Twilio integration
- Added SMS configuration to .env.example
- Updated alert_system.py with SMS support
- Added documentation in PRODUCTION_DEPLOYMENT.md
```

---

**Remember**: Quality over speed. Take time to review your changes!
