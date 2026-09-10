/**
 * Resolves a path taking into account Astro's base URL (e.g. on GitHub Pages project sites).
 */
export function getRelativePath(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${base}${cleanPath}`;
}
