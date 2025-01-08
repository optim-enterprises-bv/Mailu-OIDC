<script lang="ts">
  import { cn } from '$lib/utils';
  import { PersistedState } from 'runed';

  import { Badge } from '$lib/components/ui/badge';
  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Label } from '$lib/components/ui/label';
  import { Switch } from '$lib/components/ui/switch';

  import { link } from '$lib/components/formatters.svelte';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  const antivirus = new PersistedState('antivirus', false);
  const webdav = new PersistedState('webdav', false);
  const fetchmail = new PersistedState('fetchmail', false);
  const oletools = new PersistedState('oletools', true);
  const tika = new PersistedState('tika', false);
</script>

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{m.optional_services_title()}</h2>
      <p class="text-muted-foreground">{m.optional_services_description()}</p>
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
      <dt>{m.optional_services_o_antivirus_title()}</dt>
      <dd>
        {m.optional_services_details_antivirus()}
      </dd>
      <dt>{m.optional_services_o_webdav_title()}</dt>
      <dd>
        {m.optional_services_details_webdav()}
      </dd>
      <dt>{m.optional_services_o_fetchmail_title()}</dt>
      <dd>
        {m.optional_services_details_fetchmail()}
      </dd>
      <dt>{m.optional_services_o_oletools_title()}</dt>
      <dd>
        {m.optional_services_details_oletools()}
      </dd>
      <dt>{m.optional_services_o_tika_title()}</dt>
      <dd>
        {m.optional_services_details_tika()}
      </dd>
    </dl>
  </Dialog.Content>
</Dialog.Root>

<div class="grid max-w-2xl gap-2">
  <Label for="antivirus" class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.optional_services_o_antivirus_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render link(
          m.optional_services_o_antivirus_description({
            productLink: `[ClamAV](https://www.clamav.net)`
          })
        )}
      </p>
    </div>
    <Switch id="antivirus" bind:checked={antivirus.current} />
  </Label>
  <Label for="webdav" class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.optional_services_o_webdav_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render link(
          m.optional_services_o_webdav_description({
            productLink: `[Radicale](https://radicale.org/v3.html)`
          })
        )}
      </p>
    </div>
    <Switch id="webdav" bind:checked={webdav.current} />
  </Label>
  <Label for="fetchmail" class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.optional_services_o_fetchmail_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render link(
          m.optional_services_o_fetchmail_description({
            productLink: `[Fetchmail](https://www.fetchmail.info)`
          })
        )}
      </p>
    </div>
    <Switch id="fetchmail" bind:checked={fetchmail.current} />
  </Label>
  <Label for="oletools" class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.optional_services_o_oletools_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render link(
          m.optional_services_o_oletools_description({
            productLink: `[Oletools](https://rspamd.com/doc/modules/external_services.html#oletools-specific-details)`
          })
        )}
      </p>
    </div>
    <Switch id="oletools" bind:checked={oletools.current} />
  </Label>
  <Label for="tika" class="flex items-center justify-between gap-2 rounded-md border p-4">
    <div class="w-full">
      <strong class="text-base font-semibold">{m.optional_services_o_tika_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render link(
          m.optional_services_o_tika_description({
            productLink: `[Tika](https://tika.apache.org)`
          })
        )}
      </p>
    </div>
    <Switch id="tika" bind:checked={tika.current} />
  </Label>
</div>

<section class="space-y-2 text-muted-foreground">
  {#if antivirus.current || tika.current}
    {#if antivirus.current && tika.current}
      <Badge class="bg-red-500 hover:bg-red-500 ">{m.caution()}</Badge>
      {m.optional_services_hint_antivirus_and_tika()}
    {:else if antivirus.current}
      <Badge class="bg-amber-500 hover:bg-amber-500 ">{m.warning()}</Badge>
      {m.optional_services_hint_antivirus()}
    {:else if tika.current}
      <Badge class="bg-amber-500 hover:bg-amber-500 ">{m.warning()}</Badge>
      {m.optional_services_hint_tika()}
    {/if}
  {:else if !antivirus.current && !tika.current && !webdav.current && !fetchmail.current}
    {#if oletools.current}
      {m.optional_services_hint_defaults()}
    {:else}
      {m.optional_services_hint_none()}
    {/if}
  {/if}
</section>
