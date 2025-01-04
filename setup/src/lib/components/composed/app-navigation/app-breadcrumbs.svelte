<!-- @component Breadcrumb navigation for the application. Displayed in the header at the top of the page. -->

<script lang="ts" module>
  type BreadcrumbProps = {
    items: NavItem[];
  };
</script>

<script lang="ts">
  import type { NavItem } from '.';

  import * as Breadcrumb from '$lib/components/ui/breadcrumb';

  function recursiveBreadcrumb(items: NavItem[], breadcrumb: NavItem[] = []) {
    for (let i = items.length - 1; i >= 0; i--) {
      var item = items[i];
      if (item.isActive) breadcrumb.push(item);
      if (item.items) recursiveBreadcrumb(item.items, breadcrumb);
    }
    return breadcrumb;
  }

  const { items }: BreadcrumbProps = $props();
  const breadcrumb = $derived(recursiveBreadcrumb(items));
</script>

<Breadcrumb.Root>
  <Breadcrumb.List>
    {#each breadcrumb as item, i}
      <Breadcrumb.Item class={i === breadcrumb.length - 1 ? '' : 'hidden md:block'}>
        {#if i < breadcrumb.length - 1}
          <Breadcrumb.Link href={item.url}>{item.title}</Breadcrumb.Link>
        {:else}
          <Breadcrumb.Page>{item.title}</Breadcrumb.Page>
        {/if}
      </Breadcrumb.Item>
      {#if i < breadcrumb.length - 1}
        <Breadcrumb.Separator class="hidden md:block" />
      {/if}
    {/each}
  </Breadcrumb.List>
</Breadcrumb.Root>
