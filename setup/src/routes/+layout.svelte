<script lang="ts">
  import { i18n } from '$lib/i18n';
  import { ParaglideJS } from '@inlang/paraglide-sveltekit';

  import { ModeWatcher } from 'mode-watcher';

  import * as Sidebar from '$lib/components/ui/sidebar';

  import * as App from '$lib/components/composed/app-navigation';

  import '../app.css';
  import '@fontsource-variable/inter';
  import '@fontsource-variable/source-code-pro';

  const { children: pageContent } = $props();
</script>

<ModeWatcher />

<ParaglideJS {i18n}>
  <App.Navigation>
    {#snippet children(items: Record<string, App.NavItem[]>)}
      <App.Sidebar {items} />
      <Sidebar.Inset>
        <App.Header {items} />
        <div class="flex flex-1 flex-col gap-4 p-4 pt-0">
          {@render pageContent?.()}
        </div>
      </Sidebar.Inset>
    {/snippet}
  </App.Navigation>
</ParaglideJS>
