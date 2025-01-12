<script lang="ts" module>
  import type { Snippet } from 'svelte';
  import type { SetupContext } from './setup.svelte';

  type SetupItemProps<T> = {
    type?: 'radio' | 'checkbox' | 'list' | 'none';
    value?: T;
    title?: string | Snippet;
    description?: string | Snippet;
    moreInfo?: string | Snippet;
    children?: Snippet;
  };

  export type ItemContext<T> = {
    readonly title?: string | Snippet;
    readonly moreInfo?: string | Snippet;
    readonly type?: 'radio' | 'checkbox' | 'list' | 'none';
    value?: T;
  };
</script>

<script lang="ts" generics="T">
  import { getContext, untrack, setContext } from 'svelte';
  import { Label } from '$lib/components/ui/label';
  import { RadioGroupItem } from '$lib/components/ui/radio-group';
  import { Switch } from '$lib/components/ui/switch';

  let {
    title,
    description,
    moreInfo,
    children,
    type,
    value = $bindable()
  }: SetupItemProps<T> = $props();

  const setupContext = getContext<SetupContext<T>>('setup');
  const effectiveType = $derived(type ?? setupContext.type);

  const itemContext = {
    get title() {
      return title;
    },
    get moreInfo() {
      return moreInfo;
    },
    get type() {
      return effectiveType;
    },
    get value() {
      return value;
    },
    set value(v) {
      value = v;
    }
  };

  setContext('item', itemContext);

  $effect(() => {
    untrack(() => setupContext.items.add(itemContext));

    return () => {
      setupContext.items.delete(itemContext);
    };
  });
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

{#snippet itemContent()}
  {#if title || description}
    <header class="space-y-1">
      {@render stringOrSnippet(title, 'h3', 'text-base font-semibold')}
      {@render stringOrSnippet(description, 'p', 'text-balance text-sm text-muted-foreground')}
    </header>
  {/if}
  {@render stringOrSnippet(children, 'section', 'space-y-4')}
{/snippet}

<article class="space-y-4 rounded-md border" class:p-4={type === 'none'}>
  {#if effectiveType === 'radio' || effectiveType === 'checkbox'}
    <Label class="flex items-center justify-between gap-3 p-4">
      {#if effectiveType === 'radio' && typeof value === 'string'}
        <RadioGroupItem {value} />
      {/if}

      <div class="w-full space-y-4">
        {@render itemContent()}
      </div>

      {#if effectiveType === 'checkbox' && typeof value === 'boolean'}
        <Switch bind:checked={value} />
      {/if}
    </Label>
  {:else if effectiveType === 'list'}
    {@render children?.()}
  {:else}
    {@render itemContent()}
  {/if}
</article>
