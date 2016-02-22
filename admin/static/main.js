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
    if(typeof CryptoJS !== 'undefined') {
      pwElem = $('#password').first();
      if(pwElem.val()) {
        pwElem.val(CryptoJS.SHA512(pwElem.val()));
        pwElem = null;
      }
    }
    $('#replaceWithLoader').hide();
    $('#loader').css('display','inline-block');
    $('#loader').show();
  });
  $("a[id|='deleteLink']").click(function(){
    loopIndex = this.id.split('-')[1];
    $('#replaceDelete-'+loopIndex).hide();
    $('#loader-'+loopIndex).show();
  });
});
