<script setup lang="ts">
/**
 * The product's discreet signature under a firm tenant's pages (brand/SYSTEM.md §5): Balancia's icon at
 * 16px and "powered by {name}", in one colour — the footer's muted text, the icon included — and never
 * larger. The firm's brand leads; this only says what it runs on.
 *
 * Inline SVG so the icon takes `currentColor`: the one-colour rule is the brand's mono version
 * (`brand/logo/balancia-icon-mono.svg`), painted by the text colour instead of a fixed fill. The icon is
 * `aria-hidden`: the words beside it already say the name.
 *
 * `name` is the product's name as the API answers it (`platform.name`); with none, nothing is drawn.
 */
const props = defineProps<{
  name: string;
}>();
</script>

<template>
  <span
    v-if="props.name"
    class="text-muted inline-flex items-center gap-1.5 text-xs"
    data-testid="powered-by"
  >
    <svg
      aria-hidden="true"
      class="size-4 shrink-0"
      fill="currentColor"
      focusable="false"
      viewBox="0 0 512 512"
    >
      <path
        d="M118 52H318C371 52 414 94 414 142C414 184 388 212 348 220C300 229.6 200 244 160 257C124 268.7 82 268 82 232V88C82 68.1 98.1 52 118 52Z"
      />

      <path
        d="M82 360C82 336 100 316.6 128 304C168 286 310 262 350 258C396 253.4 438 290 438 338C438 406 384 460 306 460H118C98.1 460 82 443.9 82 424Z"
      />
    </svg>

    {{ $t('site.footer.poweredBy', { name: props.name }) }}
  </span>
</template>
