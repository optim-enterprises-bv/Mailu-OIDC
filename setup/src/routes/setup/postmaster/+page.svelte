<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { inlineCode } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const domain = new LocalStorage('domain', '');
  const postmaster = new LocalStorage('postmaster', 'admin');
</script>

<Setup.Root title={m.postmaster_title()} description={m.postmaster_description()}>
  <Setup.Item
    title={m.postmaster_o_domain_title()}
    description={m.postmaster_o_domain_description()}
    moreInfo={m.postmaster_details_domain()}
  >
    <Setup.Input bind:value={domain.current} />
  </Setup.Item>

  <Setup.Item
    title={m.postmaster_o_postmaster_title()}
    description={m.postmaster_o_postmaster_description()}
    moreInfo={m.postmaster_details_postmaster()}
  >
    <Setup.Input bind:value={postmaster.current} />
  </Setup.Item>

  {#snippet hint()}
    <p>
      {@render inlineCode(
        m.postmaster_hint({
          postmaster: postmaster.current ?? '',
          domain: domain.current ?? '',
          n: /^([aeiou])/.test(postmaster.current ?? '') ? 'n' : ''
        })
      )}
    </p>
  {/snippet}
</Setup.Root>
