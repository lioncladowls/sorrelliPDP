#!/usr/bin/env python3
"""
Clean the Sorrelli PDP HTML file.
Removes tracking, analytics, Shopify platform artifacts, and marketing widgets.
Preserves all design elements, CSS, and functional scripts.

Output: /Users/collinoswald/Documents/Script Projects/Sorrelli PDP/src/pdp-clean.html
"""

import re
import sys
from bs4 import BeautifulSoup, Comment, NavigableString, Tag

INPUT_FILE = "/Users/collinoswald/Documents/Script Projects/Sorrelli PDP/reference/original-pdp.html"
OUTPUT_FILE = "/Users/collinoswald/Documents/Script Projects/Sorrelli PDP/src/pdp-clean.html"


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Raw text pre-processing before BeautifulSoup parsing
# These are blocks that are cleanly delimited and easier to remove via regex.
# ─────────────────────────────────────────────────────────────────────────────

def preprocess_raw(html: str) -> str:
    """Remove clearly-delimited blocks before parsing."""

    # Remove GTM comment blocks (commented-out script tags)
    html = re.sub(
        r'<!--\s*Google Tag Manager\s*-->.*?<!--\s*End Google Tag Manager\s*-->',
        '',
        html, flags=re.DOTALL
    )

    # Remove the entire Klaviyo app block
    # Delimited by <!-- BEGIN app block: shopify://apps/klaviyo --> and <!-- END app block -->
    html = re.sub(
        r'<!--\s*BEGIN app block: shopify://apps/klaviyo[^>]*-->.*?<!--\s*END app block\s*-->',
        '',
        html, flags=re.DOTALL
    )

    # Remove holiday gift guide link color override style block
    html = re.sub(
        r'<style>\s*a\[href\*=["\']spellbound-edit["\'][^\]]*\].*?</style>',
        '',
        html, flags=re.DOTALL
    )

    # Remove Qikify Smart Bar block
    html = re.sub(
        r'<div id="shopify-block-[^"]*qikify-smartbar[^"]*"[^>]*>.*?</div>(?=\s*<div|</body>)',
        '',
        html, flags=re.DOTALL
    )

    # Remove Qikify Contact Form block (ends just before </body>)
    html = re.sub(
        r'<div id="shopify-block-[^"]*6052823664294247695[^"]*"[^>]*>.*?</div>(?=\s*</body>)',
        '',
        html, flags=re.DOTALL
    )

    # Remove Recurpay CSS link
    html = re.sub(
        r'<link[^>]*recurpay\.css[^>]*/?>',
        '',
        html
    )

    # Remove the entire Recurpay subscription widget script block
    # It starts with <script> (function() { //Append Script and is very long
    html = re.sub(
        r'<script>\s*\(function\(\)\s*\{[^\{]*//Append Script.*?</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove Afterpay block and everything after it (it's the last thing in the file)
    html = re.sub(
        r'<!--\s*Begin Shopify-Afterpay JavaScript Snippet.*',
        '',
        html, flags=re.DOTALL
    )

    # Remove noscript tracking iframes (ClickTrue, GTM)
    html = re.sub(
        r'<noscript><iframe[^>]*(?:ob\.esnbranding|googletagmanager)[^>]*>[^<]*</iframe></noscript>',
        '',
        html, flags=re.DOTALL
    )
    # Also remove the comment-wrapped GTM noscript
    html = re.sub(
        r'<!--\s*<noscript><iframe[^>]*googletagmanager[^>]*>.*?</noscript>\s*-->',
        '',
        html, flags=re.DOTALL
    )
    html = re.sub(r'<!--\s*End Google Tag Manager \(noscript\)\s*-->', '', html)
    # Remove the Google Tag Manager (noscript) comment marker
    html = re.sub(r'<!--\s*Google Tag Manager \(noscript\)\s*-->', '', html)

    # Remove the productInfox metadata block
    html = re.sub(
        r'<script class="productInfox"[^>]*>.*?</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove Klaviyo addedToCart tracking script block(s)
    # These scripts define function addedToCart() and use _learnq to track cart adds.
    # There are two forms - we handle both. The soup-level pass catches whatever raw misses.
    # Form 1: Multiline with "// 2024-03-12" comment
    html = re.sub(
        r'<script type="text/javascript">\s*var _learnq = _learnq \|\| \[\];\s*// 2024-03-12[^<]*(?:<(?!/script>)[^<]*)*</script>',
        '',
        html, flags=re.DOTALL
    )
    # Form 2: Compact single-line var _learnq declaration with inline function addedToCart
    html = re.sub(
        r'<script type="text/javascript">\s*var _learnq = _learnq \|\| \[\]; //var _learnq = klaviyo \|\| \[\]; function addedToCart[^<]*(?:<(?!/script>)[^<]*)*</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove back-in-stock notification style + form + script bundle
    html = re.sub(
        r'<style>[^<]*\.notify-when-back-in-stock[^<]*(?:<(?!/style>)[^<]*)*</style>\s*'
        r'<div style="display:\s*none;">\s*<div data-notify-when-back-in-stock-container>.*?</div>\s*</div>\s*'
        r'<script type="text/javascript">\s*\$\(document\)\.on\("click","\[data-notify-when-back-in-stock\]".*?</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove $$_klaviyo_public_api_key variable declaration script
    html = re.sub(
        r'<script type="text/javascript">\s*const \$\$_klaviyo_public_api_key\s*=\s*["\']YvA8vB["\'];\s*</script>',
        '',
        html
    )

    # Remove listrak analytics inline script
    html = re.sub(
        r"<!-- include 'listrak_analytics' -->\s*<script type=\"text/javascript\">!function\(\)\{var e=document\.createElement\(\"script\"\).*?</script>",
        '',
        html, flags=re.DOTALL
    )

    # Remove the AddShoppers inline script (inside content_for_header block)
    # Pattern: <!-- Adshoppers Analytics – Javascript Framework --> <script>...AddShoppers...</script>
    html = re.sub(
        r'<!--\s*Adshoppers Analytics[^>]*-->\s*<script[^>]*>[^<]*AddShoppers[^<]*(?:<(?!/script>)[^<]*)*</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove Shopify performance marks
    html = re.sub(
        r"<script>window\.performance && window\.performance\.mark && window\.performance\.mark\('shopify\.content_for_header\.[^']+'\);</script>",
        '',
        html
    )

    # Remove Shopify dynamic checkout scripts (all data-source-attribution="shopify.*" scripts)
    html = re.sub(
        r'<script[^>]*data-source-attribution="shopify\.[^"]*"[^>]*>.*?</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove orphaned Google Ads / GTM comment lines (scripts were removed, comments remain)
    html = re.sub(
        r'<!--\s*<script[^>]*googleoptimize[^>]*></script>\s*-->',
        '',
        html, flags=re.I
    )
    # Remove "Global site tag (gtag.js)" comment header (its script was already removed)
    html = re.sub(
        r'<!--\s*Global site tag \(gtag\.js\)[^\-]*-->',
        '',
        html, flags=re.I | re.DOTALL
    )
    # Remove empty/stub HTML comments left by removed blocks
    html = re.sub(r'<!--\s*-->', '', html)

    # Remove oEmbed link tag
    html = re.sub(
        r'<link[^>]*type="application/json\+oembed"[^>]*/?>',
        '',
        html
    )

    # Remove Shopify modules script
    html = re.sub(
        r'<script type="module">[^<]*\(o\.Shopify=o\.Shopify\|\|\{\}\)\.modules=!0[^<]*</script>',
        '',
        html
    )

    # Remove the Shopify trekkie load stub (starts with !function(o){function n()...)
    html = re.sub(
        r'<script>[^<]*!function\(o\)\{function n\(\)\{var o=\[\];function n\(\)\{o\.push[^<]*(?:<(?!/script>)[^<]*)*</script>',
        '',
        html, flags=re.DOTALL
    )

    # Remove shop-js payment-terms module import block
    html = re.sub(
        r'<script type="module">\s*await import\("//www\.sorrelli\.com/cdn/shopifycloud/shop-js/modules/v2/client\.payment-terms[^<]*(?:<(?!/script>)[^<]*)*</script>',
        '',
        html, flags=re.DOTALL
    )

    return html


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: BeautifulSoup tag-level cleaning
# ─────────────────────────────────────────────────────────────────────────────

# Script src patterns to REMOVE
REMOVE_SCRIPT_SRC_PATTERNS = [
    r'googletagmanager\.com',
    r'ob\.esnbranding\.com',
    r'cloudfront\.net.*redirect-app',
    r'cjshpf\.com',
    r'cj-event-st',
    r'addshoppers\.com',
    r'checkouts/internal/preloads',
    r'shop\.app/checkouts',
    r'shopifycloud/shop-js',
    r'storefront/assets/shopify_pay',
    r'shopifycloud/storefront',
    r'shopifycloud/perf-kit',
    r'shop_events_listener',
    r'trekkie\.storefront',
    r'hotjar\.js',
    r'afterpay',
    r'shopify\.loadfeatures',
    r'loadfeatures',
]
REMOVE_SCRIPT_SRC_RE = re.compile('|'.join(REMOVE_SCRIPT_SRC_PATTERNS), re.I)

# Script id/class to REMOVE
REMOVE_SCRIPT_BY_ID = {
    '__st',
    'web-pixels-manager-setup',
    'apple-pay-shop-capabilities',
    'shopify-features',
    'shop-js-analytics',
    'captcha-bootstrap',
}

# Inline script content patterns to REMOVE (any match → remove whole tag)
REMOVE_INLINE_SCRIPT_CONTENT_PATTERNS = [
    # Google Ads gtag
    r"gtag\('config'",
    r'window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];',
    # AddShoppers (belt+suspenders)
    r"js\.id\s*=\s*['\"]AddShoppers['\"]",
    r'addshoppers\.com',
    # Shopify globals block (Window.theme, Currency)
    r'Window\.theme\s*=\s*\{\}',
    # content_for_header asyncLoad (AddShoppers+CJ URLs)
    r'cloudfront\.net.*redirect-app',
    # Shopify shop/locale routes
    r"Shopify\.shop\s*=\s*['\"]sorrelli\.myshopify\.com['\"]",
    # ShopifyPay
    r"window\.ShopifyPay\s*=\s*window\.ShopifyPay\s*\|\|\s*\{\}",
    r'ShopifyPay\.apiHost',
    # Buyer consent / dynamic checkout (all data-source-attribution="shopify.*")
    r'portableWalletsHideBuyerConsent',
    r'DynamicCheckout\.CartBootstrap',
    r'Shopify\.PaymentButton\s*=\s*Shopify\.PaymentButton\s*\|\|\s*\{\}',
    # Shopify featureAssets
    r"window\.Shopify\.featureAssets\[['\"]shop-js",
    # ShopifyPaypalV4
    r'ShopifyPaypalV4VisibilityTracking',
    # ShopifyAnalytics / Trekkie / abandonment
    r'window\.ShopifyAnalytics\s*=',
    r'var trekkie = window\.ShopifyAnalytics\.lib',
    r'sendBeacon.*session_token',
    # GA stub
    r'window\.ga = function ga\(\)',
    r'ga_stub_called',
    # Klaviyo addedToCart (belt+suspenders for any remaining form)
    r'function addedToCart\(\)',
    # Performance mark start
    r"performance\.mark\(['\"]shopify\.content_for_header\.start",
    # Shopify modules (belt+suspenders)
    r'\(o\.Shopify=o\.Shopify\|\|\{\}\)\.modules=!0',
    # shop-js payment import (belt+suspenders)
    r'await import.*client\.payment-terms',
    # cart sync import (belt+suspenders)
    r'await import.*client\.init-shop-cart-sync',
    # window.Shopify.SignInWithShop
    r'SignInWithShop',
]
REMOVE_INLINE_RE = [re.compile(p, re.S | re.I) for p in REMOVE_INLINE_SCRIPT_CONTENT_PATTERNS]

# Meta attrs to REMOVE
REMOVE_META_ATTRS = [
    ('name', 'google-site-verification'),
    ('name', 'facebook-domain-verification'),
    ('name', 'robots'),
    ('id', 'shopify-digital-wallet'),
    ('name', 'shopify-digital-wallet'),
    ('name', 'shopify-checkout-api-token'),
    ('id', 'in-context-paypal-metadata'),
]

# Link href patterns to REMOVE
REMOVE_LINK_HREF_PATTERNS = [
    r'fonts\.shopifycdn\.com',
    r'cdn\.shopify\.com',
    r'v\.shopify\.com',
    r'cdn\.shopifycloud\.com',
    r'productreviews\.shopifycdn\.com',
    r'shop\.app',
    r'monorail-edge\.shopifysvc\.com',
    r'shopifycloud.*checkout',
    r'json\+oembed',
]
REMOVE_LINK_HREF_RE = re.compile('|'.join(REMOVE_LINK_HREF_PATTERNS), re.I)

# Link id to REMOVE
REMOVE_LINK_BY_ID = {'shopify-accelerated-checkout-styles'}

# Style id to REMOVE
REMOVE_STYLE_BY_ID = {'shopify-accelerated-checkout-cart'}


def should_remove_script(tag) -> bool:
    src = tag.get('src', '')
    tag_id = tag.get('id', '')
    classes = tag.get('class', [])
    if isinstance(classes, str):
        classes = [classes]
    data_attr = tag.get('data-source-attribution', '')

    if src and REMOVE_SCRIPT_SRC_RE.search(src):
        return True
    if tag_id in REMOVE_SCRIPT_BY_ID:
        return True
    if 'analytics' in classes:
        return True
    # Remove all Shopify platform scripts with data-source-attribution
    if data_attr and data_attr.startswith('shopify.'):
        return True

    # Inline script checks
    if not src:
        text = tag.get_text()
        if not text.strip():
            return False
        for pat in REMOVE_INLINE_RE:
            if pat.search(text):
                return True

    return False


def should_remove_link(tag) -> bool:
    href = tag.get('href', '')
    rel = tag.get('rel', [])
    if isinstance(rel, list):
        rel = ' '.join(rel)
    tag_id = tag.get('id', '')

    if tag_id in REMOVE_LINK_BY_ID:
        return True
    if href and REMOVE_LINK_HREF_RE.search(href):
        return True
    # Remove all preconnect/dns-prefetch links (they all go to Shopify/tracking CDNs)
    if re.search(r'preconnect|dns-prefetch', rel, re.I):
        return True
    return False


def should_remove_meta(tag) -> bool:
    for attr, val in REMOVE_META_ATTRS:
        if tag.get(attr, '').lower() == val.lower():
            return True
    return False


def should_remove_style(tag) -> bool:
    return tag.get('id', '') in REMOVE_STYLE_BY_ID


def clean_body_tag(soup):
    body = soup.find('body')
    if not body:
        return
    attrs_to_remove = [a for a in body.attrs if a.startswith('data-') and a != 'data-money-format']
    for a in attrs_to_remove:
        del body[a]


def deduplicate_megamenu(soup):
    found = [s for s in soup.find_all('script', src=True) if 'z__jsMegaMenu' in s.get('src', '')]
    for s in found[1:]:
        s.decompose()


def remove_notify_back_in_stock(soup):
    """Remove the back-in-stock notification popup: style, hidden div, and script."""
    import re

    # Remove the style block with .notify-when-back-in-stock rules
    for style in soup.find_all('style'):
        if 'notify-when-back-in-stock' in style.get_text():
            style.decompose()

    # Remove the hidden div containing the back-in-stock form
    for div in soup.find_all('div', attrs={'style': 'display: none;'}):
        if div.find(attrs={'data-notify-when-back-in-stock-container': True}):
            div.decompose()
    # Also try finding by data attribute directly
    for el in soup.find_all(attrs={'data-notify-when-back-in-stock-container': True}):
        # Walk up to the outer display:none div
        parent = el.parent
        if parent and parent.get('style', '').replace(' ', '').lower() in ('display:none;', 'display:none'):
            parent.decompose()
        else:
            el.decompose()

    # Remove the back-in-stock script
    for script in soup.find_all('script'):
        text = script.get_text()
        if 'notify-when-back-in-stock' in text or 'klaviyo_public_api_key' in text:
            script.decompose()


def process_soup(soup):
    for tag in soup.find_all('script'):
        if should_remove_script(tag):
            tag.decompose()

    for tag in soup.find_all('link'):
        if should_remove_link(tag):
            tag.decompose()

    for tag in soup.find_all('meta'):
        if should_remove_meta(tag):
            tag.decompose()

    for tag in soup.find_all('style'):
        if should_remove_style(tag):
            tag.decompose()

    # Remove back-in-stock notification popup (Klaviyo-powered)
    remove_notify_back_in_stock(soup)

    # Remove HTML comments that are tracking/Shopify artifacts
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        text = str(comment).strip()
        if any(p in text for p in [
            '//cdn.bc0a.com',
            'autopilot_sdk',
            'Global site tag',
            'gtag.js',
            'googleoptimize',
            'google optimize',
        ]):
            comment.extract()
        # Remove empty comments
        elif not text:
            comment.extract()

    clean_body_tag(soup)
    deduplicate_megamenu(soup)
    return soup


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Post-format: reindent with 2 spaces, then add section comments
# ─────────────────────────────────────────────────────────────────────────────

def prettify_2space(soup) -> str:
    """Return prettified HTML with 2-space indentation."""
    raw = soup.prettify(formatter='minimal')
    # BeautifulSoup uses 1-space indent; convert to 2-space by doubling leading spaces
    lines = raw.split('\n')
    result = []
    for line in lines:
        stripped = line.lstrip(' ')
        spaces = len(line) - len(stripped)
        result.append('  ' * spaces + stripped)
    return '\n'.join(result)


# Section comment definitions: (trigger_string, comment_to_insert_before_line_containing_trigger)
# We search for the trigger in the formatted output and insert comment just before that line.
SECTION_COMMENTS = [
    # HEAD section
    ('rel="shortcut icon"', '<!-- ═══════ FAVICON LINKS ═══════════════════════════════════════════ -->'),
    ('fancybox.css', '<!-- ═══════ CSS STYLESHEETS ══════════════════════════════════════════ -->'),
    ('jquery.min.js', '<!-- ═══════ THEME SCRIPTS (jQuery, vendors, app) ══════════════════════ -->'),
    # BODY sections - triggers match actual strings in the prettified output
    ('id="shopify-section-header-centered"', '<!-- ═══════ HEADER ════════════════════════════════════════════════════ -->'),
    ('jsAjaxCart', '<!-- ═══════ AJAX CART DRAWER ════════════════════════════════════════ -->'),
    ('id="shopify-section-mega-menu', '<!-- ═══════ MEGA MENU SECTIONS ════════════════════════════════════════ -->'),
    # Product page: trigger is the jsProduct section div
    ('jsProduct" id="shopify-section-product', '<!-- ═══════ PRODUCT PAGE ══════════════════════════════════════════════ -->'),
    ('BreadcrumbList', '<!-- ═══════ BREADCRUMBS ════════════════════════════════════════════════ -->'),
    # Product gallery: trigger from actual class name
    ('product-gallery product-gallery--left-thumbnails', '<!-- ═══════ PRODUCT GALLERY ════════════════════════════════════════════ -->'),
    ('class="product__info', '<!-- ═══════ PRODUCT INFO PANEL ═════════════════════════════════════════ -->'),
    ('Hand Crafted to Last', '<!-- ═══════ VALUE PROPS ═══════════════════════════════════════════════ -->'),
    ('video-with-text', '<!-- ═══════ VIDEO WITH TEXT ═══════════════════════════════════════════ -->'),
    ('stamped-main-widget', '<!-- ═══════ REVIEWS (Stamped.io) ══════════════════════════════════════ -->'),
    ('Woman-Founded, Woman-Led', '<!-- ═══════ WOMAN-FOUNDED SECTION ════════════════════════════════════ -->'),
    ('Here to Spark a Sisterhood', '<!-- ═══════ SISTERHOOD SECTION ═══════════════════════════════════════ -->'),
    ('class="faq', '<!-- ═══════ FAQ ACCORDION ══════════════════════════════════════════════ -->'),
    ('jsRecommendedProducts', '<!-- ═══════ RECOMMENDED PRODUCTS ══════════════════════════════════════ -->'),
    ('You May Also Like', '<!-- ═══════ YOU MAY ALSO LIKE ════════════════════════════════════════ -->'),
    # Footer: trigger from actual id in prettified output
    ('section-footer__icon-bar', '<!-- ═══════ FOOTER ════════════════════════════════════════════════════ -->'),
    ('search-popup js-search-popup', '<!-- ═══════ SEARCH POPUP ══════════════════════════════════════════════ -->'),
    ('color_mappings.js', '<!-- ═══════ COLOR MAPPINGS + COLOR SWATCH SCRIPTS ══════════════════════ -->'),
    ('userway.org accessibility widget', '<!-- ═══════ USERWAY ACCESSIBILITY WIDGET ═══════════════════════════════ -->'),
    ('stamped-script-widget', '<!-- ═══════ STAMPED.IO WIDGET SCRIPT ══════════════════════════════════ -->'),
]


def add_section_comments(html: str) -> str:
    """Insert section comments before lines that contain trigger strings."""
    lines = html.split('\n')
    result = []
    used_comments = set()
    line_lower_cache = [l.lower() for l in lines]

    for i, line in enumerate(lines):
        line_lower = line_lower_cache[i]
        for trigger, comment in SECTION_COMMENTS:
            if trigger.lower() in line_lower and trigger not in used_comments:
                used_comments.add(trigger)
                result.append('')
                result.append(comment)
                break
        result.append(line)

    return '\n'.join(result)


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Final cleanup of leftover blank lines
# ─────────────────────────────────────────────────────────────────────────────

def fix_void_element_closing_tags(html: str) -> str:
    """Remove invalid closing tags for void elements that BS4 sometimes generates."""
    # BS4 occasionally emits </link>, </meta>, </input>, </br>, etc. for void elements
    for void_el in ['link', 'meta', 'input', 'br', 'hr', 'img', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr']:
        html = re.sub(r'\s*</' + void_el + r'>', '', html, flags=re.I)
    return html


def collapse_blank_lines(html: str, max_blank: int = 2) -> str:
    """Collapse runs of more than max_blank consecutive blank lines."""
    return re.sub(r'(\n\s*){' + str(max_blank + 1) + r',}', '\n' * max_blank, html)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_html = f.read()
    orig_bytes = len(raw_html.encode('utf-8'))
    orig_lines = raw_html.count('\n')
    print(f"  Original: {orig_bytes:,} bytes, {orig_lines:,} lines")

    print("Step 1: Raw text pre-processing...")
    cleaned_raw = preprocess_raw(raw_html)
    removed_bytes = orig_bytes - len(cleaned_raw.encode('utf-8'))
    print(f"  Removed {removed_bytes:,} bytes in raw pass")

    print("Step 2: Parsing with BeautifulSoup...")
    soup = BeautifulSoup(cleaned_raw, 'html.parser')

    print("Step 3: Tag-level cleaning...")
    soup = process_soup(soup)

    print("Step 4: Formatting HTML (2-space indent)...")
    formatted = prettify_2space(soup)

    print("Step 5: Adding section comments...")
    formatted = add_section_comments(formatted)

    print("Step 6: Fixing void element closing tags...")
    formatted = fix_void_element_closing_tags(formatted)

    print("Step 7: Collapsing excess blank lines...")
    formatted = collapse_blank_lines(formatted)

    print(f"Writing to {OUTPUT_FILE}...", flush=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(formatted)

    final_bytes = len(formatted.encode('utf-8'))
    final_lines = formatted.count('\n')
    print(f"\n  Output:    {final_bytes:,} bytes, {final_lines:,} lines")
    print(f"  Reduction: {100 * (1 - final_bytes / orig_bytes):.1f}%")
    print("Done!")


if __name__ == '__main__':
    main()
