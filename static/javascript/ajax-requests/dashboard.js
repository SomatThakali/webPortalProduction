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

$(document).ready(function(){
  $('.confirm-notification').click(function(){
    data = createData($(this),'notification')
    uniqueID = data['Unique_ID']
    $.ajax({
      url: '',
      type: 'POST',
      dataType: 'json',
      data: data,
      success: function(res){
        $('#'+uniqueID).remove()
      },
      error: function(res){
        alert("It fucked")
      }
    })
  })
  $('.delete-notification').click(function(){
    data = createData($(this),'notification');
    uniqueID = data['Unique_ID']
    $.ajax({
      url: '',
      type: 'POST',
      dataType: 'json',
      data: data,
      success: function(res){
        $('#'+uniqueID).remove()
      },
      error: function(res){
        alert("DCAP fucked up the backend")
      }
    })
  })
})
