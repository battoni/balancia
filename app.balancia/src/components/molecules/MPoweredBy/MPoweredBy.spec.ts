import { describe, expect, it } from 'vitest';
import { mountWithPlugins } from '@/test/mount';
import MPoweredBy from './MPoweredBy.vue';

/*
 * The product's signature under a tenant's pages (brand/SYSTEM.md §5): the icon at 16px and the
 * words, one colour — the muted text's, the icon painting with `currentColor` — and never larger.
 */
describe('MPoweredBy', () => {
  it("signs with the product's name, the 16px icon and one muted colour", () => {
    const wrapper = mountWithPlugins(MPoweredBy, { props: { name: 'Balancia' } });
    const icon = wrapper.find('svg');

    expect(wrapper.text()).toBe('powered by Balancia');
    expect(wrapper.classes()).toEqual(expect.arrayContaining(['text-muted', 'text-xs']));
    expect(icon.classes()).toContain('size-4');
    expect(icon.attributes('fill')).toBe('currentColor');
    expect(icon.attributes('aria-hidden')).toBe('true');
  });

  it('draws nothing without a name', () => {
    expect(mountWithPlugins(MPoweredBy, { props: { name: '' } }).html()).not.toContain('powered-by');
  });
});
