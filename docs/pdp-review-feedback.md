# Sorrelli PDP — Review & Feedback

**Audit of `pdp-v1.html` against `pdp-best-practices.md` & `brand-identity.md`**
**Updated:** February 28, 2026

---

## Summary Scorecard

| Area | Grade | Notes |
|------|-------|-------|
| Above-Fold Hierarchy | **A-** | All key elements present; missing star rating |
| Product Info Panel | **A** | Price, BNPL, color selector, accordion all strong |
| Image Gallery | **C+** | 4 images; need 5-7 multi-style + zoom |
| Mobile Experience | **D** | Sticky CTA disabled; no dot indicators; no pinch-zoom |
| Brand Alignment | **B-** | Colors aligned; typography undercuts brand |
| Trust & Social Proof | **C** | Reviews empty; stars not above fold; trust strip added |
| Below-Fold Content | **C** | Accumulated, not designed; needs major restructure |
| Performance | **D+** | No lazy load, no srcset, sync jQuery |

---

## What's Working

- **Product Identity Group** — Clean $80.00 pricing, BNPL breakdown ($20 x 4), polished BNPL info modal. Exactly what best practices recommend for accessible luxury.
- **Color Selector** — Unified "Color: Panama Rose · Bright Gold-tone" with small round swatches, active/alternative divider, and "View all colorways >" link. Research-backed pattern.
- **Accordion (About/Promise/Shipping)** — Benefit-oriented labels, multiple sections can open simultaneously, smooth animation, proper ARIA attributes. Strong.
- **Trust Strip** — Compact "Lifetime Promise | Free Shipping $150+ | 30-Day Returns" between CTA and payment badges. Surfaces key trust signals at decision moment.
- **Smart Shipping Signal** — Timezone-aware "Ships Today / Tomorrow / Monday" calculation. Authentic urgency.
- **Brand Color Palette** — Rose-gold (#cab0a3), cream (#FAF3EE), warm neutrals (#eddfd3) throughout. "Hollywood Beige" in action.

---

## Critical Targets

### 1. Enable Mobile Sticky CTA
**Priority:** CRITICAL — affects 70%+ of traffic
**Status:** Code exists, commented out (~line 3649)

The sticky Add to Bag bar JS and CSS both exist but are disabled. With content above the CTA, mobile users lose access to the purchase button on any scroll. This is mandatory per best practices when content sits above CTA.

**Action:** Rewrite using IntersectionObserver (not jQuery scroll listener). Include price in sticky bar. Show only on mobile (<799px). Slide-up animation (300ms). `env(safe-area-inset-bottom)` for iPhone home bar.

### 2. Add Star Rating / Social Proof Above the Fold
**Priority:** CRITICAL — #1 trust signal
**Status:** Missing entirely

**The zero-review problem:** Most Sorrelli products have 0 reviews. Research is clear:
- Showing "0 reviews" or empty stars is negative social proof — actively harmful
- 80% of consumers are less likely to buy products with no reviews (PowerReviews)
- 60% are more likely to buy an unreviewed product if the brand itself has strong ratings

**Recommended approach:**
1. **Always show:** Brand-wide aggregate — e.g., *"Loved by thousands — 4.8/5 average rating"* — styled warm and editorial
2. **Conditionally show:** Per-product stars ONLY when product has 3+ reviews
3. **Selectively show:** Curated badges — "Bestseller," "New Arrival," "Stylist's Pick"
4. **Below fold:** When zero reviews, hide empty state entirely; show same-category reviews instead

### 3. Remove "Excluded from Discounts" Notice
**Priority:** CRITICAL — conversion speed bump at worst location
**Status:** Currently pre-CTA

**Research is unequivocal: remove it.** Reasons:
- Pure negative framing right at purchase decision moment (72% choose options framed positively vs 22% negatively)
- Introduces the concept of discounts to someone who wasn't thinking about them — can drive them to the sale section instead
- No luxury or accessible-luxury jewelry brand does this on PDPs (Mejuri, Monica Vinader, Kendra Scott, Gorjana — none)
- The absence of a sale badge already communicates "full price"

**Handle reactively instead:**
- **At checkout:** If promo code doesn't apply: *"[Product Name] is a Signature piece at its everyday best price and is not included in this promotion"*
- **FAQ:** One entry with positive framing
- **CS script:** *"This is one of our Signature pieces — always at its best value year-round."*

### 4. Expand Gallery + Enable Zoom
**Priority:** CRITICAL
**Status:** 4 images, zoom disabled

Gallery has: Product Shot, Alternate Angle, Lifestyle, Detail. Missing: on-body/model (critical for earrings — scale context), video.

Zoom is explicitly disabled (`"enable_zoom": false`). For jewelry at $80, shoppers need to see crystal facets and metalwork up close.

**Action:** Add on-model image from Image Gen project. Enable zoom. Add mobile dot indicators (thumbnails are hidden on mobile with no indication of image count).

---

## Important Targets

### 5. Upgrade Typography (V2)
**Priority:** Important — biggest lever for brand feel
**Status:** Open Sans only

Open Sans is the sole typeface — readable but forgettable. Makes the page feel like a default Shopify template, not "aspirational achievable luxury."

**V2 approach:**
- Warm serif for product name and section headings (Cormorant Garamond, Playfair Display, or similar)
- Open Sans for body copy (keeps readability)
- Warm the page background from #fff to #FDFBF9
- Shift text grays (#333/#444/#555) toward warm browns (#3D3531/#504842/#6B605A)

### 6. Fix Accessibility Gaps
**Priority:** Important
**Status:** Partial

Accordion now has proper `aria-expanded` and `<button>` elements (fixed in this session). Remaining: duplicate HTML IDs from Shopify extraction, missing skip-nav links.

### 7. CSS Custom Properties
**Priority:** Important
**Status:** Not implemented

All colors, fonts, and spacing are hardcoded in inline styles. Extract into `:root` variables as design tokens for maintainability.

---

## Below-Fold Section Audit

### SECTION A: Value Prop Cards ("Hand Crafted to Last a Lifetime")
**Verdict:** KEEP and REWORK

**What's good:** Right content, right position. Addresses three biggest anxieties: shipping speed, return risk, durability. Custom SVG icons, warm champagne background.

**What's not good:** "Wear for a Lifetime" copy is vague fluff — doesn't communicate the actual lifetime guarantee. Each card loads a separate 1200x900 background image (6 total) for what could be a CSS color. Heading overlaps with card #3.

**Action:** Fix copy on card #3. Replace background images with CSS. Merge in "Luxuriously Comfortable" from Section D.

---

### SECTION B: Hidden Second CTA
**Verdict:** REMOVE

`class="is-hidden"` — completely invisible dead code. Adds page weight with zero benefit. The sticky mobile CTA will solve the repeated-CTA need better.

---

### SECTION C: "Unboxing Your New Look" Video
**Verdict:** REMOVE

**This is the weakest section on the page:**
- iPhone X mockup (2017 device) using "Marvel Devices" CSS library — gimmicky and dated
- Generic brand unboxing video, not product-specific
- Weak testimonial: *"Support businesses online, do some online shopping!"* — reads like an unedited Instagram comment
- Terrible copy: *"It's no secret that Sorrelli jewelry is second to none"* — awkward boilerplate
- Massive vertical space: 600px desktop, 1020px mobile
- External CSS dependency just for the phone frame
- Antithetical to brand identity — "editorial but approachable" vs. 2019 growth hack aesthetic

If video is desired on PDP, it should be product-specific and in the gallery.

---

### SECTION D: Craftsmanship Features (Image + Text)
**Verdict:** REWORK and CONSOLIDATE with Section A

**What's good:** "Luxuriously Comfortable" with "monster backs" detail is a genuine differentiator. Warm color palette.

**What's not good:** "Elegantly Affordable" undermines aspirational positioning. "Handcrafted to Last a Lifetime" is the FOURTH repetition of this message. Significant overlap with Section A.

**Action:** Keep "Luxuriously Comfortable" (unique, specific). Drop "Elegantly Affordable." Merge craftsmanship content with value prop cards. Eliminate redundancy.

---

### SECTION E: Reviews
**Verdict:** REWORK

**What's good:** Cross-product review carousel is a smart fallback pattern. Warm styling.

**What's not good:** Empty product review state ("Be the first to review this item" + five gray stars) is negative social proof. Cross-product reviews are for unrelated product types (ring, necklace, different earrings). "Love it" is two words of nothing. Reviews are hardcoded, not dynamic.

**Action:** Hide empty product review state entirely (per zero-review research). Show reviews from same category (earrings) or collection. Surface longer, substantive reviews.

---

### SECTION F: "Woman-Founded, Woman-Led"
**Verdict:** CONDENSE

**What's good:** Genuinely resonates with women self-shoppers. Copy is concise and specific. Personal photo adds warmth and authenticity.

**What's not good:** Full image+text founder story is About page content on a PDP. Research shows no comparable accessible-luxury jewelry brand (Gorjana, Mejuri, BaubleBar, Ana Luisa) includes this on PDPs. They keep PDPs product-focused; brand story lives on About pages.

**Action:** Reduce to a compact trust badge/line in value prop area — e.g., icon + "Woman-Founded, Handcrafted Since 1985." Full story belongs on About page.

---

### SECTION G: "Here to Spark a Sisterhood That Sparkles"
**Verdict:** REMOVE from PDP

Two consecutive full-width brand narrative sections with family photos is About page content, full stop. Copy tries to hit too many notes in four sentences (sisterhood, connection, confidence, durability, sustainability). "Handcrafted to last a lifetime" is the FIFTH repetition. Delays shoppers from reaching FAQs and recommendations.

**Action:** Move to About page. If the "sisters" etymology is desired, distill to one line in value prop area.

---

### SECTION H: FAQ Accordion
**Verdict:** REWORK

**What's good:** FAQs are proven conversion tools. Accordion UX is correct. Shipping/returns answers are specific and useful.

**What's not good:** Q3 and Q5 are duplicates (both about returns). Q1 ("How is Sorrelli Different?") repeats messaging from Sections A, D, and G. Questions are brand-focused, not product-focused — shoppers want "What are these earrings made of?" not "How is Sorrelli Different?"

**Action:** Remove duplicate Q5. Replace Q1 with product-specific question (materials, care). Add "How do I care for my Sorrelli jewelry?" Reorder: shipping, returns, materials first.

---

### SECTIONS I + J: Recommendations ("Shop All" + "You May Also Like")
**Verdict:** CONSOLIDATE

Both containers empty in prototype. Two consecutive recommendation sections is redundant. Missing "Wear It With" / "Complete the Look" (outperforms generic recs per research).

**Action:** Consolidate into one section: "Complete the Look" (matched set data exists in product tags) + "More from Panama Rose."

---

## Recommended Below-Fold Sequence

**Current (accumulated):**
```
A. Value Props → B. Hidden CTA → C. Unboxing Video → D. Craftsmanship →
E. Reviews → F. Woman-Founded → G. Sisterhood → H. FAQ → I+J. Recommendations
```

**Recommended (intentional):**
```
1. Value Props (consolidated: shipping + returns + lifetime + "luxuriously comfortable" + "woman-founded" badge)
2. Reviews (smart fallback to same-category reviews when no product-specific ones)
3. FAQ Accordion (product-focused, no duplicates)
4. Cross-sell: "Complete the Look" + "More from Panama Rose"
```

4 focused sections instead of 10 accumulated ones. Unboxing video, hidden CTA, Sisterhood section, and duplicate craftsmanship section all cut.

---

## Brand Identity Alignment

| Brand Directive | Status | Notes |
|----------------|--------|-------|
| Warm, golden, never cold/blue | Aligned | Rose-gold, cream, warm neutral palette throughout |
| Product is always hero | Aligned | Gallery prominent above fold, dominant viewport presence |
| Editorial but approachable | **Gap** | Open Sans is generic — needs serif for headings (V2) |
| "Quiet, beautiful moment" | Partial | Below-fold brand sections try hard but unboxing video section breaks this |
| Aspirational, not pretending to be fine jewelry | Aligned | Price presentation and copy tone are honest and confident |
| Self-purchase framing | **Weak** | Copy doesn't lean into "treat yourself" / self-expression language |
| "Hollywood Beige" visual language | **Partial** | Colors yes, but typography and page background don't deliver warmth |
| Craftsmanship narrative justifies price | Aligned | Accordion, value props, and features all communicate this — but overrepeat it |

---

## Implementation Roadmap

### Wave 1 — Quick Wins (Current Session)
1. ~~Implement trust strip near CTA~~ DONE
2. Enable mobile sticky CTA
3. Remove "Excluded from discounts" notice
4. Remove unboxing video section (Section C)
5. Remove hidden second CTA (Section B)

### Wave 2 — Restructure Below-Fold
1. Consolidate Sections A + D (value props + craftsmanship)
2. Condense Section F to trust badge (woman-founded)
3. Remove Section G (sisterhood — move to About page)
4. Rework FAQ (remove dupes, product-focused questions)
5. Fix reviews (hide empty state, same-category fallback)
6. Consolidate cross-sell sections

### Wave 3 — V2 Polish
1. Upgrade typography (serif headings, warm text colors)
2. Warm page background (#fff → #FDFBF9)
3. CSS custom properties / design tokens
4. Expand gallery (on-model image, enable zoom, mobile dots)
5. Add brand-wide aggregate rating above fold
6. "Wear It With" / "Complete the Look" cross-sell
7. Curated product badges (Bestseller, New Arrival, Stylist's Pick)

---

*Source: pdp-v1.html audited against pdp-best-practices.md & brand-identity.md*
