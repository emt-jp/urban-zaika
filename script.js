/* ==========================================================================
   Urban Zaika - Restaurant Website Scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // ---------- Language Dropdown ----------
  const langDropdown = document.getElementById('langDropdown');
  const langDropdownBtn = document.getElementById('langDropdownBtn');
  const langMenu = document.getElementById('langMenu');
  const langCurrent = document.getElementById('langCurrent');
  const langOptions = langMenu ? langMenu.querySelectorAll('.lang-option') : [];

  const langLabels = { en: 'English', ja: '日本語', ur: 'اردو' };

  // Get saved language or default to Japanese
  let currentLang = localStorage.getItem('uz-lang') || 'ja';

  function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('uz-lang', lang);
    document.documentElement.lang = lang;

    // Set text direction for Urdu (RTL)
    if (lang === 'ur') {
      document.documentElement.dir = 'rtl';
    } else {
      document.documentElement.dir = 'ltr';
    }

    // Update all translatable elements
    document.querySelectorAll('[data-' + lang + ']').forEach(el => {
      const text = el.getAttribute('data-' + lang);
      if (text !== null) {
        if (text.includes('\n')) {
          el.innerHTML = text.replace(/\n/g, '<br>');
        } else {
          el.textContent = text;
        }
      }
    });

    // Update dropdown button label
    if (langCurrent) {
      langCurrent.textContent = langLabels[lang] || lang;
    }

    // Update active option
    langOptions.forEach(opt => {
      opt.classList.toggle('active', opt.getAttribute('data-lang') === lang);
    });

    // Close dropdown
    if (langDropdown) {
      langDropdown.classList.remove('open');
      langDropdownBtn.setAttribute('aria-expanded', 'false');
    }
  }

  // Set language on page load
  setLanguage(currentLang);

  // Toggle dropdown open/close
  if (langDropdownBtn) {
    langDropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = langDropdown.classList.toggle('open');
      langDropdownBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  // Option clicks
  langOptions.forEach(opt => {
    opt.addEventListener('click', (e) => {
      e.stopPropagation();
      const lang = opt.getAttribute('data-lang');
      if (lang !== currentLang) {
        setLanguage(lang);
      } else {
        langDropdown.classList.remove('open');
        langDropdownBtn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (langDropdown && !langDropdown.contains(e.target)) {
      langDropdown.classList.remove('open');
      langDropdownBtn.setAttribute('aria-expanded', 'false');
    }
  });

  // ---------- Navbar Scroll Effect ----------
  const navbar = document.getElementById('navbar');

  const handleScroll = () => {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll(); // Initial check

  // ---------- Mobile Menu Toggle ----------
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  navToggle.addEventListener('click', () => {
    navToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
    document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
  });

  // Close menu when a link is clicked
  navMenu.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navToggle.classList.remove('active');
      navMenu.classList.remove('active');
      document.body.style.overflow = '';
    });
  });

  // Close menu on outside click
  document.addEventListener('click', (e) => {
    if (navMenu.classList.contains('active') &&
        !navMenu.contains(e.target) &&
        !navToggle.contains(e.target) &&
        !langDropdown.contains(e.target)) {
      navToggle.classList.remove('active');
      navMenu.classList.remove('active');
      document.body.style.overflow = '';
    }
  });

  // ---------- Smooth Scroll for Navigation Links ----------
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = anchor.getAttribute('href');
      const target = document.querySelector(targetId);
      if (target) {
        const navHeight = navbar.offsetHeight;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  // ---------- Intersection Observer for Fade-in Animations ----------
  const fadeElements = document.querySelectorAll('.fade-in');

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -60px 0px',
    threshold: 0.1
  };

  const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        fadeObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);

  fadeElements.forEach((el, index) => {
    // Stagger animations for siblings
    el.style.transitionDelay = `${(index % 4) * 0.1}s`;
    fadeObserver.observe(el);
  });

  // ---------- Active Nav Link Highlight ----------
  const sections = document.querySelectorAll('section[id]');

  const highlightNav = () => {
    const scrollY = window.pageYOffset;
    const navHeight = navbar.offsetHeight;

    sections.forEach(section => {
      const sectionTop = section.offsetTop - navHeight - 100;
      const sectionBottom = sectionTop + section.offsetHeight;
      const sectionId = section.getAttribute('id');

      if (scrollY >= sectionTop && scrollY < sectionBottom) {
        document.querySelectorAll('.nav-link').forEach(link => {
          link.classList.remove('active-link');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active-link');
          }
        });
      }
    });
  };

  window.addEventListener('scroll', highlightNav, { passive: true });

  // ---------- Menu Category Filter ----------
  const filterTabs = document.querySelectorAll('.filter-tab');
  const menuCards = document.querySelectorAll('.menu-card[data-category]');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Update active tab
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.getAttribute('data-filter');

      menuCards.forEach(card => {
        if (filter === 'all' || card.getAttribute('data-category') === filter) {
          card.classList.remove('hidden');
          // Re-trigger fade-in if not already visible
          if (!card.classList.contains('visible')) {
            card.classList.add('visible');
          }
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });

  // ---------- Back to Top Button ----------
  const backToTopBtn = document.getElementById('backToTop');

  const handleBackToTop = () => {
    if (window.scrollY > 600) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  };

  window.addEventListener('scroll', handleBackToTop, { passive: true });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });

  // ---------- Mobile CTA Bar (show after scrolling past hero) ----------
  const mobileCta = document.getElementById('mobileCta');
  const heroSection = document.getElementById('hero');

  const handleMobileCta = () => {
    if (!heroSection || !mobileCta) return;
    const heroBottom = heroSection.offsetTop + heroSection.offsetHeight;

    if (window.scrollY > heroBottom - 100) {
      mobileCta.classList.add('visible');
    } else {
      mobileCta.classList.remove('visible');
    }
  };

  window.addEventListener('scroll', handleMobileCta, { passive: true });

  // ---------- Lazy Load Images with IntersectionObserver ----------
  const lazyImages = document.querySelectorAll('img[loading="lazy"]');

  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          // The browser handles native lazy loading, but we add a loaded class for styling
          img.addEventListener('load', () => {
            img.classList.add('loaded');
          });
          if (img.complete) {
            img.classList.add('loaded');
          }
          imageObserver.unobserve(img);
        }
      });
    }, {
      rootMargin: '100px 0px'
    });

    lazyImages.forEach(img => {
      imageObserver.observe(img);
    });
  }
});
