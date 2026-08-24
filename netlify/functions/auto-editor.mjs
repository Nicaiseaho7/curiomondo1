export default async () => {
  const enabled = String(process.env.CURIOMONDO_AUTO_PUBLISH || '').toLowerCase() === 'true';
  if (!enabled) {
    console.log('[CurioMondo Auto Editor] SAFE MODE: ciclo ogni 2 ore attivo, pubblicazione disabilitata.');
    return new Response(JSON.stringify({ok:true, mode:'safe', published:false, reason:'CURIOMONDO_AUTO_PUBLISH not enabled'}), {
      headers: {'content-type':'application/json; charset=utf-8'}
    });
  }
  console.log('[CurioMondo Auto Editor] Publishing flag enabled, but production publisher is not armed until API secrets and QA test are completed.');
  return new Response(JSON.stringify({ok:true, mode:'armed-pending-secrets', published:false}), {
    headers: {'content-type':'application/json; charset=utf-8'}
  });
};
