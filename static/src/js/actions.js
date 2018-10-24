/*
 * action types
 */

export const SET_HIGHLIGHTS = 'SET_HIGHLIGHTS';
export const UPDATE_SEARCH = 'UPDATE_SEARCH';
export const LOADING = 'LOADING';

/*
 * action creators
 */

export const createSetHighlightsMessage = (highlights) => ({
  type: SET_HIGHLIGHTS,
  highlights,
})

export const createUpdateSearchMessage = (search, suggestions) => ({
  type: UPDATE_SEARCH,
  search,
  suggestions
})

export const createLoadMessage = (loading) => ({
  type: LOADING,
  loading
})