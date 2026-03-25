# GitHub Upload Guide for IBM Planning Analytics Scraper

This guide will help you upload your web scraper project to GitHub and link it in your LinkedIn blog post.

## Step 1: Create a .gitignore File

Before uploading, you need to create a `.gitignore` file to exclude unnecessary files. Since Plan mode can only edit Markdown files, you'll need to switch to Code mode or create this file manually.

**Recommended .gitignore contents:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
scraper.log

# OS
.DS_Store
Thumbs.db

# Output files (optional - you may want to include sample outputs)
# Uncomment these if you don't want to include the CSV/Excel files
# *.csv
# *.xlsx
# *.png
```

## Step 2: Initialize Git Repository

Open terminal in the `web-scraper-project` directory and run:

```bash
cd web-scraper-project
git init
git add .
git commit -m "Initial commit: IBM Planning Analytics feature scraper"
```

## Step 3: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `ibm-planning-analytics-scraper` (or your preferred name)
   - **Description**: "Python web scraper for tracking IBM Planning Analytics Workspace features across versions"
   - **Visibility**: Public (so it can be shared in your LinkedIn post)
   - **DO NOT** initialize with README (you already have one)
5. Click "Create repository"

## Step 4: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
git remote add origin https://github.com/YOUR_USERNAME/ibm-planning-analytics-scraper.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 5: Update LinkedIn Blog Post

Once uploaded, update the GitHub link in `linkedin-blog-post.md`:

Replace:
```
**🔗 [View the complete project on GitHub](https://github.com/YOUR_USERNAME/ibm-planning-analytics-scraper)**
```

With your actual repository URL:
```
**🔗 [View the complete project on GitHub](https://github.com/your-actual-username/ibm-planning-analytics-scraper)**
```

## Step 6: Optional Enhancements

### Add Topics to Your Repository
On GitHub, add relevant topics to make your project discoverable:
- `python`
- `web-scraping`
- `ibm`
- `planning-analytics`
- `beautifulsoup`
- `data-extraction`
- `ibm-bob`

### Add a License
Consider adding a license file (e.g., MIT License) to clarify usage rights.

### Create a GitHub Release
Tag your first version:
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

## Files to Include in Repository

✅ **Include:**
- `scraper.py` - Main scraper code
- `visualize_data.py` - Visualization script
- `requirements.txt` - Dependencies
- `setup_environment.sh` - Setup script
- `README.md` - Project documentation
- `linkedin-blog-post.md` - Your blog post
- `.gitignore` - Git ignore rules
- Sample output files (1 CSV and 1 Excel file as examples)
- `ibm_features_visualization.png` - Sample visualization

❌ **Exclude (via .gitignore):**
- `venv/` - Virtual environment
- `scraper.log` - Log files
- `__pycache__/` - Python cache
- `.DS_Store` - OS files

## Verification Checklist

Before sharing on LinkedIn, verify:
- [ ] Repository is public
- [ ] README.md displays correctly
- [ ] All essential files are included
- [ ] .gitignore is working (no venv/ or log files in repo)
- [ ] Requirements.txt is up to date
- [ ] Sample output files are included
- [ ] Repository has a clear description
- [ ] Topics/tags are added
- [ ] LinkedIn blog post link is updated with correct GitHub URL

## Need Help?

If you encounter issues:
1. Check GitHub's [documentation](https://docs.github.com)
2. Verify your Git configuration: `git config --list`
3. Ensure you have the correct repository permissions

---

**Note:** You'll need to switch to Code mode or manually create the `.gitignore` file, as Plan mode can only edit Markdown files.