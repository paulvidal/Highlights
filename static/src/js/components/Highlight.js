import React from "react";
import PropTypes from 'prop-types';
import moment from 'moment';

import { toUpperCase } from '../utils';

const Highlight = ({ img_link, category, team1, team2, score1, score2, match_time, onClickShort, onClickExtended }) => {

  let title = toUpperCase(team1) + ' - ' + toUpperCase(team2);

  let formattedCategory = toUpperCase(category);

  let formattedDate = moment(match_time).format("dddd D MMMM");

  return (
    <div className="col-lg-4 col-md-6" onClick={onClickShort}>
      <div className="card mb-4 shadow-sm highlight">
        <div className="card-img-top">
            <img className="col image img-fluid" src={img_link} onError={(e)=>{e.target.src="/static/img/logo.png"}} alt="Card image cap"/>
            <p className="category">{formattedCategory}</p>
        </div>

        <div className="card-body description">
          <div className="container">
            <p className="card-text title">{title}</p>
            <small className="text-muted date">{formattedDate}</small>
          </div>

          <div className="container">
            <div className="row buttons">
              <button type="button" className="btn btn-sm btn-outline-secondary short col-12">Short highlights</button>
              <button type="button" className="btn btn-sm btn-outline-secondary extended col-12" onClick={onClickExtended}>Extended highlights</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

Highlight.propTypes = {
  img_link: PropTypes.string.isRequired,
  category: PropTypes.string.isRequired,
  team1: PropTypes.string.isRequired,
  team2: PropTypes.string.isRequired,
  score1: PropTypes.number.isRequired,
  score2: PropTypes.number.isRequired,
  date: PropTypes.instanceOf(moment).isRequired,
  onClickShort: PropTypes.func.isRequired,
  onClickExtended: PropTypes.func.isRequired,
}

export default Highlight;