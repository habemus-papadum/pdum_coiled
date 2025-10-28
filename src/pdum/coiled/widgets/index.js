"use strict";var CoiledWidgets=(()=>{var i="coiled-widget-template";function p(){if(document.getElementById(i))return;let e=document.createElement("template");e.id=i,e.innerHTML=`
    <div class="tp-widget">
      <h3 class="tp-widget__title"></h3>
      <pre class="tp-widget__body"></pre>
    </div>
  `,document.body.appendChild(e)}function r(e,t){p();let n=document.getElementById(i).content.cloneNode(!0),o=n.querySelector(".tp-widget"),s=n.querySelector(".tp-widget__title"),m=n.querySelector(".tp-widget__body");s.textContent=t.title??"Widget Preview",m.textContent=t.body??"No data provided.",e.innerHTML="",e.appendChild(n),t.metadata&&(o.dataset.metadata=JSON.stringify(t.metadata))}var a="0.1.0";var c="data-coiled-widget";function g(){let e="coiled-widget-styles";if(document.getElementById(e))return;let t=document.createElement("style");t.id=e,t.textContent=`:root {
  --widget-border: #e0e0e0;
  --widget-bg: #fafafa;
  --widget-accent: #1976d2;
  --widget-font: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.tp-widget {
  border: 1px solid var(--widget-border);
  border-radius: 8px;
  padding: 1rem;
  background: var(--widget-bg);
  font-family: var(--widget-font);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.tp-widget h3 {
  margin-top: 0;
  color: var(--widget-accent);
}

.tp-widget pre {
  background: white;
  padding: 0.75rem;
  border-radius: 6px;
  overflow-x: auto;
}
`,document.head.appendChild(t)}function l(){g(),document.querySelectorAll(`[${c}]`).forEach(t=>{let d=t,n=d.getAttribute(c);if(n)try{let o=JSON.parse(n);r(d,o)}catch(o){console.error("Failed to render widget payload",o)}})}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",l):l();window.CoiledWidgets={VERSION:a,renderWidget:r};})();
//# sourceMappingURL=index.js.map
