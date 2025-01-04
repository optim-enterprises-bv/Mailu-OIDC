<script lang="ts">
  import { openid_connect_title, openid_connect_description } from '$lib/paraglide/messages';
</script>

<header class="space-y-2">
  <h2 class="text-2xl font-bold">{openid_connect_title()}</h2>
  <p class="text-muted-foreground">{openid_connect_description()}</p>
</header>
