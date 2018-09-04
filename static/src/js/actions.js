/*
 * action types
 */

export const SET_HIGHLIGHTS = 'SET_HIGHLIGHTS';

/*
 * action creators
 */

export const createSetHighlightsMessage = (highlights, startCount) => ({
  type: SET_HIGHLIGHTS,
  startCount,
  highlights
})