<!-- @component Basic wrapper to allow for translated text in the navigation components. Also defines the navigation items for use across the application. -->

<script lang="ts" module>
  import type { Snippet } from 'svelte';

  export type NavItem = {
    title: string;
    url: string;
    icon?: typeof Icon.Blocks;
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

  import * as Sidebar from '$lib/components/ui/sidebar';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  const pathname = $derived(i18n.route(page.url.pathname));
  const items = $derived({
    main: [
      {
        title: m.home(),
        url: '/',
        icon: Icon.House,
        isActive: pathname === '/'
      },
      {
        title: m.setup(),
        url: '/setup',
        icon: Icon.Wrench,
        isActive: pathname.startsWith('/setup'),
        items: [
          {
            title: m.openid_connect_title(),
            url: '/setup/openid-connect',
            icon: Icon.ShieldEllipsis,
            isActive: pathname === '/setup/openid-connect'
          },
          {
            title: m.installation_directory_title(),
            url: '/setup/installation-directory',
            icon: Icon.FolderInput,
            isActive: pathname === '/setup/installation-directory'
          },
          {
            title: m.postmaster_title(),
            url: '/setup/postmaster',
            icon: Icon.UserRoundCheck,
            isActive: pathname === '/setup/postmaster'
          },
          {
            title: m.rate_limiting_title(),
            url: '/setup/rate-limiting',
            icon: Icon.Gauge,
            isActive: pathname === '/setup/rate-limiting'
          },
          {
            title: m.optional_services_title(),
            url: '/setup/optional-services',
            icon: Icon.Blocks,
            isActive: pathname === '/setup/optional-services'
          }
        ]
      }
    ],
    secondary: [
      {
        title: m.report_a_bug(),
        url: 'https://github.com/heviat/Mailu-OIDC/issues',
        icon: Icon.Bug
      },
      {
        title: m.source_code(),
        url: 'https://github.com/heviat/Mailu-OIDC/tree/oidc-setup/setup#readme',
        icon: Icon.Code
      }
    ]
  });

  const { children }: AppNavigationProps = $props();
</script>

<Sidebar.Provider>
  {@render children?.(items)}
</Sidebar.Provider>
