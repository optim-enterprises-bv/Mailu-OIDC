<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import { inlineCode } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const enableStats = new LocalStorage<'yes' | 'no'>('enableStats', 'no');
</script>

<Setup.Root
  type="radio"
  bind:value={enableStats.current}
  title={m.enable_stats_title()}
  description={m.enable_stats_description()}
>
  {#snippet moreInfo()}
    <p>
      {@render inlineCode(
        m.enable_stats_details({
          statsEndpointVariable: 'STATS_ENDPOINT'
        })
      )}
    </p>
  {/snippet}

  <Setup.Item
    value="yes"
    title={m.enable_stats_o_yes_title()}
    description={m.enable_stats_o_yes_description()}
  />

  <Setup.Item
    value="no"
    title={m.enable_stats_o_no_title()}
    description={m.enable_stats_o_no_description()}
  />

  {#snippet hint()}
    {#if enableStats.current === 'yes'}
      <p>{m.enable_stats_hint_yes_stats_enabled()}</p>
      <p>
        {@render inlineCode(
          m.enable_stats_hint_yes_opt_out_in_env({
            configFile: 'mailu.env',
            disableStatsVariable: 'DISABLE_STATS'
          })
        )}
      </p>
    {:else}
      <p>{m.enable_stats_hint_no()}</p>
    {/if}
  {/snippet}
</Setup.Root>
