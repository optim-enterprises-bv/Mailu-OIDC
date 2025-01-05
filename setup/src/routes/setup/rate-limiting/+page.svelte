<script lang="ts">
  import { cn } from '$lib/utils';
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { RadioGroup, RadioGroupItem } from '$lib/components/ui/radio-group';

  import { Info } from 'lucide-svelte';

  import {
    more_info,
    rate_limiting_description,
    rate_limiting_details,
    rate_limiting_hint_authIP_description,
    rate_limiting_hint_authIP_title,
    rate_limiting_hint_authUser_description,
    rate_limiting_hint_authUser_title,
    rate_limiting_hint_message_description,
    rate_limiting_hint_message_title,
    rate_limiting_hint_values,
    rate_limiting_o_custom_authIP,
    rate_limiting_o_custom_authUser,
    rate_limiting_o_custom_description,
    rate_limiting_o_custom_message,
    rate_limiting_o_custom_title,
    rate_limiting_o_defaults_description,
    rate_limiting_o_defaults_title,
    rate_limiting_title
  } from '$lib/paraglide/messages';

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

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{rate_limiting_title()}</h2>
      <p class="text-muted-foreground">{rate_limiting_description()}</p>
    </div>
    <Dialog.Trigger class={cn(buttonVariants({ variant: 'outline' }), 'rounded-full')}>
      <Info />
      {more_info()}
    </Dialog.Trigger>
  </header>

  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title class="text-xl">{more_info()}</Dialog.Title>
      <Dialog.Description class="text-base">{rate_limiting_details()}</Dialog.Description>
    </Dialog.Header>
  </Dialog.Content>
</Dialog.Root>

<RadioGroup bind:value={rateLimit.current!} class="max-w-2xl">
  <Label for="rate_limiting_defaults" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="defaults" id="rate_limiting_defaults" />
    <div class="w-full">
      <strong class="text-base font-semibold">{rate_limiting_o_defaults_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {rate_limiting_o_defaults_description()}
      </p>
    </div>
  </Label>
  <Label for="rate_limiting_custom" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="custom" id="rate_limiting_custom" />
    <div class="w-full">
      <strong class="text-base font-semibold">{rate_limiting_o_custom_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {rate_limiting_o_custom_description()}
      </p>
      {#if rateLimit.current === 'custom'}
        <section class="space-y-4 py-4">
          <div class="flex w-full max-w-sm flex-col gap-1.5">
            <Label for="rate_limiting_custom_authIP">
              {rate_limiting_o_custom_authIP()}
            </Label>
            <Input
              id="rate_limiting_custom_authIP"
              type="number"
              bind:value={rateLimitCustom.current!.authIP}
            />
          </div>
          <div class="flex w-full max-w-sm flex-col gap-1.5">
            <Label for="rate_limiting_custom_authUser">
              {rate_limiting_o_custom_authUser()}
            </Label>
            <Input
              id="rate_limiting_custom_authUser"
              type="number"
              bind:value={rateLimitCustom.current!.authUser}
            />
          </div>
          <div class="flex w-full max-w-sm flex-col gap-1.5">
            <Label for="rate_limiting_custom_message">
              {rate_limiting_o_custom_message()}
            </Label>
            <Input
              id="rate_limiting_custom_message"
              type="number"
              bind:value={rateLimitCustom.current!.message}
            />
          </div>
        </section>
      {/if}
    </div>
  </Label>
</RadioGroup>

<section class="space-y-2 text-muted-foreground">
  <p>
    {rate_limiting_hint_values()}
  </p>
  <dl class="grid w-max max-w-full grid-cols-[auto,1fr] gap-2 [&>dt]:font-semibold">
    <dt>{rate_limiting_hint_authIP_title()}</dt>
    <dd>
      {rate_limiting_hint_authIP_description({ authIP: rateLimitValues.authIP })}
    </dd>
    <dt>{rate_limiting_hint_authUser_title()}</dt>
    <dd>
      {rate_limiting_hint_authUser_description({ authUser: rateLimitValues.authUser })}
    </dd>
    <dt>{rate_limiting_hint_message_title()}</dt>
    <dd>
      {rate_limiting_hint_message_description({ message: rateLimitValues.message })}
    </dd>
  </dl>
</section>
