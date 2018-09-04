import React from "react";
import { render } from "react-dom";
import { Provider } from 'react-redux';
import { createStore } from 'redux';

import client from "./client";
import rootReducer from './reducers';
import HighlightsGallery from "./containers/HighlightsGallery";

const store = createStore(rootReducer);

render(
  <Provider store={store}>
    <HighlightsGallery />
  </Provider>,
  document.getElementById('highlights-gallery')
)

if (module.hot) {
  module.hot.accept();
}