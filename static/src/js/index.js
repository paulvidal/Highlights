import React from "react";
import ReactDOM from "react-dom";
import Index from "./app";

ReactDOM.render(<Index />, document.getElementById("index"));

if (module.hot) {
  module.hot.accept();
}