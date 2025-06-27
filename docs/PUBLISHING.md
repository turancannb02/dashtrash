# 🚀 Publishing Guide

This guide covers how to publish new releases of dashtrash to various distribution channels.

## 📦 PyPI (Python Package Index)

### Automated Publishing (Recommended)

1. **Create a release on GitHub:**
   ```bash
   # Update version and create tag
   ./scripts/release.sh 0.2.0
   
   # Push changes
   git push origin main --tags
   ```

2. **Create GitHub Release:**
   - Go to GitHub → Releases → Create a new release
   - Select the tag you just created
   - Add release notes
   - Click "Publish release"

3. **GitHub Actions will automatically:**
   - Build the package
   - Run tests
   - Publish to PyPI

### Manual Publishing

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
python -m twine check dist/*

# Upload to PyPI (requires API token)
python -m twine upload dist/*
```

## 🍺 Homebrew

### Update Formula

1. **Calculate new SHA256:**
   ```bash
   shasum -a 256 dist/dashtrash-0.2.0.tar.gz
   ```

2. **Update Brewfile:**
   ```ruby
   class Dashtrash < Formula
     # ... other fields ...
     url "https://files.pythonhosted.org/packages/source/d/dashtrash/dashtrash-0.2.0.tar.gz"
     sha256 "NEW_SHA256_HERE"
     # ... rest of formula ...
   end
   ```

3. **Submit to Homebrew:**
   ```bash
   # Create tap repository
   brew tap-new turancannb02/dashtrash
   
   # Copy formula
   cp Brewfile $(brew --repository turancannb02/dashtrash)/Formula/dashtrash.rb
   
   # Test formula
   brew install --build-from-source turancannb02/dashtrash/dashtrash
   brew test dashtrash
   
   # Push to GitHub
   cd $(brew --repository turancannb02/dashtrash)
   git add .
   git commit -m "Add dashtrash formula"
   git push origin main
   ```

## 📦 Snap Store

### Build and Upload

```bash
# Install snapcraft
sudo snap install snapcraft --classic

# Build snap
snapcraft

# Login to store
snapcraft login

# Upload and release
snapcraft upload --release=stable dashtrash_0.2.0_amd64.snap
```

## 🐳 Container Registry

### GitHub Container Registry

```bash
# Build image
docker build -t ghcr.io/turancannb02/dashtrash:0.2.0 .
docker build -t ghcr.io/turancannb02/dashtrash:latest .

# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Push images
docker push ghcr.io/turancannb02/dashtrash:0.2.0
docker push ghcr.io/turancannb02/dashtrash:latest
```

### Docker Hub

```bash
# Build image
docker build -t turancannb02/dashtrash:0.2.0 .
docker build -t turancannb02/dashtrash:latest .

# Login to Docker Hub
docker login

# Push images
docker push turancannb02/dashtrash:0.2.0
docker push turancannb02/dashtrash:latest
```

## 📋 Release Checklist

### Pre-Release

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `dashtrash/main.py`
- [ ] Update version in `main.py`
- [ ] Update `CHANGELOG.md` with new features/fixes
- [ ] Test installation locally: `pip install -e .`
- [ ] Test CLI commands work: `dashtrash --help`
- [ ] Run tests: GitHub Actions or local testing
- [ ] Update documentation if needed

### Release Process

- [ ] Run release script: `./scripts/release.sh X.Y.Z`
- [ ] Push changes: `git push origin main --tags`
- [ ] Create GitHub Release with release notes
- [ ] Verify PyPI publish (automated via GitHub Actions)
- [ ] Update Homebrew formula with new SHA256
- [ ] Build and upload Snap package
- [ ] Build and push container images
- [ ] Update installation documentation

### Post-Release

- [ ] Verify installation works: `pip install dashtrash`
- [ ] Test Homebrew installation: `brew install turancannb02/dashtrash/dashtrash`
- [ ] Update any documentation that references version numbers
- [ ] Announce release on social media/forums
- [ ] Close any resolved GitHub issues

## 🔧 Tools and Credentials

### Required Tools

```bash
# Python packaging
pip install build twine

# Container tools
docker --version
snap install snapcraft --classic

# Homebrew
brew --version
```

### Required Credentials

- **PyPI API Token**: Stored in GitHub Secrets as `PYPI_API_TOKEN`
- **GitHub Token**: For container registry access
- **Snap Store**: Login via `snapcraft login`
- **Docker Hub**: Login via `docker login`

### GitHub Secrets Setup

Add these secrets to your GitHub repository:

- `PYPI_API_TOKEN`: Your PyPI API token
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password

## 🐛 Troubleshooting

### PyPI Upload Fails

```bash
# Check package validity
python -m twine check dist/*

# Test upload to TestPyPI first
python -m twine upload --repository testpypi dist/*
```

### Homebrew Formula Issues

```bash
# Test formula locally
brew install --build-from-source ./Brewfile
brew test dashtrash

# Validate formula
brew audit --strict --online ./Brewfile
```

### Container Build Issues

```bash
# Build with verbose output
docker build --progress=plain -t dashtrash .

# Debug failed build
docker run -it --rm IMAGE_ID sh
```

## 📞 Support

For publishing issues:
- 🐛 **PyPI**: [PyPI Help](https://pypi.org/help/)
- 🍺 **Homebrew**: [Homebrew Docs](https://docs.brew.sh/)
- 📦 **Snap**: [Snapcraft Docs](https://snapcraft.io/docs)
- 🐳 **Docker**: [Docker Docs](https://docs.docker.com/) 