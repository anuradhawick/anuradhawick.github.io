# Anuradha Wickramarachchi - Personal Website

A clean, minimalist, high-performance static website built with **[Astro](https://astro.build/)** and styled with **Tailwind CSS**. Features 100% self-contained local assets, SEO optimizations, Schema.org JSON-LD structured data, and automated CI/CD deployment via **GitHub Pages**.

---

## Quick Start

### 1. Local Development
```bash
# Install dependencies
npm install

# Start development server (opens on http://localhost:4321)
npm run dev
```

### 2. Building for Production
```bash
# Build static site to dist/
npm run build

# Preview production build locally
npm run preview
```

---

## How to Add New Content

### Adding a New Blog Post
To publish a new article or note:
1. Create a new markdown file in `src/content/blog/<your-post-slug>.md`.
2. Add frontmatter metadata at the top:

```markdown
---
title: "Your Post Title"
description: "A short 1-2 sentence summary for SEO and card previews."
pubDate: 2026-09-15
heroImage: "/assets/uploads/your-image.jpg" # Optional
tags: ["Bioinformatics", "Engineering"]
categories: ["Tech"]
draft: false # Set to true to hide from production builds
---

Your content in standard Markdown goes here!

## Subheading

You can write standard Markdown, code snippets, lists, blockquotes, and embed images.
```

3. Commit and push to GitHub:
```bash
git add src/content/blog/your-post-slug.md
git commit -m "Add new post: Your Post Title"
git push origin main
```
GitHub Actions will automatically build and publish your new post!

---

### Adding a New Static Page
To add a new standalone page (e.g. `/publications` or `/contact`):
1. Create `src/pages/publications.astro` (or `src/pages/publications.md`):

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Publications" description="List of research publications.">
  <div class="prose">
    <h1>Publications</h1>
    <p>Your content goes here...</p>
  </div>
</BaseLayout>
```

2. If you want this page in the main navigation menu, add it to `navLinks` in `src/components/Header.astro`.
3. Commit and push to GitHub.

---

## GitHub Pages Deployment (CI/CD)

The repository includes an automated GitHub Actions workflow at [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) that automatically builds the site and pushes to the `gh-pages` branch.

### One-Time GitHub Settings:
1. In your GitHub repository, go to **Settings** &rarr; **Pages**.
2. Under **Build and deployment**:
   - **Source**: Select **Deploy from a branch**.
   - **Branch**: Select **`gh-pages`** and folder **`/ (root)`**.
3. Under **Settings** &rarr; **Actions** &rarr; **General**:
   - Under **Workflow permissions**, ensure **"Read and write permissions"** is selected (this allows the GitHub Actions bot to push the built files to the `gh-pages` branch).
4. Any push to `main` will now automatically build and deploy the site!

---

## Custom Domain Setup (`anuradhawick.com`)

When you are ready to point your custom domain `anuradhawick.com` to GitHub Pages:
1. In your GitHub repository, go to **Settings** &rarr; **Pages** &rarr; **Custom domain**.
2. Enter `anuradhawick.com` and save (or create `public/CNAME` containing `anuradhawick.com`).
3. Update your DNS settings at your domain registrar:
   - Configure **A records** pointing to GitHub Pages IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Configure a **CNAME record** for `www` pointing to `<your-username>.github.io`.
4. Check **Enforce HTTPS** in GitHub Pages settings.
