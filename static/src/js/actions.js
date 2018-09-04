/*
 * action types
 */

export const SET_HIGHLIGHTS = 'SET_HIGHLIGHTS';
export const UPDATE_SEARCH = 'UPDATE_SEARCH';

/*
 * action creators
 */

export const createSetHighlightsMessage = (highlights, startCount) => ({
  type: SET_HIGHLIGHTS,
  highlights,
  startCount
})

export const createUpdateSearchMessage = (search, suggestions) => ({
  type: UPDATE_SEARCH,
  search,
  suggestions
})