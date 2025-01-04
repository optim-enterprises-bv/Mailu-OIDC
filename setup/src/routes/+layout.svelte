<script lang="ts">
  import { i18n } from '$lib/i18n';
  import { ParaglideJS } from '@inlang/paraglide-sveltekit';

  import '../app.css';
  import '@fontsource-variable/inter';
  import '@fontsource-variable/source-code-pro';

  let { children } = $props();
</script>

<ParaglideJS {i18n}>
  {@render children()}
</ParaglideJS>
