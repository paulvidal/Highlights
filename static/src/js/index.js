import React from "react";
import ReactDOM from "react-dom";

import HighlightsGallery from "./HighlightsGallery";
import client from "./client";

let increment = 12;
let counter = increment;
let refresh = false

let get = (count) => {

  client.getHighlights(count, (data) => {

    _.each(data.highlights, (h) => {
      let date = new Date(Date.parse(h.date));
      h.date = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
    })

    data.highlights.sort((h1, h2) => {
      if (h1.date > h2.date) {
        return -1;
      } else if (h1.date < h2.date) {
        return 1;
      } else {
        return h2.view_count - h1.view_count;
      }
    });

    ReactDOM.render(<HighlightsGallery highlights={data.highlights}/>, document.getElementById("higlights-gallery"));

  }, (xhr, status, error) => {
    console.log(err);
  });
}

get(counter);

$(window).scroll(function() {
  if ($(window).height() + Math.ceil($(window).scrollTop() + 1) >= $(document).height()) {
    // TODO: capitalise title and competition name
    counter += increment;

    if (!refresh && counter <= 100) {
      console.log('refreshing');
      refresh = true;
      get(counter);
    }

    setTimeout(() => {
      refresh = false;
      console.log('can refresh again');
    }, 1000);
  }
});

if (module.hot) {
  module.hot.accept();
}