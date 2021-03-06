import { connect } from 'react-redux';
import { createSetHighlightsMessage, createLoadMessage } from '../actions';
import HighlightsGallery from '../components/HighlightsGallery';

const mapStateToProps = state => ({
  highlights: state.highlights,
  search: state.search.name,
  loading: state.loading
})

const mapDispatchToProps = dispatch => ({
  setHighlights: (highlights) => dispatch(createSetHighlightsMessage(highlights)),
  setLoading: (loading) => dispatch(createLoadMessage(loading))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(HighlightsGallery)