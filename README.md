# ContentForge — Free AI Content Toolkit

![Status](https://img.shields.io/badge/status-live-success)
![Price](https://img.shields.io/badge/price-free-brightgreen)
![Stack](https://img.shields.io/badge/stack-vanilla_js_%2B_python-blue)

> Free AI-powered content generation tools for bootstrapped businesses, solopreneurs, and content creators. No signup. No credit card. Just results.

**Live site:** https://contentforge2026.loca.lt

## Tools

| Tool | Description | Live |
|------|-------------|------|
| [AI Text Generator](landing/tools/ai-text-generator.html) | Blog titles, product descriptions, social captions, taglines, email copy | ✅ |
| [AI Social Caption Generator](landing/tools/ai-social-caption-generator.html) | Platform-optimized captions for Twitter/LinkedIn/Instagram/TikTok/Facebook | ✅ |
| [AI Blog Outline Generator](landing/tools/ai-blog-outline-generator.html) | SEO-optimized outlines with H2 sections and bullet points | ✅ |
| [AI Image Prompt Generator](landing/tools/ai-image-prompt-generator.html) | Optimized prompts for Midjourney/DALL-E/Stable Diffusion | ✅ |

## How It Works

1. Open any tool (no account needed)
2. Describe what you need
3. AI generates optimized content instantly
4. Copy to clipboard and use

All tools use [Pollinations.ai](https://pollinations.ai) — a free, open AI API requiring no API key.

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JavaScript (no frameworks)
- **Backend:** Python HTTP server (server.py)
- **AI:** Pollinations.ai free API
- **Hosting:** Python server + localtunnel
- **SEO:** Sitemap.xml, robots.txt, IndexNow

## Quick Start

```bash
python3 server.py
# Server starts on http://localhost:8080
```

Then tunnel with localtunnel:
```bash
npx localtunnel --port 8080
```

## Monetization

ContentForge is 100% free. If you'd like to support development:

**Bitcoin:** `1rHfsqBJb21E2EbxytMNJqM1BRveYYUHP`

## Project Structure

```
.
├── landing/                  # Web files
│   ├── index.html           # Main landing page
│   ├── blog/                # SEO content pages
│   ├── tools/               # AI tool pages
│   ├── sitemap.xml          # Search engine sitemap
│   └── robots.txt           # Search engine rules
├── server.py                # Python HTTP server
├── signups.json             # Email signups
├── strategy_plan.md         # Original strategy document
├── worklog.md               # Development log
├── journal.md               # Daily reflections
├── handoffs.md              # Human handoff points
├── validation_report.md     # Validation tracking
└── twitter_content.md       # Drafted social content
```

## License

Free and open for everyone. Built as a zero-to-profit challenge.
