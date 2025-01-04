<!-- @component Header navigation for the application. Displayed at the top of the page. -->

<script lang="ts">
  import { SidebarTrigger } from '$lib/components/ui/sidebar';
</script>

<header
  class="flex h-16 shrink-0 items-center gap-2 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12"
>
  <div class="flex items-center gap-2 px-4">
    <SidebarTrigger class="-ml-1" />
  </div>
</header>
