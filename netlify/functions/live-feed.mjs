import { getStore } from "@netlify/blobs";
import { readFile } from "node:fs/promises";

async function fallback() {
  try {
    const u = new URL("../../automation/live-seed.json", import.meta.url);
    return JSON.parse(await readFile(u, "utf8"));
  } catch {
    return { updated_at: null, items: [] };
  }
}

export default async () => {
  let payload;
  try {
    const store = getStore({ name: "curiomondo-live", consistency: "strong" });
    payload = await store.get("latest", { type: "json", consistency: "strong" });
  } catch {}
  if (!payload?.items?.length) payload = await fallback();
  return new Response(JSON.stringify(payload), {
    status: 200,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "public, max-age=30, stale-while-revalidate=60",
      "access-control-allow-origin": "https://curiomondo.it"
    }
  });
};
