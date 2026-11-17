<script setup lang="ts">
import { useFirmBrand } from '@Composables';

/*
 * The host firm's mark (rnc-4 R15): `ALogo` with the firm's logo text, for the screens that show the
 * mark on their own — sign-in, terms, not found, the repricing letter. `variant`, `tone` and classes
 * fall through to the mark. Draws nothing until a firm is known (the tab's last answer or the API's),
 * so no name the build carries ever shows. The firm's uploaded logo (`logoUrl`, rnc-4 R27) is the mark
 * when it has one. The platform firm's screens (the root's sign-in) wear Balancia's own mark,
 * `APlatformLogo`, never a text logo of the product's name (brand/SYSTEM.md §5).
 */
const { isPlatform, logoText, logoUrl } = useFirmBrand();
</script>

<template>
  <APlatformLogo v-if="isPlatform" />

  <ALogo
    v-else-if="logoText"
    :name="logoText"
    :src="logoUrl"
  />
</template>
