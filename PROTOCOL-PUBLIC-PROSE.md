# CurioMondo — Public Prose Protocol

**Identifier:** `PROTOCOL-PUBLIC-PROSE`  
**Version:** 1.0  
**Effective:** 12 November 2026, 06:50 Europe/Rome  
**Status:** normative, fail-closed, prevailing  
**Scope:** every public string a reader can see inside a news page: `h1`, `.subtitle`, `.art-body`, meta description, Open Graph description, JSON-LD `headline` / `description`, card excerpt, and RSS `description` when it is derived from the article.  
**Normative language:** technical English. From this date, CurioMondo editorial protocols are authored and controlling in English. An Italian sentence in an older protocol file is a historical annex. Where it conflicts with this document, this document wins.

This protocol does not govern image pixels, the ebook product, or the navigation contract. It governs the sentence.

## 1. Definitions

- **Public copy.** Any string rendered to a reader as journalism. Not a stylesheet, not a commit message, not an agent instruction.
- **Fact.** A proposition that a cited source asserts, or a number, name, date, place, or decision that the source states.
- **Scaffold.** A sentence that describes the article, the desk, the workflow, the reader’s supposed need, or the epistemic status of “news” in general, instead of the event.
- **Metadata leak.** A production artifact that escaped its container: a wire header, a hashtag, a CMS note, a dateline stamp, `RIPRODUZIONE RISERVATA`, `Redazione Ansa`, `News (ANSA)`, a slug pasted as prose, a generation timestamp, or the sentence “this update was published on…”.
- **Serial mould.** A paragraph whose predicate stays the same across unrelated stories and whose only variable is the title, lower-cased and dropped into the sentence.
- **Controlling text.** The sentences that remain after every scaffold sentence is deleted. If that residue is not a news story, the page is not publishable.

## 2. The newsroom test

Public copy shall read as if a human desk wrote it for a general reader who will see the story once.

A paragraph fails the test if a competent editor, shown the paragraph with the headline covered, cannot tell which event it refers to. Template sentences fail that test by construction. The following, and any close paraphrase, are forbidden inside public copy:

- “Il punto centrale della notizia, [title], va quindi separato dalle ipotesi non confermate.”
- “I dati disponibili descrivono un fatto avvenuto o una decisione annunciata, mentre conseguenze ulteriori richiedono atti, numeri o comunicazioni successive.”
- “Per il pubblico italiano la rilevanza dipende da collegamenti concreti con mercati, viaggi, sicurezza, sport, tecnologia o politiche europee.”
- “Il valore è soprattutto informativo e non giustifica allarmi o conclusioni anticipate.”
- “Il quadro potrà cambiare dopo [clause copied from a previous paragraph].”
- “Fino ad allora restano validi i fatti attribuiti alle autorità…”
- “La verifica successiva dovrà confrontare gli annunci con documenti operativi…”
- “Nel caso di [lower-cased title], una dichiarazione iniziale indica la direzione dell’evento…”
- “L’aggiornamento è stato pubblicato il [date] e definisce uno dei passaggi rilevanti della giornata.”

The prohibition is semantic, not orthographic. Translating the mould into English, or swapping one noun, does not make it legal.

## 3. Metadata isolation

Production metadata has a closed set of legal containers. It shall not appear in public copy.

| Artifact | Legal container | Forbidden in |
|---|---|---|
| Canonical URL, slug, `datePublished`, `dateModified` | `<head>`, JSON-LD | body, subtitle, excerpt |
| Wire slug, `#` topic tag, agency dateline, `© ANSA`, `RIPRODUZIONE RISERVATA` | nowhere on the public site | everywhere |
| Source name and URL | `.art-sources` only, plus an in-sentence attribution when the sentence would be false without it | a trailing `Fonte:` line, a list of mastheads, a parenthetical `(ANSA)` used as a stamp |
| Method, AI disclosure, “how this page is updated” | `.art-sources`, institutional pages, image caption | `.art-body` |
| Agent instructions, CMS commands, placeholders, `TODO` | nowhere | everywhere |

An in-sentence attribution is journalism: “according to the Mimit bulletin”. A separated credit line is metadata.

Captions that state the image is an editorial illustration are legal. They are not a licence to discuss the prompt.

## 4. Prose requirements

Public copy shall satisfy all of the following.

1. **One event per article.** The lead states the event, the actor, and the time or date. It does not restate the production of the page.
2. **Inverted pyramid without a template.** Later paragraphs add a confirmed detail, a documented consequence, or a necessary limit. They do not add a theory of news.
3. **Attribution.** A claim that is not the desk’s direct observation carries its source in the sentence. Uncertainty stays in the verb: “announced”, “estimates”, “the text has not been published”.
4. **Proper names.** Names of institutions, people, and places keep their conventional capitalisation. A title fragment inserted in lower case (“fifa ammette…”) is a generation defect and is rejected.
5. **Syntax.** One grammatical sentence ends with one terminal mark. `..` is a defect. A fused clause — a finite verb starting where the previous clause never closed — is a defect. The photographed pattern “voto dell'organo competente determineranno” is a fused clause and is rejected.
6. **Paragraph budget.** A news paragraph carries one idea, at most 60 words. A news page (`flash` or `standard`) has no `h2` or `h3` inside `.art-body`.
7. **No desk voice.** Forbidden: first-person plural of the newsroom (“we verified”, “we will update”), self-praise of the method, and promises to follow the story inside the body. The only update signal is the red card badge.
8. **No padding.** If the verified material ends, the article ends. Serial closers are not a substitute for missing facts. A story that cannot stand without scaffold is not published.
9. **Language.** News copy is Italian, professional, concrete, and free of calques from the prompt. Protocol copy — this file and the other editorial protocols — is English.

## 5. Detection

Before a push, every `.art-body` in the batch is read in full. Automated gates are necessary and not sufficient.

`tools/predeploy.py` shall strip and then reject residual hits of the method-note inventory and of the serial moulds in §2. `automation/newsroom/contaminazione.py` shall treat the same moulds as operative sentences: the sentence is deleted, the fact in any other sentence is kept, and the article is not blocked for the presence of a sentence that has been removed.

A human or agent pass still looks for what a list will miss:

- a lower-cased headline used as a noun phrase;
- a paragraph that repeats the previous paragraph with a broken join;
- a sentence that would fit any other article in the batch;
- a double stop, a missing stop, or a verb that does not agree because two sentences were concatenated.

If a paragraph mixes one fact with scaffold, the fact stays and the scaffold sentence is deleted. Nothing is invented to refill the word count. `datePublished` does not move. Title, canonical, and JSON-LD are not rewritten in order to hide a body defect.

## 6. Word count after deletion

Deleting scaffold may shorten a story. Do not replace the deleted sentence with filler.

- Count `body_words` as defined in `PROTOCOLLO-REDAZIONE-CORPO.md` § Length.
- `body_words < 200`: `DO NOT PUBLISH`. The old rule that a story under 300 words becomes a short `flash` is withdrawn.
- `body_words >= 200`: keep every remaining verified fact. There is no ceiling. Add further verified facts when they exist. Do not stop at 200 in order to look brief.
- If, after the scaffold is gone, the residue does not state the event, or cannot reach 200 words without a new invented or generic sentence: withdraw the page.

## 7. Report

After a batch, the desk reports one of these, and only if it is true:

- “Scaffold removed from N articles”, with the count.
- “No scaffold in the batch”, only after the bodies were read.

It is forbidden to report the second sentence as reassurance.

## 8. Precedence

For public copy, this protocol prevails over `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`, `PROTOCOLLO-REDAZIONE-CORPO.md`, `PROTOCOLLO-ARTICOLI-PREMIUM.md` §1-quater, and `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`. Those files remain in force for markup, risk, images, titles, and product rules that this document does not restate. Their controlling language for any new amendment is English.
