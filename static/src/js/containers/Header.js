import { connect } from 'react-redux';
import { createSetHighlightsMessage, createUpdateSearchMessage, createLoadMessage } from '../actions';
import Header from '../components/Header';

const mapStateToProps = state => ({
  name: state.search.name,
  suggestions: state.search.suggestions
})

const mapDispatchToProps = dispatch => ({
  updateSearch: (search, suggestions) => dispatch(createUpdateSearchMessage(search, suggestions)),
  setHighlights: (highlights) => dispatch(createSetHighlightsMessage(highlights)),
  setLoading: (loading) => dispatch(createLoadMessage(loading))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Header)