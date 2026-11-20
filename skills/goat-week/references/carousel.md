# Carousels: design and render

No design app needed: write each slide as HTML and screenshot it in the goat-browser.

## Design rules

- Size **1080 × 1350** (4:5). 5–8 slides.
- Slide 1 = the hook only: big text (90–120 px), 3–8 words, one accent color. It must make
  sense in one second.
- Middle slides: one idea per slide, max ~25 words, body 44–56 px, high contrast.
- Last slide: payoff recap + CTA matching `profile.md` traffic goal ("Хадгалаарай",
  "'ЗААВАР' гэж коммент бич", "Линк bio-д").
- Brand: colors and font from `profile.md`. Fonts from Google Fonts (`<link>` tag) — use one
  that supports Cyrillic (Montserrat, Inter, Roboto, Nunito, Rubik, Manrope).
- Small handle / name on each slide (bottom), slide counter optional.
- Apply `taste.md` rules (e.g. emoji use, dark vs light).

## Render

For each slide:
1. Write the slide as a complete HTML file to `post-NN/slides/slide-01.html` (body exactly
   1080×1350, `margin:0`, no scrollbars).
2. In the goat-browser: `browser_resize` to width 1080, height 1350; navigate to
   `about:blank`; with `browser_evaluate` replace the document with the HTML
   (`() => { document.open(); document.write(HTML); document.close(); }`, the HTML string
   JSON-escaped); `browser_wait_for` ~1 s so the font loads.
   (If the browser allows `file://` URLs, navigating to the file directly also works.)
3. `browser_take_screenshot` (PNG, viewport, not full page) and give a filename like
   `goat-<week>-post-NN-slide-01.png`.
4. Move the saved PNG (the tool result says where) into `post-NN/slides/` with Bash.

Then look at slide 1 and one middle slide yourself (Read the PNG) to check nothing is cut
off or overlapping. Fix and re-render if needed.

TikTok accepts the same images as a photo post; use them as-is.
