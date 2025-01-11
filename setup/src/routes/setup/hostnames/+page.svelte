<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { inlineCode } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const domain = new LocalStorage('domain', '');
  const hostnames = new LocalStorage('hostnames', [domain.current!]);
</script>

<Setup.Root type="list" title={m.hostnames_title()} description={m.hostnames_description()}>
  {#snippet moreInfo()}
    <div class="space-y-4 text-muted-foreground">
      <p>{m.hostnames_details_description()}</p>
      <p>{@render inlineCode(m.hostnames_details_guidelines({ domain: domain.current! }))}</p>
      <p>{@render inlineCode(m.hostnames_details_dns_records())}</p>
    </div>
  {/snippet}

  <Setup.Item>
    <Setup.Input bind:value={hostnames.current} title={m.hostnames_o_hostnames_title()}>
      {#snippet item(hostname)}
        {@render inlineCode(`\`${hostname}\``)}
      {/snippet}
    </Setup.Input>
  </Setup.Item>

  {#snippet hint()}
    <p>
      {@render inlineCode(m.hostnames_hint({ hostnames: hostnames.current!.join(',') }))}
    </p>
  {/snippet}
</Setup.Root>
