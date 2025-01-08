<script lang="ts">
  import { cn } from '$lib/utils';
  import { PersistedState } from 'runed';

  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';

  import { inlineCode } from '$lib/components/formatters.svelte';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  const domain = new PersistedState('domain', '');
  const postmaster = new PersistedState('postmaster', 'admin');
</script>

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{m.postmaster_title()}</h2>
      <p class="text-muted-foreground">{m.postmaster_description()}</p>
    </div>
    <Dialog.Trigger class={cn(buttonVariants({ variant: 'outline' }), 'rounded-full')}>
      <Icon.Info />
      {m.more_info()}
    </Dialog.Trigger>
  </header>

  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title class="text-xl">{m.more_info()}</Dialog.Title>
    </Dialog.Header>
    <dl
      class="[&>dd:not(:last-child)]:mb-4 [&>dd]:text-muted-foreground [&>dt]:mb-1 [&>dt]:font-semibold"
    >
      <dt>{m.postmaster_o_domain_title()}</dt>
      <dd>
        {m.postmaster_details_domain()}
      </dd>
      <dt>{m.postmaster_o_postmaster_title()}</dt>
      <dd>
        {m.postmaster_details_postmaster()}
      </dd>
    </dl>
  </Dialog.Content>
</Dialog.Root>

<div class="grid max-w-2xl gap-2">
  <div class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.postmaster_o_domain_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {m.postmaster_o_domain_description()}
      </p>
      <section class="py-4">
        <div class="flex w-full max-w-sm flex-col gap-1.5">
          <Label for="postmaster_domain">
            {m.postmaster_o_domain_title()}
          </Label>
          <Input id="postmaster_domain" bind:value={domain.current} autocomplete="off" />
        </div>
      </section>
    </div>
  </div>
  <div class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.postmaster_o_postmaster_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {m.postmaster_o_postmaster_description()}
      </p>
      <section class="py-4">
        <div class="flex w-full max-w-sm flex-col gap-1.5">
          <Label for="postmaster_domain">
            {m.postmaster_o_postmaster_title()}
          </Label>
          <Input id="postmaster_domain" bind:value={postmaster.current} autocomplete="off" />
        </div>
      </section>
    </div>
  </div>
</div>

<section class="space-y-2 text-muted-foreground">
  <p>
    {@render inlineCode(
      m.postmaster_hint({
        postmaster: postmaster.current,
        domain: domain.current,
        n: /^([aeiou])/.test(postmaster.current) ? 'n' : ''
      })
    )}
  </p>
</section>
