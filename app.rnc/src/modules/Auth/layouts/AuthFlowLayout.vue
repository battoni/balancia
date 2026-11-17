<script setup lang="ts">
import { computed } from 'vue';
import { useFirmBrand } from '@Composables';

/*
 * The sign-in's brand panel. A firm's copy is `auth.brand.*`; Balancia's own sign-in (the platform
 * firm: the root, app.<root>) carries `auth.platformBrand.*`, which leaves the Reforma out of the
 * product's slogan, and a plain teal panel: `ABrandPattern` is Battoni Dev's, never Balancia's
 * (brand/SYSTEM.md §6, §9).
 */
withDefaults(
  defineProps<{
    title?: string;
  }>(),
  {
    title: '',
  }
);

const { isPlatform } = useFirmBrand();

const copyKey = computed(() => (isPlatform.value ? 'auth.platformBrand' : 'auth.brand'));
</script>

<template>
  <div class="bg-canvas flex min-h-screen w-full">
    <aside
      class="bg-primary-500 relative hidden overflow-hidden lg:flex lg:w-[44%] lg:flex-col lg:justify-between lg:p-12 xl:p-16"
    >
      <div
        v-if="!isPlatform"
        class="text-primary-contrast absolute inset-0 opacity-[0.07]"
      >
        <ABrandPattern
          :rotate="-8"
          :tile="168"
        />
      </div>

      <div class="relative">
        <MFirmLogo
          class="text-primary-contrast text-3xl"
          tone="inherit"
        />
      </div>

      <div class="relative flex flex-col gap-6">
        <!-- The hero copy is the PROJECT's: every string is an `auth.brand.*` (a firm's) or
             `auth.platformBrand.*` (Balancia's) key, overridden in
             `src/locales/local/*.json` so a sync never reverts it. -->
        <span
          class="text-primary-contrast/70 font-mono text-sm tracking-[0.2em] uppercase"
          data-testid="auth-brand-tag"
        >
          {{ $t(`${copyKey}.tag`) }}
        </span>

        <h2
          class="text-primary-contrast text-5xl leading-[1.04] font-bold tracking-tight whitespace-pre-line xl:text-6xl"
          data-testid="auth-brand-headline"
        >
          {{ $t(`${copyKey}.headline`) }}
        </h2>

        <p
          class="text-primary-contrast/80 max-w-sm font-mono text-sm leading-relaxed"
          data-testid="auth-brand-tagline"
        >
          {{ $t(`${copyKey}.tagline`) }}
        </p>
      </div>

      <div
        class="text-primary-contrast/90 relative font-mono text-sm font-medium tracking-tight"
        data-testid="auth-brand-domain"
      >
        {{ $t(`${copyKey}.domain`) }}
      </div>
    </aside>

    <main class="relative flex flex-1 flex-col">
      <div
        v-if="!isPlatform"
        class="text-subtle pointer-events-none absolute inset-0 opacity-[0.03] lg:hidden"
      >
        <ABrandPattern :tile="150" />
      </div>

      <div class="relative flex flex-1 items-center justify-center px-4 py-4">
        <div class="flex w-full max-w-[400px] flex-col">
          <div class="mb-4 flex justify-center">
            <MFirmLogo
              class="text-2xl"
              variant="min"
            />
          </div>

          <div
            v-if="$slots.topActions"
            class="mb-4"
          >
            <slot name="topActions" />
          </div>

          <div class="border-line-strong bg-canvas w-full rounded-xl border">
            <div class="pt-5">
              <h1
                v-if="title"
                class="text-heading text-center text-xl font-medium"
              >
                {{ title }}
              </h1>
            </div>

            <Divider class="before:border-line-strong w-full" />

            <div class="flex w-full flex-col p-5">
              <slot />
            </div>
          </div>

          <div
            v-if="$slots.bottomActions"
            class="mt-4 px-2"
          >
            <slot name="bottomActions" />
          </div>
        </div>
      </div>

      <div class="relative flex justify-center pb-4">
        <ABrandSignature />
      </div>
    </main>
  </div>
</template>
