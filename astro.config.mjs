import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

const repo = process.env.GITHUB_REPOSITORY ? process.env.GITHUB_REPOSITORY.split('/')[1] : '';
const isUserRepo = repo.endsWith('.github.io');
const hasCustomDomain = process.env.CUSTOM_DOMAIN === 'true' || Boolean(process.env.ASTRO_SITE?.includes('anuradhawick.com'));

const site = process.env.ASTRO_SITE || (repo ? `https://${process.env.GITHUB_REPOSITORY_OWNER || 'anuradhawick'}.github.io` : 'https://anuradhawick.com');
const base = process.env.ASTRO_BASE || (hasCustomDomain || isUserRepo || !repo ? '/' : `/${repo}/`);

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});
