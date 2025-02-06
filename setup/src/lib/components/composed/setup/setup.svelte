<script lang="ts" module>
  import type { Snippet } from 'svelte';
  import type { ItemContext } from './item.svelte';

  type SetupProps<T> = {
    type?: 'radio' | 'checkbox' | 'list' | 'none';
    value?: T;
    title?: string | Snippet;
    description?: string | Snippet;
    moreInfoDescription?: string;
    moreInfo?: Snippet;
    children?: Snippet;
    hint?: Snippet;
  };

  export type SetupContext<T> = {
    readonly type: 'radio' | 'checkbox' | 'list' | 'none';
    readonly items: SvelteSet<ItemContext<T>>;
    value?: T;
  };
</script>

<script lang="ts" generics="T">
  import { setContext } from 'svelte';
  import { cn } from '$lib/utils';

  import { buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { RadioGroup } from '$lib/components/ui/radio-group';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';
  import { SvelteSet } from 'svelte/reactivity';

  let {
    type = 'none',
    value = $bindable(),
    title,
    description,
    moreInfoDescription,
    children,
    moreInfo,
    hint
  }: SetupProps<T> = $props();

  let itemProps = new SvelteSet<ItemContext<T>>();

  setContext('setup', {
    get type() {
      return type;
    },
    get items() {
      return itemProps;
    },
    get value() {
      return value;
    },
    set value(v) {
      value = v;
    }
  });

  const itemsHaveMoreInfo = $derived(itemProps.values().some(({ moreInfo }) => !!moreInfo));
  const hasMoreInfo = $derived(!!moreInfoDescription || !!moreInfo || itemsHaveMoreInfo);
</script>

{#snippet stringOrSnippet(
  value: string | Snippet | undefined,
  wrapper: keyof HTMLElementTagNameMap,
  wrapperClass: string
)}
  {#if value}
    <svelte:element this={wrapper} class={wrapperClass}>
      {#if typeof value === 'string'}
        {value}
      {:else}
        {@render value()}
      {/if}
    </svelte:element>
  {/if}
{/snippet}

{#snippet moreInfoButtonAndDialog()}
  <Dialog.Root>
    <Dialog.Trigger class={cn(buttonVariants({ variant: 'outline' }), 'rounded-full')}>
      <Icon.Info />
      {m.more_info()}
    </Dialog.Trigger>

    <Dialog.Content>
      <Dialog.Header>
        <Dialog.Title class="text-xl">{m.more_info()}</Dialog.Title>
        {#if moreInfoDescription}
          <Dialog.Description>{moreInfoDescription}</Dialog.Description>
        {/if}
      </Dialog.Header>

      {@render moreInfo?.()}

      {#if itemsHaveMoreInfo}
        <dl>
          {#each itemProps.values() as { title, moreInfo }}
            {#if title && moreInfo}
              {@render stringOrSnippet(title, 'dt', 'mb-1 font-semibold')}
              {@render stringOrSnippet(
                moreInfo,
                'dd',
                'not-last:mb-4 text-muted-foreground'
              )}
            {/if}
          {/each}
        </dl>
      {/if}
    </Dialog.Content>
  </Dialog.Root>
{/snippet}

<article class="max-w-2xl space-y-4">
  <header class="flex items-center justify-between gap-2">
    <div class="space-y-2">
      {@render stringOrSnippet(title, 'h2', 'text-2xl font-bold')}
      {@render stringOrSnippet(description, 'p', 'text-muted-foreground')}
    </div>
    {#if hasMoreInfo}
      {@render moreInfoButtonAndDialog()}
    {/if}
  </header>

  <section class="space-y-2">
    {#if type === 'radio' && typeof value === 'string'}
      <RadioGroup bind:value child={children} />
    {:else}
      {@render children?.()}
    {/if}
  </section>

  {#if hint}
    <footer class="space-y-2 text-muted-foreground">{@render hint()}</footer>
  {/if}
</article>
