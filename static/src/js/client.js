/*
 * Returns an array of highlights to display, with the 24 first sorted by
 */
function getHighlights(count, successCallback, errorCallBack, search='') {
  let url = '/highlights?count=' + count;

  if (search !== '') {
    url += '&search=' + encodeURIComponent(search)
  }

  $.ajax({
    type: 'GET',
    url: url,
    success: successCallback,
    error: errorCallBack
  });
}

export default {
  getHighlights
};