---
name: sync-portfolio-tools
description: >-
  Scans Anuradha Wickramarachchi's published software packages across Crates.io,
  PyPI, Bioconda/Anaconda, and recent GitHub repositories, and audits or updates
  the tools, applications, and starter templates displayed across the portfolio site
  (src/pages/apps.astro, src/pages/templates.astro, and src/pages/index.astro).
---

# Sync Portfolio Tools & Software Ecosystem

This skill guides the agent in scanning Anuradha Wickramarachchi's developer ecosystem across package registries and GitHub, identifying newly published or updated packages, and syncing them into the portfolio site.

## When to Use This Skill

Activate this skill when:
- The user requests to update, refresh, or audit tools on the portfolio website.
- The user mentions publishing a new crate to Crates.io, a package to PyPI, a conda package, or creating a new GitHub repository.
- The user asks to sync packages from `anuradhawick` accounts across registries.

---

## Step-by-Step Procedure

### 1. Run the Ecosystem Scanner

Execute the bundled Python scanner script:

```bash
python3 .agents/skills/sync-portfolio-tools/scripts/scan_ecosystem.py
```

Optional: To output a raw JSON dump for automated processing, run:
```bash
python3 .agents/skills/sync-portfolio-tools/scripts/scan_ecosystem.py --json
```

This script queries:
- **Crates.io**: `https://crates.io/api/v1/crates?user_id=266446`
- **PyPI**: JSON API for user's Python packages (`avldb`, `s3-avldb`, `pykmertools`, `cogent3-pykmertools`, `rs-avl`, `rsbio-seq`, etc.)
- **Bioconda / Anaconda**: `https://api.anaconda.org/package/bioconda/kmertools`
- **GitHub**: Recent non-fork repositories via `https://api.github.com/users/anuradhawick/repos?sort=pushed&per_page=100`

---

### 2. Categorize Discovered Projects

Map each package or tool into the appropriate section in `src/pages/apps.astro`:

| Category | Typical Repos / Packages | Target Section |
| :--- | :--- | :--- |
| **Signature Applications** | Standalone desktop / web apps (e.g. `Clipper`, `IceBreak`, `TypeFaster`, `Kmertools`) | `Signature Tools & Applications` |
| **Rust Crates** | Published to crates.io (e.g. `lambdamux`, `rs-avl`, `sqlite-functions`) | `Published Rust Crates (crates.io)` |
| **Python Packages** | Published to PyPI (e.g. `avldb`, `s3-avldb`, `cogent3-pykmertools`, `rsbio-seq`) | `Python & Database Packages (PyPI)` |
| **Metagenomics & Genomics** | Algorithmic bioinformatics research (`MetaBCC-LR`, `LRBinner`, `OBLR`, `Seq2Vec`, `Seq2CovVec`) | `Metagenomics & Plasmid Recovery` |
| **Utilities, GPU & IoT** | Microcontroller firmware, CUDA kernels, WebAssembly, templates (`kmertools-wasm`, `CUDA-k-mer-counting`, `M5StickC`) | `Computer Vision, GPU, WASM & Embedded IoT` |

If a repository is a starter template or cloud blueprint (e.g. `icebreak`, `rs_template`, `tf_template`), also audit **`src/pages/templates.astro`**.

---

### 3. Fetch Logos or Assets (If Applicable)

If a new signature application has a dedicated logo in its repository (e.g. `logo.png` or `public/icon.png`):
1. Fetch and store the image locally in `public/assets/uploads/<tool-name>-logo.png`.
2. Reference the asset via `image="/assets/uploads/<tool-name>-logo.png"`.

---

### 4. Update Astro Pages

Add or update the `<ToolCard />` component in `src/pages/apps.astro`. Use the available props:

```astro
<ToolCard
  title="PackageName"
  description="Concise description highlighting functionality and architecture."
  image="/assets/uploads/..."       <!-- Optional -->
  githubUrl="https://github.com/..."
  crateUrl="https://crates.io/crates/..." <!-- If on crates.io -->
  pypiUrl="https://pypi.org/project/..."   <!-- If on PyPI -->
  condaUrl="https://anaconda.org/..."     <!-- If on Bioconda -->
  liveUrl="https://..."                  <!-- Optional live demo -->
  tags={["Rust", "AWS", "crates.io"]}
  featured={false}
/>
```

Keep Tailwind CSS v4 styling rules intact:
- Use CSS variable syntax `(--color-name)` rather than `[var(--color-name)]`.

---

### 5. Verification & Testing

Always verify the updates before committing:

1. **Type and Astro Checks**:
   ```bash
   npm run astro check
   ```
   Must pass with 0 errors and 0 warnings.

2. **Production Build**:
   ```bash
   npm run build
   ```
   Must build all static HTML pages and generate `dist/` cleanly.

3. **Git Review**:
   ```bash
   git diff src/
   ```
   Inspect differences for formatting and accuracy.
