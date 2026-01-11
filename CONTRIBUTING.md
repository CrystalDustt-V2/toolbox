# Contributing to ToolBox CLI

Thank you for your interest in contributing to ToolBox CLI! We welcome contributions from the community to help make this tool even better.

## How to Contribute

### 1. Reporting Bugs
- Use the GitHub Issue Tracker to report bugs.
- Provide a clear and descriptive title.
- Include steps to reproduce the issue, the expected behavior, and the actual behavior.
- Mention your operating system and Python version.

### 2. Suggesting Features
- Open an issue on the GitHub Issue Tracker.
- Describe the feature you'd like to see and why it would be useful.
- If possible, suggest an implementation approach.

### 3. Submitting Pull Requests
- Fork the repository.
- Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b fix/your-bug-fix`.
- Make your changes.
- Ensure your code follows the existing style (PEP 8 for Python).
- Write tests for your changes.
- Run the tests to ensure everything is working correctly:
  ```bash
  pytest
  ```
- Commit your changes with clear and descriptive messages.
- Push your branch to your fork: `git push origin feature/your-feature-name`.
- Open a pull request against the `main` branch of the original repository.

## Plugin Development

ToolBox is designed with a modular plugin architecture. To create a new plugin:
1. Create a new directory in `src/toolbox/plugins/`.
2. Add an `__init__.py` file.
3. Define a class that inherits from `BasePlugin`.
4. Implement `get_metadata()` and `register_commands()`.
5. Register your plugin in the `PluginManager` (this happens automatically if it's in the `plugins` package).

## Code of Conduct

Please be respectful and professional in all interactions within the community.

## License

By contributing to ToolBox CLI, you agree that your contributions will be licensed under the MIT License.
