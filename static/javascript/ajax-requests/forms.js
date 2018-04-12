function getRequest(id){
  var arr = id.split('_');
  event = arr.shift();
  form = arr.join('_');
  return {event: event, form: form}
}

$(document).ready(function(){
  $('.form-button').click(function(e){
    e.preventDefault();
    var id = $(this).attr('id');
    var action = getRequest(id);

    console.log(action)
    $.ajax({
      url: '',
      type: 'get',
      dataType: 'json',
      data: action,
      success: function(res){
        console.log(res);
      },
      error: function(res){
        console.log("oops");
      }
    })
  })
})
