import { connect } from 'react-redux';
import { createSetHighlightsMessage, createUpdateSearchMessage } from '../actions';
import Header from '../components/Header';

const mapStateToProps = state => ({
  name: state.search.name,
  suggestions: state.search.suggestions
})

const mapDispatchToProps = dispatch => ({
  updateSearch: (search, suggestions) => dispatch(createUpdateSearchMessage(search, suggestions)),
  setHighlights: (highlights, startCount) => dispatch(createSetHighlightsMessage(highlights, startCount))
})

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Header)