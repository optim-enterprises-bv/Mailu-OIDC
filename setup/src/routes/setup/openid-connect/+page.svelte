<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { githubRepository, inlineCode } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const dockerOrg = new LocalStorage('dockerOrg', 'ghcr.io/heviat');
</script>

<Setup.Root
  type="radio"
  bind:value={dockerOrg.current}
  title={m.openid_connect_title()}
  description={m.openid_connect_description()}
>
  {#snippet moreInfo()}
    <p>{m.openid_connect_details()}</p>
  {/snippet}

  <Setup.Item value="ghcr.io/heviat" title={m.openid_connect_o_yes_title()}>
    {#snippet description()}
      {@render githubRepository(m.openid_connect_o_yes_description(), {
        title: 'heviat/Mailu-OIDC',
        href: 'https://github.com/heviat/Mailu-OIDC'
      })}
    {/snippet}
  </Setup.Item>

  <Setup.Item value="ghcr.io/mailu" title={m.openid_connect_o_no_title()}>
    {#snippet description()}
      {@render githubRepository(m.openid_connect_o_no_description(), {
        title: 'Mailu/Mailu',
        href: 'https://github.com/mailu/Mailu'
      })}
    {/snippet}
  </Setup.Item>

  {#snippet hint()}
    <p>
      {@render inlineCode(m.openid_connect_hint({ dockerOrg: dockerOrg.current! }))}
    </p>
  {/snippet}
</Setup.Root>
