<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { bold, inlineCode, link } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const rootDefault = '/mailu';
  const root = new LocalStorage('root', rootDefault);
  const tlsFlavor = new LocalStorage<'letsencrypt' | 'cert' | 'notls'>('tlsFlavor', 'letsencrypt');
</script>

<Setup.Root
  type="radio"
  bind:value={tlsFlavor.current}
  title={m.tls_flavor_title()}
  description={m.tls_flavor_description()}
>
  {#snippet moreInfo()}
    <p>{m.tls_flavor_details()}</p>
  {/snippet}

  <Setup.Item value="letsencrypt" title={m.tls_flavor_o_letsencrypt_title()}>
    {#snippet description()}
      {@render link(
        m.tls_flavor_o_letsencrypt_description({
          productLink: `[Let's Encrypt](https://letsencrypt.org/)`
        })
      )}
    {/snippet}
  </Setup.Item>

  <Setup.Item
    value="cert"
    title={m.tls_flavor_o_cert_title()}
    description={m.tls_flavor_o_cert_description()}
  />

  <Setup.Item value="notls" title={m.tls_flavor_o_notls_title()}>
    {#snippet description()}
      {@render bold(m.tls_flavor_o_notls_description())}
    {/snippet}
  </Setup.Item>

  {#snippet hint()}
    {#if tlsFlavor.current === 'letsencrypt'}
      <p>{m.tls_flavor_hint_letsencrypt()}</p>
    {:else if tlsFlavor.current === 'cert'}
      <p>
        {m.tls_flavor_hint_cert_you_have_to_setup()}<br />
        {@render inlineCode(
          m.tls_flavor_hint_cert_filenames({
            certFile: `${root.current ?? rootDefault}/certs/cert.pem`,
            keyFile: `${root.current ?? rootDefault}/certs/key.pem`
          })
        )}
      </p>
      <p>
        {@render inlineCode(
          m.tls_flavor_hint_cert_change_paths_in_env({
            configFile: 'mailu.env',
            certVariable: 'TLS_CERT_FILENAME',
            keyVariable: 'TLS_KEYPAIR_FILENAME'
          })
        )}
      </p>
    {:else}
      <p>{m.tls_flavor_hint_notls_disabled()}</p>
      <Setup.Alert variant="caution" children={m.tls_flavor_hint_notls_use_reverse_proxy()} />
    {/if}
  {/snippet}
</Setup.Root>
