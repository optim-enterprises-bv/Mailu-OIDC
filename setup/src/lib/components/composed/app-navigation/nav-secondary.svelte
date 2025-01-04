<script lang="ts" module>
  type NavSecondaryProps = {
    items: NavItem[];
  };
</script>

<script lang="ts">
  import type { ComponentProps } from 'svelte';
  import type { NavItem } from '.';

  import * as Sidebar from '$lib/components/ui/sidebar';

  let {
    ref = $bindable(null),
    items,
    ...restProps
  }: ComponentProps<typeof Sidebar.Group> & NavSecondaryProps = $props();
</script>

<Sidebar.Group bind:ref {...restProps}>
  <Sidebar.GroupContent>
    <Sidebar.Menu>
      {#each items as item (item.title)}
        <Sidebar.MenuItem>
          <Sidebar.MenuButton size="sm">
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
        </Sidebar.MenuItem>
      {/each}
    </Sidebar.Menu>
  </Sidebar.GroupContent>
</Sidebar.Group>
