const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() { navigation.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
toggle.addEventListener('click', () => { const open = navigation.classList.toggle('open'); toggle.setAttribute('aria-expanded', String(open)); });
navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && navigation.classList.contains('open')) { closeMenu(); toggle.focus(); } });
document.querySelector('#year').textContent = new Date().getFullYear();
const lazyVideos = document.querySelectorAll('video[data-lazy]');
if ('IntersectionObserver' in window) {
  const videoObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const v = e.target;
      if (e.isIntersecting) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } else v.pause();
    });
  }, { threshold: 0.35 });
  lazyVideos.forEach(v => videoObserver.observe(v));
} else {
  lazyVideos.forEach(v => { v.setAttribute('controls', ''); });
}
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  lazyVideos.forEach(v => { v.setAttribute('controls', ''); });
}
