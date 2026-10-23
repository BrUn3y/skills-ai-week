/* Translate fallback notices emitted by Archify's reader at runtime. */
(() => {
  const nativeTheme = JSON.parse(document.getElementById('aiweek-native-theme').textContent);
  window.aiWeekStyleViewer = html => html.replace('</head>', '<style id="aiweek-viewer-style">' + nativeTheme.css + '</style></head>');
  // Start in the event palette; light and system controls remain available.
  document.querySelector('[data-theme-choice="dark"]')?.click();
  const phrases = new Map([
    ['This diagram cannot fit this page width with readable text. Open the interactive view to inspect it.', 'Abre la vista interactiva para ampliar y explorar este diagrama.'],
    ['▶ Step through', '▶ Recorrer paso a paso'],
    ['▶ Walk the flow', '▶ Recorrer el flujo'],
    ['Step through', 'Recorrer paso a paso'],
    ['Walk the flow', 'Recorrer el flujo'],
    ['Copy', 'Copiar'], ['Copied', 'Copiado'],
    ['Back', 'Anterior'], ['Next', 'Siguiente'], ['Done', 'Terminar'],
    ['分支 1', 'Rama 1'],
  ]);
  function translate(root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.parentElement?.closest('script,style,pre,code,textarea')) continue;
      const text = node.textContent.trim();
      if (phrases.has(text)) node.textContent = node.textContent.replace(text, phrases.get(text));
    }
  }
  translate(document.body);
  new MutationObserver(records => {
    for (const record of records) {
      if (record.type === 'characterData') {
        const parent = record.target.parentElement;
        if (parent) translate(parent);
      } else for (const node of record.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) translate(node);
        else if (node.nodeType === Node.TEXT_NODE && node.parentElement) translate(node.parentElement);
      }
    }
  }).observe(document.body, { childList: true, subtree: true, characterData: true });
})();
