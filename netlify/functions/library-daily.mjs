export default async () => {
  const enabled = String(process.env.CURIOMONDO_LIBRARY_AUTO_PUBLISH || '').toLowerCase() === 'true';
  if (!enabled) {
    console.log('[CurioMondo Library] SAFE MODE: ciclo giornaliero attivo, pubblicazione guide disabilitata.');
    return new Response(JSON.stringify({ok:true, mode:'safe', target_guides:3, published:false}), {
      headers: {'content-type':'application/json; charset=utf-8'}
    });
  }
  console.log('[CurioMondo Library] Publishing flag enabled, but production publisher is not armed until API secrets and QA test are completed.');
  return new Response(JSON.stringify({ok:true, mode:'armed-pending-secrets', target_guides:3, published:false}), {
    headers: {'content-type':'application/json; charset=utf-8'}
  });
};
