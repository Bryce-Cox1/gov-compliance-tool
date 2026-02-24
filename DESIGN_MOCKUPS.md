# Gov Compliance Tool - Design Mockups & Visual Guide

## Overview

This document describes the visual design of the new agentic chat interface for the Government Compliance Tool. The design prioritizes **trust, elegance, and accessibility** while modernizing the UX with conversational AI patterns.

---

## Visual Design System

### Color Palette

#### Primary Colors
```
Navy Blue (#1e3a5f)
├─ Used for: Headers, primary buttons, authority elements
├─ Psychology: Trust, professionalism, government authority
└─ Contrast ratio: 10.2:1 with white (AAA)

Soft Blue (#4a6fa5)
├─ Used for: Interactive elements, links, accents
├─ Psychology: Approachable, reliable, calming
└─ Contrast ratio: 5.8:1 with white (AA)

Sage Green (#8da377)
├─ Used for: Success states, passed checks, compliance badges
├─ Psychology: Natural, approved, accomplished
└─ Contrast ratio: 4.7:1 with white (AA)

Warm Gold (#e8b86d)
├─ Used for: Warnings, improvement opportunities
├─ Psychology: Encouraging, optimistic, non-threatening
└─ Contrast ratio: 2.9:1 with black (readable on white)
```

#### Why These Colors Work
1. **Navy blue** conveys government authority without being cold
2. **Low saturation** creates sophisticated, professional appearance
3. **Warm accents** (gold, sage) add approachability
4. **Soft edges** reduce cognitive stress
5. **All colors pass WCAG AA** contrast requirements

---

## Screen Mockups

### Mockup 1: Initial State (Welcome)

```
┌────────────────────────────────────────────────────────────┐
│  ◉  Gov Compliance Assistant          Target Grade: [7 ▾] │ ← Navy header
├────────────────────────────────────────────────────────────┤
│                                                            │
│     ◉  Hi! I'm your Government Compliance Assistant.      │ ← AI bubble (left)
│        I'll help you check your content against the       │   White background
│        Australian Government Style Manual standards...     │   Soft shadow
│                                                            │
│        ✓ Score your text for reading level               │
│        ✓ Rewrite it to meet accessibility standards      │
│        ✓ Explain what needs improvement                  │
│                                                            │
│        Just paste your content below to get started!      │
│        10:23 AM                                           │
│                                                            │
│                                                            │
│              ┌────────────────────┐                        │
│              │    📄              │                        │
│              │ Paste your         │ ← Empty state
│              │ government content │   (centered)
│              │                    │
│              └────────────────────┘
│                                                            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [        Paste your content here...              ] [Send]│ ← Input area (bottom)
│  Press Enter to send, Shift+Enter for new line            │
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Clean, minimal header with logo and grade selector
- Welcoming AI message establishes conversational tone
- Empty state guidance (hidden after first message)
- Sticky input at bottom (always accessible)

---

### Mockup 2: User Submits Text

```
┌────────────────────────────────────────────────────────────┐
│  ◉  Gov Compliance Assistant          Target Grade: [7 ▾] │
├────────────────────────────────────────────────────────────┤
│                                                            │
│     ◉  Hi! I'm your Government Compliance Assistant...    │
│        [welcome message]                                  │
│        10:23 AM                                           │
│                                                            │
│                                                            │
│                    The application should be submitted   👤│ ← User bubble (right)
│                    by the applicant to the relevant...  👤│   Navy gradient
│                    10:24 AM                              👤│   White text
│                                                            │
│     ◉  ⋯ Analyzing your text against AGSM standards...    │ ← Thinking state
│        10:24 AM                                           │   Animated dots
│                                                            │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [        Paste your content here...              ] [Send]│
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- User message right-aligned with distinct styling
- Avatar icons differentiate user vs AI
- Thinking state shows system is working
- Timestamps add human context

---

### Mockup 3: Results Display (Scores)

```
┌────────────────────────────────────────────────────────────┐
│  ◉  Gov Compliance Assistant          Target Grade: [7 ▾] │
├────────────────────────────────────────────────────────────┤
│  [Previous messages scrolled up...]                        │
│                                                            │
│     ◉  I've analyzed your text. Here's what I found:      │
│                                                            │
│        ┌────────────────────────────────────────────────┐ │
│        │ Original Text                    58% compliant │ │ ← Score card
│        ├────────────────────────────────────────────────┤ │   Light gray bg
│        │ ⚠  Reading Grade     9.2  Target: ≤8.0       │ │
│        │ ⚠  Avg Sentence      24 words  Target: ≤20   │ │
│        │ ✓  Longest Sentence  32 words  Target: ≤35   │ │
│        │ ⚠  Passive Voice     45%  Target: ≤20%       │ │
│        └────────────────────────────────────────────────┘ │
│                                                            │
│        I've also created an improved version that meets   │
│        the standards:                                     │
│                                                            │
│        ┌────────────────────────────────────────────────┐ │
│        │ Improved Text                    92% compliant │ │ ← Success card
│        ├────────────────────────────────────────────────┤ │   Soft green tint
│        │ ✓  Reading Grade     7.4  Target: ≤8.0       │ │
│        │ ✓  Avg Sentence      16 words  Target: ≤20   │ │
│        │ ✓  Longest Sentence  24 words  Target: ≤35   │ │
│        │ ✓  Passive Voice     8%   Target: ≤20%       │ │
│        └────────────────────────────────────────────────┘ │
│        10:24 AM                                           │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [        Ask a follow-up question...             ] [Send]│
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Inline score cards within AI message
- Color-coded status (✓ green, ⚠ amber)
- Before/after comparison immediate
- Maintains conversation flow

---

### Mockup 4: Comparison View (Full Detail)

```
│     ◉  [Continued from above...]                          │
│                                                            │
│        ┌────────────────────────────────────────────────┐ │
│        │ Improved Version              87% confidence  │ │ ← Comparison card
│        ├────────────────────────────────────────────────┤ │
│        │ Before                  │ After               │ │
│        ├─────────────────────────┼─────────────────────┤ │
│        │ The application should  │ Submit your         │ │
│        │ be submitted by the     │ application to the  │ │
│        │ applicant to the        │ relevant department.│ │
│        │ relevant department. It │ Complete all fields │ │
│        │ is important that all   │ accurately before   │ │ ← Side-by-side
│        │ fields are completed... │ submitting...       │ │   text comparison
│        │                         │                     │ │
│        │                         │ [📋 Copy improved]  │ │
│        └─────────────────────────┴─────────────────────┘ │
│                                                            │
│        ℹ️  Improved in 2 iterations. The rewritten text   │
│           meets grade 7 standards while preserving your   │
│           original meaning.                               │
│        10:24 AM                                           │
│                                                            │
├────────────────────────────────────────────────────────────┤
│  [        Ask a follow-up question...             ] [Send]│
└────────────────────────────────────────────────────────────┘
```

**Key Features:**
- Side-by-side before/after view
- Confidence badge (color-coded)
- One-click copy button for improved text
- Explanatory notes in info box

---

### Mockup 5: Mobile View (Responsive)

```
┌──────────────────────────┐
│ ◉ Gov Compliance         │ ← Compact header
│   Target Grade: [7 ▾]    │
├──────────────────────────┤
│                          │
│  ◉  Hi! I'm your Gov     │
│     Compliance           │
│     Assistant...         │
│     10:23 AM             │
│                          │
│          [User text]   👤│ ← Full width
│          10:24 AM      👤│   bubbles
│                          │
│  ◉  Here's what I found: │
│                          │
│  ┌──────────────────────┐│
│  │ Reading Grade        ││ ← Stacked
│  │ 9.2  Target: ≤8.0    ││   metrics
│  │ ⚠                    ││
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ Avg Sentence         ││
│  │ 24 words  Target: ≤20││
│  │ ⚠                    ││
│  └──────────────────────┘│
│                          │
│  ┌──────────────────────┐│ ← Full-width
│  │ Before               ││   comparison
│  │ [text...]            ││   (stacked)
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ After                ││
│  │ [text...]            ││
│  │ [Copy]               ││
│  └──────────────────────┘│
│                          │
├──────────────────────────┤
│ [    Type message...   ] │ ← Touch-friendly
│ [Clear]           [Send] │   input
└──────────────────────────┘
```

**Key Features:**
- Single-column layout (no side-by-side)
- Larger touch targets (44x44px minimum)
- Stacked metrics for readability
- Simplified header (no logo text)
- Bottom input always visible

---

## Component Library

### 1. Message Bubbles

#### AI Message Bubble
```css
Background: White
Border: 1px solid #e4e9f2
Border-radius: 18px (except bottom-left: 4px)
Padding: 16px 20px
Shadow: Soft 0-2px-8px rgba(0,0,0,0.05)
Text: #1a2332, 16px, line-height 1.75
Max-width: 80% of container
```

**Visual Example:**
```
    ◉
    ┌─────────────────────────────────────┐
    │ I've analyzed your text. Here's    │
    │ what I found:                      │
    │                                    │
    │ • Reading grade: 9.2 (too high)   │
    │ • Passive voice: 45% (too much)   │
    └─────────────────────────────────────
      10:24 AM
```

#### User Message Bubble
```css
Background: Linear gradient #4a6fa5 → #1e3a5f
Color: White
Border-radius: 18px (except bottom-right: 4px)
Padding: 12px 16px
Shadow: Medium 0-2px-8px rgba(30,58,95,0.15)
Max-width: 70% of container
Align: Right
```

**Visual Example:**
```
                                            ┌──────────────────────┐
                                            │ Analyze this text    │
                                            │ for compliance       │
                                            └─────────────────────    👤
                                              10:23 AM
```

---

### 2. Insight Cards

#### Score Card (Within Message)
```css
Background: #f5f7fa (light gray)
Border: 1px solid #e4e9f2
Border-radius: 12px
Padding: 16px
Margin: 12px 0 (inside message bubble)
Shadow: 0-1px-3px rgba(0,0,0,0.05)
```

**Structure:**
```
┌─────────────────────────────────────────┐
│ Original Text              58% compliant│ ← Header (flex)
├─────────────────────────────────────────┤
│ ⚠  Reading Grade    9.2   Target: ≤8.0 │
│ ⚠  Avg Sentence     24    Target: ≤20  │ ← Metrics grid
│ ✓  Longest Sentence 32    Target: ≤35  │   (2-4 columns)
│ ⚠  Passive Voice    45%   Target: ≤20% │
└─────────────────────────────────────────┘
```

**Color Rules:**
- Failed check (⚠): Border-left #f4a261 (warm amber)
- Passed check (✓): Border-left #52b788 (sage green)
- Badge background: Match border color at 15% opacity

---

### 3. Metric Item

**Anatomy:**
```
┌───────────────────────────────┐
│ ⚠  Reading Grade              │ ← Icon (32px circle)
│    9.2                         │ ← Value (18px, bold)
│    Target: ≤8.0                │ ← Target (12px, gray)
└───────────────────────────────┘
```

**Pass State:**
```css
Border-left: 3px solid #52b788
Icon background: #d8f3dc
Icon color: #52b788
Hover: Lift 2px, shadow increase
```

**Fail State:**
```css
Border-left: 3px solid #e76f51
Icon background: #ffe5e0
Icon color: #e76f51
```

---

### 4. Comparison Card

**Layout:**
```
┌────────────────────────────────────────────┐
│ Improved Version            87% confidence │ ← Header
├────────────────────────────────────────────┤
│  Before               │  After             │
│ ┌─────────────────────┼───────────────────┐│
│ │ The application     │ Submit your       ││
│ │ should be submitted │ application to... ││
│ │ by the applicant... │                   ││
│ │                     │ [📋 Copy]         ││
│ └─────────────────────┴───────────────────┘│
└────────────────────────────────────────────┘
```

**Styling:**
- After column: Light green tint (#d8f3dc background)
- Text areas: Rounded 8px, max-height 300px, scrollable
- Copy button: Appears on hover, bottom of After panel

---

### 5. Action Buttons

#### Primary Button (Send)
```css
Background: Linear gradient #4a6fa5 → #1e3a5f
Color: White
Padding: 12px 24px
Border-radius: 14px
Shadow: 0-4px-8px rgba(74,111,165,0.2)
Font: 16px, weight 600

Hover:
  Transform: translateY(-2px)
  Shadow: 0-8px-16px rgba(74,111,165,0.3)

Active:
  Transform: translateY(0)
```

#### Secondary Button (Copy, Clear)
```css
Background: Transparent
Border: 1px solid #d1d9e6
Color: #4a6fa5
Padding: 8px 16px
Border-radius: 10px

Hover:
  Background: #4a6fa5
  Color: White
  Border-color: #4a6fa5
```

---

## Typography Specifications

### Font Family
```css
font-family: 'Inter', 'SF Pro Display', -apple-system, 
             BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Helvetica Neue', Arial, sans-serif;
```

### Type Scale
```
Hero:     32px / 40px (2rem / 2.5rem)
H1:       24px / 30px (1.5rem)
H2:       20px / 28px (1.25rem)
H3:       18px / 26px (1.125rem)
Body:     16px / 28px (1rem / 1.75 line-height)
Small:    14px / 22px (0.875rem)
Tiny:     12px / 18px (0.75rem)
```

### Font Weights
```
Regular: 400 (body text)
Medium:  500 (labels, emphasis)
Semibold: 600 (headings, buttons)
Bold:    700 (metric values, scores)
```

### Letter Spacing
```
Headings: -0.02em (tighter, more compact)
Body:     0 (normal)
Labels:   0.01em (slightly looser for legibility)
```

---

## Animation & Motion

### Principles
1. **Purposeful:** Every animation serves a function
2. **Swift:** 150-300ms for most transitions
3. **Natural:** Ease curves, not linear
4. **Respectful:** Honor prefers-reduced-motion

### Key Animations

#### Message Slide In
```css
@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
Duration: 300ms
Easing: ease-out
```

#### Thinking Dots
```css
content: '...'
0-20%:  '.'
40%:    '..'
60-100%: '...'
Duration: 1.4s
Loop: infinite
```

#### Button Hover
```css
Transform: translateY(-2px)
Shadow: Increase from md → lg
Duration: 150ms
Easing: ease
```

#### Score Reveal (Stagger)
```css
Each metric item:
  Fade in: 0 → 1 opacity
  Slide up: 10px → 0
  Delay: Index × 100ms
Total duration: 250ms per item
```

---

## Accessibility Features

### WCAG 2.1 AA Compliance

#### Color Contrast
```
Text on white:
  Navy #1e3a5f:     10.2:1 (AAA)
  Blue #4a6fa5:     5.8:1 (AA)
  Gray #6b7c93:     4.9:1 (AA)

UI Components:
  All borders:      ≥3:1 against background
  All focus rings:  ≥3:1 against background
```

#### Keyboard Navigation
- All interactive elements reachable via Tab
- Focus visible (2px blue outline, 2px offset)
- Enter/Space activate buttons
- Enter sends message, Shift+Enter = new line

#### Screen Reader Support
```html
<main role="main" aria-label="Compliance analysis chat">
  <div role="log" aria-live="polite" aria-atomic="false">
    <!-- Messages announced as they appear -->
  </div>
</main>

<textarea aria-label="Government content to analyze">
<button aria-label="Analyze text for compliance">
<button aria-label="Copy improved text" title="Copy improved text">
```

#### Motion Preferences
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Responsive Breakpoints

### Desktop (1024px+)
- Two-column comparison view
- Max-width chat: 900px
- Side-by-side metrics (2-4 columns)

### Tablet (768-1023px)
- Reduced padding
- 2-column metrics
- Slightly narrower message bubbles

### Mobile (320-767px)
- Single column everything
- Stacked metrics (1 column)
- Full-width message bubbles
- Larger touch targets (44x44px min)
- Simplified header

---

## Dark Mode (Future Enhancement)

### Dark Color Palette
```css
--dark-bg: #0f1419
--dark-surface: #1a2332
--dark-primary: #7fb3d5 (lighter blue for contrast)
--dark-text: #e4e9f2
--dark-border: #2d3748

Strategy:
- Reduce contrast (80% opacity on whites)
- Increase primary color luminance
- Maintain semantic colors (success, warning, error)
```

---

## Design Tokens (CSS Variables)

All design values are stored as CSS custom properties for easy theming:

```css
:root {
  /* Colors */
  --primary-navy: #1e3a5f;
  --primary-blue: #4a6fa5;
  --success-green: #52b788;
  --warning-amber: #f4a261;
  --error-coral: #e76f51;
  
  /* Spacing (0.25rem increments) */
  --space-xs: 0.25rem;  /* 4px */
  --space-sm: 0.5rem;   /* 8px */
  --space-md: 1rem;     /* 16px */
  --space-lg: 1.5rem;   /* 24px */
  --space-xl: 2rem;     /* 32px */
  
  /* Typography */
  --text-sm: 0.875rem;  /* 14px */
  --text-base: 1rem;    /* 16px */
  --text-lg: 1.125rem;  /* 18px */
  --text-xl: 1.25rem;   /* 20px */
  
  /* Shadows */
  --shadow-sm: 0 2px 4px rgba(26, 35, 50, 0.06);
  --shadow-md: 0 4px 8px rgba(26, 35, 50, 0.08);
  --shadow-lg: 0 8px 16px rgba(26, 35, 50, 0.1);
  
  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 18px;
  --radius-full: 9999px;
}
```

---

## Implementation Checklist

- [x] HTML structure (semantic, accessible)
- [x] CSS styling (colors, typography, layout)
- [x] JavaScript (message handling, API integration)
- [x] Responsive design (mobile-first)
- [x] Accessibility (WCAG AA)
- [x] Animations (tasteful, purposeful)
- [ ] Loading states (skeleton screens)
- [ ] Error handling (user-friendly messages)
- [ ] Chat history (localStorage persistence)
- [ ] Export functionality (PDF, Word)
- [ ] Dark mode theme
- [ ] i18n support (multilingual)

---

## Comparison: Before vs After

### Before (Traditional Form)
❌ Form-based interaction (fill → submit → wait)  
❌ All results shown at once (overwhelming)  
❌ Static display (no interactivity)  
❌ Dated visual style (harsh colors, hard edges)  
❌ No guidance or suggestions  
❌ One-shot analysis (no iteration)  

### After (Agentic Chat)
✅ Conversational flow (natural, engaging)  
✅ Progressive disclosure (easier to digest)  
✅ Interactive components (copy, expand, regenerate)  
✅ Modern, soft aesthetics (trust-promoting colors)  
✅ Contextual help (AI explains issues)  
✅ Iterative refinement (back-and-forth)  

---

## Conclusion

This design transforms the Gov Compliance Tool from a utilitarian form into an engaging, trustworthy AI assistant. Key achievements:

1. **Trust-promoting color palette** (navy, sage, soft neutrals)
2. **Elegant, soft aesthetics** (rounded corners, gentle shadows)
3. **Conversational UX** (chat bubbles, streaming, natural flow)
4. **Accessibility-first** (WCAG AA, keyboard nav, screen readers)
5. **Mobile-optimized** (responsive, touch-friendly)
6. **Modern typography** (Inter, clear hierarchy)

The design feels **professional** without being cold, **modern** without being trendy, and **accessible** without sacrificing aesthetics. Perfect for government content professionals who need reliable, efficient compliance checking.
