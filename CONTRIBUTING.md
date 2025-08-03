# Contributing Guidelines

Thanks for your interest in contributing to OwO Dusk! 🎉 We're excited to have you as part of our community. Here are some friendly guidelines to help make the contribution process smooth for everyone.

## 🤝 How to Contribute

We welcome all kinds of contributions:
- 🐛 **Bug Reports** - Found something broken? Let us know!
- ✨ **Feature Requests** - Have a cool idea? We'd love to hear it!
- 🔧 **Code Contributions** - Ready to get your hands dirty? Awesome!
- 📚 **Documentation** - Help make our docs even better!
- 🎨 **UI/UX Improvements** - Make things prettier and more user-friendly!

## 📋 Before You Start

### For Major Changes
- 💬 **Let's chat first!** Open an issue or discussion before starting work on major features
- 📱 **Discord is faster:** DM `@echoquill` on Discord for quick questions
- 🎯 **Check existing issues** to see if someone's already working on it

### For Bug Fixes & Small Features
- 🚀 Feel free to jump right in with a PR!

## 🔄 Pull Request Guidelines

### The Golden Rules
- **One feature = One PR** 📦
  - Keep PRs focused and manageable
  - Makes reviewing, testing, and merging much easier
- **No massive PRs please!** 💔
  - We love your enthusiasm, but huge PRs are hard to review
  - Break large changes into smaller, logical chunks

### PR Checklist
- [ ] Fork the repo and create a feature branch
- [ ] Test your changes locally
- [ ] Write clear, descriptive commit messages
- [ ] Update documentation if needed
- [ ] Make sure your code follows our style guidelines

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- A Discord account for testing

### Getting Started
```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/owo-dusk.git
cd owo-dusk

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies and setup
python setup.py

# Run the application
python uwu.py
```

### Creating a Feature Branch
```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

## 📝 Code Style Guidelines

### General Principles
- **Keep it clean and readable** 🧹
- **Simple is better than complex** ✨
- **Consistency matters** 🎯

### Naming Conventions
```python
# Variables and functions: snake_case
user_token = "your_token"
def send_message():
    pass

# Classes: PascalCase  
class CaptchaSolver:
    pass

# Constants: UPPER_CASE
MAX_RETRIES = 3
```

### Code Organization
- Keep functions small and focused
- Use meaningful variable and function names
- Add comments for complex logic
- Remove unused imports and variables

## 💬 Commit Message Format

We use simple, clear commit messages. Here's the format:

```
type: brief description

Examples:
feat: add captcha solver dashboard
fix: resolve token validation issue
docs: update installation instructions
refactor: clean up message handling code
style: improve code formatting
test: add unit tests for core functions
```

### Commit Types
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `refactor` - Code refactoring
- `style` - Code style/formatting
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

## 🧪 Testing Your Changes

Before submitting a PR:

1. **Test locally** - Make sure everything works on your machine
2. **Test different scenarios** - Try various inputs and edge cases
3. **Check for errors** - Look for any console errors or exceptions
4. **Test on your platform** - Ensure it works on your OS (Windows/macOS/Linux/Termux)

## 📤 Submitting Your PR

### PR Title Format
```
type: Brief description of changes

Examples:
feat: Add automatic captcha detection
fix: Handle connection timeout errors
docs: Update README installation steps
```

### PR Description Template
```markdown
## What does this PR do?
Brief description of your changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature  
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (please describe)

## Testing
- [ ] Tested on Windows/macOS/Linux
- [ ] Tested on Termux (if applicable)
- [ ] No console errors
- [ ] Existing functionality still works

## Screenshots (if applicable)
Add screenshots here if your changes affect the UI.
```

## 🎉 After Your PR

- We'll review your PR as soon as possible
- We might ask for changes - don't worry, it's normal!
- Once approved, we'll merge it and you'll be a contributor! 🎊

## 🆘 Need Help?

- 💬 **Discord:** DM `@echoquill` for quick questions
- 🐛 **Issues:** Create an issue for bugs or feature requests  
- 📖 **Discussions:** Use GitHub discussions for general questions

## 🏆 Recognition

All contributors will be:
- Given a special role in our Discord server
- Forever appreciated by the community! ❤️

---

<div align="center">
  <sub>Thanks for making OwO Dusk better! 🚀</sub>
</div>
