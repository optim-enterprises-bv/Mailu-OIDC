<script lang="ts">
  import { userPrefersMode, resetMode, setMode } from 'mode-watcher';

  import * as DropdownMenu from '$lib/components/ui/dropdown-menu';

  import { Sun, Moon, Monitor } from 'lucide-svelte';

  import { dark_theme, light_theme, system_theme, toggle_theme } from '$lib/paraglide/messages';
</script>

<DropdownMenu.Sub>
  <DropdownMenu.SubTrigger>
    <Sun
      class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
    />
    <Moon
      class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
    />
    {toggle_theme()}
  </DropdownMenu.SubTrigger>
  <DropdownMenu.SubContent>
    <DropdownMenu.RadioGroup value={$userPrefersMode}>
      <DropdownMenu.RadioItem value="light" onSelect={() => setMode('light')}>
        <Sun size={18} class="me-2 align-middle" />
        {light_theme()}
      </DropdownMenu.RadioItem>
      <DropdownMenu.RadioItem value="dark" onSelect={() => setMode('dark')}>
        <Moon size={18} class="me-2 align-middle" />
        {dark_theme()}
      </DropdownMenu.RadioItem>
      <DropdownMenu.RadioItem value="system" onSelect={() => resetMode()}>
        <Monitor size={18} class="me-2 align-middle" />
        {system_theme()}
      </DropdownMenu.RadioItem>
    </DropdownMenu.RadioGroup>
  </DropdownMenu.SubContent>
</DropdownMenu.Sub>
