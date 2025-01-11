<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { inlineCode, link } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const rootDefault = '/mailu';
  const root = new LocalStorage('root', rootDefault);
  const rootCustom = new LocalStorage('root__custom', '/var/mailu');
</script>

<Setup.Root
  type="radio"
  bind:value={root.current}
  title={m.installation_directory_title()}
  description={m.installation_directory_description()}
>
  <Setup.Item value={rootDefault} title={m.installation_directory_o_default_title()}>
    {#snippet description()}
      {@render inlineCode(
        m.installation_directory_o_default_description({ installDir: rootDefault })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    value={rootCustom.current}
    title={m.installation_directory_o_custom_title()}
    description={m.installation_directory_o_custom_description()}
  >
    {#if root.current === rootCustom.current}
      <Setup.Input
        bind:value={rootCustom.current}
        title={m.installation_directory_o_custom_title()}
      />
    {/if}
  </Setup.Item>

  {#snippet hint()}
    <p>
      {@render inlineCode(
        m.installation_directory_hint_install_dir({ installDir: root.current ?? '' })
      )}
    </p>

    {#if root.current && root.current.replace(/[^/]/g, '').length > 2}
      <Setup.Alert variant="warning">
        {@render link(
          m.installation_directory_hint_more_than_two_subdirs_warning({
            openIssueLink: 'https://github.com/Mailu/Mailu/issues/3164'
          })
        )}
      </Setup.Alert>
    {/if}
  {/snippet}
</Setup.Root>
