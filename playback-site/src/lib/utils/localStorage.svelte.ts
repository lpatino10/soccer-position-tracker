import { browser } from "$app/environment";

export function localStorageState(key: string, initial: string) {
  if (!browser) {
    return;
  }

  let value = $state(localStorage.getItem(key) ?? initial);

  $effect.root(() => {
    $effect(() => {
      localStorage.setItem(key, value);
    });
  });

  return {
    get value() { return value; },
    set value(v) { value = v; }
  };
}
