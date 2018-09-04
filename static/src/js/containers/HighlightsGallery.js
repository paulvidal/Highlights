import { connect } from 'react-redux';
import { createSetHighlightsMessage } from '../actions';
import HighlightsGallery from '../components/HighlightsGallery';

const mapStateToProps = state => ({
  highlights: state.highlights,
  search: state.search.name
})

const mapDispatchToProps = dispatch => ({
  setHighlights: (highlights, startCount) => dispatch(createSetHighlightsMessage(highlights, startCount))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(HighlightsGallery)