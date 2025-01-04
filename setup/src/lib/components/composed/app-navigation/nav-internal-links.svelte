<script lang="ts" module>
  type NavInternalLinksProps = {
    items: NavItem[];
  };
</script>

<script lang="ts">
  import type { ComponentProps } from 'svelte';
  import type { NavItem } from '.';

  import * as Collapsible from '$lib/components/ui/collapsible';
  import * as Sidebar from '$lib/components/ui/sidebar';

  import ChevronRight from 'lucide-svelte/icons/chevron-right';

  let {
    ref = $bindable(null),
    items,
    ...restProps
  }: ComponentProps<typeof Sidebar.Group> & NavInternalLinksProps = $props();
</script>

<Sidebar.Group bind:ref {...restProps}>
  <Sidebar.Menu>
    {#each items as item (item.title)}
      <Collapsible.Root open={item.isActive}>
        {#snippet child({ props })}
          <Sidebar.MenuItem {...props}>
            <Sidebar.MenuButton isActive={item.isActive}>
              {#snippet tooltipContent()}
                {item.title}
              {/snippet}
              {#snippet child({ props })}
                <a href={item.url} {...props}>
                  <item.icon />
                  <span>{item.title}</span>
                </a>
              {/snippet}
            </Sidebar.MenuButton>
            {#if item.items?.length}
              <Collapsible.Trigger>
                {#snippet child({ props })}
                  <Sidebar.MenuAction {...props} class="data-[state=open]:rotate-90">
                    <ChevronRight />
                    <span class="sr-only">Toggle</span>
                  </Sidebar.MenuAction>
                {/snippet}
              </Collapsible.Trigger>
              <Collapsible.Content>
                <Sidebar.MenuSub>
                  {#each item.items as subItem (subItem.title)}
                    <Sidebar.MenuSubItem>
                      <Sidebar.MenuSubButton href={subItem.url} isActive={subItem.isActive}>
                        <span>{subItem.title}</span>
                      </Sidebar.MenuSubButton>
                    </Sidebar.MenuSubItem>
                  {/each}
                </Sidebar.MenuSub>
              </Collapsible.Content>
            {/if}
          </Sidebar.MenuItem>
        {/snippet}
      </Collapsible.Root>
    {/each}
  </Sidebar.Menu>
</Sidebar.Group>
