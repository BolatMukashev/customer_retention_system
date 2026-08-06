---
version: "alpha"
name: "Bento Produtividade Flexível"
description: "Modular and organized Bento Style landing page for a customizable productivity platform. Ideal for landing pages, modern websites. AI-ready template."
colors:
  primary: "#ADD8E6"
  secondary: "#98FB98"
  tertiary: "#FFFFFF"
  neutral: "#F0F2F5"
  surface: "#FFFACD"
  accent: "#FFDAB9"
typography:
  h1:
    fontFamily: Inter
    fontSize: 2.5rem
    fontWeight: 700
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
rounded:
  sm: 12px
  md: 24px
  lg: 36px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.sm}"
    padding: 12px
---

## Overview

Modular and organized Bento Style landing page for a customizable productivity platform. Ideal for landing pages, modern websites. AI-ready template. Before Notion blew the doors off in 2018, productivity tools were rigid. You got rows and columns — maybe a kanban board if the product team felt generous. The workspace was their workspace, not yours.

Notion changed the contract. Suddenly every block was draggable, resizable, nestable. Coda followed with its own take — tables that behaved like apps, layouts that morphed per user. The bento grid wasn't just aesthetic anymore; it became the interaction model itself. Each cell a micro-app. Each arrangement a personal system. The modular layout stopped being a design choice and became an expectation.

What's interesting is how this bled outward. Linear adopted dense, customizable panels. Craft went modular. Even legacy tools like Confluence started bolting on block-based editing. The bento grid for productivity isn't a trend — it's infrastructure now. Users don't just want to see their data arranged nicely. They want to rearrange it themselves, endlessly, until the tool disappears into their workflow.

- Density: 3/10 — Airy
- Variance: 2/10 — Structured
- Motion: 4/10 — Subtle

- **Style:** Modular, Organized, Modern
- **Keywords:** productivity, modular, customizable, bento grid, organized, efficient, modern, intuitive, flexible, clean
- **Era:** 2026+ Organização Inteligente
- **Light/Dark:** ✓ Full / ✗ No

## Colors

- **Azul Claro** (#ADD8E6) — Accent highlight, links and focus states
- **Verde Menta** (#98FB98) — Secondary surface or text color
- **Branco** (#FFFFFF) — Light surface, card backgrounds
- **Cinza Suave** (#F0F2F5) — Secondary text, borders, muted elements
- **Amarelo Pastel** (#FFFACD) — Warning states, attention indicators
- **Rosa Pêssego** (#FFDAB9) — Decorative accent, highlight elements
- **Roxo Lavanda** (#E6E6FA) — Accent color, emphasis elements
- **Preto** (#333333) — Deep contrast surface


## Typography

- **Display / Hero:** Bento — Weight 700, tight tracking, used for headline impact
- **Accent:** Inter — Used for decorative or emphasis text
- **Body:** Bento — Weight 400, 16px/1.6 line-height, max 72ch per line
- **UI Labels / Captions:** Bento — 0.875rem, weight 500, slight letter-spacing
- **Monospace:** JetBrains Mono — Used for code, metadata, and technical values

Scale:
- Hero: clamp(2.5rem, 5vw, 4rem)
- H1: 2.25rem
- H2: 1.5rem
- Body: 1rem / 1.6
- Small: 0.875rem


## Layout

- **Grid:** CSS Grid primary. Max-width containment: 1280px centered with 1.5rem side padding.
- **Spacing rhythm:** Balanced. Base unit: 0.5rem (8px).
- **Section vertical gaps:** clamp(4rem, 8vw, 8rem).
- **Hero layout:** Split-screen (text left, visual right).
- **Feature sections:** Zig-zag alternating text+image rows. No 3-equal-columns.
- **Mobile collapse:** All multi-column layouts collapse below 768px. No horizontal overflow.
- **z-index contract:** base (0) / sticky-nav (100) / overlay (200) / modal (300) / toast (500).


## Elevation & Depth

Layouts de grid "Bento" com cards arredondados e sombras suaves, tipografia sans-serif limpa, ícones minimalistas, micro-interações de hover com expansão de card, transições de elementos suaves e organizadas, foco na modularidade e personalização.

- **Physics:** Ease-out curves, 200-300ms duration. Smooth and predictable.
- **Entry animations:** Fade + translate-Y (16px → 0) over 420ms ease-out. Staggered cascades for lists: 80ms between items.
- **Hover states:** Subtle color shift + shadow adjustment over 200ms.
- **Page transitions:** Fade only (200ms).
- **Performance:** Only transform and opacity animated. No layout-triggering properties.


## Shapes

Base corner radius: 12px. See rounded tokens in front matter for the full scale.


## Components

- **Primary Button:** Rounded (12px) shape. Accent color fill. Hover: 8% darken + subtle lift shadow. Active: -1px translate tactile press. Font weight 600. No outer glows.
- **Secondary / Ghost Button:** Outline variant. 1.5px border in muted color. Text in primary color. Hover: subtle background fill.
- **Cards:** Rounded (12px) corners. Surface background. Subtle shadow (0 2px 12px rgba(0,0,0,0.06)). 1px border stroke.
- **Inputs:** Label above input. 1px border stroke. Focus ring: 2px accent color offset 2px. Error text below in semantic red. No floating labels.
- **Navigation:** Primary surface background. Active item: accent color indicator. Font weight 500 when active.
- **Skeletons:** Shimmer animation matching component dimensions. No circular spinners.
- **Empty States:** Icon-based composition with descriptive text and action button.


## Do's and Don'ts

- No emojis in UI — use icon system only (Lucide, Heroicons)
- No pure black (#000000) — use off-black or charcoal variants
- No oversaturated accent colors (saturation cap: 80%)
- No 3-column equal-width feature layouts — use zig-zag or asymmetric grid
- No `h-screen` — use `min-h-[100dvh]`
- No AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen"
- No broken external image links — use picsum.photos or inline SVG
- No generic lorem ipsum in demos

- Do Layouts de grid "Bento"
- Do Cards arredondados
- Do Sombras suaves
- Do Tipografia sans-serif limpa
- Do Ícones minimalistas
- Do Micro-interações de expansão de card.


## Use Case

Landing pages, Modern websites

<!-- Source: https://designmd.app/library/bento-produtividade-flexivel · designmd.app -->
