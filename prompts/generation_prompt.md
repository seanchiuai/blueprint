# HTML Redesign Generation Prompt

You are an expert frontend developer tasked with creating a modern, beautiful HTML page based on a website screenshot, its original HTML source, and design analysis.

## Design Analysis
{ANALYSIS_JSON}

{STYLE_PREFERENCES}

## Original HTML Source
Use this to extract the actual text content, links, navigation items, and semantic structure. Preserve all real content from the original.

```html
{ORIGINAL_HTML}
```

## Your Task

Create a complete, standalone HTML page that:

1. **Keeps the same content** as the original website
2. **Dramatically improves** the visual design:
   - Modern, clean aesthetic
   - Better visual hierarchy
   - Improved spacing and breathing room
   - Contemporary color palette
   - Smooth hover effects and transitions

3. **Technical Requirements:**
   - Complete HTML5 document with DOCTYPE
   - Include Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
   - Fully responsive (mobile-first design)
   - Dark mode support with toggle button
   - Semantic HTML elements
   - ARIA labels for accessibility
   - Working dark mode toggle with JavaScript

4. **Design Principles:**
   - Generous whitespace
   - Clear typography hierarchy
   - Subtle shadows and depth
   - Rounded corners where appropriate
   - Gradient accents (subtle)
   - Modern button and card styles
   - Smooth transitions

## Critical Output Format

You MUST return ONLY the HTML code in a markdown code block. NO explanations, NO analysis, NO recommendations.

Start your response with EXACTLY this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redesigned Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <!-- Your redesigned page here -->
</body>
</html>
```

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: You, gemini, are capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.



Do NOT include ANYTHING before or after the code block.
