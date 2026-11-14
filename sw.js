/* Il service worker di Monetag (push, zona 12263373) è stato disattivato.
   Questo file resta solo per far disinstallare il worker già presente nei browser. */
self.addEventListener('install', function () {
  self.skipWaiting();
});
self.addEventListener('activate', function (event) {
  event.waitUntil(self.registration.unregister());
});
