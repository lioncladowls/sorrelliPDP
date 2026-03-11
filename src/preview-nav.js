/**
 * Sorrelli Redesign — Standalone Preview Nav
 *
 * Include on any page: <script src="preview-nav.js"></script>
 * Place a <div id="preview-nav"></div> where you want the nav to appear.
 * The script auto-detects the current page and sets active states.
 */
(function() {
  'use strict';

  // ── Auth guard ──
  // Redirect to index.html if not authenticated
  var AUTH_HASH = '1e4a2148';
  var AUTH_KEY = 'sorrelli_preview_auth';
  if (sessionStorage.getItem(AUTH_KEY) !== AUTH_HASH) {
    window.location.replace('index.html');
    return;
  }

  // ── Page registry ──
  var pages = {
    'pdp-v2.html':                { group: 'product', label: 'Mockup' },
    'design-philosophy.html':     { group: 'product', label: 'Design Philosophy' },
    'customization-guide.html':   { group: 'product', label: 'Customization Guide' },
    'cart.html':                  { group: 'cart',    label: 'Mockup' },
    'cart-design-philosophy.html':{ group: 'cart',    label: 'Design Philosophy' },
    'cart-developer-guide.html':  { group: 'cart',    label: 'Developer Guide' }
  };

  // ── Detect current page ──
  var path = window.location.pathname;
  var filename = path.substring(path.lastIndexOf('/') + 1) || 'index.html';
  var current = pages[filename] || {};

  // ── Helper: active class if match ──
  function activeIf(condition) {
    return condition ? ' preview-nav__group-btn--active' : '';
  }
  function activeLinkIf(condition) {
    return condition ? ' preview-nav__dropdown-link--active' : '';
  }

  // ── Determine if this page has a drawer to open ──
  // Show "Open Drawer" on pages that have a .cart-drawer element
  var hasDrawer = !!document.querySelector('.cart-drawer') || !!document.querySelector('[data-open-drawer-target]');

  // ── Build nav HTML ──
  var html = ''
    + '<nav class="preview-nav">'
    + '  <div class="preview-nav__inner">'
    + '    <span class="preview-nav__label">Sorrelli Redesign</span>'
    + '    <div class="preview-nav__groups">'
    // Product Page group
    + '      <div class="preview-nav__group" data-nav-group>'
    + '        <button class="preview-nav__group-btn' + activeIf(current.group === 'product') + '" data-nav-toggle>'
    + '          Product Page'
    + '          <svg viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"/></svg>'
    + '        </button>'
    + '        <div class="preview-nav__dropdown">'
    + '          <a href="pdp-v2.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'pdp-v2.html') + '">Mockup</a>'
    + '          <a href="design-philosophy.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'design-philosophy.html') + '">Design Philosophy</a>'
    + '          <a href="customization-guide.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'customization-guide.html') + '">Customization Guide</a>'
    + '        </div>'
    + '      </div>'
    // Separator
    + '      <div class="preview-nav__sep"></div>'
    // Cart Page group
    + '      <div class="preview-nav__group" data-nav-group>'
    + '        <button class="preview-nav__group-btn' + activeIf(current.group === 'cart') + '" data-nav-toggle>'
    + '          Cart Page'
    + '          <svg viewBox="0 0 10 6"><path d="M1 1l4 4 4-4"/></svg>'
    + '        </button>'
    + '        <div class="preview-nav__dropdown">'
    + '          <a href="cart.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'cart.html') + '">Mockup</a>'
    + '          <a href="cart-design-philosophy.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'cart-design-philosophy.html') + '">Design Philosophy</a>'
    + '          <a href="cart-developer-guide.html" class="preview-nav__dropdown-link' + activeLinkIf(filename === 'cart-developer-guide.html') + '">Developer Guide</a>'
    + '        </div>'
    + '      </div>'
    // Open Drawer button (always shown — opens drawer on pages that have one, links to cart.html?drawer=1 on pages that don't)
    + '      <div class="preview-nav__sep"></div>'
    + '      <button class="preview-nav__drawer-btn" id="preview-nav-open-drawer">'
    + '        <svg viewBox="0 0 24 24" style="width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;"><path d="M3 3h7v18H3zM10 3h11v18H10z"/><path d="M14 9h4M14 12h4M14 15h4"/></svg>'
    + '        Open Drawer'
    + '      </button>'
    + '      <div class="preview-nav__sep"></div>'
    + '      <button class="preview-nav__logout-btn" id="preview-nav-logout">'
    + '        <svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
    + '        Log Out'
    + '      </button>'
    + '    </div>'
    + '  </div>'
    + '</nav>';

  // ── CSS ──
  var css = ''
    + '.preview-nav { background: #3D3531; border-bottom: 1px solid rgba(255,255,255,0.08); position: sticky; top: 0; z-index: 9999; }'
    + '.preview-nav__inner { max-width: 1200px; margin: 0 auto; padding: 10px 24px; display: flex; align-items: center; justify-content: space-between; gap: 12px; }'
    + '.preview-nav__label { font-size: 13px; font-weight: 600; color: #cab0a3; letter-spacing: 0.06em; text-transform: uppercase; white-space: nowrap; }'
    + '.preview-nav__groups { display: flex; gap: 4px; align-items: center; }'
    + '.preview-nav__group { position: relative; }'
    + '.preview-nav__group-btn { font-size: 13px; font-family: "Open Sans", sans-serif; color: rgba(255,255,255,0.6); background: none; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 5px; }'
    + '.preview-nav__group-btn:hover { color: #ffffff; background: rgba(255,255,255,0.08); }'
    + '.preview-nav__group-btn--active { color: #ffffff; background: rgba(255,255,255,0.12); }'
    + '.preview-nav__group-btn svg { width: 10px; height: 10px; fill: currentColor; opacity: 0.6; transition: transform 0.2s ease; }'
    + '.preview-nav__group.is-open .preview-nav__group-btn svg { transform: rotate(180deg); }'
    + '.preview-nav__dropdown { position: absolute; top: calc(100% + 6px); left: 0; min-width: 200px; background: #2a2222; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 6px 0; opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(-4px); transition: all 0.2s ease; box-shadow: 0 8px 24px rgba(0,0,0,0.3); }'
    + '.preview-nav__group.is-open .preview-nav__dropdown { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0); }'
    + '.preview-nav__dropdown-link { display: block; font-size: 13px; color: rgba(255,255,255,0.6); text-decoration: none; padding: 8px 16px; transition: all 0.15s ease; }'
    + '.preview-nav__dropdown-link:hover { color: #ffffff; background: rgba(255,255,255,0.08); }'
    + '.preview-nav__dropdown-link--active { color: #ffffff; }'
    + '.preview-nav__sep { width: 1px; height: 20px; background: rgba(255,255,255,0.12); margin: 0 4px; }'
    + '.preview-nav__drawer-btn { font-size: 12px; font-family: "Open Sans", sans-serif; color: #cab0a3; background: rgba(202,176,163,0.12); border: 1px solid rgba(202,176,163,0.3); padding: 5px 12px; border-radius: 4px; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 5px; white-space: nowrap; }'
    + '.preview-nav__drawer-btn:hover { background: rgba(202,176,163,0.22); border-color: rgba(202,176,163,0.5); }'
    + '.preview-nav__logout-btn { font-size: 12px; font-family: "Open Sans", sans-serif; color: rgba(255,255,255,0.45); background: none; border: 1px solid rgba(255,255,255,0.12); padding: 5px 12px; border-radius: 4px; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 5px; white-space: nowrap; }'
    + '.preview-nav__logout-btn:hover { color: rgba(255,255,255,0.8); border-color: rgba(255,255,255,0.3); background: rgba(255,255,255,0.06); }'
    + '@media (max-width: 480px) { .preview-nav__inner { padding: 8px 16px; } .preview-nav__label { display: none; } .preview-nav__groups { width: 100%; justify-content: center; } .preview-nav__drawer-btn { font-size: 11px; padding: 4px 10px; } }';

  // ── Inject ──
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  // Insert nav at placeholder or as first child of body
  var placeholder = document.getElementById('preview-nav');
  if (placeholder) {
    placeholder.outerHTML = html;
  } else {
    document.body.insertAdjacentHTML('afterbegin', html);
  }

  // ── Dropdown toggle JS ──
  document.querySelectorAll('[data-nav-toggle]').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var group = btn.closest('[data-nav-group]');
      var wasOpen = group.classList.contains('is-open');
      document.querySelectorAll('[data-nav-group]').forEach(function(g) { g.classList.remove('is-open'); });
      if (!wasOpen) group.classList.add('is-open');
    });
  });
  document.querySelectorAll('.preview-nav__dropdown').forEach(function(dd) {
    dd.addEventListener('click', function(e) { e.stopPropagation(); });
  });
  document.addEventListener('click', function() {
    document.querySelectorAll('[data-nav-group]').forEach(function(g) { g.classList.remove('is-open'); });
  });

  // ── Log Out button ──
  var logoutBtn = document.getElementById('preview-nav-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      sessionStorage.removeItem(AUTH_KEY);
      window.location.replace('index.html');
    });
  }

  // ── Open Drawer button ──
  var drawerBtn = document.getElementById('preview-nav-open-drawer');
  if (drawerBtn) {
    drawerBtn.addEventListener('click', function() {
      // If page has a drawer, open it directly
      var drawer = document.querySelector('.cart-drawer');
      var backdrop = document.querySelector('.cart-drawer-backdrop');
      if (drawer && backdrop) {
        drawer.classList.add('is-open');
        backdrop.classList.add('is-open');
        document.body.style.overflow = 'hidden';
        drawer.setAttribute('aria-hidden', 'false');
      } else {
        // Navigate to cart with drawer open
        window.location.href = 'cart.html?drawer=1';
      }
    });
  }
})();
