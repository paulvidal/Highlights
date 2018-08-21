import React, { Component }  from "react";

class Highlight extends Component {

  constructor (props) {
    super(props);
  }

  toUpperCase(str) {
    return str.replace(/(^|\s)\S/g, l => l.toUpperCase())
  }

  onClickShort() {
    window.open(this.props.highlight.link);
  }

  onClickExtended() {
    window.open(this.props.highlight.link_extended);
  }

  render () {
    let h = this.props.highlight;

    let img_link = h.img_link;
    let category = this.toUpperCase(h.category);

    let title = this.toUpperCase(h.team1) + ' - ' + this.toUpperCase(h.team2);

    let date = h.date.toLocaleString('en-gb', {
      weekday: 'long',
      month: 'long',
      day: 'numeric'
    });

    return (
      <div className="col-lg-4 col-md-6" onClick={this.onClickShort.bind(this)}>
        <div className="card mb-4 shadow-sm highlight">
          <div className="card-img-top">
              <img className="col image img-fluid" src={img_link} onError={(e)=>{e.target.src="/static/img/logo.png"}} alt="Card image cap"/>
              <p className="category">{category}</p>
          </div>

          <div className="card-body description">
            <div className="container">
              <p className="card-text title">{title}</p>
              <small className="text-muted date">{date}</small>
            </div>

            <div className="container">
              <div className="row buttons">
                <button type="button" className="btn btn-sm btn-outline-secondary short col-12">Short highlight</button>
                <button type="button" className="btn btn-sm btn-outline-secondary extended col-12" onClick={this.onClickExtended.bind(this)}>Extended highlight</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Highlight;