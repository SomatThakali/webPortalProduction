function appendCSRFToken(data){
  var csrf_token = getCSRFToken();
  data['csrfmiddlewaretoken'] = csrf_token;
  return data;
}
function getCSRFToken(){
  var csrf_token=$('meta[name="csrf-token"]').attr('content')
  return csrf_token
}
function createData($item,type){
  var id = $item.attr('id');
  id = id.split('_');
  var uniqueID = id[1]
  var action = id[0]
  var data = {'Unique_ID': uniqueID, 'action': action, 'type': type}
  data = appendCSRFToken(data)
  return data
}
function isEmpty($div){
  return $div.find('div').length==0
}

$(document).ready(function(){
  if (isEmpty($('#notification-accordion'))){
    $('#notification-accordion').append("<h3>No notifications at this moment!</h3>");
  }
  if (isEmpty($('#todo-accordion'))){
    $('#todo-accordion').append("<h3>No ToDos recorded.</h3>")
  }
  $('.confirm-notification').click(function(){
    data = createData($(this),'notification')
    uniqueID = data['Unique_ID']
    $.ajax({
      url: '',
      type: 'POST',
      data: data,
      success: function(res){
        alert("The notification has been acted upon.")
        $('#'+uniqueID).remove()
        if (isEmpty($('#notification-accordion'))){
          $('#notification-accordion').append("<h3>No more notifications for now!</h3>");
        }
      },
      error: function(res){
        alert("Sorry, you're request cannot be processed right now!")
      }
    })
  })
  $('.delete-notification').click(function(){
    data = createData($(this),'notification');
    uniqueID = data['Unique_ID']
    $.ajax({
      url: '',
      type: 'POST',
      data: data,
      success: function(res){
        alert("The notification has successfully been deleted.")
        $('#'+uniqueID).remove()
        if (isEmpty($('#notification-accordion'))){
          $('#notification-accordion').append("<h3>No more notifications for now!</h3>");
        }
      },
      error: function(res){
        alert("Sorry, you're request cannot be processed right now!")
      }
    })
  })
  $('.complete-todo').click(function(){
    data = createData($(this),'todo');
    uniqueID = data['Unique_ID']
    $.ajax({
      url: '',
      type:'POST',
      data: data,
      success: function(res){
        alert("Your todo item has successfully been removed.")
        $('#'+uniqueID).remove()
        if (isEmpty($('#todo-accordion'))){
          $('#todo-accordion').append("<h3>No more tasks recorded for now!</h3>");
        }
      },
      error: function(res){
        alert("Sorry, you're request cannot be process right now!")
      }
    })
  })
})
