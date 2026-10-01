// DOM audit for the critic: run inside the page (browse js "$(cat tools/audit.js)").
// Reports visible touch targets under 48x48 px, visible text under 13 px, and whether the app
// has scrolled (a scrolled #app means hidden layers are leaking into view), and text below
// WCAG AA contrast (4.5:1, or 3:1 for large text).
(() => {
  const app = document.querySelector('#app');
  const shown = el => {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' &&
      !el.closest('[inert]') && !el.closest('.view:not(.on)') && !el.closest('.overlay:not(.on)') &&
      !el.closest('.leaflet-control-attribution') &&
      !(el.classList.contains('leaflet-marker-icon') && !el.classList.contains('leaflet-interactive'));
  };
  const name = el => `${el.tagName.toLowerCase()}.${String(el.className.baseVal ?? el.className).split(' ')[0]}`;
  const targets = [];
  app.querySelectorAll('button, a, input, summary, [role=button]').forEach(el => {
    if (!shown(el)) return;
    const r = el.getBoundingClientRect();
    if (r.height < 47.5 || r.width < 47.5) {
      const label = (el.getAttribute('aria-label') || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 26);
      targets.push(`${name(el)} "${label}" ${Math.round(r.width)}x${Math.round(r.height)}`);
    }
  });
  const text = new Set();
  app.querySelectorAll('*').forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || !shown(el)) return;
    if (el.closest('.leaflet-control-attribution')) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < 13) text.add(`${name(el)} ${fs}px`);
  });
  // WCAG contrast of text against the nearest opaque background (skips text over the map)
  const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
  const lum = ([r, g, b]) => [r, g, b].map(v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; })
    .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { if (e.id === 'map') return null;
    const c = rgb(getComputedStyle(e).backgroundColor); if (c.length >= 3 && (c[3] === undefined || c[3] > 0.9)) return c; } return [255, 255, 255]; };
  const contrast = new Set();
  app.querySelectorAll('*').forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) || !shown(el)) return;
    const cs = getComputedStyle(el), bg = bgOf(el); if (!bg || parseFloat(cs.opacity) < 1) return;
    const [l1, l2] = [lum(rgb(cs.color)), lum(bg)].sort((x, y) => y - x), ratio = (l1 + 0.05) / (l2 + 0.05);
    const large = parseFloat(cs.fontSize) >= 24 || (parseFloat(cs.fontSize) >= 18.66 && +cs.fontWeight >= 700);
    if (ratio < (large ? 3 : 4.5)) contrast.add(`${name(el)} "${el.textContent.trim().slice(0, 18)}" ${ratio.toFixed(2)}:1`);
  });
  return JSON.stringify({scrolled: app.scrollTop + document.scrollingElement.scrollTop,
    smallTargets: targets.slice(0, 25), smallText: [...text].slice(0, 12), lowContrast: [...contrast].slice(0, 12)});
})()
