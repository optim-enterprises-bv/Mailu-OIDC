<script lang="ts">
  import { userPrefersMode, resetMode, setMode } from 'mode-watcher';

  import * as DropdownMenu from '$lib/components/ui/dropdown-menu';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';
</script>

<DropdownMenu.Sub>
  <DropdownMenu.SubTrigger>
    <Icon.Sun
      class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
    />
    <Icon.Moon
      class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
    />
    {m.toggle_theme()}
  </DropdownMenu.SubTrigger>
  <DropdownMenu.SubContent>
    <DropdownMenu.RadioGroup value={$userPrefersMode}>
      <DropdownMenu.RadioItem value="light" onSelect={() => setMode('light')}>
        <Icon.Sun size={18} class="me-2 align-middle" />
        {m.light_theme()}
      </DropdownMenu.RadioItem>
      <DropdownMenu.RadioItem value="dark" onSelect={() => setMode('dark')}>
        <Icon.Moon size={18} class="me-2 align-middle" />
        {m.dark_theme()}
      </DropdownMenu.RadioItem>
      <DropdownMenu.RadioItem value="system" onSelect={() => resetMode()}>
        <Icon.Monitor size={18} class="me-2 align-middle" />
        {m.system_theme()}
      </DropdownMenu.RadioItem>
    </DropdownMenu.RadioGroup>
  </DropdownMenu.SubContent>
</DropdownMenu.Sub>
