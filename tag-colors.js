(function() {
  'use strict';
  
  function updateTagColors() {
    const pills = document.querySelectorAll('.nav-tag-pill');
    console.log('[Tag Colors] Found', pills.length, 'tag pills');
    
    pills.forEach(function(pill) {
      const text = pill.textContent.trim().toUpperCase();
      console.log('[Tag Colors] Tag text:', text);
      
      if (text === 'NEW') {
        pill.classList.add('tag-new');
        console.log('[Tag Colors] Applied tag-new class to:', pill);
      } else if (text === 'BETA') {
        pill.classList.remove('tag-new');
      }
    });
  }

  // Run on initial load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateTagColors);
  } else {
    updateTagColors();
  }
  
  // Run after delays to catch async content
  setTimeout(updateTagColors, 100);
  setTimeout(updateTagColors, 500);
  setTimeout(updateTagColors, 1000);
  setTimeout(updateTagColors, 2000);

  // Watch for DOM changes
  var observer = new MutationObserver(function(mutations) {
    var shouldUpdate = false;
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes.length > 0) {
        mutation.addedNodes.forEach(function(node) {
          if (node.nodeType === 1 && 
              (node.classList && node.classList.contains('nav-tag-pill') ||
               node.querySelector && node.querySelector('.nav-tag-pill'))) {
            shouldUpdate = true;
          }
        });
      }
    });
    if (shouldUpdate) {
      updateTagColors();
    }
  });
  
  observer.observe(document.body, { 
    childList: true, 
    subtree: true
  });

  console.log('[Tag Colors] Script initialized');
})();

