---
name: Terminal High Contrast
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#393939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1b1b1b'
  surface-container: '#1f1f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353535'
  on-surface: '#e2e2e2'
  on-surface-variant: '#b9cac9'
  inverse-surface: '#e2e2e2'
  inverse-on-surface: '#303030'
  outline: '#839493'
  outline-variant: '#3a4a49'
  surface-tint: '#00dddd'
  primary: '#ffffff'
  on-primary: '#003737'
  primary-container: '#00fbfb'
  on-primary-container: '#007070'
  inverse-primary: '#006a6a'
  secondary: '#edffe1'
  on-secondary: '#013a00'
  secondary-container: '#28ff1d'
  on-secondary-container: '#027100'
  tertiary: '#ffffff'
  on-tertiary: '#690100'
  tertiary-container: '#ffdad4'
  on-tertiary-container: '#cc0100'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#00fbfb'
  primary-fixed-dim: '#00dddd'
  on-primary-fixed: '#002020'
  on-primary-fixed-variant: '#004f4f'
  secondary-fixed: '#77ff61'
  secondary-fixed-dim: '#02e600'
  on-secondary-fixed: '#002200'
  on-secondary-fixed-variant: '#015300'
  tertiary-fixed: '#ffdad4'
  tertiary-fixed-dim: '#ffb4a8'
  on-tertiary-fixed: '#410000'
  on-tertiary-fixed-variant: '#930100'
  background: '#131313'
  on-background: '#e2e2e2'
  surface-variant: '#353535'
typography:
  headline-lg:
    fontFamily: JetBrains Mono
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: JetBrains Mono
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
spacing:
  unit: 4px
  gutter: 1px
  margin-sm: 8px
  margin-md: 16px
  margin-lg: 24px
  panel-padding: 12px
---

## Brand & Style

The design system is a rigorous, high-density framework engineered for extreme legibility and technical precision. It draws direct inspiration from terminal environments and high-contrast developer interfaces, prioritizing function over decorative aesthetics. 

The brand personality is authoritative, transparent, and focused. It operates on a "True Black" foundation to maximize OLED efficiency and minimize eye strain in low-light environments. There is zero tolerance for ambiguity; every interactive element is defined by razor-sharp borders and piercing accent colors. The target audience includes developers, security researchers, and power users who require a distraction-free, high-information-density UI that mirrors their mental model of structured code.

## Colors

The palette is strictly utilitarian, utilizing a high-contrast ratio that meets or exceeds WCAG AAA standards. 

- **Primary Cyan (#00FFFF):** Used for focus states, active borders, and critical interactive calls to action.
- **Success Green (#00FF00):** Reserved for positive status indicators, "go" actions, and successful build states.
- **Error Red (#FF0000):** Used for destructive actions, syntax errors, and critical alerts.
- **Universal Background (#000000):** Applied globally across all panels, sidebars, and editors. No gray-scale elevation is permitted.
- **Typography (#FFFFFF):** All primary text is pure white to ensure maximum vibration against the black void.

## Typography

Typography is exclusively monospaced to maintain a predictable vertical and horizontal rhythm, essential for data alignment. The design system uses **JetBrains Mono** for its increased x-height and distinct character shapes, which prevent "l/1/I" confusion.

- **Headlines:** Keep sizing modest; hierarchy is driven by color and weight rather than massive scale.
- **Body Text:** Optimized for long-form reading of technical documentation and logs.
- **Labels:** Always uppercase when used for metadata or terminal-style headers to differentiate from interactive content.

## Layout & Spacing

This design system employs a **Fixed Grid** philosophy where UI regions are partitioned by 1px solid borders. 

- **Density:** The layout is high-density. Vertical rhythm follows a 4px baseline.
- **Grid:** A 12-column system is used for dashboard views, but most application views rely on a "sidebar-editor-panel" triptych.
- **Separation:** Elements are never separated by whitespace alone; 1px borders in White or Cyan must be used to define the boundaries of different functional areas (e.g., between the file explorer and the main editor).

## Elevation & Depth

Depth is conveyed through **Containment** rather than shadows or tonal shifts.

- **No Shadows:** Shadows are strictly prohibited. The UI is 2D and flat.
- **Border-Based Hierarchy:** Primary focus is indicated by a 1px Cyan border. Secondary or inactive areas use a 1px White or dim-gray border.
- **Overlays:** Modals and tooltips do not use backdrop blurs. They are solid #000000 boxes with a 1px White border, visually "floating" only by virtue of their border-defined edge against the background content.

## Shapes

The shape language is defined by a **0px radius**. All corners—including buttons, input fields, modals, and checkboxes—must be sharp 90-degree angles. This reinforces the technical, grid-locked nature of the system and ensures that borders align perfectly without anti-aliasing artifacts on low-resolution displays.

## Components

### Buttons
Buttons are rectangular with 1px borders. 
- **Primary:** #000000 background, #00FFFF border, #00FFFF text. On hover, invert to #00FFFF background and #000000 text.
- **Ghost:** #000000 background, #FFFFFF border, #FFFFFF text.

### Input Fields
Inputs consist of a #000000 background and a 1px White border. Upon focus, the border changes to 1px Cyan. Text entry is always monospaced.

### Lists & Navigation
Active items in a list are indicated by a solid #00FFFF left-border (2px wide) and White text. Inactive items use a dim-white text. There are no background "hover highlights" unless they are high-contrast Cyan.

### Chips & Badges
Small rectangular boxes with 1px White borders. Status-specific chips (Success/Error) use Neon Green or Neon Red borders respectively.

### Checkboxes & Radios
Square-only. A selected checkbox is a Black square with a Cyan border and a Cyan "X" or solid inner square. No rounded radio buttons; use a square with a smaller centered square for selection.

### Cards & Panels
Cards are simple containers defined by a 1px White border. They do not have background fills different from the #000000 workspace.