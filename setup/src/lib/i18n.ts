import { goto } from '$app/navigation';
import * as runtime from '$lib/paraglide/runtime';
import { createI18n } from '@inlang/paraglide-sveltekit';

export const i18n = createI18n(runtime, {
  prefixDefaultLanguage: 'always'
});

export function setLanguage(href: string, newLanguage: runtime.AvailableLanguageTag) {
  const localisedPath = i18n.resolveRoute(href, newLanguage);
  goto(localisedPath);
}
