import React, { Component }  from "react";
import PropTypes from 'prop-types';

import client from "../client";
import Highlight from "./Highlight";
import DefaultHighlight from "./DefaultHighlight";
import LoadButton from "./LoadButton";

export const DEFAULT_HIGHLIGHTS_COUNT = 6

export const START_COUNT = 18;
export const INCREMENT_COUNT = 12;

let TIMEOUT = null;

class HighlightsGallery extends Component {

  constructor(props) {
    super(props);

    this.refreshGallery = this.refreshGallery.bind(this);
    this.refreshGallery();
  }

  refreshGallery(callback) {
    client.getHighlights(this.props.highlights.length + (this.props.highlights.length === 0 ? START_COUNT : INCREMENT_COUNT) , (data) => {
      this.props.setHighlights(data.highlights);
      if (callback) {
        callback();
      }

    }, (xhr, status, error) => {
      console.log(error);
      if (callback) {
        callback();
      }
    }, this.props.search);
  }

  render() {
    // Determine if should display button
    const refreshButton = (this.props.highlights.length - START_COUNT) % INCREMENT_COUNT === 0
      ? (<LoadButton
           refreshGallery={this.refreshGallery}
          />)
      : null;

    if (this.props.highlights.length > 0) {

      return (
        <div className="gallery py-5 bg-light">
          <div className="container">
            <div className="row">
              {
                _.map(this.props.highlights, h => {

                  const onClickShort = () => {
                    window.open(h.link);
                  };

                  const onClickExtended = () => {
                    window.open(h.link_extended);
                  };

                  return (
                    <Highlight
                      key={h.link}
                      img_link={h.img_link}
                      category={h.category}
                      team1={h.team1}
                      team2={h.team2}
                      score1={h.score1}
                      score2={h.score2}
                      match_time={h.match_time}
                      onClickShort={onClickShort}
                      onClickExtended={onClickExtended}
                      />
                  );

                })
              }
            </div>

            {refreshButton}
          </div>
        </div>
      );

    } else {

      // LOADING
      if (this.props.loading) {

        clearTimeout(TIMEOUT);

        TIMEOUT = setTimeout(() => {
          this.props.setLoading(false);
        }, 1500);

        return (
          <div className="gallery py-5 bg-light">
            <div className="container">
              <div className="row">
                {
                  _.map(Array.from(Array(DEFAULT_HIGHLIGHTS_COUNT).keys()), i => {

                    return (
                      <DefaultHighlight
                        key={i}
                        />
                    );
                  })
                }
              </div>
            </div>
          </div>
        );

      // NO RESULT
      } else {

        return (
          <div className="gallery py-5 bg-light">
            <div className="container">
              <div className="no-result row justify-content-center">
                <h2>{'No results found' + (this.props.search ? ' for ': '')} <strong>{this.props.search ? this.props.search : ''}</strong></h2>
                <div className="col-9 col-md-8 col-lg-5">
                  <img id="no-result-image" className="img-fluid" src={`${STATIC_URL}img/logo.png`} />
                </div>
              </div>
            </div>
          </div>
        );

      }

    }
  }
}

HighlightsGallery.propTypes = {
  highlights: PropTypes.array.isRequired
}

export default HighlightsGallery;