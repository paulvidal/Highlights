import { combineReducers } from 'redux';
import { SET_HIGHLIGHTS, UPDATE_SEARCH } from './actions';
import moment from 'moment';

function setHighlights(state = [], action) {
  switch (action.type) {

    case SET_HIGHLIGHTS:
      const startCount = action.startCount;
      let highlights = action.highlights;

      _.each(highlights, (h) => {
        h.date = moment(h.date).seconds(0).minutes(0).hours(0).milliseconds(0);
      })

      highlights = highlights.slice(0, startCount).sort((h1, h2) => {
        if (h1.date > h2.date) {
          return -1;
        } else if (h1.date < h2.date) {
          return 1;
        } else if (h1.view_count === h2.view_count) {
          return h1.team1.localeCompare(h2.team1);
        } else  {
          return h2.view_count - h1.view_count;
        }
      }).concat(highlights.slice(startCount, highlights.length));

      return highlights;

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

const rootReducer = combineReducers({
  highlights: setHighlights,
  search: search
});

export default rootReducer;