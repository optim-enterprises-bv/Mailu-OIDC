<script lang="ts" module>
  import type { Snippet } from 'svelte';

  export { githubRepository, inlineCode, link };

  const markdown = {
    inlineCode: {
      regex: /`([^`]+)`/g,
      replaceText: '<InlineCode/>',
      render: inlineCodeRenderer
    },
    link: {
      regex: /\[([^\]]+)\]\(([^\)]+)\)/g,
      replaceText: '<Link/>',
      render: linkRenderer
    }
  } as Record<string, { regex: RegExp; replaceText: string; render: Snippet<[RegExpExecArray]> }>;
</script>

{#snippet inlineCodeRenderer(match: RegExpExecArray | string[])}
  {@const [_, code] = match}
  <code class="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm">{code}</code>
{/snippet}

{#snippet linkRenderer(match: RegExpExecArray | string[])}
  {@const [_, title, href] = match}
  <a
    {href}
    target="_blank"
    rel="noopener noreferrer"
    class="inline-block rounded-sm text-blue-700 underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-8 focus-visible:outline-black dark:text-blue-400"
    data-no-translate>{title}</a
  >
{/snippet}

{#snippet generic(
  text: string,
  replacer: { regex: RegExp; replaceText?: string; render: Snippet<[RegExpExecArray]> }
)}
  {@const replaceParts = [...text.matchAll(replacer.regex)]}
  {@const textParts = text
    .replace(replacer.regex, replacer.replaceText ?? '<Element/>')
    .split(replacer.replaceText ?? '<Element/>')}

  {#each textParts as textPart, i}
    {textPart}{#if i < textParts.length - 1}
      {@render replacer.render(replaceParts[i])}
    {/if}
  {/each}
{/snippet}

{#snippet githubRepository(text: string, options: { href: string; title: string })}
  {@const [textBefore, textAfter] = text.split('<GithubRepository/>')}
  {textBefore}{@render linkRenderer(['', options.title, options.href])}{textAfter}
{/snippet}

{#snippet inlineCode(text: string)}
  {@render generic(text, markdown.inlineCode)}
{/snippet}

{#snippet link(text: string)}
  {@render generic(text, markdown.link)}
{/snippet}
