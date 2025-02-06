<script lang="ts">
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import * as Setup from '$lib/components/composed/setup';

  import * as m from '$lib/paraglide/messages';

  const rateLimitDefaults = {
    authIP: 5,
    authUser: 50,
    message: 200
  };

  const rateLimit = new LocalStorage<'defaults' | 'custom'>('rateLimit', 'defaults');
  const rateLimitCustom = new LocalStorage('rateLimit__custom', { ...rateLimitDefaults });

  const rateLimitValues = $derived(
    rateLimit.current === 'defaults' ? rateLimitDefaults : rateLimitCustom.current!
  );
</script>

<Setup.Root
  type="radio"
  bind:value={rateLimit.current}
  title={m.rate_limiting_title()}
  description={m.rate_limiting_description()}
>
  {#snippet moreInfo()}
    <p>{m.rate_limiting_details()}</p>
  {/snippet}

  <Setup.Item
    type="radio"
    value="defaults"
    title={m.rate_limiting_o_defaults_title()}
    description={m.rate_limiting_o_defaults_description()}
  />

  <Setup.Item
    type="radio"
    value="custom"
    title={m.rate_limiting_o_custom_title()}
    description={m.rate_limiting_o_custom_description()}
  >
    {#if rateLimit.current === 'custom'}
      <Setup.Input
        type="number"
        bind:value={rateLimitCustom.current!.authIP}
        title={m.rate_limiting_o_custom_authIP()}
      />
      <Setup.Input
        type="number"
        bind:value={rateLimitCustom.current!.authUser}
        title={m.rate_limiting_o_custom_authUser()}
      />
      <Setup.Input
        type="number"
        bind:value={rateLimitCustom.current!.message}
        title={m.rate_limiting_o_custom_message()}
      />
    {/if}
  </Setup.Item>

  {#snippet hint()}
    <p>
      {m.rate_limiting_hint_values()}
    </p>
    <dl class="grid w-max max-w-full grid-cols-[auto_1fr] gap-x-4 gap-y-1 ps-6 [&>dt]:font-medium">
      <dt>{m.rate_limiting_hint_authIP_title()}</dt>
      <dd>
        {m.rate_limiting_hint_authIP_description({ authIP: rateLimitValues.authIP })}
      </dd>
      <dt>{m.rate_limiting_hint_authUser_title()}</dt>
      <dd>
        {m.rate_limiting_hint_authUser_description({ authUser: rateLimitValues.authUser })}
      </dd>
      <dt>{m.rate_limiting_hint_message_title()}</dt>
      <dd>
        {m.rate_limiting_hint_message_description({ message: rateLimitValues.message })}
      </dd>
    </dl>
  {/snippet}
</Setup.Root>
