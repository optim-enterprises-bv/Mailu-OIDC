<!-- @component Header navigation for the application. Displayed at the top of the page. -->

<script lang="ts" module>
  type HeaderProps = {
    items: Record<string, NavItem[]>;
  };
</script>

<script lang="ts">
  import { AppBreadcrumbs, type NavItem } from '.';

  import { Separator } from '$lib/components/ui/separator';
  import { SidebarTrigger } from '$lib/components/ui/sidebar';

  const { items }: HeaderProps = $props();
</script>

<header
  class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
>
  <div class="flex items-center gap-2 px-4">
    <SidebarTrigger class="-ml-1" />
    <Separator orientation="vertical" class="mr-2 h-4" />
    <AppBreadcrumbs items={items.main} />
  </div>
</header>
