# Small Biz Website Builder

A repeatable engine for a local web-design / marketing business: **find small businesses that customers already love (great Google reviews) but that have no website or a badly outdated one, then build them a modern site and package it as a single, click-through pitch artifact.** Works for any city/region â€” swap the location and the category list.

The deliverable is ONE published webpage with two layers:
1. an **operator dashboard** (a clear board of prospect cards), and
2. one **rebuilt concept site per business**, reachable by clicking a card â€” all in a single self-contained HTML file using a JS view-swap (no external navigation).

---

## Tools used
- **SearchPlaces** (Google Places) â€” discovery + authoritative name/address/rating/review-count/Maps-link.
- **WebSearch / WebFetch / Agent subagents** â€” qualify each candidate's real website/social/review state.
- **screenshot_sites.py** (bundled) â€” capture real "current website" screenshots.
- **SaveFile + PublishFilePublicly** â€” turn local images into embeddable pub URLs.
- **GenerateImage** â€” hero imagery for the *rebuilds only* (never on dashboard cards).
- **PublishWebpage** â€” publish/update the single artifact (reuse `artifactId` to update in place).
- **Airtable (optional)** â€” log prospects for future sessions.

---

## Phase 1 â€” Discover (Google Places sweep)
Run `SearchPlaces` across many categories where independents tend to neglect digital. Set a wide `radius` (10â€“16 km) and the target `locationQuery` (e.g. "Kitchener, Ontario, Canada").

High-yield categories: independent restaurants & ethnic eateries, bakeries/patisseries, butchers / European or ethnic delis & grocers, florists, barbers / nail & spa, auto repair / detailing, tailors & alterations / dry cleaners, pet grooming, garden centres, furniture / home, appliance/upholstery repair.

**Key fact:** SearchPlaces returns name, rating, `userRatingsTotal`, address, and a `googleMapsUrl` (use as the reviews link) â€” but **NOT** website or socials. You must verify those separately (Phase 2). Skip chains; keep owner-operated independents with a real review base.

Build a long candidate list (rating, review count, address, Maps cid).

## Phase 2 â€” Qualify (find the real gap)
For ~20â€“30 promising candidates, verify the three signals. Parallelize with subagents (each takes a cluster of ~5; have them return a tight scorecard). For each business confirm:
- **Website:** none found / social-media-only / DIY-outdated / broken / modern. Capture the exact URL.
- **Social:** Facebook + Instagram URLs + rough activity (active/dormant/none).
- **Reviews:** rating + count (a great-reviews filter is **â‰¥ 4.2â˜…**; tighten to 4.5â˜…+ for a premium board). Optionally whether owners reply.
- **Redesign facts:** what they sell, specialties, neighbourhood, years in business, an origin story, a couple of real review quotes.

**Anti-fabrication:** if something isn't found, record "none found" â€” never invent a URL or quote. Treat the Google Places fields (name/address/rating/reviews-link) as authoritative; use research only for website/social/quotes.

Pick the final set for **diversity of industry** (so the rebuilds look different) and a clean gap thesis. **Drop any business whose current site is genuinely modern** â€” badging it "outdated" is dishonest and undercuts the pitch.

## Phase 3 â€” Capture the current state
This is what makes the dashboard land: show the business's REAL current site (usually underwhelming) or a "No website" tile.
- Write the target URLs and run `RunWithCredentials`/Bash: `python3 screenshot_sites.py shots <url1> <url2> ...` (the bundled script polls thum.io until a real PNG is returned).
- **VIEW every PNG (Read tool)** before using it. Discard any that captured a Cloudflare "verify you're human" page, a 404, or a blank.
- For each good shot: `SaveFile(path)` â†’ `PublishFilePublicly(fileId)` â†’ embed the **pub.hyperagent.com** URL.
- **No website?** Use a grey "No website" tile (no screenshot).
- **Screenshot blocked** (interactive Cloudflare gate; no automated renderer can pass)? Don't fake it â€” use an honest "view live â†—" tile with the real URL.

## Phase 4 â€” Build the rebuilds (one concept site per business)
Each rebuild is a `<section class="view" id="v-xxx">` inside the single file, hidden until opened. Make them **genuinely distinct** â€” vary the *layout architecture and a signature device*, not just the palette, or they read as one template re-skinned. Examples that worked: printed diner menu (dotted-leader menu + "OPEN" stamp); dark industrial work-order (hazard stripes, service ledger, work-order ticket); fashion-house atelier (sticky vertical sidebar + IG lookbook); street-food poster (marquee + receipt); editorial florist lookbook (numbered ordering flow); seed-packet garden almanac (live availability board); heritage museum timeline; rounded playful pet brand (phone-mockup booking).
- Scope each view's CSS by its id (`#v-xxx .foo {â€¦}`) so pages can't collide; set background/color/fonts on `#v-xxx` (id specificity beats the base `.view` rule).
- Demonstrate the FIX their gap implies: online ordering, 24/7 booking, a gallery, a menu with prices, e-commerce, a reputation/"we answer every review" promise, etc.
- Hero imagery for rebuilds: `GenerateImage` â†’ `PublishFilePublicly` â†’ embed pub URL. Match the emotional register to the brand; avoid generic blue/purple AI-gradient clichÃ©s.
- Footer on every rebuild: a one-line "independent redesign concept â€” not affiliated with/endorsed by the business."

## Phase 5 â€” Assemble the operator dashboard (the home view)
A first-time viewer must understand it in 3 seconds: *great businesses, weak/missing sites, click to see the rebuild.* Keep cards minimal â€” resist clutter (no gap-meters/opportunity-scores/pitch-hooks on the card).

Dashboard = dark "cockpit" (e.g. near-black `#0d0d0f`, off-white text, one bright CTA accent like lime `#C9F24D`, gold `#ffc24b` for stars). A clear `<h1>`, one-sentence explainer, and a legend (Outdated / No website / Great reviews).

**Each card has exactly four things:**
1. **Current-site preview** â€” a browser-chrome frame (3 dots + the real domain in an address bar) wrapping the real screenshot; OR a grey hatched **"No website"** tile.
2. **A big gold star badge** â€” `â˜… 4.9` + `GREAT REVIEWS` + the review count.
3. **A status tag** â€” red **"No website"** or amber **"Outdated website."**
4. **A CTA button** â€” e.g. "See new website â†’" â€” that calls `openView('v-xxx')`.

**Do NOT put generated/aspirational imagery on dashboard cards** â€” it makes it look like the business already has that polish. The card shows reality; the polish lives behind the button.

## Phase 6 â€” (optional) Interactive lead feature
A working interactive feature inside a rebuild is a huge upsell demo. Example that landed well: a **speed-to-quote** wizard for an auto shop â€” a 5-step state machine (Service â†’ Vehicle â†’ Details â†’ animated Estimate with line items + tax â†’ Book â†’ Confirmation) with pre-filled demo data so it click-throughs cleanly, and a closing line that the whole quote+booking happened "with zero staff involvement." Build it as a small vanilla-JS module scoped to the view.

## Phase 7 â€” (optional) Track prospects in Airtable
Log each prospect (name, category, city, rating, reviews, current-site URL, gap, pitch hook, concept link, stage). Note: a connected Airtable MCP often **lacks schema-write scope (403 on create_field/create_table)** â€” if so, pack everything into the default Name + Notes fields rather than designing new columns. Field IDs (`fldâ€¦`) are usually required, not field names.

---

## Honesty guardrails (non-negotiable)
- Concept pages are clearly labelled **independent mockups**, not affiliated with the business.
- Ratings/links reflect **public data at research time** â€” say so.
- Never fabricate a URL, review quote, or screenshot. "No preview" is honest; a faked screenshot is not.
- Drop (don't mislabel) businesses whose current site is actually good.

## Hard-won technical gotchas
1. **Embedding images in PublishWebpage:** thread-scoped `/api/files/...` URLs do NOT load inside the published sandboxed iframe. Always `PublishFilePublicly` first and embed the `pub.hyperagent.com` URL. (External hotlinks are unreliable too â€” publish to pub.)
2. **Screenshots:** remote Browserbase `BrowserSaveScreenshot` often errors "No screenshot to save" â€” don't rely on it. Use the bundled `screenshot_sites.py` (thum.io via curl; poll past the loading GIF). PageSpeed screenshot API is quota-blocked without a key. Interactive Cloudflare gates defeat all automated renderers.
3. **Single-file app:** keep the dashboard + all rebuild views in one HTML file; toggle with JS. Reuse `artifactId` on `PublishWebpage` to update in place (versions increment).
4. **Distinctness:** scope every view's CSS by `#id` and give each its own layout DNA.
5. **SearchPlaces** gives rating/reviews but never website/social â€” verify separately.
6. **SearchIntegrations for Airtable** spills a huge payload to a file â€” grep it for action names; don't read inline.

---

## Reusable: the view-swap core
```html
<main id="board"><!-- dashboard cards; each button: onclick="openView('v-xxx')" --></main>
<div class="backbar" id="backbar"><button onclick="closeView()">â† Back to board</button>
  <span id="backTitle"></span><a id="backVisit" target="_blank" rel="noopener">Compare: current â†—</a></div>
<div id="views">
  <section class="view" id="v-xxx" data-name="Business" data-visit="https://currentsite"> â€¦ rebuild â€¦ </section>
</div>
<script>
(function(){
  var board=document.getElementById('board'),bar=document.getElementById('backbar'),
      t=document.getElementById('backTitle'),v2=document.getElementById('backVisit'),last=0;
  window.openView=function(id){var v=document.getElementById(id);if(!v)return;last=scrollY;
    board.style.display='none';document.querySelectorAll('.view').forEach(x=>x.classList.remove('show'));
    v.classList.add('show');bar.classList.add('show');t.textContent=(v.dataset.name||'')+' â€” concept site';
    if(v.dataset.visit){v2.href=v.dataset.visit;v2.style.display='';}else{v2.style.display='none';}
    document.body.classList.add('viewing');scrollTo(0,0);};
  window.closeView=function(){document.querySelectorAll('.view').forEach(x=>x.classList.remove('show'));
    bar.classList.remove('show');board.style.display='';document.body.classList.remove('viewing');scrollTo(0,last);};
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('viewing'))closeView();});
})();
</script>
```
CSS essentials: `.view{display:none;min-height:100vh}` Â· `.view.show{display:block;padding-top:54px}` (offset a fixed back-bar) Â· `.backbar{position:fixed;top:0;left:0;right:0;display:none}` Â· `.backbar.show{display:flex}`.

## Operator-dashboard card pattern
```html
<article class="op-card">
  <div class="op-shot">
    <div class="op-chrome"><span class="cd"><i></i><i></i><i></i></span><span class="addr">theirdomain.com</span></div>
    <span class="op-wbadge old">Outdated website</span>            <!-- or .no "No website" -->
    <div class="op-shotimg" style="background-image:url('PUB_SCREENSHOT_URL')"></div>
    <!-- no-website variant: <div class="op-none"><div class="g">ðŸŒ</div><div class="t">No website</div></div> -->
  </div>
  <div class="op-b">
    <div class="op-name">Business Name</div>
    <div class="op-cat">Category Â· City</div>
    <div class="op-rev"><div class="op-revnum">â˜… 4.9</div><div class="op-revtxt">
      <div class="lab">Great reviews</div><div class="cnt">324 Google reviews</div></div></div>
    <button class="op-btn" onclick="openView('v-xxx')">See new website â†’</button>
  </div>
</article>
```
