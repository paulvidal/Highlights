import React, { Component } from "react";
import PropTypes from 'prop-types';

import { START_COUNT } from "./HighlightsGallery";
import client from "../client";
import { toUpperCase } from '../utils';

class Header extends Component {

  constructor(props) {
    super(props);

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(name) {
    this.props.setLoading(true);
    this.props.updateSearch(name, []);

    client.getHighlights(START_COUNT, (data) => {
      this.props.setHighlights(data.highlights);
      this.props.updateSearch(name, data.suggestions);

    }, (xhr, status, error) => {
      console.log(error);
    }, name);
  }

  render() {
    let dropdownClass = "dropdown-menu dropdown-menu-left col-12 visible "
    let suggestions = null;
    const inputValue = this.props.name ? this.props.name : '';

    // Suggestions for search
    if (this.props.suggestions && this.props.suggestions.length <= 4) {
      dropdownClass += (this.props.suggestions.length === 0 ? 'd-none' : 'd-block');
      suggestions = _.map(this.props.suggestions, s => {
        const name = toUpperCase(s);

        return (
          <button key={s} className="btn dropdown-item" type="button" onClick={() => this.handleChange(name)}>{toUpperCase(s)}</button>
        );
      });
    }

    return (
      <div className="navbar navbar-dark bg-dark shadow-sm">
        <div className="container d-flex justify-content-between">
          <a href="/" className="brand navbar-brand d-flex align-items-center col-md-auto col-12">
            <img className="logo" src={`${STATIC_URL}img/logo.png`} alt="Card image cap"/>
            <strong>Highlights Bot</strong>
          </a>

          <div id="search" className="input-group input-group-md col-lg-4 col-md-6 col-12">
            <input type="text" className="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-sm" value={inputValue} onChange={(e) => this.handleChange(e.target.value)}></input>
            <div className="input-group-prepend">
              <span id="search-button" className="input-group-text">Search</span>
            </div>
            <div id="search-dropdown" className={dropdownClass}>
              {suggestions}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

Header.propTypes = {
  updateSearch: PropTypes.func.isRequired
}

export default Header;