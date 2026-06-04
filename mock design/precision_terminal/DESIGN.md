---
name: Precision Terminal
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#c6c6ca'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#8f9094'
  outline-variant: '#45474a'
  surface-tint: '#c6c6ca'
  primary: '#c6c6ca'
  on-primary: '#2f3034'
  primary-container: '#121417'
  on-primary-container: '#7d7e82'
  inverse-primary: '#5d5e62'
  secondary: '#c4c6ce'
  on-secondary: '#2d3037'
  secondary-container: '#464950'
  on-secondary-container: '#b6b8c0'
  tertiary: '#4ae176'
  on-tertiary: '#003915'
  tertiary-container: '#001906'
  on-tertiary-container: '#009241'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2e2e6'
  primary-fixed-dim: '#c6c6ca'
  on-primary-fixed: '#1a1c1f'
  on-primary-fixed-variant: '#45474a'
  secondary-fixed: '#e1e2ea'
  secondary-fixed-dim: '#c4c6ce'
  on-secondary-fixed: '#191c22'
  on-secondary-fixed-variant: '#44474d'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  data-tabular:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
  label-xs:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
  ticker-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
spacing:
  unit: 4px
  container-padding: 8px
  gutter: 1px
  stack-compact: 4px
  stack-default: 12px
  edge-margin: 0px
---

## Brand & Style
The design system is engineered for high-performance financial environments where information density and cognitive speed are paramount. The brand personality is authoritative, clinical, and unapologetically technical. It eschews aesthetic trends in favor of raw utility and data-driven hierarchy.

The visual style is a fusion of **Modern Corporate** and **Technical Brutalism**. It utilizes a strict border-based grid system to delineate information without wasting pixels on whitespace or shadows. The interface should feel like a high-precision instrument—fast, stable, and transparent. Every pixel must serve a functional purpose; there are no decorative flourishes.

## Colors
The palette is optimized for long-duration monitor usage in low-light environments, prioritizing legibility and status signaling.

- **Foundations:** Use `background_deep` for the primary application shell and `background_surface` for nested panels and data containers.
- **Typography:** Use `#FFFFFF` for primary data points and active headers. Use `text_muted` (#94A3B8) for secondary labels and metadata.
- **Indicators:** The green and red values are reserved strictly for directional market movement and status alerts. Do not use these for branding or decorative elements.
- **Borders:** Use `#2D333D` for all structural grid lines. This low-contrast border ensures separation without creating visual noise.

## Typography
Typography in this design system is treated as data. We utilize **Inter** for its exceptional legibility and comprehensive support for OpenType features.

- **Tabular Figures:** For all numerical data, the `tnum` (tabular numbers) feature must be enabled. This ensures that columns of numbers align perfectly, allowing users to scan price changes vertically without visual staggering.
- **Monospacing:** **JetBrains Mono** is introduced for labels and command-line inputs to distinguish "system instructions" from "market data."
- **Scale:** The scale is intentionally tight. We prioritize fitting more information on the screen over comfortable whitespace.
- **Hierarchy:** Use weight (Medium vs. Regular) and color (White vs. Gray) rather than size to establish hierarchy.

## Layout & Spacing
This design system utilizes a **Fixed Grid** model based on a 4px base unit. The layout is designed to be "edge-to-edge."

- **The 1px Gutter:** Containers are separated by 1px solid borders (`#2D333D`) rather than margins. This creates a "bento-box" style layout where every panel is locked into a global grid.
- **High Density:** Standard padding inside cells and cards should be kept to `8px` (2 units).
- **Responsiveness:** On desktop, panels are resizable and snappable. On mobile, the grid collapses into a single-column stack, but font sizes remain consistent to preserve data density.
- **Scrollbars:** Custom, ultra-thin scrollbars (4px width) should be used to maximize the data-viewing area.

## Elevation & Depth
In a financial terminal, "depth" is a distraction. This design system is **entirely flat**. 

- **No Shadows:** Shadows are strictly prohibited as they blur the lines between data sets.
- **Layering:** Hierarchy is achieved through color-stepping. If a modal or pop-over is required, it should use a solid `1px` border of a lighter gray (#475569) to separate itself from the background.
- **Active State:** Focus and active states are indicated by high-contrast border color changes (e.g., primary white) or subtle background shifts to a lighter navy, never through elevation.

## Shapes
The shape language is **Sharp**. 

- **Hard Edges:** All buttons, input fields, panels, and dropdowns use a 0px border radius. This maximizes the usable area within every pixel and reinforces the "terminal" aesthetic.
- **Strict Geometry:** Icons should be stroke-based, using 1.5px or 2px weights with square caps and joins to match the container architecture.

## Components
- **Data Tables:** The core component. Rows must have a fixed height (e.g., 24px or 32px). Use zebra-striping (a subtle #1A1D23 vs #121417) only if borders are disabled.
- **Command Input:** A persistent, monospaced text field at the bottom or top of the interface. It should resemble a CLI, allowing users to type tickers (e.g., `/AAPL`) for fast navigation.
- **Candlestick Charts:** Use `#22C55E` for hollow/filled bullish bars and `#EF4444` for bearish bars. Grid lines within charts must align with the global 4px spacing unit.
- **Buttons:** Primary buttons are solid White with Black text. Secondary buttons are outlined in `#94A3B8`.
- **Ticker Tape:** A continuous horizontal scroll at the screen's edge. Use JetBrains Mono for the price strings to ensure no horizontal "jumping" as numbers change.
- **Input Fields:** Minimalist design—just a bottom border or a 1px ghost outline. No rounded corners. Background should be slightly darker than the surface it sits on.