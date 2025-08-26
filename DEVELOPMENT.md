# Development Workflow Guide
## J1 PhD Dissertation Notebook

### Git Workflow

#### Daily Development
1. **Start your day:**
   ```bash
   git pull origin main
   ```

2. **Make changes to your research code**

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Brief description of changes made"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin main
   ```

#### Before Major Changes
1. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-analysis-method
   ```

2. **Work on your feature**

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Implement new analysis method for CRAC optimization"
   ```

4. **Push branch:**
   ```bash
   git push origin feature/new-analysis-method
   ```

5. **Create Pull Request on GitHub** (when ready to merge)

### Research Workflow

#### Adding New Modules
1. Create new directory in appropriate section
2. Add `main.py` with module logic
3. Update `config.yaml` with module configuration
4. Test the module
5. Commit and push changes

#### Data Management
- Keep raw data in `data/` directory
- Generated outputs go in `output/` directories
- Use `.gitignore` to exclude large files and outputs
- Document data sources in README

#### Collaboration with Advisors
- Use GitHub Issues for research questions
- Create Pull Requests for major changes
- Share repository link with Dr. Wangda Zuo and collaborators
- Use GitHub Discussions for research discussions

### Best Practices

#### Code Quality
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Test your code before committing

#### Documentation
- Update README.md for major changes
- Document research methodology in code comments
- Keep configuration files up to date
- Maintain clear commit messages

#### Research Integrity
- Never commit sensitive data or credentials
- Keep research data backed up
- Document all assumptions and methodologies
- Version control all research code

### Useful Commands

```bash
# Check repository status
git status

# View commit history
git log --oneline

# Create and switch to new branch
git checkout -b branch-name

# Merge changes from main
git merge main

# View differences
git diff

# Reset to previous commit (if needed)
git reset --hard HEAD~1
```

### GitHub Features for Research

#### Issues
- Track research questions
- Document bugs or improvements
- Assign tasks to collaborators

#### Projects
- Organize research milestones
- Track progress on dissertation chapters
- Manage conference paper submissions

#### Wiki
- Document research methodology
- Maintain literature review
- Share technical specifications

#### Releases
- Tag major research milestones
- Archive completed research phases
- Share stable versions with advisors

### Contact
For questions about this workflow, contact:
- **Michael Maloney** - michael.maloney@psu.edu
- **Dr. Wangda Zuo** - Primary advisor
- **Michael Weter** - LBNL National Labs collaborator
