function getFormID(tabId){
    var prefix= tabId.split('-')[0];
    var tableId = prefix + '-form'
    tableId = "#"+tableId;
    return tableId
}


$(document).ready(function(){
  $('.tab').click(function(){
    var newTabId = $(this).attr('id');
    var $activeTab = $('.active'); //Current active tab
    var newFormId = getFormID(newTabId); //To be form

    var oldTabId = $activeTab.attr('id');
    var oldFormId = getFormID(oldTabId);
    $activeTab.removeClass('active');
    $activeTab.addClass('unactive');
    $(oldFormId).removeClass('show');
    $(oldFormId).addClass('hide');

    $(this).addClass('active');
    $(this).removeClass('unactive');
    $(newFormId).addClass('show');
    $(newFormId).removeClass('hide');



  })
})
