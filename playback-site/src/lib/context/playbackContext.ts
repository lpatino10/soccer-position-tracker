import { getContext, setContext } from 'svelte';

export type PlaybackSpeed = 0.5 | 1 | 2;

export interface PlaybackState {
  speed: PlaybackSpeed;
  isPlaying: boolean;
  currentFrame: number;
  frameCount: number;
}

const KEY = Symbol('playbackState');

export const setPlaybackContext = (state: PlaybackState) => setContext(KEY, state);
export const getPlaybackState = (): PlaybackState => getContext(KEY);
