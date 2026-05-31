/**
 * Smart Merchant OS — main.js
 * Single shared JS file. Implements exactly the FR-042 allow-list:
 *   1. Theme (dark/light) init + toggle
 *   2. Sidebar drawer open/close with focus-trap
 *   3. Actions dropdowns ([data-actions-dropdown])
 *   4. Modals ([data-modal-trigger] / [data-modal] / [data-modal-close])
 *   5. Tab switcher ([data-tabs])
 *   6. Copy to clipboard ([data-copy])
 *   7. Profile menu dropdown
 *   8. Focus-trap helper
 *   9. lucide.createIcons() on DOMContentLoaded + window.renderIcons()
 *  10. Date-range selector toggle ([data-date-range])
 *
 * NO npm modules. NO ES module syntax. Classic <script defer> import only.
 */

/* ─── 1. Theme ────────────────────────────────────────────────────────────── */

function initTheme() {
  // Pre-paint script in _head.html already applied the class; this just wires the button.
  var btn = document.querySelector('[data-theme-toggle]');
  if (btn) {
    btn.addEventListener('click', function () {
      var isDark = document.documentElement.classList.toggle('dark');
      try { localStorage.setItem('smos:theme', isDark ? 'dark' : 'light'); } catch (e) {}
    });
  }
}

function setTheme(mode) {
  document.documentElement.classList.toggle('dark', mode === 'dark');
  try { localStorage.setItem('smos:theme', mode); } catch (e) {}
}

/* ─── 8. Focus-trap helper ────────────────────────────────────────────────── */

var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

function trapFocus(container) {
  var focusable = Array.from(container.querySelectorAll(FOCUSABLE));
  if (!focusable.length) return function () {};
  var first = focusable[0];
  var last  = focusable[focusable.length - 1];
  function handler(e) {
    if (e.key !== 'Tab') return;
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus(); }
    } else {
      if (document.activeElement === last)  { e.preventDefault(); first.focus(); }
    }
  }
  container.addEventListener('keydown', handler);
  first.focus();
  return function () { container.removeEventListener('keydown', handler); };
}

/* ─── 2. Sidebar drawer ───────────────────────────────────────────────────── */

function initSidebar() {
  var sidebar  = document.querySelector('[data-sidebar], #sidebar');
  var overlay  = document.querySelector('[data-sidebar-overlay]');
  var toggleBtns = document.querySelectorAll('[data-sidebar-toggle]');
  if (!sidebar) return;

  var releaseTrap = null;

  function openSidebar() {
    sidebar.classList.remove('translate-x-full');
    if (overlay) { overlay.classList.remove('hidden'); overlay.setAttribute('aria-hidden', 'false'); }
    toggleBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    releaseTrap = trapFocus(sidebar);
    document.addEventListener('keydown', onEscSidebar);
  }

  function closeSidebar() {
    sidebar.classList.add('translate-x-full');
    if (overlay) { overlay.classList.add('hidden'); overlay.setAttribute('aria-hidden', 'true'); }
    toggleBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    if (releaseTrap) { releaseTrap(); releaseTrap = null; }
    document.removeEventListener('keydown', onEscSidebar);
  }

  function onEscSidebar(e) {
    if (e.key === 'Escape') closeSidebar();
  }

  toggleBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      isOpen ? closeSidebar() : openSidebar();
    });
  });

  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }
}

/* ─── 3. Actions dropdowns ────────────────────────────────────────────────── */

function initDropdowns() {
  document.addEventListener('click', function (e) {
    // Close all open dropdowns when clicking outside
    document.querySelectorAll('[data-actions-dropdown]').forEach(function (wrapper) {
      var panel = wrapper.querySelector('.dropdown-panel');
      var trigger = wrapper.querySelector('[aria-expanded]');
      if (!wrapper.contains(e.target)) {
        if (panel) panel.classList.add('hidden');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      }
    });
  });

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-actions-dropdown] > [aria-haspopup], [data-actions-dropdown] > button');
    if (!trigger) return;
    var wrapper = trigger.closest('[data-actions-dropdown]');
    if (!wrapper) return;
    var panel = wrapper.querySelector('.dropdown-panel');
    if (!panel) return;
    var isOpen = trigger.getAttribute('aria-expanded') === 'true';
    // Close siblings first
    document.querySelectorAll('[data-actions-dropdown]').forEach(function (w) {
      if (w !== wrapper) {
        var p = w.querySelector('.dropdown-panel');
        var t = w.querySelector('[aria-expanded]');
        if (p) p.classList.add('hidden');
        if (t) t.setAttribute('aria-expanded', 'false');
      }
    });
    panel.classList.toggle('hidden', isOpen);
    trigger.setAttribute('aria-expanded', String(!isOpen));
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('[data-actions-dropdown]').forEach(function (w) {
        var p = w.querySelector('.dropdown-panel');
        var t = w.querySelector('[aria-expanded]');
        if (p) p.classList.add('hidden');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });
}

/* ─── 4. Modals ───────────────────────────────────────────────────────────── */

function initModals() {
  var backdrop = document.querySelector('[data-modal-backdrop]');
  var openModals = [];
  var releaseTrap = null;
  var lastFocused = null;

  function openModal(modal) {
    if (!backdrop || !modal) return;
    lastFocused = document.activeElement;
    backdrop.classList.remove('hidden');
    backdrop.classList.add('flex');
    backdrop.setAttribute('aria-hidden', 'false');
    // Move modal inside backdrop if not already there
    if (!backdrop.contains(modal)) backdrop.appendChild(modal);
    modal.classList.remove('hidden');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('role', 'dialog');
    releaseTrap = trapFocus(modal);
    openModals.push(modal);
    document.addEventListener('keydown', onEscModal);
  }

  function closeModal() {
    var modal = openModals.pop();
    if (modal) {
      modal.classList.add('hidden');
      modal.removeAttribute('aria-modal');
    }
    if (!openModals.length) {
      if (backdrop) {
        backdrop.classList.add('hidden');
        backdrop.classList.remove('flex');
        backdrop.setAttribute('aria-hidden', 'true');
      }
      if (releaseTrap) { releaseTrap(); releaseTrap = null; }
      document.removeEventListener('keydown', onEscModal);
      if (lastFocused && lastFocused.focus) { try { lastFocused.focus(); } catch (_) {} }
    }
  }

  function onEscModal(e) {
    if (e.key === 'Escape') closeModal();
  }

  // Trigger buttons — [data-modal-trigger] or [data-modal-open]
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-modal-trigger],[data-modal-open]');
    if (!trigger) return;
    var targetId = trigger.getAttribute('data-modal-trigger') || trigger.getAttribute('data-modal-open');
    var modal = document.getElementById(targetId) || document.querySelector('[data-modal="' + targetId + '"]');
    if (!modal) return;
    // Self-contained modal (has its own backdrop bg — no shared backdrop element needed)
    if (!backdrop) {
      lastFocused = document.activeElement;
      modal.classList.remove('hidden');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('role', 'dialog');
      releaseTrap = trapFocus(modal);
      openModals.push(modal);
      modal.addEventListener('click', function onBackdropClick(ev) {
        if (ev.target === modal) { closeModal(); modal.removeEventListener('click', onBackdropClick); }
      });
      document.addEventListener('keydown', onEscModal);
    } else {
      openModal(modal);
    }
  });

  // Close buttons inside modal
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-modal-close]')) closeModal();
  });

  // Backdrop click-outside
  if (backdrop) {
    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop) closeModal();
    });
  }
}

/* ─── 5. Tab switcher ─────────────────────────────────────────────────────── */

function initTabs() {
  document.addEventListener('click', function (e) {
    var tab = e.target.closest('[data-tab]');
    if (!tab) return;
    var group = tab.getAttribute('data-tab-group') || tab.closest('[data-tabs]') && tab.closest('[data-tabs]').getAttribute('data-tabs');
    if (!group) return;

    // Deactivate all tabs in group
    document.querySelectorAll('[data-tab-group="' + group + '"], [data-tabs="' + group + '"] [data-tab]').forEach(function (t) {
      t.setAttribute('aria-selected', 'false');
      t.classList.remove('tab-active');
    });

    // Activate clicked tab
    tab.setAttribute('aria-selected', 'true');
    tab.classList.add('tab-active');

    // Show target panel, hide others
    var targetPanel = tab.getAttribute('data-tab');
    document.querySelectorAll('[data-tab-panel][data-tab-group="' + group + '"]').forEach(function (panel) {
      panel.classList.toggle('hidden', panel.getAttribute('data-tab-panel') !== targetPanel);
    });
  });
}

/* ─── 6. Copy to clipboard ────────────────────────────────────────────────── */

function initCopy() {
  // Ensure toast element exists
  if (!document.getElementById('copied-toast')) {
    var toast = document.createElement('div');
    toast.id = 'copied-toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.textContent = 'تم النسخ ✓';
    document.body.appendChild(toast);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var key = btn.getAttribute('data-copy');
    // Look for the value in a sibling/nearby input[data-copy-value] or data-copy-value attr
    var valueEl = btn.closest('[data-copy-container]') && btn.closest('[data-copy-container]').querySelector('[data-copy-value]');
    // Fallback: a copy shortcut outside the container can target a [data-copy-value] element
    // whose id matches the data-copy key (e.g. data-copy="caption-value" → <pre id="caption-value">).
    if (!valueEl && key) {
      var byId = document.getElementById(key);
      if (byId && byId.hasAttribute('data-copy-value')) valueEl = byId;
    }
    var text = (valueEl && (valueEl.value || valueEl.textContent.trim())) || btn.getAttribute('data-copy-value') || key;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(showCopiedToast, showCopiedToast);
    } else {
      // Fallback for file:// context
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      } catch (_) {}
      showCopiedToast();
    }
  });
}

function showCopiedToast() {
  var toast = document.getElementById('copied-toast');
  if (!toast) return;
  toast.classList.add('show');
  setTimeout(function () { toast.classList.remove('show'); }, 1500);
}

/* ─── 7. Profile menu (already handled by initDropdowns) ──────────────────── */
// The profile menu uses [data-actions-dropdown="profile-menu"] which is covered by initDropdowns().

/* ─── 9. Lucide icons ─────────────────────────────────────────────────────── */

function renderIcons() {
  if (window.lucide && typeof window.lucide.createIcons === 'function') {
    window.lucide.createIcons();
  }
}

/* ─── 10. Date-range selector ─────────────────────────────────────────────── */

function initDateRange() {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-date-range]');
    if (btn) {
      var popover = document.querySelector('[data-date-popover]');
      if (popover) {
        var isOpen = popover.classList.toggle('hidden');
        btn.setAttribute('aria-expanded', String(!isOpen));
      }
      return;
    }
    // Close if clicking outside
    var popover = document.querySelector('[data-date-popover]');
    if (popover && !popover.classList.contains('hidden')) {
      if (!popover.contains(e.target)) {
        popover.classList.add('hidden');
        var dateBtn = document.querySelector('[data-date-range]');
        if (dateBtn) dateBtn.setAttribute('aria-expanded', 'false');
      }
    }
  });
}

/* ─── 11. Favorite toggle ────────────────────────────────────────────────── */

function initFavoriteToggle() {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-favorite-toggle]');
    if (!btn) return;
    e.preventDefault();
    var isFav = btn.classList.toggle('is-favorited');
    btn.setAttribute('aria-pressed', String(isFav));
  });
}

/* ─── 12. Gallery switch ─────────────────────────────────────────────────── */

function initGallery() {
  document.addEventListener('click', function (e) {
    var thumb = e.target.closest('[data-gallery-thumb]');
    if (!thumb) return;
    var gallery = thumb.closest('[data-gallery]');
    if (!gallery) return;
    var mainImg = gallery.querySelector('[data-gallery-main]');
    if (!mainImg) return;
    var src = thumb.getAttribute('data-src');
    var alt = thumb.getAttribute('data-alt');
    if (src) mainImg.src = src;
    if (alt) mainImg.alt = alt;
    gallery.querySelectorAll('[data-gallery-thumb]').forEach(function (t) {
      t.classList.remove('is-active');
    });
    thumb.classList.add('is-active');
  });
}

/* ─── 13. Segmented tabs ─────────────────────────────────────────────────── */

function initSegmentedTabs() {
  document.addEventListener('click', function (e) {
    var seg = e.target.closest('[data-segment]');
    if (!seg) return;
    var group = seg.closest('[data-segments]');
    if (!group) return;
    group.querySelectorAll('[data-segment]').forEach(function (s) {
      s.classList.remove('is-active');
      s.setAttribute('aria-selected', 'false');
    });
    seg.classList.add('is-active');
    seg.setAttribute('aria-selected', 'true');
  });
}

/* ─── 14. Bottom-nav active highlight ────────────────────────────────────── */

function initBottomNavActive() {
  var nav = document.querySelector('[data-bottom-nav]');
  if (!nav) return;
  var path = location.pathname;
  var filename = path.substring(path.lastIndexOf('/') + 1);
  var hash = location.hash;
  var fullTarget = filename + hash;
  nav.querySelectorAll('a[data-nav-target]').forEach(function (a) {
    var target = a.getAttribute('data-nav-target');
    if (target === fullTarget || target === filename) {
      a.classList.add('is-active');
      a.setAttribute('aria-current', 'page');
    }
  });
  var sidebar = document.querySelector('aside [data-nav-target]');
  if (!sidebar) {
    var aside = nav.closest('body').querySelector('aside[data-nav-target], aside [data-nav-target]');
    if (!aside) {
      var sidebarLinks = document.querySelectorAll('.sidebar-link[data-nav-target]');
      sidebarLinks.forEach(function (a) {
        var target = a.getAttribute('data-nav-target');
        if (target === fullTarget || target === filename) {
          a.classList.add('is-active');
          a.setAttribute('aria-current', 'page');
        }
      });
    }
  }
  var sidebarLinks = document.querySelectorAll('aside .sidebar-link[data-nav-target]');
  sidebarLinks.forEach(function (a) {
    var target = a.getAttribute('data-nav-target');
    if (target === fullTarget || target === filename) {
      a.classList.add('is-active');
      a.setAttribute('aria-current', 'page');
    }
  });
}

/* ─── Boot ────────────────────────────────────────────────────────────────── */

document.addEventListener('DOMContentLoaded', function () {
  initTheme();
  initSidebar();
  initDropdowns();
  initModals();
  initTabs();
  initCopy();
  initDateRange();
  initFavoriteToggle();
  initGallery();
  initSegmentedTabs();
  initBottomNavActive();
  renderIcons();
});

// Expose for use after dynamic DOM insertions
window.renderIcons = renderIcons;
window.setTheme    = setTheme;
