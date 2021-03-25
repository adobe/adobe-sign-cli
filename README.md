# Adobe Sign CLI

Basic CLI utility for administrative tasks for Adobe Sign.

## Goals

Sometimes power users run into repetitive tasks, or requirements that are not achievable via the sign UI.  This CLI makes things easier and/or achievable.

### Installation

For easy installation, use pipx to install the shell as an executable.  You can also install w/ normal pip, if you want to use the base library in a project.

```bash
# pipx
pipx install adobesign
sign --help
```

```bash
# pip
pip install adobesign
sign
```

### Development

For development, install with poetry.

```bash
git clone foo
poetry install
poetry shell
sign
```

### Usage

Usage instructions for your code.

Example:

```bash
# RTFM
sign

# Clone a template
sign clone-template

# List users w/ multipls groups, but still in default
sign default-primary-report
```

If you want to skip assigning your key, every time you run a script, you can save the key & base_uri in your env, or a .env file.

```bash
# Saving access via .env
cp .env.dist .env
code .env

# Saving to your env
export INTEGRATION_KEY={integration_key}
export BASE_URI={integration_key}
```

### Contributing

Contributions are welcomed! Read the [Contributing Guide](./.github/CONTRIBUTING.md) for more information.

### Licensing

This project is licensed under the Apache V2 License. See [LICENSE](LICENSE) for more information.
