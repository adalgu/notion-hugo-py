# Notion-Hugo One-Click Deploy

Transform your Notion database into a beautiful Hugo blog with one command.

## 🚀 One-Click Deployment

Deploy your Notion blog instantly with this single command:

```bash
curl -sSL https://raw.githubusercontent.com/adalgu/notion-hugo-py/main/scripts/quick-deploy-github.sh | bash
```

This will:
- Set up a complete Hugo blog repository
- Configure Notion API integration
- Deploy to GitHub Pages automatically
- Create a sample Notion database structure

## ✨ Features

- **Zero Configuration**: Automated setup from Notion to live blog
- **Real-time Sync**: Webhook-based updates from Notion
- **Hugo Integration**: Beautiful, fast static site generation
- **GitHub Pages**: Free hosting with custom domain support
- **Vercel Ready**: Alternative deployment option included

## � Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation instructions
- [Deployment Options](docs/DEPLOYMENT_OPTIONS.md) - GitHub Pages vs Vercel
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## � Manual Installation

If you prefer manual setup:

```bash
# Clone the repository
git clone https://github.com/adalgu/notion-hugo-py.git
cd notion-hugo-py

# Install dependencies
pip install -e .

# Run the setup wizard
python setup.py
```

## � How It Works

1. **Notion Database**: Create content in your structured Notion database
2. **API Sync**: Automated synchronization via Notion API
3. **Hugo Generation**: Convert to Hugo-compatible markdown
4. **Auto Deploy**: Push changes trigger automatic deployment

## 🔧 Configuration

The system supports:
- Custom Hugo themes
- Flexible property mapping
- Draft/publish workflows
- SEO optimization
- Image handling

## 📄 License

MIT License - feel free to use for personal and commercial projects.

## 🤝 Contributing

Contributions welcome! See our development docs for guidelines.
