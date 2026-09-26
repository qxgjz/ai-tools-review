with open('app/globals.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Enhance mobile optimizations
old_mobile = '''/* Mobile optimizations */
@media (max-width: 768px) {
  html { font-size: 15px; }
  
  button, a, [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }
  
  body {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
  
  p, li, span { line-height: 1.7; }
}

@media (max-width: 480px) {
  html { font-size: 14px; }
}'''

new_mobile = '''/* Mobile optimizations - Taste Skill compliant */
@media (max-width: 768px) {
  html { font-size: 15px; -webkit-text-size-adjust: 100%; }
  
  /* Touch targets - minimum 44x44px per WCAG and Taste Skill */
  button, a, [role="button"], input[type="submit"], input[type="button"] {
    min-height: 44px;
    min-width: 44px;
    touch-action: manipulation;
  }
  
  /* Safe area insets for notched devices */
  body {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
    padding-left: env(safe-area-inset-left);
    padding-right: env(safe-area-inset-right);
  }
  
  /* Better readability on mobile */
  p, li, span { line-height: 1.75; }
  
  /* Prevent horizontal overflow */
  .overflow-x-auto { -webkit-overflow-scrolling: touch; }
  
  /* Smooth scrolling but respect reduced motion */
  @media (prefers-reduced-motion: no-preference) {
    html { scroll-behavior: smooth; }
  }
  
  /* Better image rendering on mobile */
  img { 
    image-rendering: -webkit-optimize-contrast;
    max-width: 100%;
    height: auto;
  }
  
  /* Prevent text size adjust on orientation change */
  body { -webkit-text-size-adjust: 100%; }
  
  /* Better focus states for touch */
  button:focus-visible, a:focus-visible {
    outline: 2px solid #10b981;
    outline-offset: 2px;
  }
}

@media (max-width: 480px) {
  html { font-size: 14px; }
  
  /* Extra small screen optimizations */
  h1 { font-size: 1.875rem !important; line-height: 1.2 !important; }
  h2 { font-size: 1.5rem !important; line-height: 1.3 !important; }
  h3 { font-size: 1.25rem !important; }
  
  /* More compact spacing on very small screens */
  .p-8 { padding: 1.25rem !important; }
  .p-6 { padding: 1rem !important; }
  .py-20 { padding-top: 3rem !important; padding-bottom: 3rem !important; }
  .py-16 { padding-top: 2.5rem !important; padding-bottom: 2.5rem !important; }
}

/* Mobile-specific performance optimizations */
@media (max-width: 768px) {
  /* Disable heavy effects on mobile for performance */
  .backdrop-blur-sm, .backdrop-blur-md, .backdrop-blur-lg {
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
  }
  
  /* Reduce shadow intensity on mobile */
  .shadow-2xl { box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); }
  
  /* Better text rendering */
  * {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
}'''

content = content.replace(old_mobile, new_mobile)

with open('app/globals.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Mobile experience optimized:')
print('- Enhanced touch targets (44x44px, touch-action: manipulation)')
print('- Full safe area insets (top/bottom/left/right)')
print('- Better readability (line-height 1.75)')
print('- Smooth scrolling with reduced motion respect')
print('- Better image rendering on mobile')
print('- Focus states for touch accessibility')
print('- Extra small screen optimizations (<480px)')
print('- Mobile performance optimizations (reduced blur/shadow)')
print('- Better text rendering (antialiased)')
