# 🐾 Git-Critters

<p align="center">
  <b>Dynamic, animated companions powered by your GitHub contributions & programming languages!</b><br>
  <i>Watch your Giraffe grow a ridiculously tall neck, your Snowman get plump, your Code Train stretch across the tracks, your Monkey climb higher into the canopy, and your Buffalo collect milk cans for every 100 commits!</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-Automated-orange?style=for-the-badge&logo=githubactions&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

---

## 🌟 Meet The Critters

Every creature's traits, size, and colors are generated **algorithmically** using your real GitHub activity:

| Creature | How It Scales with GitHub Data | Live Demo |
| :--- | :--- | :---: |
| 🦒 **The Giraffe** | **Neck stretches taller** with total commits. Spots are colored with your top programming languages. Bends gently in the breeze while chewing leaves. | <img src="assets/giraffe.gif" width="160" /> |
| ⛄ **The Snowman** | **Belly diameter expands** with commits (from a tiny snowball to a massive frosty companion!). Wears a scarf & top hat ribbon striped with your languages amidst falling snow. | <img src="assets/snowman.gif" width="160" /> |
| 🚂 **The Snake Train** | **Carriage count lengthens** with commits. Each wagon is painted with a language badge while piston wheels chug and steam puffs rise. | <img src="assets/snake_train.gif" width="220" /> |
| 🐒 **The Monkey & Tree** | **Tree trunk & canopy rise taller** as contributions climb. A playful monkey swings between branches holding a golden banana next to language fruit. | <img src="assets/monkey_tree.gif" width="160" /> |
| 🐃 **The Buffalo** | Stands chewing cud while **shiny milk cans line up beside it** (1 milk can for every 100 commits!), each wrapped with language colored bands. | <img src="assets/buffalo.gif" width="180" /> |

---

## 🚀 Quick Start: Add a Critter to Your Profile

You can add any critter to your GitHub profile repository (`<username>/<username>`) in 2 simple steps:

### 1. Create the GitHub Workflow
In your profile repository, create a new workflow file at `.github/workflows/critter.yml`:

```yaml
name: Git-Critters

on:
  schedule:
    # Runs daily just after midnight UTC
    - cron: "0 0 * * *"
  workflow_dispatch: # Allows manual trigger anytime
  push:
    branches: [main]
    paths: [.github/workflows/critter.yml]

permissions:
  contents: write

concurrency: critter

jobs:
  critter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Choose: giraffe, snowman, snake_train, monkey_tree, buffalo, or all
      - uses: Nightkilller/git-critters@v1
        with:
          creature: giraffe
          output-dir: critters

      - name: Commit if changed
        shell: bash
        run: |
          git add critters/*.gif
          if git diff --cached --quiet; then
            echo "Critter unchanged; nothing to commit."
            exit 0
          fi
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git commit -m "critter: update companion growth & languages"
          git push
```

### 2. Embed into your `README.md`
Add your chosen creature into your profile `README.md`:

```html
<!-- Pick the critter you generated: -->
<div align="center">
  <img src="critters/giraffe.gif" width="240" alt="My GitHub Giraffe" />
</div>
```

*(Replace `giraffe.gif` with `snowman.gif`, `snake_train.gif`, `monkey_tree.gif`, or `buffalo.gif` depending on your choice!)*

---

## ⚙️ Configuration Options

| Input | Default | Description |
| :--- | :--- | :--- |
| `creature` | `giraffe` | Choose `giraffe`, `snowman`, `snake_train`, `monkey_tree`, `buffalo`, or `all` |
| `username` | `${{ github.repository_owner }}` | The GitHub account whose stats power the critter |
| `output-dir` | `critters` | Folder where generated `.gif` files will be saved |
| `token` | `${{ github.token }}` | GitHub token for reading public stats (default token is sufficient) |

---

## 💻 Local CLI Usage

You can also generate critters locally on your computer:

```bash
# 1. Clone repository
git clone https://github.com/Nightkilller/git-critters.git
cd git-critters

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate any creature for any username!
python3 -m src.cli --username torvalds --creature giraffe --output-dir dist
python3 -m src.cli --username Nightkilller --creature all --output-dir dist
```

---

## 🧠 The Science & Math

How do raw GitHub commits transform into living artwork?

- **Logarithmic Morphology**: Animal sizes scale via $y = y_0 + K \cdot \ln(1 + \text{commits})$. This guarantees early visual gratification (a beginner with 50 commits sees noticeable growth) while preventing extreme committers from stretching the canvas off-screen.
- **Language Palette Translation**: The GitHub API returns language distributions. Hex codes (e.g. Python `#3572A5`, JS `#F7DF1E`, C++ `#F34B7D`) are dynamically sampled and applied to spots, scarves, train wagons, tree fruits, and milk can bands.
- **Continuous Kinematic Cycles**: Tails, necks, ears, and pistons undulate along seamless periodic sine waves ($\theta = A \cdot \sin(\omega t)$) so animations loop smoothly without harsh jumps.

---

## 📄 License

MIT License © 2026 [Aditya Gupta (Nightkilller)](https://github.com/Nightkilller). Feel free to use, modify, and share!
