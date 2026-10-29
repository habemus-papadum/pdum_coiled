import { renderWidget } from './widget';
import type { WidgetPayload } from './types';

export interface InitOptions {
  target: HTMLElement;
  payload: WidgetPayload;
}

export function initWidget(options: InitOptions) {
  renderWidget(options.target, options.payload);
}

export { renderWidget };
export type { WidgetPayload };
