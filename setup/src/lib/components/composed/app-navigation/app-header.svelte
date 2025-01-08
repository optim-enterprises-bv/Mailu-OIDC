<!-- @component Header navigation for the application. Displayed at the top of the page. -->

<script lang="ts" module>
  type HeaderProps = {
    items: Record<string, App.NavItem[]>;
  };
</script>

<script lang="ts">
  import { Separator } from '$lib/components/ui/separator';
  import * as Sidebar from '$lib/components/ui/sidebar';

  import * as App from '.';

  const { items }: HeaderProps = $props();
</script>

<header
  class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
>
  <div class="flex items-center gap-2 px-4">
    <Sidebar.Trigger class="-ml-1" />
    <Separator orientation="vertical" class="mr-2 h-4" />
    <App.Breadcrumbs items={items.main} />
  </div>
</header>
