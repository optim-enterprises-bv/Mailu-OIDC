<script lang="ts">
  import { i18n } from '$lib/i18n';
  import { ParaglideJS } from '@inlang/paraglide-sveltekit';

  import { ModeWatcher } from 'mode-watcher';

  import {
    AppHeader,
    AppNavigation,
    AppSidebar,
    type NavItem
  } from '$lib/components/composed/app-navigation';

  import { SidebarInset } from '$lib/components/ui/sidebar';

  import '../app.css';
  import '@fontsource-variable/inter';
  import '@fontsource-variable/source-code-pro';

  const { children: pageContent } = $props();
</script>

<ModeWatcher />

<ParaglideJS {i18n}>
  <AppNavigation>
    {#snippet children(items: Record<string, NavItem[]>)}
      <AppSidebar {items} />
      <SidebarInset>
        <AppHeader {items} />
        <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
          {@render pageContent?.()}
        </div>
      </SidebarInset>
    {/snippet}
  </AppNavigation>
</ParaglideJS>
