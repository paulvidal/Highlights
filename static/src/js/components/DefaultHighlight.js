import React from "react";

const DefaultHighlight = () => {

  return (
    <div className="col-lg-4 col-md-6">
      <div className="card mb-4 shadow-sm highlight">
        <div className="card-img-top default-image animated-background">
            <img className="col image img-fluid"/>
        </div>

        <div className="card-body description default-description">
          <div className="container">
            <p className="card-text default-title animated-background"></p>
            <small className="container-fluid text-muted default-date animated-background"></small>
          </div>

        </div>
      </div>
    </div>
  );
}

export default DefaultHighlight;