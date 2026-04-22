# UI Design Preview

## 🎨 Visual Design System

### Color Palette
```
Primary Blue:    #7DD3FC  ████████
Accent Lavender: #C7D2FE  ████████
Muted Gray:      #64748B  ████████
Background:      #F8FAFC  ████████
Card White:      #FFFFFF  ████████
Text Dark:       #1E293B  ████████
```

## 📱 Page Layouts

### Home Page
```
┌─────────────────────────────────────────────────────────┐
│  [📄] Scheme Explainer    Home  Compare     [@]         │ ← Navbar (sticky)
├─────────────────────────────────────────────────────────┤
│                                                          │
│              ✨ AI-Powered Insights                      │
│                                                          │
│         Understand Government                            │
│         Schemes Instantly                                │
│                                                          │
│    Get clear, simple explanations of any government     │
│              scheme in seconds                           │
│                                                          │
│  ┌──────────────────────────────────────┐  ┌────────┐  │
│  │ Enter a scheme name...               │  │ Search │  │
│  └──────────────────────────────────────┘  └────────┘  │
│                                                          │
│              Popular Schemes                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  PMAY    │ │ Ayushman │ │ PM-KISAN │ │ Sukanya  │  │
│  │          │ │  Bharat  │ │          │ │ Samriddhi│  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                                                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │ 🔍       │ │ ✨       │ │ 📋       │                │
│  │ Instant  │ │   AI     │ │ Compare  │                │
│  │ Search   │ │Explain   │ │ Schemes  │                │
│  └──────────┘ └──────────┘ └──────────┘                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Results Page
```
┌─────────────────────────────────────────────────────────┐
│  [📄] Scheme Explainer    Home  Compare     [@]         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Pradhan Mantri Awas Yojana                             │
│  AI-generated explanation                                │
│                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐      │
│  │ 📄 Summary      [📋]│  │ 👥 Eligibility  [📋]│      │
│  │                     │  │                     │      │
│  │ This scheme is a    │  │ To be eligible...   │      │
│  │ government initiative│  │ - Indian citizen    │      │
│  │ designed to provide │  │ - Income criteria   │      │
│  │ financial assistance│  │ - Documentation     │      │
│  │ ...                 │  │ ...                 │      │
│  └─────────────────────┘  └─────────────────────┘      │
│                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐      │
│  │ 🎁 Benefits     [📋]│  │ ✅ Process      [📋]│      │
│  │                     │  │                     │      │
│  │ Beneficiaries receive│  │ 1. Visit portal     │      │
│  │ direct financial    │  │ 2. Fill form        │      │
│  │ assistance, subsidies│  │ 3. Upload docs      │      │
│  │ ...                 │  │ 4. Submit           │      │
│  └─────────────────────┘  └─────────────────────┘      │
│                                                          │
│              [ 🔄 Explain Simpler ]                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Compare Page
```
┌─────────────────────────────────────────────────────────┐
│  [📄] Scheme Explainer    Home  Compare     [@]         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│              Compare Schemes                             │
│    Compare two government schemes side by side           │
│                                                          │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ First scheme name    │  │ Second scheme name   │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                          │
│              [ → Compare ]                               │
│                                                          │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │ Scheme 1             │  │ Scheme 2             │    │
│  ├──────────────────────┤  ├──────────────────────┤    │
│  │ Summary              │  │ Summary              │    │
│  │ ...                  │  │ ...                  │    │
│  ├──────────────────────┤  ├──────────────────────┤    │
│  │ Eligibility          │  │ Eligibility          │    │
│  │ ...                  │  │ ...                  │    │
│  ├──────────────────────┤  ├──────────────────────┤    │
│  │ Benefits             │  │ Benefits             │    │
│  │ ...                  │  │ ...                  │    │
│  └──────────────────────┘  └──────────────────────┘    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🎯 UI Components

### Card Component
```
┌─────────────────────────────────────┐
│  [Icon] Title               [Copy]  │ ← Hover shows copy button
│                                     │
│  Content text goes here with        │
│  proper spacing and readable        │
│  typography. Cards have subtle      │
│  shadows and rounded corners.       │
│                                     │
└─────────────────────────────────────┘
  ↑ Hover: shadow increases
```

### Button Variants
```
Primary:    [ Search ]  ← Blue background, white text
Secondary:  [ Retry  ]  ← Border only, hover changes color
```

### Input Field
```
┌─────────────────────────────────────┐
│ Enter a scheme name...              │ ← Placeholder text
└─────────────────────────────────────┘
  ↑ Focus: blue glow ring appears
```

### Loading Skeleton
```
┌─────────────────────────────────────┐
│ ████████████░░░░░░░░░░░░░░░░░░░░░░ │ ← Animated pulse
│ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░ │
│ ████████████████░░░░░░░░░░░░░░░░░░ │
└─────────────────────────────────────┘
```

## 📐 Spacing & Typography

### Spacing Scale
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

### Typography
- Heading 1: 48px (3rem) - Bold
- Heading 2: 32px (2rem) - Semibold
- Heading 3: 24px (1.5rem) - Semibold
- Body: 16px (1rem) - Regular
- Small: 14px (0.875rem) - Regular

### Border Radius
- Input/Button: 8px (rounded-lg)
- Card: 16px (rounded-2xl)
- Avatar: 50% (rounded-full)

## 🎭 Interactions

### Hover Effects
- Cards: Shadow increases, slight scale
- Buttons: Background darkens slightly
- Links: Color changes from muted to dark

### Focus States
- Inputs: Blue ring glow (ring-2 ring-primary/50)
- Buttons: Outline appears
- Links: Underline appears

### Transitions
- All: 200ms ease-in-out
- Smooth, not jarring
- Consistent across components

## 📱 Responsive Breakpoints

```
Mobile:     < 768px   (1 column)
Tablet:     768-1024px (2 columns)
Desktop:    > 1024px   (3-4 columns)
```

### Mobile Adjustments
- Stack cards vertically
- Full-width inputs
- Hamburger menu (if needed)
- Larger touch targets

## ✨ Special Effects

### Glass Morphism (Navbar)
- Semi-transparent background
- Backdrop blur
- Subtle border

### Gradient Accents
- Avatar: Primary to Accent gradient
- Badges: Soft background with primary text

### Shadows
- Card: `shadow-sm` (subtle)
- Card Hover: `shadow-md` (medium)
- Button: `shadow-sm` (subtle)

---

**Design Philosophy**: Clean, minimal, professional
**Inspiration**: Modern SaaS products (Linear, Vercel, Stripe)
**Accessibility**: WCAG 2.1 AA compliant colors
