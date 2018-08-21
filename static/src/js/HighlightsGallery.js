import React, { Component }  from "react";
import Highlight from "./Highlight";

class HighlightsGallery extends Component {

  constructor (props) {
    super(props);
  }

  render () {
    let highlights = this.props.highlights;

    return (
      <div className="album py-5 bg-light">
        <div className="container">
          <div className="row">
            {
              _.map(highlights, h => {

                return (
                  <Highlight
                    key={h.link}
                    highlight={h} />
                );

              })
            }
          </div>
        </div>
      </div>
    );
  }
}

export default HighlightsGallery;