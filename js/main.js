/* robot fantôme — main.js
   Fades images in once loaded. That's it. */

(function () {
  'use strict';

  function fadeInOnLoad(img) {
    if (img.complete) {
      img.classList.add('loaded');
    } else {
      img.addEventListener('load', function () {
        img.classList.add('loaded');
      });
    }
  }

  document.querySelectorAll('img').forEach(fadeInOnLoad);
})();
