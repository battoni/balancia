import type { Page } from '@playwright/test';

/*
 * WCAG contrast of rendered text: each element's colour over the first painted ground at or above
 * it, both flattened to `rgb()` through a canvas so translucent tints and `color-mix` resolve the way
 * the screen shows them. The other contrast specs carry their own copy of this; new ones use it.
 */
export interface RenderedPair {
  label: string;
  colour: string;
  background: string;
}

function luminance([red, green, blue]: number[]) {
  const channels = [red, green, blue].map((value) => {
    const srgb = value! / 255;

    return srgb <= 0.03928 ? srgb / 12.92 : ((srgb + 0.055) / 1.055) ** 2.4;
  });

  return 0.2126 * channels[0]! + 0.7152 * channels[1]! + 0.0722 * channels[2]!;
}

function parseRgb(colour: string) {
  return (colour.match(/\d+(\.\d+)?/g) ?? []).slice(0, 3).map(Number);
}

export function contrastOf(pair: RenderedPair) {
  const [lighter, darker] = [luminance(parseRgb(pair.colour)), luminance(parseRgb(pair.background))].sort(
    (first, second) => second - first
  );

  return (lighter! + 0.05) / (darker! + 0.05);
}

/** Every text-bearing element under `selector` (itself included), paired with the ground it sits on. */
export async function renderedTextPairs(page: Page, selector: string): Promise<RenderedPair[]> {
  return page.evaluate((query) => {
    const context = document.createElement('canvas').getContext('2d', { willReadFrequently: true })!;
    const body = window.getComputedStyle(document.body).backgroundColor;

    function toRgb(colour: string, under = body): string {
      context.clearRect(0, 0, 1, 1);
      context.fillStyle = under;
      context.fillRect(0, 0, 1, 1);
      context.fillStyle = colour;
      context.fillRect(0, 0, 1, 1);

      const [red, green, blue] = context.getImageData(0, 0, 1, 1).data;

      return `rgb(${red}, ${green}, ${blue})`;
    }

    function ground(element: Element | null): string {
      for (let node = element; node; node = node.parentElement) {
        const background = window.getComputedStyle(node).backgroundColor;

        if (background !== 'rgba(0, 0, 0, 0)' && !background.endsWith(', 0)') && !background.endsWith('/ 0)')) {
          return toRgb(background);
        }
      }

      return toRgb(body, '#ffffff');
    }

    const roots = [...document.querySelectorAll(query)];
    const elements = roots.flatMap((root) => [root, ...root.querySelectorAll('*')]);

    return elements
      .filter((element) =>
        [...element.childNodes].some((node) => node.nodeType === Node.TEXT_NODE && node.textContent?.trim())
      )
      .map((element) => {
        const background = ground(element);

        return {
          label: `${query} "${element.textContent?.trim().slice(0, 32)}"`,
          colour: toRgb(window.getComputedStyle(element).color, background),
          background,
        };
      });
  }, selector);
}
