# Phase: accessibility

## Objective
Pages usable by everyone, measured with an automated audit and confirmed on the real HTML.

## Determine
- Start from the baseline audit (same representative pages, desktop and mobile).
- Checks automated audits miss or accept:
  - image alternative text equal to file names or to attachment titles, empty on informative images (some builders print the attachment title when the library alternative text is empty);
  - links and buttons made only of an icon without an accessible name;
  - zoom disabled in the viewport;
  - contrast below 4.5:1 on normal text (active menu items, light greys, text on coloured backgrounds);
  - main content not declared, maps and iframes without a title, positive tabindex;
  - more than one H1, headings out of order;
  - reduced-motion preference that breaks sliders or transitions;
  - forms without visible labels, autocomplete or messages in the page's language; privacy consent present where personal data is collected.
- Language consistency: interface strings of theme and forms in a language other than the page's own, a copyright year that does not update, texts that name another organization or look copied, brand words.

## Decide
- Fix with the tools of the editor that built each part (principle 9).
- Write alternative text in the media library and wherever the page keeps its own copy (content markup, builder data), so the rendered page shows it, after looking at each image: people by name and role, places by what and where, an image inside a link by its destination, logos by the company name, decorative images empty.
- Translate leftover interface strings; make the copyright year automatic; flag copied texts and content claims for the owner instead of rewriting them; keep brand words unchanged.
- Check a sample of pages by hand after the automated audit; do not repeat identical checks on every page.

## Risks to check
- Reduced-motion handling can remove every transition: redefine the ones the design needs.
- Changing colours for contrast changes the design: compare with the live site and keep the change minimal.
- An audit can pass with meaningless alternative text.

## Exit criteria
Automated audit at the target on the sampled pages; no informative image without a meaningful alternative text in the rendered page; the hand-checked sample passes.

## Report
Audit scores before/after, alternative texts written (count), fixes by type, items flagged for the owner.
