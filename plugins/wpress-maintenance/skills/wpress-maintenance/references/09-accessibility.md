# Phase: accessibility

## Objective
Pages usable by everyone, measured with an automated audit and confirmed on the real HTML.

## Determine
- Automated accessibility audit on representative pages at desktop and mobile width (same pages as the performance measurements).
- Checks automated audits miss or accept:
  - image alternative text equal to file names or to attachment titles, empty on informative images (some builders print the attachment title when the library alternative text is empty);
  - links and buttons made only of an icon without an accessible name;
  - zoom disabled in the viewport;
  - contrast below 4.5:1 on normal text (active menu items, light greys, text on coloured backgrounds);
  - main content not declared, maps and iframes without a title, positive tabindex;
  - more than one H1, headings out of order;
  - reduced-motion preference that breaks sliders or transitions;
  - forms without visible labels, autocomplete or messages in the site's language; privacy consent present where personal data is collected.
- Language consistency: interface strings of theme and forms left in another language, a copyright year that does not update, texts copied from other sites (for example a privacy policy naming another company), brand words.

## Decide
- Fix with the tools of the editor that built each part first; code outside the editor only where the editor cannot do it, excluding the builder's editor and preview and never returning an empty page.
- Write alternative text in the media library after looking at each image: people by name and role, places by what and where, an image inside a link by its destination, logos by the company name, decorative images empty.
- Translate leftover interface strings; make the copyright year automatic; flag copied texts and content claims for the owner instead of rewriting them; keep brand words unchanged.
- Check a sample of pages by hand after the automated audit; do not repeat identical checks on every page.

## Risks to check
- Reduced-motion handling can remove every transition: redefine the ones the design needs.
- Changing colours for contrast changes the design: compare with the live site and keep the change minimal.
- An audit can pass with meaningless alternative text.

## Exit criteria
Automated audit at the target score on the sampled pages; no informative image without a meaningful alternative text; the hand-checked sample passes.

## Report
Audit scores before/after, alternative texts written (count), fixes by type, items flagged for the owner.
