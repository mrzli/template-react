# Controls

Additional conventions and requirements for the `src/controls/` components.

## Appearance

### Border radius

All controls must use **square corners** (border-radius: 0).

In `src/index.css`, set the shadcn `--radius` CSS variable to `0` in both the `:root` and `.dark` blocks:

```css
--radius: 0rem;
```

### Sizing

All controls must use a **compact** size by default — reduced padding, tight spacing, and smaller touch targets compared to the shadcn defaults. The goal is dense, information-rich UIs rather than spacious, touch-optimised ones.
