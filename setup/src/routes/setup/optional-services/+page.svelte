<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { link } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const antivirus = new LocalStorage('antivirus', false);
  const webdav = new LocalStorage('webdav', false);
  const fetchmail = new LocalStorage('fetchmail', false);
  const oletools = new LocalStorage('oletools', true);
  const tika = new LocalStorage('tika', false);
</script>

<Setup.Root
  type="checkbox"
  title={m.optional_services_title()}
  description={m.optional_services_description()}
>
  <Setup.Item
    bind:value={antivirus.current}
    title={m.optional_services_o_antivirus_title()}
    moreInfo={m.optional_services_details_antivirus()}
  >
    {#snippet description()}
      {@render link(
        m.optional_services_o_antivirus_description({
          productLink: `[ClamAV](https://www.clamav.net)`
        })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    bind:value={webdav.current}
    title={m.optional_services_o_webdav_title()}
    moreInfo={m.optional_services_details_webdav()}
  >
    {#snippet description()}
      {@render link(
        m.optional_services_o_webdav_description({
          productLink: `[WebDAV](https://en.wikipedia.org/wiki/WebDAV)`
        })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    bind:value={fetchmail.current}
    title={m.optional_services_o_fetchmail_title()}
    moreInfo={m.optional_services_details_fetchmail()}
  >
    {#snippet description()}
      {@render link(
        m.optional_services_o_fetchmail_description({
          productLink: `[Fetchmail](https://fetchmail.info)`
        })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    bind:value={oletools.current}
    title={m.optional_services_o_oletools_title()}
    moreInfo={m.optional_services_details_oletools()}
  >
    {#snippet description()}
      {@render link(
        m.optional_services_o_oletools_description({
          productLink: `[OleTools](https://oletools.com)`
        })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    bind:value={tika.current}
    title={m.optional_services_o_tika_title()}
    moreInfo={m.optional_services_details_tika()}
  >
    {#snippet description()}
      {@render link(
        m.optional_services_o_tika_description({
          productLink: `[Tika](https://tika.apache.org)`
        })
      )}
    {/snippet}
  </Setup.Item>

  {#snippet hint()}
    {#if antivirus.current || tika.current}
      <Setup.Alert variant={antivirus.current && tika.current ? 'caution' : 'warning'}>
        {#if antivirus.current && tika.current}
          {m.optional_services_hint_antivirus_and_tika()}
        {:else if antivirus.current}
          {m.optional_services_hint_antivirus()}
        {:else if tika.current}
          {m.optional_services_hint_tika()}
        {/if}
      </Setup.Alert>
    {:else if !antivirus.current && !tika.current && !webdav.current && !fetchmail.current}
      {#if oletools.current}
        {m.optional_services_hint_defaults()}
      {:else}
        {m.optional_services_hint_none()}
      {/if}
    {/if}
  {/snippet}
</Setup.Root>
