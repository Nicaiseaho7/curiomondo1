# Article body contract — CurioMondo

**Status:** normative, fail-closed  
**Date:** 22 September 2026; prose control updated 12 November 2026  
**Normative language:** English  
**Prose authority:** `PROTOCOL-PUBLIC-PROSE.md` prevails for what a reader may read. This file remains the technical contract for public markup. It does not replace the risk gate, the image protocol, or `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`.

Speed does not outrank quality. If the verified material is not enough for a complete, original article: `DO NOT PUBLISH`.

## Principle

Public text follows `PROTOCOL-PUBLIC-PROSE.md`.

Do not optimise the text so that it “looks like a newspaper”. Optimise it so that a reader leaves knowing the event.

Every article states the fact at once, separates facts from statements and estimates, gives only documented consequences, adds information the headline did not already exhaust, stays adult and plain, and stops when the facts stop.

Internal notes, automated checks, masthead lists, processing timestamps, and desk conversation never enter the public body.

## Markup

- **Title (`h1`):** `PROTOCOLLO-TITOLI-CTR.md` v2.1. Informative, specific, and true. A question is allowed only when the piece is actually a question. No serial “what changes” pattern.
- **Standfirst (`.subtitle`):** one or two facts that are not already the headline.
- **Lead:** the first paragraph of `.art-body`. It stands alone.
- **Body:** `.art-body` with `data-editorial-protocol="4.0"` and `data-article-format` (`flash` | `standard` | `feature`). New articles do not declare `data-length-policy="3000-7000"`. News pages set `data-plain-lead="true"`.
- **`h2` / `h3`:** forbidden in `notizie/*.html` for `flash` and `standard`. Allowed only in a long evergreen feature, and only when the heading is informative. Generic labels (`Il contesto`, `Cosa sappiamo`, `Il punto`) are forbidden everywhere in news.
- **Sources:** only in `.art-sources`, outside `.art-body`, and before the related-story block.
- **Evergreen module:** `.cm-evergreen-reader` under the article, never inside the news body.

## Length

Length follows the verified material. Stretching to a quota is forbidden.

Orientation, not a target to fill:

- a verified flash: about 250–450 words, and legally shorter when the event is small;
- a full news story: about 700–1,200 words;
- a premium piece: about 1,200–2,200 words when the documents support it.

After serial scaffold is removed, a short true story stays short and is marked `flash` if it is under 300 words. It is not refilled.

## Free composition

No fixed sequence of sections. Timelines, tables, key figures, and documents appear only when they clarify this story. In `notizie/*.html` they do not introduce `h2` / `h3`.

Guide furniture is forbidden in news: “In sintesi” boxes, “Attenzione” callouts, question-shaped sections, and coloured badges with an inline background. The category label is plain text.

## Tone

Professional Italian. Direct verbs. No editorial first person (“we verified”, “we do not publish”, “we believe”).

## Sources inside the body

Forbidden inside `.art-body`, in any form:

- a closing line `Fonte:`, `Fonti:`, `Fonte primaria:`, `Fonti consultate:`;
- a masthead list (“ANSA, Reuters, BBC”) used as a credit;
- fact-checking notes, `Conferma:`, `Letture:`, `Europe/Rome`, processing times, “at the time of verification”, “the outlets align”.

Linked sources live only under **Fonti consultate** (`.art-sources`). A source name inside a sentence is allowed only as journalistic attribution: “according to the Mimit bulletin”. Never as its own credit line.

## Public-text prohibitions

Desk notes, operational instructions, “do not confuse”, “anyone searching”, “no article”, material from another story, and repetition of the same fact or figure.

A paragraph that the reader can lose without losing the story is deleted. The serial moulds named in `PROTOCOL-PUBLIC-PROSE.md` §2 are in that class.

## Facts and uncertainty

Do not publish a promise, a proposal, an estimate, or a rumour as a fact. Use “announced”, “according to the statement”, “the text has not been published”, “the figure is an estimate”.

## Predeploy

`tools/predeploy.py` reads `.art-body` and blocks the deploy on forbidden expressions, duplicate sentences where the length policy applies, paragraphs over 60 words, headings inside news, sources placed after the related block, and a featured card that is missing its three figures or its marked keyword. `automation/newsroom/contaminazione.py` removes operative sentences and serial scaffold before that gate. Source names remain mandatory in `.art-sources`.

## Incident imagery

Heroes for road deaths, workplace deaths, construction incidents, and motorway crashes shall not show overturned cars, wreckage, twisted metal, broken glass in close-up, blood, bodies, stretchers, or a staged reconstruction. A quiet context is allowed: cones, an empty stretch of road, barriers, a night motorway with no crashed vehicle. No licence plates, including invented ones. The tone is documentary and respectful. A violation means the image is regenerated before go-live.

## Trend radar

The body of a news story does not mention queries, Google Trends, rising searches, thresholds, or volumes. The radar stays internal. In `.art-sources` every link carries the real name of the source, never “Fonte consultata”.
