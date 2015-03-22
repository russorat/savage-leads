function showInputRow(btn) {
  $('#hiddenRow').show(250);
  $('#addNewBtn').hide();
  $('#submitLead').show();
  $(":input").first().focus();
}

$(function() {
  $('#addNewBtn').click(function() {
    showInputRow(this);
  });
  $('form').submit(function() {
    pwElem = $('#password').first();
    pwElem.val(CryptoJS.SHA512(pwElem.val()));
    pwElem = null;
  });
});
