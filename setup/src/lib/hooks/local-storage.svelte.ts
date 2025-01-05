import { on } from 'svelte/events';
import { createSubscriber } from 'svelte/reactivity';

const isBrowser = typeof globalThis.window !== 'undefined';

// recursive proxy to take care of assignment in deeply nested values
function recursive_proxy<T extends Record<string, unknown>>(obj: T, set: (val: T) => void) {
  return new Proxy(obj, {
    get(target, key) {
      // on get if it's an object we return a new recursive proxy
      if (target[key as never] && typeof target[key as never] === 'object') {
        return recursive_proxy(target[key as never] as T, () => {
          // but in this case the set function will just call `set` with the original target
          // value...this means it will "climb up" to the top where the original object would
          // actually be set
          set(target);
        });
      }
      // if it's not an object we just return the value
      return Reflect.get(target, key);
    },
    set(target, key, value) {
      // on set we set the value on the target and call the set function (if it's the root proxy will actually set
      // the value otherwise will start "climbing")
      const res = Reflect.set(target, key, value);
      set?.(target);
      return res;
    }
  });
}

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
    // if we are on the server we return either the fallback or null
    if (!isBrowser) return this.#fallback ?? null;
    // this is the magic of `createSubscriber`...it allow us to rerun this code
    // when we call update but only if we are in a reactive context
    this.#subscribe();
    const str_value = window.localStorage.getItem(this.#key);
    let value = null;
    if (str_value) {
      try {
        value = JSON.parse(str_value);
      } catch {
        /** empty */
      }
    }
    // create a function to set the current value from within the proxy
    // it needs to be an arrow function
    const set = (new_value: T) => {
      this.current = new_value;
    };
    // if it's an object we want to keep track of writes to the nested properties
    // we can create a recursive proxy if we care about deep assignment
    if (value && typeof value === 'object') {
      value = recursive_proxy(value, set);
    }
    // we need to proxify the fallback if there's one so that we can catch changes
    // when we don't have a value in the local storage
    return (value ?? (this.#fallback ? recursive_proxy(this.#fallback, set) : null)) as T;
  }
  set current(new_value: T) {
    if (!isBrowser) return;
    // if we are on the client let's set the key and trigger the re-read
    window.localStorage.setItem(this.#key, JSON.stringify(new_value));
    this.#update?.();
  }
}
