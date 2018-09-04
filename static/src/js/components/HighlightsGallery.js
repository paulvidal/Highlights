import React  from "react";
import PropTypes from 'prop-types';

import client from "../client";
import Highlight from "./Highlight";
import LoadButton from "./LoadButton";

const START_COUNT = 18;
const INCREMENT_COUNT = 12;

const HighlightsGallery = ({ highlights, setHighlights }) => {

  // Get the highlights callback
  const refreshGallery = (callback) => {
    client.getHighlights(highlights.length + (highlights.length === 0 ? START_COUNT : INCREMENT_COUNT) , (data) => {
      setHighlights(data.highlights, START_COUNT);
      if (callback) {
        callback();
      }

    }, (xhr, status, error) => {
      console.log(error);
      if (callback) {
        callback();
      }
    });
  };

  // Load the first batch of highlights to display
  if (highlights.length === 0) {
    refreshGallery();
  }

  return (
    <div className="gallery py-5 bg-light">
      <div className="container">
        <div className="row">
          {
            _.map(highlights, h => {

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
                  date={h.date}
                  onClickShort={onClickShort}
                  onClickExtended={onClickExtended}
                  />
              );

            })
          }
        </div>

        <LoadButton
          refreshGallery={refreshGallery}
          />
      </div>
    </div>
  );
}

HighlightsGallery.propTypes = {
  highlights: PropTypes.array.isRequired
}

export default HighlightsGallery;