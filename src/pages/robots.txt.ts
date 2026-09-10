import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => {
  const sitemapUrl = new URL('sitemap-index.xml', site || 'https://anuradhawick.com').href;
  const content = `User-agent: *
Allow: /

Sitemap: ${sitemapUrl}
`;
  return new Response(content, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
};
