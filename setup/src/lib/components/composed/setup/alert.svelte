<script lang="ts" module>
  import type { Snippet } from 'svelte';

  type AlertProps = {
    title?: string;
    variant: Alert.AlertVariant;
    children?: Snippet;
  };
</script>

<script lang="ts">
  import * as Alert from '$lib/components/ui/alert';

  import * as Icon from 'lucide-svelte';
  import * as m from '$lib/paraglide/messages';

  const { title, variant, children }: AlertProps = $props();

  const fallbackTitle = $derived.by(() => {
    switch (variant) {
      case 'warning':
        return m.warning();
      default:
        return m.caution();
    }
  });
  const AlertIcon = $derived.by(() => {
    switch (variant) {
      case 'caution':
        return Icon.AlertOctagon;
      case 'warning':
        return Icon.AlertTriangle;
      case 'info':
        return Icon.Info;
      case 'destructive':
        return Icon.BadgeAlert;
      default:
        return Icon.AlertCircle;
    }
  });
</script>

<Alert.Root {variant} class="transition-colors">
  <AlertIcon class="size-4" />
  <Alert.Title>{title ?? fallbackTitle}</Alert.Title>
  <Alert.Description>
    {@render children?.()}
  </Alert.Description>
</Alert.Root>
