/* Google Analytics 4 — G-EGCM3F9Y2L. Parte solo dopo il consenso «statistiche». */
(function () {
  var ID = 'G-EGCM3F9Y2L';
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;
  function consentState() {
    try {
      var saved = JSON.parse(localStorage.getItem('cm_consent_v2') || 'null');
      return { analytics: !!(saved && saved.analytics), marketing: !!(saved && saved.marketing) };
    } catch (error) {
      return { analytics: false, marketing: false };
    }
  }
  function payload(state) {
    return {
      analytics_storage: state.analytics ? 'granted' : 'denied',
      ad_storage: state.marketing ? 'granted' : 'denied',
      ad_user_data: state.marketing ? 'granted' : 'denied',
      ad_personalization: state.marketing ? 'granted' : 'denied'
    };
  }
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    functionality_storage: 'denied',
    personalization_storage: 'denied',
    security_storage: 'granted',
    wait_for_update: 500
  });
  var loaded = false;
  function loadGa() {
    if (loaded || document.querySelector('script[src*="googletagmanager.com/gtag/js"]')) {
      loaded = true;
      return;
    }
    loaded = true;
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(script);
  }
  var state = consentState();
  if (state.analytics) {
    gtag('consent', 'update', payload(state));
    gtag('js', new Date());
    gtag('config', ID, { anonymize_ip: true });
    loadGa();
  }
  var counted = state.analytics;
  function sync() {
    var next = consentState();
    gtag('consent', 'update', payload(next));
    if (next.analytics) {
      if (!loaded) {
        gtag('js', new Date());
        gtag('config', ID, { anonymize_ip: true });
        loadGa();
      }
      if (!counted) {
        counted = true;
        gtag('event', 'page_view');
      }
    }
    if (!next.analytics) counted = false;
  }
  new MutationObserver(sync).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-consent-analytics', 'data-consent-marketing']
  });
})();
