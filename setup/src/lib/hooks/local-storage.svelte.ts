import { on } from 'svelte/events';
import { createSubscriber } from 'svelte/reactivity';

const isBrowser = typeof globalThis.window !== 'undefined';

function isObject(obj: unknown): obj is Record<string, unknown> {
  return typeof obj === 'object' && obj !== null && !Array.isArray(obj);
}

/**
 * Create a recursive proxy to take care of assignment in deeply nested values
 */
function recursiveProxy<T extends Record<string, unknown> | unknown[]>(
  obj: T,
  set: (val: T) => void
) {
  return new Proxy(obj, {
    get(target, key) {
      if (target[key as never] && typeof target[key as never] === 'object') {
        return recursiveProxy(target[key as never] as T, () => {
          set(target);
        });
      }
      return Reflect.get(target, key);
    },
    set(target, key, value) {
      const res = Reflect.set(target, key, value);
      set?.(target);
      return res;
    }
  });
}

/**
 * Reactive local storage
 */
export class LocalStorage<T> {
  readonly #key: string;
  readonly #subscribe: ReturnType<typeof createSubscriber>;
  #update: Parameters<Parameters<typeof createSubscriber>[0]>[0] | undefined;
  readonly #fallback?: T;

  constructor(key: string, fallback?: T) {
    this.#key = key;
    this.#fallback = fallback;
    this.#subscribe = createSubscriber((update) => {
      this.#update = update;
      return on(window, 'storage', (event) => {
        if (event.key === this.#key) {
          update();
        }
      });
    });
  }

  get current(): T | null {
    if (!isBrowser) return this.#fallback ?? null;

    this.#subscribe();

    const strValue = window.localStorage.getItem(this.#key);
    let value = null;
    if (strValue) {
      try {
        value = JSON.parse(strValue);
      } catch {
        /** empty */
      }
    }

    const set = (newValue: T) => {
      this.current = newValue;
    };

    if (value !== null) {
      if (typeof value === 'object') return recursiveProxy(value, set);
      return value;
    }

    if (this.#fallback !== undefined) {
      if (isObject(this.#fallback)) return recursiveProxy(this.#fallback, set) as T;
      return this.#fallback;
    }

    return null;
  }
  set current(newValue: T) {
    if (!isBrowser) return;

    window.localStorage.setItem(this.#key, JSON.stringify(newValue));
    this.#update?.();
  }
}
