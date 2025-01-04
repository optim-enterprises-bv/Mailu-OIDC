<script lang="ts">
  import * as DropdownMenu from '$lib/components/ui/dropdown-menu';
  import * as Sidebar from '$lib/components/ui/sidebar';
  import { useSidebar } from '$lib/components/ui/sidebar';

  import ThemeSelector from './selector-theme.svelte';
  import LanguageSelector from './selector-language.svelte';

  import { ChevronsUpDown, Settings2 } from 'lucide-svelte';

  import {
    display_preferences_title,
    display_preferences_description
  } from '$lib/paraglide/messages';

  const sidebar = useSidebar();
</script>

{#snippet profile()}
  <div
    class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground"
  >
    <Settings2 class="size-4" />
  </div>
  <div class="grid flex-1 text-left text-sm leading-tight">
    <span class="truncate font-semibold">{display_preferences_title()}</span>
    <span class="truncate text-xs">{display_preferences_description()}</span>
  </div>
{/snippet}

<Sidebar.Menu>
  <Sidebar.MenuItem>
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        {#snippet child({ props })}
          <Sidebar.MenuButton
            {...props}
            size="lg"
            class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
          >
            {@render profile()}
            <ChevronsUpDown class="ml-auto size-4" />
          </Sidebar.MenuButton>
        {/snippet}
      </DropdownMenu.Trigger>
      <DropdownMenu.Content
        class="w-[--bits-dropdown-menu-anchor-width] min-w-56 rounded-lg"
        side={sidebar.isMobile ? 'bottom' : 'right'}
        align="end"
        sideOffset={4}
      >
        <DropdownMenu.Label class="p-0 font-normal">
          <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
            {@render profile()}
          </div>
        </DropdownMenu.Label>
        <DropdownMenu.Separator />
        <DropdownMenu.Group>
          <ThemeSelector />
          <LanguageSelector />
        </DropdownMenu.Group>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  </Sidebar.MenuItem>
</Sidebar.Menu>
