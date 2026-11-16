<script setup lang="ts">
import { computed } from 'vue';
import { BALANCIA_LOGO, BALANCIA_NAME } from '@Assets';

/**
 * Balancia's mark (brand/SYSTEM.md §5) — the platform's own screens wear it instead of a firm's
 * (`MFirmLogo`, `MNavbarBrand`, `ThePublicLayout`, while the host firm is the platform firm). A raster
 * mark (`<img>` of brand/logo/'s files), so it takes `variant` and `tone` and nothing else (celer-09).
 *
 * - `variant="full"` is the lockup, `min` the icon alone.
 * - `tone="brand"` follows the scheme: the light file on a light ground, the dark one on a dark ground.
 *   Both are rendered and the scheme hides one — the one place `dark:` is the right tool, because which
 *   FILE to show is not a colour a token can flip.
 * - `tone="inherit"` means the mark sits on a filled brand band (the sign-in aside, teal): the white file,
 *   whatever the scheme.
 *
 * Sized like `ALogo`, by the parent's font: `1.75em` high. Never recoloured, stretched or retyped.
 */
const props = withDefaults(
  defineProps<{
    tone?: 'brand' | 'inherit';
    variant?: 'full' | 'min';
  }>(),
  {
    tone: 'brand',
    variant: 'full',
  }
);

const files = computed(() => BALANCIA_LOGO[props.variant]);
const isOnBand = computed(() => props.tone === 'inherit');
const sizeClass = computed(() => (props.variant === 'min' ? 'aspect-square h-[1.75em] w-[1.75em]' : 'h-[1.75em] w-auto'));
</script>

<template>
  <span
    class="inline-flex items-center leading-none"
    data-testid="platform-logo"
  >
    <img
      v-if="isOnBand"
      data-testid="platform-logo-white"
      :alt="BALANCIA_NAME"
      :class="['max-w-full object-contain', sizeClass]"
      :src="files.white"
    />

    <template v-else>
      <img
        data-testid="platform-logo-light"
        :alt="BALANCIA_NAME"
        :class="['max-w-full object-contain dark:hidden', sizeClass]"
        :src="files.light"
      />

      <img
        data-testid="platform-logo-dark"
        :alt="BALANCIA_NAME"
        :class="['hidden max-w-full object-contain dark:block', sizeClass]"
        :src="files.dark"
      />
    </template>
  </span>
</template>
