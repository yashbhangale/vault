# Quartz Theme Enhancements

## Overview
Your Quartz setup has been enhanced with modern animations, effects, and improved theming to create a more engaging and visually appealing experience.

## 🎨 Color Theme Updates

### Light Mode
- **Background**: Pure white (#ffffff) for cleaner look
- **Primary**: Vibrant blue (#3b82f6) for better contrast
- **Accent**: Purple (#8b5cf6) for visual interest
- **Modern gray scale**: Improved readability

### Dark Mode
- **Background**: Deep slate (#0f172a) for comfortable reading
- **Primary**: Light blue (#60a5fa) that's easy on the eyes
- **Accent**: Soft purple (#a78bfa)
- **Enhanced contrast**: Better text visibility

## ✨ Animations & Effects

### Page Transitions
- **Fade In**: Smooth page load animations
- **Slide In**: Sidebars animate from left/right
- **Scale In**: Modal dialogs appear with scaling effect
- **Progress Bar**: Animated gradient loading indicator with shimmer effect

### Interactive Elements

#### Links
- **Underline Animation**: Gradient underline appears on hover
- **Lift Effect**: Links slightly raise when hovered
- **Internal Links**: Glowing shadow effect on hover
- **Active State**: Subtle scale animation on click

#### Buttons & Controls
- **Ripple Effect**: Click creates expanding circle animation
- **Hover Lift**: Buttons raise with shadow on hover
- **Dark Mode Toggle**: Rotates 180° with scale animation
- **Smooth Transitions**: All state changes are fluid

### Component Animations

#### Search
- **Enhanced Input**: Focus creates glowing border with shadow
- **Result Cards**: Slide in with colored left border on hover
- **Modal Backdrop**: Blurred background with fade-in
- **Search Button**: Lift effect with blue shadow

#### Explorer (File Tree)
- **Active Items**: Gradient background with colored left border
- **Hover Effects**: Items shift right with background highlight
- **Folder Icons**: Scale and glow on hover
- **Smooth Expansion**: Folders open/close with easing

#### Table of Contents
- **Active Section**: Gradient background with animated left border
- **Hover States**: Smooth color and transform transitions
- **Scroll Tracking**: Active item updates with animation

#### Code Blocks
- **Top Border**: Gradient accent line
- **Hover Elevation**: Blocks lift with enhanced shadow
- **Line Highlighting**: Smooth background transitions

#### Callouts
- **Left Accent Bar**: Colored bar expands on hover
- **Shadow Effects**: Elevated appearance on hover
- **Slide Animation**: Content shifts right when hovered
- **Rounded Corners**: Modern 8px border radius

#### Graph View
- **Card Style**: Rounded corners with shadow
- **Hover Elevation**: Graph lifts when hovered
- **Modal Animation**: Scale in with backdrop blur
- **Icon Effects**: Toolbar icons glow on hover

### Visual Effects

#### Images
- **Hover Zoom**: 3% scale increase
- **Shadow Depth**: Enhanced shadow on hover
- **Smooth Transitions**: All transforms are fluid

#### Blockquotes
- **Gradient Background**: Subtle color fade
- **Hover Expansion**: Border grows wider
- **Slide Effect**: Content shifts right
- **Quote Mark**: Large decorative quotation mark

#### Headings
- **Left Border**: Animated gradient accent appears on hover
- **Gradient Text**: Main heading uses gradient fill
- **Anchor Links**: Fade in on hover

#### Tags
- **Pill Design**: Rounded background with border
- **Hover Transform**: Lift and scale animation
- **Gradient Fill**: Background transforms to gradient
- **Shadow Effect**: Colored shadow appears

## 🎯 User Experience Improvements

### Scrollbar
- **Custom Styling**: Gradient-colored thumb
- **Rounded Design**: Modern appearance
- **Hover State**: Darkens on interaction

### Selection
- **Gradient Highlight**: Text selection uses brand colors
- **Text Shadow**: Subtle shadow for depth

### Loading States
- **Shimmer Animation**: Progress indicators have moving highlight
- **Cursor Change**: Body shows wait cursor during loading
- **Smooth Transitions**: All state changes are animated

### Responsive Design
- **Mobile Optimized**: Reduced animations on smaller screens
- **Touch Friendly**: Appropriate hover states
- **Reduced Motion**: Respects user's motion preferences

## 🚀 Performance Considerations

All animations use:
- **CSS Transforms**: Hardware accelerated
- **Cubic Bezier Easing**: Natural motion curves
- **Will-Change Properties**: Optimized rendering
- **Reduced Motion Support**: Accessibility compliance

## 🎨 Customization

### Color Variables
Colors are defined in `/quartz.config.ts`. Modify the `colors` object to change the theme:

```typescript
colors: {
  lightMode: {
    secondary: "#3b82f6", // Primary brand color
    tertiary: "#8b5cf6",   // Accent color
    // ... other colors
  }
}
```

### Animation Speed
Animations use consistent timing values:
- **Fast**: 0.2s (micro-interactions)
- **Standard**: 0.3s (most transitions)
- **Slow**: 0.5s+ (major state changes)

Adjust these in `/quartz/styles/custom.scss` by modifying the `transition` properties.

### Disable Animations
To disable animations for accessibility:
- Animations respect `prefers-reduced-motion`
- Users can enable reduced motion in their OS settings

## 📁 Modified Files

### Configuration
- `/quartz.config.ts` - Updated color theme

### Styles
- `/quartz/styles/custom.scss` - Main animation definitions
- `/quartz/styles/base.scss` - Global enhancements
- `/quartz/styles/callouts.scss` - Callout styling
- `/quartz/components/styles/search.scss` - Search animations
- `/quartz/components/styles/explorer.scss` - File tree effects
- `/quartz/components/styles/darkmode.scss` - Toggle animations
- `/quartz/components/styles/toc.scss` - TOC effects
- `/quartz/components/styles/footer.scss` - Footer styling
- `/quartz/components/styles/graph.scss` - Graph view enhancements

## 🛠️ Building & Testing

To see the changes:

```bash
npx quartz build --serve
```

Then visit `http://localhost:8080` to see your enhanced Quartz site!

## 💡 Tips

1. **Test Dark Mode**: Use the dark mode toggle to see both themes
2. **Try Search**: Press `/` or click search to see modal animations
3. **Explore Files**: Click folders to see smooth expansion animations
4. **Hover Effects**: Move your mouse over links, cards, and images
5. **Page Navigation**: Click internal links to see smooth transitions

## 🎉 Enjoy Your Enhanced Quartz!

Your notes now have a modern, polished appearance with smooth animations that enhance the reading experience without being distracting.

