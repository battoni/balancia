import { computed } from 'vue';
import { describe, expect, it, vi } from 'vitest';
import { mountWithPlugins } from '@/test/mount';
import i18n from '@Libraries/i18n';
import AuthFlowLayout from './AuthFlowLayout.vue';

/*
 * Balancia's own sign-in (the platform firm: the root, app.<root>): its own copy, without the Reforma
 * as the product's slogan, and a plain teal panel — `ABrandPattern` is Battoni Dev's (brand/SYSTEM.md).
 */
vi.mock('@Composables', async (importOriginal) => {
  const original = await importOriginal<Record<string, unknown>>();

  return {
    ...original,
    useFirmBrand: () => ({
      isPlatform: computed(() => true),
      logoText: computed(() => 'Balancia'),
      logoUrl: computed(() => null),
    }),
  };
});

describe('AuthFlowLayout on the platform', () => {
  it("speaks Balancia's copy and draws no Battoni Dev pattern", () => {
    const wrapper = mountWithPlugins(AuthFlowLayout, {
      global: { stubs: { ABrandPattern: true, APlatformLogo: true, Divider: true, MFirmLogo: true } },
      props: { title: 'Entrar' },
    });

    expect(wrapper.get('[data-testid="auth-brand-tag"]').text()).toBe(i18n.global.t('auth.platformBrand.tag'));
    expect(wrapper.get('[data-testid="auth-brand-headline"]').text()).toBe(
      i18n.global.t('auth.platformBrand.headline')
    );
    expect(wrapper.get('[data-testid="auth-brand-tagline"]').text()).toBe(i18n.global.t('auth.platformBrand.tagline'));
    expect(wrapper.get('[data-testid="auth-brand-tagline"]').text()).not.toMatch(/hub|Reforma/i);
    expect(wrapper.findComponent({ name: 'ABrandPattern' }).exists()).toBe(false);
  });
});
