# Sorrelli PDP Redesign — Project Scope

## What This Project Is

A ground-up redesign of the Sorrelli.com Product Detail Page (PDP). We're taking the current production Shopify PDP, stripping it down to its structural essentials, and rebuilding the presentation layer to align with Sorrelli's brand identity: **aspirational, achievable luxury**.

## The Problem

The current PDP is a standard Shopify production page — functional but bloated. It carries years of accumulated theme code, third-party scripts, tracking pixels, and generic e-commerce patterns that don't serve the brand. The page works, but it doesn't *feel* like Sorrelli. For a brand built on warmth, intimacy, and curated beauty, the shopping experience should match the product experience.

## The Goal

Design a PDP that:

1. **Feels like the brand** — warm, golden, editorial, intimate. The same "quiet, beautiful moment" that defines Sorrelli's visual identity should carry through to the shopping experience.
2. **Strips the bloat** — remove unnecessary Shopify theme cruft, redundant scripts, and generic patterns. Keep what matters, cut what doesn't.
3. **Keeps the full page design** — we're not removing features or sections. We're refining how they look and feel. Every functional element the current PDP has should be accounted for.
4. **Optimizes for conversion** — luxury feel with clear purchase flow. The product is the hero, the experience builds desire, and the path to purchase is effortless.

## What We're Working From

### Reference HTML
- **Source:** [Kathleen Studded Dangle Earrings](https://www.sorrelli.com/products/kathleen-studded-dangle-earrings-eff80bgpro)
- **File:** `reference/original-pdp.html` — full production HTML (~5,900 lines of Shopify output)
- This serves as our structural reference for what sections/elements exist on the current PDP

### Brand Identity
- **File:** `docs/brand-identity.md` — distilled from the Image Gen Project's creative direction
- Defines the visual language, color palette, mood, and principles that should drive every design decision

## Approach

1. **Audit the current HTML** — identify every meaningful section, component, and feature on the existing PDP. Separate structure from bloat.
2. **Define the component map** — what stays, what goes, what gets redesigned
3. **Rebuild clean** — new HTML/CSS that delivers the same functionality with the brand's visual identity baked in
4. **Iterate** — refine based on how it looks and feels, not just whether it works

## Project Rules

1. **`reference/original-pdp.html` is read-only.** It's a historical record of the production PDP. Never modify it.
2. **All work happens in new files.** Build forward from the reference, don't edit it.
3. **Git for everything.** Atomic commits for each meaningful change so we can roll back surgically. Feature branches, not direct-to-main.
4. **Commit messages explain the "why."** Future-us needs to understand intent when reverting.

## What This Is NOT

- Not a Shopify theme — this is a standalone HTML/CSS prototype
- Not a backend project — no Liquid, no server logic, no cart integration (yet)
- Not a pixel-perfect clone — we're redesigning, not replicating

## Project Structure

```
Sorrelli PDP/
├── docs/
│   ├── brand-identity.md    # Brand visual language & principles
│   └── project-scope.md     # This file
├── reference/
│   └── original-pdp.html    # Current production PDP (raw Shopify HTML)
└── src/                     # Redesigned PDP (to be built)
```
