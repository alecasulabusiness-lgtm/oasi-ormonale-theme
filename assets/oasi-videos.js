/* Video YouTube a caricamento al clic (indirizzo privacy-enhanced, nessuna richiesta a YouTube prima del clic). */
(function () {
  if (window.__oasiVideos) return;
  window.__oasiVideos = true;

  document.addEventListener('click', function (event) {
    var button = event.target.closest ? event.target.closest('.oasi-video__play') : null;
    if (!button) return;

    var frame = button.parentElement;
    var id = frame && frame.getAttribute('data-yt');
    if (!id) return;

    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    iframe.title = button.getAttribute('aria-label') || 'Video';
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    iframe.setAttribute('allowfullscreen', '');
    iframe.setAttribute('loading', 'lazy');

    frame.appendChild(iframe);
    button.remove();
  });
})();
