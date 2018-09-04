import React, { Component }  from "react";
import PropTypes from "prop-types";

class LoadButton extends Component {

  constructor(props) {
    super(props);

    this.state = {
      loading: false
    };
  }

  render() {
    const loading = this.state.loading;
    const refreshGallery = this.props.refreshGallery;
    const className = ["btn", "btn-primary", "btn-lg", "btn-block", "col-4"]

    // Click event handler
    let onClick = () => {
      this.setState({
        loading: true
      });

      refreshGallery(() => {
        this.setState({
          loading: false
        });
      });
    }

    // Determine button state
    let button = (
      <button type="button" className={className.join(" ")} onClick={onClick}>More highlights</button>
    );

    if (this.state.loading) {
      button = (
        <button type="button" className={className.join(" ")} onClick={onClick} disabled>Loading...</button>
      );
    }

    return (
      <div className="row justify-content-center">
        {button}
      </div>
    )
  }
}

LoadButton.propTypes = {
  refreshGallery: PropTypes.func.isRequired
}

export default LoadButton;