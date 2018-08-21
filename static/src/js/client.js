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