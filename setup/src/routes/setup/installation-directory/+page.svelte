<script lang="ts">
  import { PersistedState } from 'runed';

  import { Badge } from '$lib/components/ui/badge';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { RadioGroup, RadioGroupItem } from '$lib/components/ui/radio-group';

  import { inlineCode, link } from '$lib/components/formatters.svelte';

  import * as m from '$lib/paraglide/messages';

  const rootDefault = '/mailu';
  const root = new PersistedState('root', rootDefault);
  const rootCustom = new PersistedState('root__custom', '/var/mailu');
</script>

<header class="flex max-w-2xl items-center justify-between gap-2">
  <div class="space-y-2">
    <h2 class="text-2xl font-bold">{m.installation_directory_title()}</h2>
    <p class="text-muted-foreground">{m.installation_directory_description()}</p>
  </div>
</header>

<RadioGroup bind:value={root.current} class="max-w-2xl">
  <Label
    for="installation_directory_default"
    class="flex items-center space-x-4 rounded-md border p-4"
  >
    <RadioGroupItem value="/mailu" id="installation_directory_default" />
    <div class="w-full">
      <strong class="text-base font-semibold">{m.installation_directory_o_default_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {@render inlineCode(
          m.installation_directory_o_default_description({ installDir: rootDefault })
        )}
      </p>
    </div>
  </Label>
  <Label
    for="installation_directory_custom"
    class="flex items-center space-x-4 rounded-md border p-4"
  >
    <RadioGroupItem value={rootCustom.current} id="installation_directory_custom" />
    <div class="w-full">
      <strong class="text-base font-semibold">{m.installation_directory_o_custom_title()}</strong>
      <p class="mt-1 block text-balance text-sm text-muted-foreground">
        {m.installation_directory_o_custom_description()}
      </p>
      {#if root.current === rootCustom.current}
        <section class="py-4">
          <div class="flex w-full max-w-sm flex-col gap-1.5">
            <Label for="installation_directory_custom_input">
              {m.installation_directory_o_custom_title()}
            </Label>
            <Input
              id="installation_directory_custom_input"
              value={rootCustom.current}
              oninput={(event) => {
                rootCustom.current = event.currentTarget.value;
                root.current = rootCustom.current;
              }}
            />
          </div>
        </section>
      {/if}
    </div>
  </Label>
</RadioGroup>

<section class="space-y-2 text-muted-foreground">
  <p>
    {@render inlineCode(m.installation_directory_hint_install_dir({ installDir: root.current }))}
  </p>
  {#if root.current && root.current.replace(/[^/]/g, '').length > 2}
    <p>
      <Badge class="bg-amber-500 hover:bg-amber-500 ">{m.warning()}</Badge>
      {@render link(
m.installation_directory_hint_more_than_two_subdirs_warning({
          openIssueLink: 'https://github.com/Mailu/Mailu/issues/3164'
        })
      )}
    </p>
  {/if}
</section>
