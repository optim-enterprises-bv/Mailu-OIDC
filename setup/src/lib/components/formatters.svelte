<script lang="ts" module>
  export { githubRepository };
  export { inlineCode };
</script>

{#snippet githubRepository(text: string, options: { href: string; title: string })}
  {@const [textBefore, textAfter] = text.split('<GithubRepository/>')}
  {textBefore}<a
    href={options.href}
    target="_blank"
    rel="noopener noreferrer"
    class="inline-block rounded-sm text-blue-700 underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-8 focus-visible:outline-black dark:text-blue-400"
    data-no-translate>{options.title}</a
  >{textAfter}
{/snippet}

{#snippet inlineCode(text: string)}
  {@const [textBefore, code, textAfter] = text.split('`')}
  {textBefore}<code class="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm"
    >{code}</code
  >{textAfter}
{/snippet}
