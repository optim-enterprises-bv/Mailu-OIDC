<script lang="ts">
  import { page } from '$app/state';

  import { i18n, setLanguage } from '$lib/i18n';
  import { language } from '$lib/paraglide/messages';
  import { languageTag } from '$lib/paraglide/runtime';

  import * as DropdownMenu from '$lib/components/ui/dropdown-menu';

  import { Languages } from 'lucide-svelte';

  const href = $derived(i18n.route(page.url.pathname));

  const languages = [
    {
      tag: 'de',
      name: 'Deutsch'
    },
    {
      tag: 'en',
      name: 'English'
    }
  ] as const;

  let isOpen = $state(false);
</script>

<DropdownMenu.Sub bind:open={isOpen}>
  <DropdownMenu.SubTrigger>
    <Languages />
    {language()}: <kbd class="text-sm tracking-widest opacity-60">{languageTag()}</kbd>
  </DropdownMenu.SubTrigger>
  <DropdownMenu.SubContent>
    <DropdownMenu.RadioGroup value={languageTag()}>
      {#each languages as language}
        <DropdownMenu.RadioItem
          value={language.tag}
          onSelect={() => setLanguage(href, language.tag)}
        >
          <span>{language.name}</span>
          <DropdownMenu.Shortcut>{language.tag}</DropdownMenu.Shortcut>
        </DropdownMenu.RadioItem>
      {/each}
    </DropdownMenu.RadioGroup>
  </DropdownMenu.SubContent>
</DropdownMenu.Sub>
