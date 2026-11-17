import { flushPromises } from '@vue/test-utils';
import { delay, http, HttpResponse } from 'msw';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ALogo from '@/components/atoms/ALogo/ALogo.vue';
import APlatformLogo from '@/components/atoms/APlatformLogo/APlatformLogo.vue';
import { mountWithPlugins } from '@/test/mount';
import { server } from '@/test/msw/server';

/*
 * rnc-4 R10, A11: the back office's rail and drawer write the host firm's logo text and the
 * product's name (`platform.name`, R9) — from the firm's answer, never a name in the build.
 */
const ALVORADA = {
  address: null,
  brand_accent: '#f4b63f',
  brand_primary: '#0f5c4d',
  business_hours: [],
  logo_text: 'Alvorada Contabilidade',
  mailbox: null,
  name: 'Alvorada Contabilidade',
  phone: null,
  phone_href: null,
  platform: { name: 'Balancia' },
  slug: 'alvorada',
};

async function mountBrand() {
  vi.resetModules();

  const { useFirmBrand } = await import('@Composables');
  const { default: MNavbarBrand } = await import('./MNavbarBrand.vue');

  await useFirmBrand().load();

  const wrapper = mountWithPlugins(MNavbarBrand, { global: { components: { ALogo, APlatformLogo } } });

  await flushPromises();

  return wrapper;
}

beforeEach(() => {
  sessionStorage.clear();
  server.use(http.get('http://localhost/public/firm', () => HttpResponse.json({ data: ALVORADA })));
});

describe('MNavbarBrand', () => {
  it("writes the firm's logo text in the tile and beside it, and the product's name", async () => {
    const wrapper = await mountBrand();

    expect(wrapper.find('[role="img"]').attributes('aria-label')).toBe('Alvorada Contabilidade');
    expect(wrapper.find('[data-testid="navbar-firm-name"]').text()).toBe('Alvorada Contabilidade');
    expect(wrapper.find('[data-testid="navbar-platform-name"]').text()).toBe('Balancia');
  });

  it('writes no other firm while the answer is on its way', async () => {
    server.use(
      http.get('http://localhost/public/firm', async () => {
        await delay(300);

        return HttpResponse.json({ data: ALVORADA });
      })
    );
    vi.resetModules();

    const { default: MNavbarBrand } = await import('./MNavbarBrand.vue');
    const wrapper = mountWithPlugins(MNavbarBrand, { global: { components: { ALogo, APlatformLogo } } });

    expect(wrapper.text()).not.toContain('Franco');
    expect(wrapper.find('[role="img"]').exists()).toBe(false);
  });

  // rnc-4 R27, A43: a firm with an uploaded logo shows it in the rail, asked on the page's own origin.
  it("shows the firm's uploaded logo in the tile", async () => {
    server.use(
      http.get('http://localhost/public/firm', () =>
        HttpResponse.json({ data: { ...ALVORADA, logo_url: 'http://localhost:8000/storage/firms/3/logo.png' } })
      )
    );

    const wrapper = await mountBrand();
    const image = wrapper.find('img[data-testid="logo-image"]');

    expect(image.attributes('src')).toBe('/storage/firms/3/logo.png');
    expect(image.attributes('alt')).toBe('Alvorada Contabilidade');
  });

  // Balancia rename, step 3: the console's tile is Balancia's icon, and the product is not named twice.
  it("shows Balancia's icon in the platform firm's tile, without repeating the product's name", async () => {
    server.use(
      http.get('http://localhost/public/firm', () =>
        HttpResponse.json({
          data: { ...ALVORADA, is_platform: true, logo_text: 'Balancia', name: 'Balancia', slug: 'balancia' },
        })
      )
    );

    const wrapper = await mountBrand();

    expect(wrapper.find('img[data-testid="platform-logo-light"]').attributes('src')).toContain('balancia-icon');
    expect(wrapper.find('[data-testid="navbar-firm-name"]').text()).toBe('Balancia');
    expect(wrapper.find('[data-testid="navbar-platform-name"]').exists()).toBe(false);
  });
});
