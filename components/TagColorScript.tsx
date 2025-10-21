export default function TagColorScript() {
  return (
    <script
      dangerouslySetInnerHTML={{
        __html: `
          (function() {
            function updateTagColors() {
              document.querySelectorAll('.nav-tag-pill').forEach(function(pill) {
                var text = pill.textContent.trim().toUpperCase();
                if (text === 'NEW') {
                  pill.classList.add('tag-new');
                } else {
                  pill.classList.remove('tag-new');
                }
              });
            }
            
            if (document.readyState === 'loading') {
              document.addEventListener('DOMContentLoaded', updateTagColors);
            } else {
              updateTagColors();
            }
            
            // Watch for dynamic content changes
            var observer = new MutationObserver(updateTagColors);
            observer.observe(document.body, { childList: true, subtree: true });
          })();
        `,
      }}
    />
  );
}

