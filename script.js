/* ============================================================
   RAPIZ - Más que velocidad | JavaScript
   ============================================================ */

(function () {
  'use strict';

  /* ---------- Navbar: scroll effect + active link ---------- */
  const header = document.getElementById('header');

  function updateHeader() {
    header.classList.toggle('scrolled', window.scrollY > 20);
  }
  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  /* Smooth nav highlight */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav__link');

  function highlightNav() {
    let current = '';
    sections.forEach(sec => {
      if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
    });
    navLinks.forEach(link => {
      const href = link.getAttribute('href').slice(1);
      link.classList.toggle('active', href === current);
    });
  }
  window.addEventListener('scroll', highlightNav, { passive: true });

  /* ---------- Mobile menu ---------- */
  const toggle = document.getElementById('nav-toggle');
  const menu   = document.getElementById('nav-menu');
  const close  = document.getElementById('nav-close');

  function openMenu()  { menu.classList.add('open');  document.body.style.overflow = 'hidden'; }
  function closeMenu() { menu.classList.remove('open'); document.body.style.overflow = ''; }

  toggle?.addEventListener('click', openMenu);
  close?.addEventListener('click', closeMenu);

  /* Close on link click */
  menu?.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      /* Close all */
      document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));

      /* Toggle clicked */
      if (!isOpen) {
        item.classList.add('open');
        btn.setAttribute('aria-expanded', 'true');
      } else {
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  /* ---------- Intersection Observer: fade-in animations ---------- */
  const animEl = document.querySelectorAll('[data-animate]');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const delay = entry.target.dataset.delay || 0;
          setTimeout(() => entry.target.classList.add('visible'), Number(delay));
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    animEl.forEach(el => observer.observe(el));
  } else {
    /* Fallback: show everything */
    animEl.forEach(el => el.classList.add('visible'));
  }

  /* ---------- Hero speedometer animation ---------- */
  const arc      = document.getElementById('speed-arc');
  const numEl    = document.getElementById('speed-num');
  const maxDash  = 251;
  const targetMbps = 100;
  let started = false;

  function animateSpeed() {
    if (started) return;
    started = true;
    let current = 0;
    const step = () => {
      current += 2;
      if (current > targetMbps) current = targetMbps;
      const offset = maxDash - (maxDash * current / targetMbps);
      if (arc) arc.style.strokeDashoffset = offset;
      if (numEl) numEl.textContent = current;
      if (current < targetMbps) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  const heroSection = document.querySelector('.hero');
  if (heroSection && 'IntersectionObserver' in window) {
    const heroObs = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) { animateSpeed(); heroObs.disconnect(); }
    }, { threshold: 0.3 });
    heroObs.observe(heroSection);
  } else {
    setTimeout(animateSpeed, 600);
  }

  /* ---------- Smooth scroll for anchor links ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      const offset = 72;
      window.scrollTo({ top: target.offsetTop - offset, behavior: 'smooth' });
    });
  });

  /* ---------- Animated counter for why-rapiz section (optional) ---------- */
  function countUp(el, target, duration) {
    let start = null;
    const step = (ts) => {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const value = Math.floor(progress * target);
      el.textContent = value;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  /* ---------- Coverage map dot hover: label via CSS, no JS needed ---------- */

  /* ---------- Editable plan fields: persist in sessionStorage ---------- */
  document.querySelectorAll('[contenteditable="true"]').forEach(el => {
    const key = 'rapiz_' + (el.closest('.plan-card, .promo-card')?.querySelector('h3')?.textContent?.trim() || Math.random()) + '_' + (el.className || el.tagName);
    const saved = sessionStorage.getItem(key);
    if (saved) el.textContent = saved;

    el.addEventListener('input', () => sessionStorage.setItem(key, el.textContent));
    el.addEventListener('focus', () => { if (el.textContent.trim().replace(/_/g,'') === '') el.textContent = ''; });
  });

  /* ---------- WhatsApp float: hide while navbar CTA is visible ---------- */
  const waFloat = document.querySelector('.wa-float');
  const headerCta = document.querySelector('.nav__actions .btn--whatsapp');

  if (waFloat && headerCta && 'IntersectionObserver' in window) {
    const ctaObs = new IntersectionObserver(([entry]) => {
      waFloat.style.opacity = entry.isIntersecting ? '0' : '1';
      waFloat.style.pointerEvents = entry.isIntersecting ? 'none' : 'auto';
    });
    ctaObs.observe(headerCta);
  }
})();
