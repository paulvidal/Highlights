import { combineReducers } from 'redux';
import { SET_HIGHLIGHTS, UPDATE_SEARCH, LOADING } from './actions';
import moment from 'moment';

function setHighlights(state = [], action) {
  switch (action.type) {

    case SET_HIGHLIGHTS:
      return action.highlights;;

    default:
      return state;
  }
}

function search(state = {}, action) {
  switch (action.type) {

    case UPDATE_SEARCH:
      return {
        name: action.search,
        suggestions: action.suggestions
      }

    default:
      return state;
  }
}

function loading(state = true, action) {
  switch (action.type) {

    case LOADING:
      return action.loading;

    default:
      return state;
  }
}

const rootReducer = combineReducers({
  highlights: setHighlights,
  search: search,
  loading: loading
});

export default rootReducer;