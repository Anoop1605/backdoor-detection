# Contributing to Backdoor Detection System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/backdoor-detection.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit with clear messages: `git commit -m "Add: feature description"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## 📋 Development Setup

### Install Dependencies
```bash
# For demo development
pip3 install flask psutil

# For full system development
pip3 install -r requirements.txt
cd backend_scripts && pip3 install -r requirements.txt
```

### Run Tests
```bash
cd backend_scripts
python3 test_integration.py
```

## 🎯 Areas for Contribution

### High Priority
- [ ] Additional ML models for detection
- [ ] Performance optimizations
- [ ] Additional network attack patterns
- [ ] Enhanced visualization in dashboard

### Medium Priority
- [ ] Unit tests for all modules
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Additional documentation

### Low Priority
- [ ] UI/UX improvements
- [ ] Additional demo scenarios
- [ ] Code refactoring

## 📝 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Comment complex logic
- Keep functions focused and small

## 🧪 Testing

- Test all new features thoroughly
- Ensure existing tests pass
- Add new tests for new functionality
- Test on clean environment before submitting

## 📖 Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Update SETUP_GUIDE.md if setup changes
- Document configuration options

## 🐛 Bug Reports

When reporting bugs, please include:
- OS and Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs
- Screenshots if applicable

## 💡 Feature Requests

For feature requests, please describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternative solutions considered
- Additional context

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.
