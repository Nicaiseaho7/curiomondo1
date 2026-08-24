(function(){
  'use strict';
  var TURBO_MS=15000;
  window.cmV32TurboInstalled=true; // impedisce al vecchio handler breve di registrarsi
  var turboTimer=null,turboTick=null;
  function $(id){return document.getElementById(id)}
  function turbo15(){
    var stage=$('cmOrbitStage'),btn=$('cmEarthBoostBtn');
    if(!stage)return;
    if(turboTimer)clearTimeout(turboTimer);
    if(turboTick)clearInterval(turboTick);
    stage.classList.remove('is-hyper');
    stage.classList.add('is-turbo');
    var end=Date.now()+TURBO_MS;
    function label(){
      if(!btn)return;
      var sec=Math.max(0,Math.ceil((end-Date.now())/1000));
      btn.innerHTML='Pianeti in orbita veloce <span class="cm-earth-boost-countdown">'+sec+'s</span> <b>✦</b>';
    }
    label();
    turboTick=setInterval(label,250);
    turboTimer=setTimeout(function(){
      stage.classList.remove('is-turbo');
      clearInterval(turboTick);
      turboTick=null;turboTimer=null;
      if(btn)btn.innerHTML='Fai girare i pianeti <b>✦</b>';
    },TURBO_MS);
  }
  function init(){
    var btn=$('cmEarthBoostBtn');
    if(btn)btn.addEventListener('click',function(e){e.preventDefault();e.stopImmediatePropagation();turbo15()},true);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
