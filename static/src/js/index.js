import React from "react";
import { render } from "react-dom";
import { Provider } from 'react-redux';
import { createStore } from 'redux';

import client from "./client";
import rootReducer from './reducers';
import HighlightsGallery from "./containers/HighlightsGallery";
import Header from "./containers/Header";

const store = createStore(rootReducer);

render(
  <Provider store={store}>
    <HighlightsGallery />
  </Provider>,
  document.getElementById('highlights-gallery')
)

render(
  <Provider store={store}>
    <Header />
  </Provider>,
  document.getElementById('header')
)

if (module.hot) {
  module.hot.accept();
}