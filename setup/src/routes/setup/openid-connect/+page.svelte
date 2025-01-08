<script lang="ts">
  import { PersistedState } from 'runed';
  import { cn } from '$lib/utils';

  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { RadioGroup, RadioGroupItem } from '$lib/components/ui/radio-group';
  import { Label } from '$lib/components/ui/label';

  import { githubRepository, inlineCode } from '$lib/components/formatters.svelte';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  const dockerOrg = new PersistedState('dockerOrg', 'ghcr.io/heviat');
</script>

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{m.openid_connect_title()}</h2>
      <p class="text-muted-foreground">{m.openid_connect_description()}</p>
    </div>
    <Dialog.Trigger class={cn(buttonVariants({ variant: 'outline' }), 'rounded-full')}>
      <Icon.Info />
      {m.more_info()}
    </Dialog.Trigger>
  </header>

  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title class="text-xl">{m.more_info()}</Dialog.Title>
      <Dialog.Description class="text-base">{m.openid_connect_details()}</Dialog.Description>
    </Dialog.Header>
  </Dialog.Content>
</Dialog.Root>

<RadioGroup bind:value={dockerOrg.current} class="max-w-2xl">
  <Label for="openid_connect_yes" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="ghcr.io/heviat" id="openid_connect_yes" />
    <div class="w-full">
      <strong class="text-base font-semibold">{m.openid_connect_o_yes_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render githubRepository(m.openid_connect_o_yes_description(), {
          title: 'heviat/Mailu-OIDC',
          href: 'https://github.com/heviat/Mailu-OIDC'
        })}
      </p>
    </div>
  </Label>
  <Label for="openid_connect_no" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="ghcr.io/mailu" id="openid_connect_no" />
    <div class="w-full">
      <strong class="text-base font-semibold">{m.openid_connect_o_no_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render githubRepository(m.openid_connect_o_no_description(), {
          title: 'Mailu/Mailu',
          href: 'https://github.com/mailu/Mailu'
        })}
      </p>
    </div>
  </Label>
</RadioGroup>

<p class="text-muted-foreground">
  {@render inlineCode(m.openid_connect_hint({ dockerOrg: dockerOrg.current }))}
</p>
