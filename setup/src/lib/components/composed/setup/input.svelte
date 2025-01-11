<script lang="ts" module>
  import type { Snippet } from 'svelte';

  type InputProps<T> = {
    id?: string;
    type?: 'email' | 'file' | 'number' | 'password' | 'tel' | 'text' | 'url' | 'list';
    value: T;
    title?: string;
    item?: Snippet<[string, number]>;
  };

  function isList(type: string, value: unknown): value is string[] {
    return type === 'list' && Array.isArray(value);
  }
</script>

<script lang="ts" generics="T">
  import type { SetupContext } from './setup.svelte';
  import type { ItemContext } from './item.svelte';

  import { getContext } from 'svelte';
  import { cn } from '$lib/utils';

  import { Button, buttonVariants } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import * as Table from '$lib/components/ui/table';
  import * as Tooltip from '$lib/components/ui/tooltip';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  let { type, id, value = $bindable(), title, item: itemSnippet }: InputProps<T> = $props();

  const setupContext = getContext<SetupContext<T>>('setup');
  const itemContext = getContext<ItemContext<T>>('item');

  const parentType = $derived(itemContext.type ?? setupContext.type);
  const effectiveType = $derived.by(() => {
    if (!type && parentType !== 'list') return 'text';
    return type ?? itemContext.type ?? setupContext.type;
  });

  let editId = $state<number | null>(null);
  let newItemValue = $state('');
</script>

{#if isList(effectiveType, value)}
  {#snippet action(
    ActionIcon: typeof Icon.Icon,
    title: string,
    onclick: () => void,
    disabled?: boolean,
    className?: string
  )}
    <Tooltip.Root>
      <Tooltip.Trigger
        class={cn(buttonVariants({ size: 'icon', variant: 'outline' }), className)}
        {onclick}
        {disabled}
      >
        <ActionIcon />
      </Tooltip.Trigger>
      <Tooltip.Content>
        <p>{title}</p>
      </Tooltip.Content>
    </Tooltip.Root>
  {/snippet}

  <Table.Root>
    <Table.Header>
      <Table.Row>
        <Table.Head>{title}</Table.Head>
        <Table.Head class="w-52 text-right">{m.actions()}</Table.Head>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {#each value as item, itemId}
        <Table.Row>
          <Table.Cell class="py-2">
            {#if editId === itemId}
              <Input type="text" placeholder="mail.example.com" bind:value={value[itemId]} />
            {:else if itemSnippet}
              {@render itemSnippet(item, itemId)}
            {:else}
              {item}
            {/if}
          </Table.Cell>
          <Table.Cell class="py-2 text-right">
            <Tooltip.Provider>
              {@render action(
                Icon.ChevronUp,
                m.move_up(),
                () =>
                  Array.isArray(value) &&
                  ([value[itemId], value[itemId - 1]] = [value[itemId - 1], value[itemId]]),
                editId !== null || itemId === 0 || value.length < 2,
                '-mr-1 rounded-r-none'
              )}
              {@render action(
                Icon.ChevronDown,
                m.move_down(),
                () =>
                  Array.isArray(value) &&
                  ([value[itemId], value[itemId + 1]] = [value[itemId + 1], value[itemId]]),
                editId !== null || itemId === value.length - 1 || value.length < 2,
                '-ml-[1px] rounded-l-none'
              )}
              {#if editId === itemId}
                {@render action(Icon.Save, m.save(), () => (editId = null))}
              {:else}
                {@render action(Icon.PenLine, m.edit(), () => (editId = itemId), editId !== null)}
              {/if}
              {@render action(
                Icon.Trash,
                m.remove(),
                () => Array.isArray(value) && value.splice(itemId, 1),
                editId !== null || value.length < 2
              )}
            </Tooltip.Provider>
          </Table.Cell>
        </Table.Row>
      {/each}
    </Table.Body>
    <Table.Footer>
      <Table.Row>
        <Table.Cell colspan={2} class="px-4 py-3">
          <div class="flex items-center space-x-2">
            <Input type="text" placeholder="mail.example.com" bind:value={newItemValue} />
            <Button
              variant="secondary"
              onclick={() => {
                if (Array.isArray(value)) value.push(newItemValue);
                newItemValue = '';
              }}
              disabled={editId !== null || newItemValue === ''}>{m.add()}</Button
            >
          </div>
        </Table.Cell>
      </Table.Row>
    </Table.Footer>
  </Table.Root>
{:else}
  <div class="flex w-full max-w-sm flex-col gap-1.5">
    {#if title}
      <Label for={id}>
        {title}
      </Label>
    {/if}
    <Input
      {id}
      type={effectiveType}
      {value}
      autocomplete="off"
      oninput={(event) => {
        const newValue = event.currentTarget.value as T;
        if (setupContext?.value === value) {
          setupContext.value = newValue;
        }
        value = newValue;
      }}
    />
  </div>
{/if}
