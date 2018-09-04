/*
 * Returns an array of highlights to display, with the 24 first sorted by
 */
function getHighlights(count, successCallback, errorCallBack) {
  $.ajax({
    type: 'GET',
    url: '/highlights?count=' + count,
    success: successCallback,
    error: errorCallBack
  });
}

export default {
  getHighlights
};