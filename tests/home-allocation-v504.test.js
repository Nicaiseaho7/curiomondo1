'use strict';
const assert = require('node:assert/strict');
const A = require('../assets/js/home-allocation-v504.js');
const fs = require('node:fs');
const now = new Date('2026-09-22T10:00:00+02:00');
const item = (id, date, section = 'Italia / Sport', extra = {}) => ({ id, url: `/notizie/${id}.html`, title: id, dateISO: date, firstPublishedAt: date, section, ...extra });

assert.equal(A.isPromotable(item('x', '2026-09-22T07:01:00+02:00'), now), true, '2h59 deve essere idoneo');
assert.equal(A.isPromotable(item('x', '2026-09-22T07:00:00+02:00'), now), false, '3h esatte devono scadere');
assert.equal(A.isPromotable(item('x', '2026-09-21T23:30:00+02:00'), new Date('2026-09-22T00:00:00+02:00')), false, 'mezzanotte italiana deve scadere');
const lateAllocation = A.allocate([item('late', '2026-09-22T23:30:00+02:00', 'Politica', { homepagePriority: 90 })], { now: new Date('2026-09-22T23:45:00+02:00') });
assert.equal(A.nextExpiry(lateAllocation).toISOString(), '2026-09-22T22:00:00.000Z', 'il timer deve scattare alla mezzanotte italiana');
assert.equal(A.isPromotable({ ...item('x', '2026-09-22T07:01:00+02:00'), modifiedAt: '2026-09-22T09:59:00+02:00' }, now), true, 'modifiedAt non deve cambiare la finestra');
assert.equal(A.isPromotable(item('future', '2026-09-22T10:01:00+02:00'), now), false, 'il futuro deve essere escluso');

const items = [
  item('lead', '2026-09-22T09:30:00+02:00', 'Mondo / Politica', { homepagePriority: 90 }),
  item('lead-alias', '2026-09-22T09:29:00+02:00', 'Politica', { url: '/notizie/lead.html' }),
  ...Array.from({ length: 7 }, (_, i) => item(`sport-${i}`, `2026-09-22T09:${20 - i}:00+02:00`, 'Italia / Sport', i === 5 ? { homepagePriority: 50 } : {})),
  item('multi', '2026-09-22T08:30:00+02:00', 'Italia / Politica', { primaryCategory: 'politica' })
];
const result = A.allocate(items, { now });
assert.equal(result.featured.id, 'lead');
assert.equal(result.latest.length, 5);
const shown = [result.featured, ...result.latest, ...result.sections.flatMap((s) => [s.lead, ...s.cards]), ...result.rest].filter(Boolean).map(A.canonicalKey);
assert.equal(shown.length, new Set(shown).size, 'tutti gli identificativi mostrati devono essere unici');
assert.ok(!result.latest.some((entry) => entry.id === 'lead'), 'il primo piano non deve ripetersi nelle ultime');
assert.ok(!result.sections.flatMap((s) => s.cards).some((entry) => result.latest.includes(entry)), 'le categorie non devono ripetere le ultime');
assert.ok(result.sections.every((section) => section.lead), 'ogni categoria visualizzata deve avere una card grande prima del carosello');
assert.ok(result.sections.every((section) => section.cards.length > 0), 'nessuna card grande deve apparire senza carosello');
assert.ok(result.sections.every((section) => 1 + section.cards.length <= A.CONFIG.smallCardsPerCategory), 'la card grande deve provenire dal carosello senza aumentare il numero di card');
assert.ok(result.sections.every((section) => section.cards.every((entry) => A.categoryFor(entry)?.id === section.category.id)), 'ogni carosello deve contenere soltanto card della propria categoria');
assert.equal(A.categoryFor(items.at(-1)).id, 'politica', 'primaryCategory deve prevalere sulle categorie multiple');
assert.ok(!fs.readFileSync(require.resolve('../assets/js/home-sections-v504.js'), 'utf8').includes('wrap.remove()'), 'un errore immagine non deve eliminare il riquadro e causare salti');
console.log('home-allocation-v504: tutti i test superati');
