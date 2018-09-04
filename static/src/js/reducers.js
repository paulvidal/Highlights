import { combineReducers } from 'redux';
import { SET_HIGHLIGHTS } from './actions';

function setHighlights(state = [], action) {
  switch (action.type) {

    case SET_HIGHLIGHTS:
      const startCount = action.startCount;
      let highlights = action.highlights;

      _.each(highlights, (h) => {
        let date = new Date(Date.parse(h.date));
        h.date = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
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

const rootReducer = combineReducers({
  highlights: setHighlights
});

export default rootReducer;