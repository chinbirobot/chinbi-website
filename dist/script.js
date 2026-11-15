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
const lightbox = document.querySelector('#videoLightbox');
if (lightbox) {
  const lbVideo = lightbox.querySelector('video');
  const lbTitle = lightbox.querySelector('.lb-title');
  const openVideo = (src, title) => {
    lbVideo.src = src; lbTitle.textContent = title || '';
    if (lightbox.showModal) lightbox.showModal(); else lightbox.setAttribute('open', '');
    const p = lbVideo.play(); if (p && p.catch) p.catch(() => {});
  };
  const closeVideo = () => { lbVideo.pause(); lbVideo.removeAttribute('src'); lbVideo.load(); if (lightbox.close) lightbox.close(); else lightbox.removeAttribute('open'); };
  document.querySelectorAll('[data-video]').forEach(el => {
    el.addEventListener('click', () => {
      const label = el.querySelector('[data-i18n^="prodMove"]');
      openVideo(el.getAttribute('data-video'), label ? label.textContent : '');
    });
  });
  lightbox.querySelector('.lb-close').addEventListener('click', closeVideo);
  lightbox.addEventListener('click', e => { if (e.target === lightbox) closeVideo(); });
  lightbox.addEventListener('cancel', e => { e.preventDefault(); closeVideo(); });
}
