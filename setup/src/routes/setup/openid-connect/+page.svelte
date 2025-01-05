<script lang="ts">
  import { PersistedState } from 'runed';
  import { cn } from '$lib/utils';

  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { RadioGroup, RadioGroupItem } from '$lib/components/ui/radio-group';
  import { Label } from '$lib/components/ui/label';

  import { Info } from 'lucide-svelte';

  import {
    openid_connect_title,
    openid_connect_description,
    openid_connect_details,
    openid_connect_o_yes_title,
    openid_connect_o_yes_description,
    openid_connect_o_no_title,
    openid_connect_o_no_description,
    openid_connect_hint,
    more_info
  } from '$lib/paraglide/messages';

  const dockerOrg = new PersistedState('dockerOrg', 'ghcr.io/heviat');
</script>

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{openid_connect_title()}</h2>
      <p class="text-muted-foreground">{openid_connect_description()}</p>
    </div>
    <Dialog.Trigger class={cn(buttonVariants({ variant: 'outline' }), 'rounded-full')}>
      <Info />
      {more_info()}
    </Dialog.Trigger>
  </header>

  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title class="text-xl">{more_info()}</Dialog.Title>
      <Dialog.Description class="text-base">{openid_connect_details()}</Dialog.Description>
    </Dialog.Header>
  </Dialog.Content>
</Dialog.Root>

{#snippet githubRepository(text: string, options: { href: string; title: string })}
  {@const [textBefore, textAfter] = text.split('<GithubRepository/>')}
  {textBefore}<a
    href={options.href}
    target="_blank"
    rel="noopener noreferrer"
    class="inline-block rounded-sm text-blue-700 underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-8 focus-visible:outline-black dark:text-blue-400"
    >{options.title}</a
  >{textAfter}
{/snippet}

{#snippet inlineCode(text: string)}
  {@const [textBefore, code, textAfter] = text.split('`')}
  {textBefore}<code class="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm"
    >{code}</code
  >{textAfter}
{/snippet}

<RadioGroup bind:value={dockerOrg.current} class="max-w-2xl">
  <Label for="openid_connect_yes" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="ghcr.io/heviat" id="openid_connect_yes" />
    <div class="w-full">
      <strong class="text-base font-semibold">{openid_connect_o_yes_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render githubRepository(openid_connect_o_yes_description(), {
          title: 'heviat/Mailu-OIDC',
          href: 'https://github.com/heviat/Mailu-OIDC'
        })}
      </p>
    </div>
  </Label>
  <Label for="openid_connect_no" class="flex items-center space-x-4 rounded-md border p-4">
    <RadioGroupItem value="ghcr.io/mailu" id="openid_connect_no" />
    <div class="w-full">
      <strong class="text-base font-semibold">{openid_connect_o_no_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render githubRepository(openid_connect_o_no_description(), {
          title: 'mailu/Mailu',
          href: 'https://github.com/mailu/Mailu'
        })}
      </p>
    </div>
  </Label>
</RadioGroup>

<p class="text-muted-foreground">
  {@render inlineCode(openid_connect_hint({ dockerOrg: dockerOrg.current }))}
</p>
