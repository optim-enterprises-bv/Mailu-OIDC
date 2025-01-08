<script lang="ts">
  import { cn } from '$lib/utils';
  import { LocalStorage } from '$lib/hooks/local-storage.svelte';

  import { Button, buttonVariants } from '$lib/components/ui/button';
  import * as Dialog from '$lib/components/ui/dialog';
  import { Input } from '$lib/components/ui/input';
  import * as Table from '$lib/components/ui/table';
  import * as Tooltip from '$lib/components/ui/tooltip';

  import { inlineCode } from '$lib/components/formatters.svelte';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  let editId = $state<number | null>(null);
  let newItemValue = $state('');

  const domain = new LocalStorage('domain', '');
  const hostnames = new LocalStorage('hostnames', [domain.current!]);
</script>

<Dialog.Root>
  <header class="flex max-w-2xl items-center justify-between gap-2">
    <div class="space-y-2">
      <h2 class="text-2xl font-bold">{m.hostnames_title()}</h2>
      <p class="text-muted-foreground">{m.hostnames_description()}</p>
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
    <div class="space-y-4 text-muted-foreground">
      <p>{m.hostnames_details_description()}</p>
      <p>{@render inlineCode(m.hostnames_details_guidelines({ domain: domain.current! }))}</p>
      <p>{@render inlineCode(m.hostnames_details_dns_records())}</p>
    </div>
  </Dialog.Content>
</Dialog.Root>

<div class="grid max-w-2xl gap-2">
  <div class="flex items-center justify-between gap-2 rounded-md border">
    <Table.Root>
      <Table.Header>
        <Table.Row>
          <Table.Head>{m.hostnames_title()}</Table.Head>
          <Table.Head class="w-52 text-right">{m.actions()}</Table.Head>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {#each hostnames.current! as item, itemId}
          <Table.Row>
            <Table.Cell class="py-2">
              {#if editId === itemId}
                <Input
                  type="text"
                  placeholder="mail.example.com"
                  bind:value={hostnames.current![itemId]}
                />
              {:else}
                {@render inlineCode(`\`${item}\``)}
              {/if}
            </Table.Cell>
            <Table.Cell class="py-2 text-right">
              <Tooltip.Provider>
                <Tooltip.Root>
                  <Tooltip.Trigger
                    class={cn(
                      buttonVariants({ size: 'icon', variant: 'outline' }),
                      '-mr-1 rounded-r-none'
                    )}
                    onclick={() => {
                      [hostnames.current![itemId], hostnames.current![itemId - 1]] = [
                        hostnames.current![itemId - 1],
                        hostnames.current![itemId]
                      ];
                    }}
                    disabled={editId !== null || itemId === 0 || hostnames.current!.length < 2}
                  >
                    <Icon.ChevronUp />
                  </Tooltip.Trigger>
                  <Tooltip.Content>
                    <p>{m.move_up()}</p>
                  </Tooltip.Content>
                </Tooltip.Root>
                <Tooltip.Root>
                  <Tooltip.Trigger
                    class={cn(
                      buttonVariants({ size: 'icon', variant: 'outline' }),
                      '-ml-[1px] rounded-l-none'
                    )}
                    onclick={() => {
                      [hostnames.current![itemId], hostnames.current![itemId + 1]] = [
                        hostnames.current![itemId + 1],
                        hostnames.current![itemId]
                      ];
                    }}
                    disabled={editId !== null ||
                      itemId === hostnames.current!.length - 1 ||
                      hostnames.current!.length < 2}
                  >
                    <Icon.ChevronDown />
                  </Tooltip.Trigger>
                  <Tooltip.Content>
                    <p>{m.move_down()}</p>
                  </Tooltip.Content>
                </Tooltip.Root>
                <Tooltip.Root>
                  {#if editId === itemId}
                    <Tooltip.Trigger
                      class={buttonVariants({ size: 'icon', variant: 'outline' })}
                      onclick={() => {
                        editId = null;
                      }}
                    >
                      <Icon.Save />
                    </Tooltip.Trigger>
                    <Tooltip.Content>
                      <p>{m.save()}</p>
                    </Tooltip.Content>
                  {:else}
                    <Tooltip.Trigger
                      class={buttonVariants({ size: 'icon', variant: 'outline' })}
                      onclick={() => {
                        editId = itemId;
                      }}
                      disabled={editId !== null}
                    >
                      <Icon.PenLine />
                    </Tooltip.Trigger>
                    <Tooltip.Content>
                      <p>{m.edit()}</p>
                    </Tooltip.Content>
                  {/if}
                </Tooltip.Root>
                <Tooltip.Root>
                  <Tooltip.Trigger
                    class={buttonVariants({ size: 'icon', variant: 'outline' })}
                    onclick={() => {
                      hostnames.current!.splice(itemId, 1);
                    }}
                    disabled={editId !== null || hostnames.current!.length < 2}
                  >
                    <Icon.Trash />
                  </Tooltip.Trigger>
                  <Tooltip.Content>
                    <p>{m.remove()}</p>
                  </Tooltip.Content>
                </Tooltip.Root>
              </Tooltip.Provider>
            </Table.Cell>
          </Table.Row>
        {/each}
      </Table.Body>
      <Table.Footer>
        <Table.Row>
          <Table.Cell colspan={2} class="py-2">
            <div class="flex items-center space-x-2">
              <Input type="text" placeholder="mail.example.com" bind:value={newItemValue} />
              <Button
                variant="secondary"
                onclick={() => {
                  hostnames.current!.push(newItemValue);
                  newItemValue = '';
                }}
                disabled={editId !== null || newItemValue === ''}>{m.add()}</Button
              >
            </div>
          </Table.Cell>
        </Table.Row>
      </Table.Footer>
    </Table.Root>
  </div>
</div>

<section class="space-y-2 text-muted-foreground">
  <p>
    {@render inlineCode(m.hostnames_hint({ hostnames: hostnames.current!.join(',') }))}
  </p>
</section>
