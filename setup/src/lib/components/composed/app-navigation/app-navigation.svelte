<!-- @component Basic wrapper to allow for translated text in the navigation components. Also defines the navigation items for use across the application. -->

<script lang="ts" module>
  import type { Snippet } from 'svelte';

  export type NavItem = {
    title: string;
    url: string;
    icon?: typeof Blocks;
    isActive?: boolean;
    hidden?: boolean;
    items?: NavItem[];
  };

  type AppNavigationProps = {
    children: Snippet<[Record<string, NavItem[]>]>;
  };
</script>

<script lang="ts">
  import { i18n } from '$lib/i18n';
  import { page } from '$app/state';

  import { SidebarProvider } from '$lib/components/ui/sidebar';

  import { Blocks, Bug, Code, House, Wrench } from 'lucide-svelte';

  import { home, report_a_bug, setup, source_code } from '$lib/paraglide/messages';

  const pathname = $derived(i18n.route(page.url.pathname));
  const items = $derived({
    main: [
      {
        title: home(),
        url: '/',
        icon: House,
        isActive: pathname === '/'
      },
      {
        title: setup(),
        url: '/setup',
        icon: Wrench,
        isActive: pathname.startsWith('/setup')
      }
    ],
    secondary: [
      {
        title: report_a_bug(),
        url: 'https://github.com/heviat/Mailu-OIDC/issues',
        icon: Bug
      },
      {
        title: source_code(),
        url: 'https://github.com/heviat/Mailu-OIDC/tree/oidc-setup/setup#readme',
        icon: Code
      }
    ]
  });

  let { children }: AppNavigationProps = $props();
</script>

<SidebarProvider>
  {@render children?.(items)}
</SidebarProvider>
