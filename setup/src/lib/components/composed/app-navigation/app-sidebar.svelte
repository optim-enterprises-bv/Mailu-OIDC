<!-- @component Sidebar navigation for the application. Displayed on the left side of the page. -->

<script lang="ts" module>
  type SidebarProps = {
    items: Record<string, NavItem[]>;
  };
</script>

<script lang="ts">
  import type { ComponentProps } from 'svelte';
  import type { NavItem } from '.';

  import * as Sidebar from '$lib/components/ui/sidebar/index.js';

  import NavInternalLinks from './nav-internal-links.svelte';
  import NavSecondary from './nav-secondary.svelte';
  import NavUserMenu from './nav-user-menu.svelte';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  let {
    ref = $bindable(null),
    collapsible = 'icon',
    items,
    ...restProps
  }: ComponentProps<typeof Sidebar.Root> & SidebarProps = $props();
</script>

<Sidebar.Root bind:ref {collapsible} {...restProps}>
  <Sidebar.Header>
    <Sidebar.Menu>
      <Sidebar.MenuItem>
        <Sidebar.MenuButton size="lg">
          {#snippet child({ props })}
            <a href="/" {...props}>
              <div
                class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground"
              >
                <Icon.WandSparkles class="size-4" />
              </div>
              <div class="grid flex-1 text-left text-sm leading-tight">
                <span class="truncate font-semibold">{m.mailu_setup_utility_title()}</span>
                <span class="truncate text-xs">by Heviat</span>
              </div>
            </a>
          {/snippet}
        </Sidebar.MenuButton>
      </Sidebar.MenuItem>
    </Sidebar.Menu>
  </Sidebar.Header>
  <Sidebar.Content>
    <NavInternalLinks items={items.main} />
    <NavSecondary items={items.secondary} class="mt-auto" />
  </Sidebar.Content>
  <Sidebar.Footer>
    <NavUserMenu />
  </Sidebar.Footer>
</Sidebar.Root>
