import type { WidgetPayload } from './types';

const TEMPLATE_ID = 'coiled-widget-template';

function ensureTemplate() {
  if (document.getElementById(TEMPLATE_ID)) {
    return;
  }

  const template = document.createElement('template');
  template.id = TEMPLATE_ID;
  template.innerHTML = `
    <div class="tp-widget">
      <h3 class="tp-widget__title"></h3>
      <pre class="tp-widget__body"></pre>
    </div>
  `;
  document.body.appendChild(template);
}

export function renderWidget(element: HTMLElement, payload: WidgetPayload) {
  ensureTemplate();

  const template = document.getElementById(TEMPLATE_ID) as HTMLTemplateElement;
  const clone = template.content.cloneNode(true) as DocumentFragment;

  const container = clone.querySelector('.tp-widget') as HTMLElement;
  const title = clone.querySelector('.tp-widget__title') as HTMLElement;
  const body = clone.querySelector('.tp-widget__body') as HTMLElement;

  title.textContent = payload.title ?? 'Widget Preview';
  body.textContent = payload.body ?? 'No data provided.';

  element.innerHTML = '';
  element.appendChild(clone);

  if (payload.metadata) {
    container.dataset.metadata = JSON.stringify(payload.metadata);
  }
}
