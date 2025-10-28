import { renderWidget } from './widget';
import type { WidgetPayload } from './types';
import { VERSION } from './version';

const DATA_ATTRIBUTE = 'data-coiled-widget';
declare const __WIDGET_STYLES__: string;

function injectStyles() {
  const styleId = 'coiled-widget-styles';
  if (document.getElementById(styleId)) {
    return;
  }

  const style = document.createElement('style');
  style.id = styleId;
  style.textContent = typeof __WIDGET_STYLES__ === 'string' ? __WIDGET_STYLES__ : '';
  document.head.appendChild(style);
}

function boot() {
  injectStyles();
  const nodes = document.querySelectorAll(`[${DATA_ATTRIBUTE}]`);
  nodes.forEach((node) => {
    const element = node as HTMLElement;
    const raw = element.getAttribute(DATA_ATTRIBUTE);
    if (!raw) {
      return;
    }

    try {
      const payload = JSON.parse(raw) as WidgetPayload;
      renderWidget(element, payload);
    } catch (error) {
      console.error('Failed to render widget payload', error);
    }
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', boot);
} else {
  boot();
}

(window as typeof window & { CoiledWidgets?: Record<string, unknown> }).CoiledWidgets = {
  VERSION,
  renderWidget,
};
