import { describe, expect, it } from 'vitest';
import { mountWithPlugins } from '@/test/mount';
import APlatformLogo from './APlatformLogo.vue';

/*
 * Balancia's mark (brand/SYSTEM.md §5): the lockup or the icon, in the file that matches the ground —
 * light and dark both rendered for the scheme to pick, white alone on a filled brand band.
 */
describe('APlatformLogo', () => {
  it('draws the lockup in its light and dark files, the scheme hiding one', () => {
    const wrapper = mountWithPlugins(APlatformLogo);

    const light = wrapper.find('img[data-testid="platform-logo-light"]');
    const dark = wrapper.find('img[data-testid="platform-logo-dark"]');

    expect(light.attributes('src')).toMatch(/balancia-logo\.svg/);
    expect(light.classes()).toContain('dark:hidden');
    expect(dark.attributes('src')).toMatch(/balancia-logo-dark\.svg/);
    expect(dark.classes()).toContain('dark:block');
    expect(light.attributes('alt')).toBe('Balancia');
  });

  it('draws the icon alone in min', () => {
    const wrapper = mountWithPlugins(APlatformLogo, { props: { variant: 'min' } });

    expect(wrapper.find('img[data-testid="platform-logo-light"]').attributes('src')).toMatch(/balancia-icon\.svg/);
    expect(wrapper.find('img[data-testid="platform-logo-dark"]').attributes('src')).toMatch(/balancia-icon-dark\.svg/);
  });

  it('draws only the white file on a brand band (tone inherit)', () => {
    const wrapper = mountWithPlugins(APlatformLogo, { props: { tone: 'inherit' } });

    expect(wrapper.findAll('img')).toHaveLength(1);
    expect(wrapper.find('img').attributes('src')).toMatch(/balancia-logo-white\.svg/);
  });
});
